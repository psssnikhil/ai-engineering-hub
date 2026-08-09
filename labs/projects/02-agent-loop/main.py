"""
Project 02: Production-Grade ReAct Agent Loop from Scratch
==========================================================
Course 07 — AI Agents Fundamentals

Features:
  1. Parameter Schema Validation: Inspects parameters against JSON Schema tools before execution.
  2. Parallel Tool Execution: Concurrently evaluates multiple tool calls in a single turn using threads.
  3. Context-Compressing Memory: Summarizes intermediate steps when history exceeds constraints.
  4. Human-In-The-Loop (HITL) Gate: Halts and requests verification for dangerous actions.
  5. Detailed Tracing & Cost Accounting: Tracks token consumption and costs per reasoning step.
"""

import os
import sys
import json
import time
from typing import List, Dict, Any, Callable, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway

# Token Cost configuration (estimate)
INPUT_TOKEN_RATE = 0.0015 / 1000  # $ per token
OUTPUT_TOKEN_RATE = 0.0020 / 1000


# --- Tools Definitions ---

def calculator(expression: str) -> str:
    """Evaluate math expression safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Invalid characters in expression."
    try:
        # Use simple eval after filtering
        res = eval(expression)
        return str(res)
    except Exception as e:
        return f"Error: Failed to evaluate math. Details: {e}"


def get_system_status(component: str) -> str:
    """Query status of system component."""
    status_db = {
        "vector_db": "Status: ONLINE | Latency: 12ms | Chunks: 150,000",
        "llm_gateway": "Status: ONLINE | Primary: OpenAI | Fallback: Anthropic",
    }
    return status_db.get(component.lower(), f"Unknown component '{component}'")


def execute_database_update(query: str, changes: Dict[str, Any]) -> str:
    """Critical action requiring Human-in-the-loop authorization."""
    return f"Success: Database updated (Query: '{query}', Changes: {json.dumps(changes)})"


# Tool Schema and registry
TOOLS_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The math expression to run"}
                },
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
                "properties": {
                    "component": {"type": "string", "description": "Name of the component"}
                },
                "required": ["component"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_database_update",
            "description": "CRITICAL: Modifies database records. Requires exact query matching and input changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "changes": {"type": "object"}
                },
                "required": ["query", "changes"],
            },
        },
    },
]

TOOL_REGISTRY: Dict[str, Tuple[Callable, List[str], Dict[str, type]]] = {
    "calculator": (calculator, ["expression"], {"expression": str}),
    "get_system_status": (get_system_status, ["component"], {"component": str}),
    "execute_database_update": (execute_database_update, ["query", "changes"], {"query": str, "changes": dict}),
}


class ToolValidator:
    """Validates tool arguments against registered schemas before running."""
    @staticmethod
    def validate_and_execute(name: str, args: Dict[str, Any], hitl_approved: bool = False) -> str:
        if name not in TOOL_REGISTRY:
            return f"Error: Tool '{name}' is not registered."

        func, required, types = TOOL_REGISTRY[name]
        
        # Check required fields
        for field in required:
            if field not in args:
                return f"Error: Missing required argument '{field}' for tool '{name}'."
        
        # Check argument types
        for k, v in args.items():
            if k in types:
                expected_type = types[k]
                if not isinstance(v, expected_type):
                    return f"Error: Argument '{k}' must be of type {expected_type.__name__}, got {type(v).__name__}."

        # Human in the loop gate for database updates
        if name == "execute_database_update" and not hitl_approved:
            return "Error: Execution BLOCKED. Tool 'execute_database_update' requires user confirmation. Call with HITL flag enabled."

        try:
            return func(**args)
        except Exception as e:
            return f"Error executing tool '{name}': {e}"


class ReActAgentState:
    """Manages conversational history, summaries, logs, and token tracking."""
    def __init__(self, system_prompt: str, goal: str):
        self.system_prompt = system_prompt
        self.goal = goal
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": goal}
        ]
        self.cumulative_cost = 0.0
        self.total_tokens = 0
        self.step_logs: List[Dict[str, Any]] = []

    def log_tokens(self, prompt: str, response: str) -> None:
        p_tokens = len(prompt.split())
        r_tokens = len(response.split())
        self.total_tokens += (p_tokens + r_tokens)
        self.cumulative_cost += (p_tokens * INPUT_TOKEN_RATE + r_tokens * OUTPUT_TOKEN_RATE)

    def append_message(self, role: str, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None, tool_call_id: Optional[str] = None) -> None:
        msg: Dict[str, Any] = {"role": role, "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        if tool_call_id:
            msg["tool_call_id"] = tool_call_id
        self.messages.append(msg)

    def compress_memory(self, gateway: LLMGateway) -> None:
        """Summarizes past turns if conversational context gets too long."""
        if len(self.messages) <= 8:
            return

        print("  [Memory Management] History size exceeds threshold. Compressing context...")
        # Summarize mid-conversations (exclude system prompt, user goal, and last 2 messages)
        to_summarize = self.messages[2:-2]
        
        summary_prompt = (
            "Summarize the following intermediate steps of an agent execution trace. "
            "Retain tools called and facts discovered. Keep it short:\n"
            f"{json.dumps(to_summarize)}"
        )
        try:
            resp = gateway.generate([{"role": "user", "content": summary_prompt}], temperature=0.0)
            summary_content = f"Summary of previous research steps: {resp.content}"
            
            # Keep system, original goal, the new summary, and the last 2 turns
            new_messages = [
                self.messages[0],
                self.messages[1],
                {"role": "system", "content": summary_content}
            ] + self.messages[-2:]
            self.messages = new_messages
        except Exception as e:
            print(f"  [Memory Management] Context compression failed: {e}")


class ProductionReActAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None, max_steps: int = 6):
        self.gateway = gateway or LLMGateway()
        self.max_steps = max_steps

    def run(self, goal: str, auto_approve_hitl: bool = False) -> Dict[str, Any]:
        system_prompt = (
            "You are an advanced autonomous ReAct agent. You solve tasks by thinking, selecting tools, "
            "analyzing observations, and looping until complete. Focus on accuracy."
        )
        state = ReActAgentState(system_prompt, goal)

        print(f"Goal: {goal}\n")
        
        for step in range(self.max_steps):
            print(f"--- Step {step + 1} ---")
            state.compress_memory(self.gateway)

            # Generate step action
            t_start = time.time()
            resp = self.gateway.generate(messages=state.messages, tools=TOOLS_SCHEMAS, temperature=0.0)
            t_duration = time.time() - t_start
            
            state.log_tokens(str(state.messages), resp.content or "")

            # Log execution trace
            step_log = {
                "step": step + 1,
                "latency_sec": round(t_duration, 3),
                "model": resp.model_name,
                "tool_calls": resp.tool_calls
            }
            state.step_logs.append(step_log)

            if resp.tool_calls:
                # Append assistant tool call payload
                state.append_message(
                    role="assistant",
                    content=resp.content or "",
                    tool_calls=resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None
                )

                # Process tool calls in parallel using thread pool
                tool_results = []
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = []
                    for tc in resp.tool_calls:
                        fn_name = tc["name"]
                        fn_args = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
                        print(f"  Action: {fn_name}({fn_args})")
                        
                        # HITL Authorization Check
                        hitl_approved = False
                        if fn_name == "execute_database_update":
                            if auto_approve_hitl:
                                print("  [HITL Gate] Automatically authorized database modification.")
                                hitl_approved = True
                            else:
                                # Interactive console check or standard rejection
                                print(f"  [HITL Gate] Database update requested: '{fn_args.get('query')}'")
                                confirmation = input("  Authorize execution? (y/n): ").strip().lower()
                                hitl_approved = confirmation == 'y'

                        f = executor.submit(ToolValidator.validate_and_execute, fn_name, fn_args, hitl_approved)
                        futures.append((tc["id"], fn_name, f))

                    for tc_id, fn_name, future in futures:
                        obs = future.result()
                        print(f"  Observation ({fn_name}): {obs}")
                        tool_results.append((tc_id, obs))

                # Append results to conversation state
                for tc_id, obs in tool_results:
                    state.append_message(role="tool", content=obs, tool_call_id=tc_id)

            else:
                print("  Final Answer Reached.")
                return {
                    "status": "success",
                    "final_answer": resp.content,
                    "cumulative_cost": round(state.cumulative_cost, 6),
                    "total_tokens": state.total_tokens,
                    "step_logs": state.step_logs
                }

        print("Agent reached max execution steps.")
        return {
            "status": "max_steps_reached",
            "final_answer": "Stopped due to step limits.",
            "cumulative_cost": round(state.cumulative_cost, 6),
            "total_tokens": state.total_tokens,
            "step_logs": state.step_logs
        }


if __name__ == "__main__":
    print("=== Running ReAct Agent Loop ===")
    agent = ProductionReActAgent()
    
    # Run simple math & status check
    goal = "Query vector_db status and compute (150000 * 0.05) - 250."
    res = agent.run(goal, auto_approve_hitl=True)
    print(f"\nFinal Result:\n{json.dumps(res, indent=2)}")
