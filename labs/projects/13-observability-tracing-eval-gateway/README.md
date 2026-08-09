# Project 13: Observability, Tracing & Real-Time Eval AI Gateway

**Domain:** LLMOps, Telemetry Gateway & Continuous Production Evals  
**Course Mapping:** Course 12 (LLMOps) & Course 13 (LLM Evaluation)

---

## 🎯 Overview

An enterprise AI proxy gateway demonstrating OpenTelemetry distributed trace context propagation, Prometheus SLA telemetry aggregation (TTFT, token metrics, cost estimation), continuous online faithfulness evaluation, and circuit-breaker model fallback routing.

---

## 🚀 Key Features

1. **OpenTelemetry Trace Spans**: Captures `ai_gateway.ingress`, `gen_ai.client.generate`, and `ai_gateway.online_eval` spans.
2. **Prometheus Telemetry**: Tracks aggregated prompt/completion token consumption, request failures, and USD costs.
3. **Continuous Real-Time Evals**: Runs light-weight faithfulness evaluation inline without blocking response streaming.
4. **Resilient Circuit Breaker**: Routes requests to fallback model replicas on latency spikes or provider errors.

---

## 💻 Quickstart

Run the gateway demo:

```bash
python main.py
```
