"""Tool Registry for Autonomous Agent Platform."""

import json
from typing import Dict, List, Any, Callable


def search_web(query: str) -> str:
    """Search online knowledge base."""
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
    return f"# {title}\n\n{content}\n\n---\n*Report generated autonomously by Agent Platform.*"


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

TOOL_FUNCTIONS: Dict[str, Callable] = {
    "search_web": search_web,
    "calculate": calculate,
    "generate_markdown_report": generate_markdown_report,
}
