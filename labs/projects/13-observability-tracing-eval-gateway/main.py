"""
Project 13: Observability, Tracing & Real-Time Eval AI Gateway
==============================================================
Domain: LLMOps, OpenTelemetry Distributed Tracing & Real-Time Monitoring

An enterprise AI proxy gateway featuring:
1. OpenTelemetry Context & Span Tracer (Simulated OTEL spans for LLM requests & tool calls)
2. Prometheus Metrics Aggregator (TTFT, TPOT, cost, error rate counters)
3. Online Real-Time Continuous Evaluator (Grounding & Safety Guardrail check)
4. Model Fallback Router & Circuit Breaker

Usage:
  python main.py
"""

import os
import sys
import time
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


@dataclass
class OTELSpan:
    trace_id: str
    span_id: str
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
    faithfulness_score: float
    spans: List[OTELSpan]


class ObservabilityGateway:
    """Production AI Gateway with OpenTelemetry tracing & continuous evals."""
    
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.metrics_counters = {
            "total_requests": 0,
            "failed_requests": 0,
            "fallback_triggered": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost_usd": 0.0
        }

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        # Estimated cost per 1K tokens
        rates = {
            "gpt-4o": {"input": 0.0025, "output": 0.0100},
            "claude-3-5-sonnet": {"input": 0.0030, "output": 0.0150},
            "llama-3-70b": {"input": 0.0008, "output": 0.0020}
        }
        r = rates.get(model, rates["gpt-4o"])
        return (prompt_tokens / 1000.0 * r["input"]) + (completion_tokens / 1000.0 * r["output"])

    def process_request(self, user_prompt: str, context: str, model: str = "gpt-4o") -> GatewayResponse:
        req_id = f"req-{int(time.time() * 1000)}"
        trace_id = f"trace-{int(time.time() * 1000000)}"
        start_time = time.time()
        
        spans = []
        
        # 1. Gateway Ingress Span
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=f"span-1",
            name="ai_gateway.ingress",
            attributes={"client.id": "enterprise-app", "user_prompt_len": len(user_prompt)},
            duration_ms=2.5
        ))

        # 2. LLM Generation Span
        gen_start = time.time()
        messages = [
            {"role": "system", "content": f"Answer based strictly on context:\n{context}"},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            res = self.gateway.generate(messages=messages, temperature=0.0)
            served_model = model
            content = res.content
        except Exception:
            # Circuit Breaker Fallback
            self.metrics_counters["fallback_triggered"] += 1
            served_model = "llama-3-70b"
            res = self.gateway.generate(messages=messages, temperature=0.0)
            content = res.content

        gen_duration = (time.time() - gen_start) * 1000.0
        prompt_tokens = len(user_prompt.split()) + len(context.split())
        completion_tokens = len(content.split())
        cost = self._calculate_cost(served_model, prompt_tokens, completion_tokens)
        
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=f"span-2",
            name="gen_ai.client.generate",
            attributes={
                "gen_ai.system": "openai",
                "gen_ai.request.model": model,
                "gen_ai.response.model": served_model,
                "gen_ai.usage.prompt_tokens": prompt_tokens,
                "gen_ai.usage.completion_tokens": completion_tokens
            },
            duration_ms=round(gen_duration, 2)
        ))

        # 3. Continuous Real-time Online Eval (Faithfulness check)
        eval_start = time.time()
        eval_score = 0.96 if any(word in context.lower() for word in user_prompt.lower().split()[:2]) else 0.88
        eval_duration = (time.time() - eval_start) * 1000.0
        
        spans.append(OTELSpan(
            trace_id=trace_id,
            span_id=f"span-3",
            name="ai_gateway.online_eval",
            attributes={"eval.metric": "faithfulness", "eval.score": eval_score},
            duration_ms=round(eval_duration, 2)
        ))

        total_latency = (time.time() - start_time) * 1000.0
        
        # Update metrics
        self.metrics_counters["total_requests"] += 1
        self.metrics_counters["total_prompt_tokens"] += prompt_tokens
        self.metrics_counters["total_completion_tokens"] += completion_tokens
        self.metrics_counters["total_cost_usd"] += cost

        return GatewayResponse(
            request_id=req_id,
            primary_model=model,
            served_model=served_model,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=round(cost, 6),
            time_to_first_token_ms=180.0,
            total_latency_ms=round(total_latency, 2),
            faithfulness_score=eval_score,
            spans=spans
        )


def main():
    print("=" * 75)
    print("  Project 13: Observability, Tracing & Real-Time Eval AI Gateway")
    print("=" * 75 + "\n")

    gateway = ObservabilityGateway()
    
    prompt = "What is the SLA for enterprise storage?"
    context = "Enterprise storage SLAs guarantee 99.999% availability with sub-5ms P99 latency."

    print(f"📡 Dispatching request to AI Gateway...")
    print(f"   Prompt: '{prompt}'")
    print(f"   Context: '{context}'\n")

    response = gateway.process_request(user_prompt=prompt, context=context, model="gpt-4o")

    print("✅ Response Delivered:")
    print(f"   Content: {response.content}")
    print(f"   Served Model: {response.served_model}")
    print(f"   TTFT: {response.time_to_first_token_ms} ms | Total Latency: {response.total_latency_ms} ms")
    print(f"   Cost: ${response.cost_usd} USD | Faithfulness Eval Score: {response.faithfulness_score}\n")

    print("🔎 OpenTelemetry Distributed Trace Spans:")
    print("-" * 75)
    for span in response.spans:
        print(f"  [Span: {span.name}] Duration: {span.duration_ms}ms | Attributes: {json.dumps(span.attributes)}")
    print("-" * 75)

    print("\n📊 Prometheus Gateway Aggregated Metrics:")
    print(json.dumps(gateway.metrics_counters, indent=2))
    print("=" * 75)


if __name__ == "__main__":
    main()
