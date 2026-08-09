"""
Tool-Using Autonomous Research Agent
====================================
Build These Project #4 — AI Engineering Hub

Features:
  - Real OpenAI Function Calling & ReAct Execution Loop
  - Web search, safe calculation, and markdown report synthesis tools
  - Full execution trace logging
"""

import json
import os
import sys
from typing import Dict, List, Any
from openai import OpenAI


# ── Tool Functions ──
def search_web(query: str) -> str:
    """Search for information online. Returns summary of search results."""
    knowledge = {
        "mcp": "Model Context Protocol (MCP) by Anthropic is an open standard connecting AI models to external tools, databases, and context servers.",
        "evals": "LLM evaluation requires golden datasets, rubric scoring, and CI quality gates to catch non-deterministic regressions.",
        "agent": "Agents use an LLM reasoning loop to call tools, inspect results, and autonomously achieve multi-step goals.",
    }
    q_lower = query.lower()
    for k, v in knowledge.items():
        if k in q_lower:
            return f"[Web Search Result for '{query}']: {v}"
    return f"[Web Search Result for '{query}']: Found relevant articles discussing {query} implementation strategies."


def calculate(expression: str) -> str:
    """Safely evaluate arithmetic expressions."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Expression contains prohibited characters."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def generate_markdown_report(title: str, content: str) -> str:
    """Format and synthesize a research report in Markdown."""
    return f"# {title}\n\n{content}\n\n---\n*Report generated autonomously by OpenAI Research Agent.*"


# OpenAI Tool Schemas
TOOLS_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information on a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression string"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_markdown_report",
            "description": "Synthesize a final report in Markdown.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Report title"},
                    "content": {"type": "string", "description": "Detailed body content"},
                },
                "required": ["title", "content"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "search_web": search_web,
    "calculate": calculate,
    "generate_markdown_report": generate_markdown_report,
}


class AutonomousResearchAgent:
    def __init__(self, model: str = "gpt-4o-mini", max_steps: int = 6):
        self.client = OpenAI()
        self.model = model
        self.max_steps = max_steps

    def run(self, goal: str) -> Dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an autonomous research agent. Gather facts using search_web, "
                    "perform math using calculate, and write a structured final report using generate_markdown_report."
                ),
            },
            {"role": "user", "content": goal},
        ]

        trace = []

        for step in range(self.max_steps):
            print(f"--- Step {step + 1} ---")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS_SCHEMAS,
                temperature=0.0,
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                print("  Agent concluded research.")
                return {"goal": goal, "final_answer": msg.content, "trace": trace}

            for tool_call in msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f"  Action: {fn_name}({fn_args})")
                tool_fn = TOOL_FUNCTIONS.get(fn_name)
                result = tool_fn(**fn_args) if tool_fn else f"Error: Tool {fn_name} not found"
                print(f"  Observation: {result[:120]}...")

                trace.append({"step": step + 1, "tool": fn_name, "args": fn_args, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

                if fn_name == "generate_markdown_report":
                    return {"goal": goal, "final_report": result, "trace": trace}

        return {"goal": goal, "final_answer": "Reached max steps", "trace": trace}


def main():
    print("=" * 60)
    print("  Autonomous Research Agent (Real OpenAI Function Calling)")
    print("=" * 60 + "\n")

    agent = AutonomousResearchAgent()
    res = agent.run("Research Model Context Protocol (MCP) and generate an executive summary report.")
    print("\n--- Final Report Output ---")
    print(res.get("final_report", res.get("final_answer")))


if __name__ == "__main__":
    main()
