"""Autonomous ReAct & Plan-Then-Execute Agent Engine with OpenTelemetry Tracing."""

import json
import uuid
import time
from typing import Dict, List, Any, Optional

try:
    from tools import TOOLS_SCHEMAS, TOOL_FUNCTIONS
except ImportError:
    from .tools import TOOLS_SCHEMAS, TOOL_FUNCTIONS

from labs.common.gateway import LLMGateway


class AgentOTELTracer:
    """Simulates OpenTelemetry Distributed Tracing conventions for autonomous operations."""
    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or f"trace-{uuid.uuid4().hex[:12]}"
        self.spans: List[Dict[str, Any]] = []

    def start_span(self, name: str, parent_span_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> str:
        span_id = f"span-{uuid.uuid4().hex[:8]}"
        span = {
            "trace_id": self.trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "name": name,
            "start_time": time.time(),
            "attributes": attributes or {},
            "status": "ACTIVE"
        }
        self.spans.append(span)
        return span_id

    def end_span(self, span_id: str, status: str = "OK", attributes: Optional[Dict[str, Any]] = None) -> None:
        for span in self.spans:
            if span["span_id"] == span_id:
                span["end_time"] = time.time()
                span["duration_ms"] = round((span["end_time"] - span["start_time"]) * 1000.0, 2)
                span["status"] = status
                if attributes:
                    span["attributes"].update(attributes)
                break


class AutonomousAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None, max_steps: int = 6):
        self.gateway = gateway or LLMGateway()
        self.max_steps = max_steps

    def create_initial_plan(self, goal: str, tracer: AgentOTELTracer) -> List[Dict[str, Any]]:
        """Formulate a step-by-step reasoning plan using the LLM before calling tools."""
        span_id = tracer.start_span("agent.create_initial_plan", attributes={"goal": goal})
        
        prompt = (
            f"Goal: {goal}\n\n"
            "Create a detailed plan of action to accomplish this goal using the tools: search_web, calculate, generate_markdown_report.\n"
            "Format the output strictly as a JSON list of tasks: [{\"id\": 1, \"description\": \"...\", \"tool_needed\": \"...\"}]."
        )
        messages = [
            {"role": "system", "content": "You are a lead planner. Output only valid JSON lists, no other text."},
            {"role": "user", "content": prompt}
        ]

        try:
            resp = self.gateway.generate(messages=messages, temperature=0.0)
            # Find and parse JSON list
            import re
            match = re.search(r"(\[.*\])", resp.content, re.DOTALL)
            if match:
                plan = json.loads(match.group(1))
                tracer.end_span(span_id, "OK", {"plan_steps_count": len(plan)})
                return plan
        except Exception as e:
            print(f"  [Planner Warning] Could not formulate structured plan: {e}. Falling back to default plan.")
        
        # Fallback default plan
        fallback_plan = [
            {"id": 1, "description": "Research details regarding goal using web search.", "tool_needed": "search_web"},
            {"id": 2, "description": "Format and write the markdown report.", "tool_needed": "generate_markdown_report"}
        ]
        tracer.end_span(span_id, "FALLBACK", {"error": "JSON parsing failed"})
        return fallback_plan

    def run(self, goal: str) -> Dict[str, Any]:
        tracer = AgentOTELTracer()
        root_span_id = tracer.start_span("agent.run_execution_loop", attributes={"goal": goal})

        # Step 1: Formulate Initial Plan
        plan = self.create_initial_plan(goal, tracer)
        print("Initial Structured Execution Plan:")
        print(json.dumps(plan, indent=2))

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an autonomous research agent. Gather facts using search_web, "
                    "perform math using calculate, and write a structured final report using generate_markdown_report.\n"
                    f"Execution Plan: {json.dumps(plan)}"
                ),
            },
            {"role": "user", "content": goal},
        ]

        trace = []

        for step in range(self.max_steps):
            step_span_id = tracer.start_span(f"agent.step_{step+1}")
            print(f"\n--- Agent Step {step + 1} ---")
            
            resp = self.gateway.generate(messages=messages, tools=TOOLS_SCHEMAS, temperature=0.0)

            if not resp.tool_calls:
                print("  Agent completed task (No more tool calls).")
                tracer.end_span(step_span_id, "COMPLETE")
                break

            # Append assistant turn
            messages.append({
                "role": "assistant",
                "content": resp.content or "",
                "tool_calls": resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None,
            })

            for tool_call in resp.tool_calls:
                fn_name = tool_call["name"]
                fn_args = json.loads(tool_call["arguments"]) if isinstance(tool_call["arguments"], str) else tool_call["arguments"]
                
                tool_span_id = tracer.start_span(f"agent.tool_call.{fn_name}", parent_span_id=step_span_id, attributes={"args": str(fn_args)})
                print(f"  Action: {fn_name}({fn_args})")
                
                tool_fn = TOOL_FUNCTIONS.get(fn_name)
                
                # Execute tool with retries
                result = "Error: Tool execution failed."
                for retry in range(2):
                    try:
                        result = tool_fn(**fn_args) if tool_fn else f"Error: Tool {fn_name} not found"
                        break
                    except Exception as e:
                        print(f"    [Tool Retry] Attempt {retry+1} failed: {e}")
                        time.sleep(0.1)

                print(f"  Observation: {result[:120]}...")
                tracer.end_span(tool_span_id, "OK" if "Error" not in result else "ERROR", {"result_preview": result[:50]})

                trace.append({"step": step + 1, "tool": fn_name, "args": fn_args, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })

                if fn_name == "generate_markdown_report":
                    # Successful generation terminates loop
                    tracer.end_span(step_span_id, "COMPLETE")
                    tracer.end_span(root_span_id, "OK")
                    return {
                        "goal": goal,
                        "plan": plan,
                        "final_report": result,
                        "provider_used": resp.provider_name,
                        "trace": trace,
                        "otel_spans": tracer.spans
                    }

            tracer.end_span(step_span_id, "STEP_PROCESSED")

        tracer.end_span(root_span_id, "MAX_STEPS")
        return {
            "goal": goal,
            "plan": plan,
            "final_answer": "Reached max execution steps.",
            "trace": trace,
            "otel_spans": tracer.spans
        }
