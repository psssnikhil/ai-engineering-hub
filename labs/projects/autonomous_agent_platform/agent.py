"""Autonomous ReAct Agent Engine using Multi-Provider Gateway."""

import json
from typing import Dict, List, Any, Optional
from labs.common.gateway import LLMGateway, OpenAIProvider, AnthropicProvider
from .tools import TOOLS_SCHEMAS, TOOL_FUNCTIONS


class AutonomousAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None, max_steps: int = 6):
        self.gateway = gateway or LLMGateway(providers=[
            OpenAIProvider(model="gpt-4o-mini"),
            AnthropicProvider(model="claude-3-5-haiku-20241022"),
        ])
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
            print(f"--- Agent Step {step + 1} ---")
            resp = self.gateway.generate(messages=messages, tools=TOOLS_SCHEMAS, temperature=0.0)

            if not resp.tool_calls:
                print("  Agent completed task.")
                return {
                    "goal": goal,
                    "final_answer": resp.content,
                    "provider_used": resp.provider_name,
                    "trace": trace,
                }

            # Append assistant turn with tool calls
            messages.append({
                "role": "assistant",
                "content": resp.content or "",
                "tool_calls": resp.raw_response.choices[0].message.tool_calls,
            })

            for tool_call in resp.tool_calls:
                fn_name = tool_call["name"]
                fn_args = json.loads(tool_call["arguments"])

                print(f"  Action: {fn_name}({fn_args})")
                tool_fn = TOOL_FUNCTIONS.get(fn_name)
                result = tool_fn(**fn_args) if tool_fn else f"Error: Tool {fn_name} not found"
                print(f"  Observation: {result[:100]}...")

                trace.append({"step": step + 1, "tool": fn_name, "args": fn_args, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })

                if fn_name == "generate_markdown_report":
                    return {
                        "goal": goal,
                        "final_report": result,
                        "provider_used": resp.provider_name,
                        "trace": trace,
                    }

        return {"goal": goal, "final_answer": "Reached max steps", "trace": trace}
