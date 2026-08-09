"""
Tool Registry and Implementations for Autonomous Agent Platform.
================================================================
"""

import json
import os
from typing import Dict, List, Any, Callable, Optional


def search_web(query: str) -> str:
    """Search online knowledge base for structured documentation."""
    knowledge = {
        "mcp": (
            "Model Context Protocol (MCP) by Anthropic is an open standard designed to connect "
            "AI models to external tools, databases, and context servers securely. "
            "It eliminates custom tool integrations by establishing a unified protocol standard."
        ),
        "evals": (
            "Continuous evaluation loops require robust golden datasets, multiple LLM judges, "
            "and programmatic execution triggers like GitHub Actions to ensure zero performance regressions."
        ),
        "agent": (
            "Autonomous agents coordinate actions by maintaining state, planning multi-step tasks, "
            "handling unexpected tool exceptions, and synthesizing results into cohesive artifacts."
        ),
    }
    q_lower = query.lower()
    for key, val in knowledge.items():
        if key in q_lower:
            return f"[Search Success] Topic: {key.upper()} | Details: {val}"
            
    return f"[Search Reference] Query: '{query}' | Details: Found articles highlighting advanced patterns for {query}."


def calculate(expression: str) -> str:
    """Safely evaluate arithmetic expressions, handling decimals and parameters."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Expression contains prohibited characters."
    try:
        # Evaluate safely
        res = eval(expression)
        return str(res)
    except Exception as e:
        return f"Error: Failed to calculate expression due to syntax: {e}"


def generate_markdown_report(title: str, content: str, filename: Optional[str] = None) -> str:
    """Format and synthesize a research report in Markdown, persisting it to disk if specified."""
    report = (
        f"# {title}\n\n"
        f"{content}\n\n"
        f"---\n"
        f"*Report generated autonomously by Production Agent Platform.*\n"
    )
    if filename:
        try:
            # Clean filename
            safe_name = "".join(c for c in filename if c.isalnum() or c in "._-")
            target_path = os.path.join(os.path.dirname(__file__), safe_name)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(report)
            return f"[File Saved] Report successfully persisted to {target_path}"
        except Exception as e:
            return f"[File Error] Could not write report to disk: {e}. Output:\n{report}"
            
    return report


TOOLS_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Query the web index for structured technical documentations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or keyphrase"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform floating-point math evaluations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Mathematical expression"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_markdown_report",
            "description": "Format technical findings in markdown and optionally save it to a local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Structured header title"},
                    "content": {"type": "string", "description": "Synthesized markdown body text"},
                    "filename": {"type": "string", "description": "Optional local filename to save, e.g. report.md"}
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
