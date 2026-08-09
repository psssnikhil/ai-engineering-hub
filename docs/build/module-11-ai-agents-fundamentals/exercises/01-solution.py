"""
Exercise 01: Build a ReAct Agent Loop (Solution)
=================================================
Course 07 — AI Agents Fundamentals
"""

import json
import os

from openai import OpenAI


def calculator(expression: str) -> str:
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return f"Error: expression contains invalid characters"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def lookup(topic: str) -> str:
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

TOOL_MAP = {
    "calculator": calculator,
    "lookup": lookup,
}


def run_agent(query: str, max_steps: int = 5) -> str:
    """ReAct agent loop: reason → act → observe → repeat."""
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

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        # 1. Call the LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            temperature=0,
        )
        assistant_msg = response.choices[0].message

        # 2. Check if the LLM wants to use tools
        if assistant_msg.tool_calls:
            # Append the assistant message with tool_calls AS-IS
            messages.append(assistant_msg)

            # 3. Execute each tool call
            for tool_call in assistant_msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f"  Tool: {fn_name}({fn_args})")

                # Execute the tool
                if fn_name in TOOL_MAP:
                    result = TOOL_MAP[fn_name](**fn_args)
                else:
                    result = f"Error: unknown tool '{fn_name}'"

                print(f"  Result: {result}")

                # Append tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # 4. No tool calls — the agent is done
            final_answer = assistant_msg.content
            print(f"  Final answer generated (no more tool calls)")
            return final_answer

    # 5. Max steps reached
    return f"Agent stopped after {max_steps} steps. Last response: {assistant_msg.content}"


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
