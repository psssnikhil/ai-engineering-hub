"""
Project 02: ReAct Agent Loop from Scratch
=========================================
Course 07 — AI Agents Fundamentals

A pure Python ReAct (Reasoning + Acting) Agent loop supporting multi-provider LLMs.
Uses `labs.common.gateway` for standardized provider access and tool execution.

Usage:
  python main.py
"""

import os
import sys
import json
from typing import List, Dict, Any, Callable, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


def calculator(expression: str) -> str:
    """Evaluate math expression safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Invalid characters"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def get_system_status(component: str) -> str:
    """Query status of system component."""
    status_db = {
        "vector_db": "Status: ONLINE | Latency: 12ms | Chunks: 150,000",
        "llm_gateway": "Status: ONLINE | Primary: OpenAI | Fallback: Anthropic",
    }
    return status_db.get(component.lower(), f"Unknown component '{component}'")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "Check status of system components like vector_db or llm_gateway",
            "parameters": {
                "type": "object",
                "properties": {"component": {"type": "string"}},
                "required": ["component"],
            },
        },
    },
]

TOOL_MAP: Dict[str, Callable] = {
    "calculator": calculator,
    "get_system_status": get_system_status,
}


class ReActAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def run(self, goal: str, max_steps: int = 5) -> str:
        messages = [
            {"role": "system", "content": "You are an autonomous ReAct agent. Use tools to solve tasks step by step."},
            {"role": "user", "content": goal},
        ]

        for step in range(max_steps):
            print(f"--- Step {step + 1} ---")
            resp = self.gateway.generate(messages=messages, tools=TOOLS, temperature=0.0)

            if resp.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": resp.content or "",
                    "tool_calls": resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None,
                })

                for tc in resp.tool_calls:
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
                    print(f"  Action: {fn_name}({fn_args})")
                    
                    func = TOOL_MAP.get(fn_name)
                    obs = func(**fn_args) if func else f"Error: Tool {fn_name} not found"
                    print(f"  Observation: {obs}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": obs,
                    })
            else:
                print("  Final Answer Reached.")
                return resp.content

        return "Agent stopped: Max steps reached."


if __name__ == "__main__":
    print("--- Project 02: Running ReAct Agent Loop ---")
    agent = ReActAgent()
    query = "Check the status of vector_db and calculate 150000 * 0.05"
    print(f"Goal: {query}\n")
    final_answer = agent.run(query)
    print(f"\nFinal Answer:\n{final_answer}")
