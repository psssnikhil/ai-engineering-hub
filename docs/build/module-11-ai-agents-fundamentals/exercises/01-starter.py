"""
Exercise 01: Build a ReAct Agent Loop (Starter)
================================================
Course 07 — AI Agents Fundamentals

Goal: Implement a ReAct-style agent loop from scratch that can use tools
      to answer questions. The agent alternates between reasoning (LLM call)
      and acting (tool execution) until it reaches a final answer.

Instructions:
  1. Fill in the TODO sections below
  2. Set OPENAI_API_KEY in your environment (or use .env)
  3. Run: python 01-starter.py
  4. Compare your output with 01-solution.py

Requirements: pip install openai
"""

import json
import os

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("pip install openai  — then re-run this exercise")


# ── Tools ─────────────────────────────────────────────────────────────
# These are the tools the agent can call. Each has a Python function
# and an OpenAI-format tool schema.

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Only supports basic math."""
    try:
        # SAFETY: only allow basic math operations
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return f"Error: expression contains invalid characters"
        result = eval(expression)  # Safe because we validated input
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def lookup(topic: str) -> str:
    """Look up a fact from a small knowledge base."""
    knowledge = {
        "paris": "Paris is the capital of France with a population of about 2.1 million in the city and 12 million in the metro area.",
        "python": "Python is a programming language created by Guido van Rossum in 1991. It emphasizes readability and simplicity.",
        "rag": "RAG (Retrieval-Augmented Generation) is a technique that combines information retrieval with LLM generation to produce grounded answers.",
        "transformer": "The Transformer architecture was introduced in 'Attention Is All You Need' (Vaswani et al., 2017). It uses self-attention instead of recurrence.",
        "react": "ReAct (Reason + Act) is an agent pattern where the LLM alternates between thinking and taking actions. Introduced by Yao et al., 2022.",
    }
    key = topic.lower().strip()
    for k, v in knowledge.items():
        if k in key:
            return v
    return f"No information found about '{topic}'."


# OpenAI tool schemas
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression. Use for any arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '12000000 * 0.15'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup",
            "description": "Look up a fact about a topic. Use when you need factual information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to look up"
                    }
                },
                "required": ["topic"]
            }
        }
    },
]

# Map tool names to Python functions
TOOL_MAP = {
    "calculator": calculator,
    "lookup": lookup,
}


# ── The Agent Loop ────────────────────────────────────────────────────

def run_agent(query: str, max_steps: int = 5) -> str:
    """
    TODO: Implement the ReAct agent loop.

    The loop should:
    1. Initialize messages with a system prompt and the user query
    2. Call the LLM with messages and tools
    3. If the response has tool_calls:
       a. Execute each tool call
       b. Append the assistant message and tool results to messages
       c. Continue the loop
    4. If the response has NO tool_calls (just text):
       a. Return the text — the agent is done
    5. If max_steps is reached, return the last response content
       or a message saying the agent ran out of steps

    Hints:
    - Use client.chat.completions.create() with model, messages, tools params
    - Tool call results use role="tool" and must include tool_call_id
    - The assistant message with tool_calls must be appended AS-IS to messages
    """
    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions step by step. "
                "Use the available tools when you need facts or calculations. "
                "Think through the problem before acting."
            ),
        },
        {"role": "user", "content": query},
    ]

    # TODO: Implement the agent loop here
    # for step in range(max_steps):
    #     1. Call LLM
    #     2. Check for tool_calls
    #     3. Execute tools and append results
    #     4. Or return final answer
    pass


# ── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "What is the population of Paris, and what is 15% of that?",
        "What is RAG and what year was the Transformer paper published?",
        "What is 42 * 17 + 3?",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print(f"{'='*60}")
        result = run_agent(q)
        print(f"\nFinal Answer: {result}")
