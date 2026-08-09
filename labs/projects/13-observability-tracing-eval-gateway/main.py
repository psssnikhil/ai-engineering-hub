"""
Project 13: Observability, Tracing & Real-Time Eval AI Gateway
==============================================================
Domain: LLMOps, OpenTelemetry Distributed Tracing & Real-Time Monitoring

Features:
  1. OpenTelemetry Context Tracing: Implements span hierarchies matching trace conventions.
  2. Prometheus Metrics Aggregator: Formats aggregated operational metrics in official Prometheus format.
  3. Real-Time Online Evaluator: Validates prompt safety and answer grounding on the fly.
  4. Circuit Breaker Fallback Router: Automatically trips and redirects requests to secondary models.
"""

import os
import sys
import time
import json
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


@dataclass
class OTELSpan:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    attributes: Dict[str, Any]
    duration_ms: float
    status: str = "OK"


@dataclass
class GatewayResponse:
    request_id: str
    primary_model: str
    served_model: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    time_to_first_token_ms: float
    total_latency_ms: float
    safety_score: float
    faithfulness_score: float
    spans: List[OTELSpan]


class CircuitBreaker:
    """Monitors request failures and trips route fallback when error thresholds are crossed."""
    def __init__(self, failure_threshold: int = 2, recovery_timeout_sec: float = 5.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.failure_count = 0
        self.last_state_change = time.time()

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = time.time()
            print(f"  [Circuit Breaker] Tripped! State transitioned to OPEN. Fallbacks active.")

    def allow_request(self) -> bool:
        if self.state == "OPEN":
            # Check timeout for half-open check
            if time.time() - self.last_state_change > self.recovery_timeout_sec:
                self.state = "HALF-OPEN"
                print("  [Circuit Breaker] Entering HALF-OPEN state. Testing primary route.")
                return True
            return False
        return True


class ObservabilityGateway:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.circuit_breaker = CircuitBreaker()
        
        # Prometheus metric registers
        self.metrics = {
            "gateway_requests_total": 0,
            "gateway_errors_total": 0,
            "gateway_fallbacks_total": 0,
            "gateway_token_usage_total": {"prompt": 0, "completion": 0},
            "gateway_cost_usd_total": 0.0,
            "gateway_request_duration_ms_sum": 0.0
        }

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        rates = {
            "gpt-4o": {"input": 0.0025, "output": 0.0100},
            "claude-3-5-sonnet": {"input": 0.0030, "output": 0.0150},
            "mock-offline-v1": {"input": 0.0, "output": 0.0}
        }
        r = rates.get(model, rates["gpt-4o"])
        return (prompt_tokens / 1000.0 * r["input"]) + (completion_tokens / 1000.0 * r["output"])

    def process_request(self, user_prompt: str, context: str, model: str = "gpt-4o") -> GatewayResponse:
        request_id = f"req-{uuid.uuid4().hex[:8]}"
        trace_id = f"trace-{uuid.uuid4().hex[:12]}"
        
        start_time = time.time()
        spans = []

        # Span 1: Gateway Ingress
        span_ingress_id = f"span-1"
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=span_ingress_id,
            parent_span_id=None,
            name="gateway.ingress",
            attributes={"client.id": "enterprise-web", "prompt_len": len(user_prompt)},
            duration_ms=1.2
        ))

        # Span 2: Input Guardrail Check
        guard_start = time.time()
        # Mock safety check
        is_safe = "hack" not in user_prompt.lower()
        safety_score = 1.0 if is_safe else 0.1
        guard_duration = (time.time() - guard_start) * 1000.0
        
        span_guard_id = f"span-2"
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=span_guard_id,
            parent_span_id=span_ingress_id,
            name="gateway.guardrails.input",
            attributes={"metric.safety_score": safety_score},
            duration_ms=round(guard_duration, 2)
        ))

        if safety_score < 0.5:
            # Short-circuit block
            total_lat = (time.time() - start_time) * 1000.0
            self.metrics["gateway_errors_total"] += 1
            return GatewayResponse(
                request_id=request_id,
                primary_model=model,
                served_model="guardrail_blocked",
                content="Request blocked: safety validation failed.",
                prompt_tokens=0,
                completion_tokens=0,
                cost_usd=0.0,
                time_to_first_token_ms=0.0,
                total_latency_ms=round(total_lat, 2),
                safety_score=safety_score,
                faithfulness_score=1.0,
                spans=spans
            )

        # Span 3: LLM Generation (with Circuit Breaker logic)
        gen_start = time.time()
        served_model = model
        
        messages = [
            {"role": "system", "content": f"Answer based strictly on context:\n{context}"},
            {"role": "user", "content": user_prompt}
        ]

        # Check circuit breaker
        llm_success = True
        try:
            if not self.circuit_breaker.allow_request():
                # Primary circuit is open. Route straight to fallback!
                print("  [AI Gateway] Routing directly to fallback model due to tripped circuit.")
                self.metrics["gateway_fallbacks_total"] += 1
                served_model = "mock-offline-v1"
                # Call local mock provider or alternate gateway route
                res = self.gateway.generate(messages=messages, temperature=0.0)
                content = res.content
            else:
                # Attempt primary generation
                try:
                    # In reference testing, simulate primary model calling OpenAI
                    # If OPENAI_API_KEY is missing, let it raise exception to test Circuit Breaker
                    if not os.getenv("OPENAI_API_KEY"):
                        raise RuntimeError("API Key not found (Simulating API Down)")
                    res = self.gateway.generate(messages=messages, temperature=0.0)
                    content = res.content
                    self.circuit_breaker.record_success()
                except Exception as e:
                    print(f"  [AI Gateway] Primary API call failed: {e}. Activating fallback routing.")
                    llm_success = False
                    self.circuit_breaker.record_failure()
                    self.metrics["gateway_fallbacks_total"] += 1
                    
                    # Fallback to secondary model
                    served_model = "mock-offline-v1"
                    res = self.gateway.generate(messages=messages, temperature=0.0)
                    content = res.content
        except Exception as general_err:
            content = "Service temporarily unavailable due to gateway disruptions."
            llm_success = False
            self.metrics["gateway_errors_total"] += 1

        gen_duration = (time.time() - gen_start) * 1000.0
        prompt_tokens = len(user_prompt.split()) + len(context.split())
        completion_tokens = len(content.split())
        cost = self._calculate_cost(served_model, prompt_tokens, completion_tokens)

        span_llm_id = f"span-3"
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=span_llm_id,
            parent_span_id=span_ingress_id,
            name="gateway.llm.generate",
            attributes={
                "model.primary": model,
                "model.served": served_model,
                "tokens.prompt": prompt_tokens,
                "tokens.completion": completion_tokens,
                "cost.usd": cost,
                "status.success": llm_success
            },
            duration_ms=round(gen_duration, 2)
        ))

        # Span 4: Output Faithfulness Evaluation
        eval_start = time.time()
        # Heuristic check: check if words from answer exist in context
        common_words = set(content.lower().split()).intersection(set(context.lower().split()))
        faithfulness_score = len(common_words) / max(1, len(content.split()))
        eval_duration = (time.time() - eval_start) * 1000.0

        span_eval_id = f"span-4"
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=span_eval_id,
            parent_span_id=span_ingress_id,
            name="gateway.eval.faithfulness",
            attributes={"metric.faithfulness_score": round(faithfulness_score, 2)},
            duration_ms=round(eval_duration, 2)
        ))

        total_latency = (time.time() - start_time) * 1000.0

        # Update metrics
        self.metrics["gateway_requests_total"] += 1
        self.metrics["gateway_token_usage_total"]["prompt"] += prompt_tokens
        self.metrics["gateway_token_usage_total"]["completion"] += completion_tokens
        self.metrics["gateway_cost_usd_total"] += cost
        self.metrics["gateway_request_duration_ms_sum"] += total_latency

        return GatewayResponse(
            request_id=request_id,
            primary_model=model,
            served_model=served_model,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=round(cost, 6),
            time_to_first_token_ms=180.0,
            total_latency_ms=round(total_latency, 2),
            safety_score=safety_score,
            faithfulness_score=round(faithfulness_score, 2),
            spans=spans
        )

    def export_prometheus_metrics(self) -> str:
        """Serializes current registers into Prometheus exposition text format."""
        lines = [
            "# HELP gateway_requests_total Total requests processed by the AI proxy gateway.",
            "# TYPE gateway_requests_total counter",
            f"gateway_requests_total {self.metrics['gateway_requests_total']}",
            
            "# HELP gateway_errors_total Total errors encountered (failed or blocked requests).",
            "# TYPE gateway_errors_total counter",
            f"gateway_errors_total {self.metrics['gateway_errors_total']}",
            
            "# HELP gateway_fallbacks_total Total circuit breaker fallbacks triggered.",
            "# TYPE gateway_fallbacks_total counter",
            f"gateway_fallbacks_total {self.metrics['gateway_fallbacks_total']}",

            "# HELP gateway_token_usage_total Total tokens processed.",
            "# TYPE gateway_token_usage_total counter",
            f"gateway_token_usage_total{{type=\"prompt\"}} {self.metrics['gateway_token_usage_total']['prompt']}",
            f"gateway_token_usage_total{{type=\"completion\"}} {self.metrics['gateway_token_usage_total']['completion']}",

            "# HELP gateway_cost_usd_total Total aggregated API costs in USD.",
            "# TYPE gateway_cost_usd_total counter",
            f"gateway_cost_usd_total {round(self.metrics['gateway_cost_usd_total'], 6)}",

            "# HELP gateway_request_duration_ms_sum Total query latency sum in milliseconds.",
            "# TYPE gateway_request_duration_ms_sum counter",
            f"gateway_request_duration_ms_sum {round(self.metrics['gateway_request_duration_ms_sum'], 2)}"
        ]
        return "\n".join(lines)


def main():
    print("=" * 75)
    print("  Production AI Proxy Gateway with Circuit Breaker (Project 13)")
    print("=" * 75 + "\n")

    gateway = ObservabilityGateway()
    
    prompt = "What is the SLA for enterprise storage?"
    context = "Enterprise storage SLAs guarantee 99.999% availability with sub-5ms latency."

    print("--- Test 1: Normal Request (API Fallback Demo) ---")
    res1 = gateway.process_request(user_prompt=prompt, context=context)
    print(f"Served Model: {res1.served_model} | Latency: {res1.total_latency_ms} ms")
    print(f"Content: {res1.content}\n")

    # Force circuit breaker trip by sending multiple failed requests (simulated)
    print("--- Test 2: Triggering Circuit Breaker ---")
    gateway.circuit_breaker.record_failure()
    gateway.circuit_breaker.record_failure()  # Should trip now
    
    print(f"Circuit Breaker Status: {gateway.circuit_breaker.state}")
    
    # Request should bypass primary and served immediately from fallback mock
    res2 = gateway.process_request(user_prompt=prompt, context=context)
    print(f"Served Model: {res2.served_model} | Latency: {res2.total_latency_ms} ms")
    print(f"Content: {res2.content}\n")

    print("--- Exporting Prometheus Metrics Endpoint ---")
    print(gateway.export_prometheus_metrics())
    print("=" * 75)


if __name__ == "__main__":
    main()
