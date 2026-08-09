"""
Exercise 01: Build a Resilient LLM Gateway with Fallbacks (Solution)
=====================================================================
Course 12 — LLMOps & Production Systems
"""

import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class GatewayRequest:
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7


@dataclass
class GatewayResponse:
    content: str
    provider_used: str
    latency_ms: float
    retries: int


class MockProviderAPI:
    """Simulates an external LLM API provider with latency and failure rate."""

    def __init__(self, name: str, failure_rate: float = 0.3, latency_range: Tuple[float, float] = (0.1, 0.4)):
        self.name = name
        self.failure_rate = failure_rate
        self.latency_range = latency_range

    def call(self, prompt: str) -> str:
        time.sleep(random.uniform(*self.latency_range))
        if random.random() < self.failure_rate:
            raise RuntimeError(f"Provider {self.name} HTTP 503 Service Unavailable")
        return f"[{self.name} Answer]: Processed '{prompt[:30]}...'"


class LLMGateway:
    """Production LLM Gateway with routing, fallbacks, and rate limiting."""

    def __init__(self, primary_provider: MockProviderAPI, fallback_providers: List[MockProviderAPI], max_requests_per_minute: int = 10):
        self.primary = primary_provider
        self.fallbacks = fallback_providers
        self.max_rpm = max_requests_per_minute
        self.request_timestamps: List[float] = []

    def _check_rate_limit(self) -> bool:
        """Sliding-window rate limiter implementation."""
        now = time.time()
        # Filter timestamps within the 60-second window
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 60.0]

        if len(self.request_timestamps) >= self.max_rpm:
            return False

        self.request_timestamps.append(now)
        return True

    def generate(self, request: GatewayRequest, max_retries_per_provider: int = 2) -> GatewayResponse:
        """Execute request with retries and provider fallback chain."""
        if not self._check_rate_limit():
            raise PermissionError(f"Rate limit exceeded ({self.max_rpm} RPM maximum)")

        start_time = time.time()
        total_retries = 0

        all_providers = [self.primary] + self.fallbacks

        for provider in all_providers:
            for attempt in range(max_retries_per_provider):
                try:
                    content = provider.call(request.prompt)
                    latency = (time.time() - start_time) * 1000.0
                    return GatewayResponse(
                        content=content,
                        provider_used=provider.name,
                        latency_ms=latency,
                        retries=total_retries,
                    )
                except Exception:
                    total_retries += 1
                    # Exponential backoff before retrying
                    time.sleep(0.05 * (2 ** attempt))

        raise RuntimeError("All LLM providers unavailable after fallback chain")


if __name__ == "__main__":
    primary_api = MockProviderAPI(name="OpenAI-GPT-4o", failure_rate=0.7)
    fallback_1 = MockProviderAPI(name="Anthropic-Claude-3.5", failure_rate=0.2)
    fallback_2 = MockProviderAPI(name="Google-Gemini-1.5", failure_rate=0.1)

    gateway = LLMGateway(
        primary_provider=primary_api,
        fallback_providers=[fallback_1, fallback_2],
        max_requests_per_minute=5,
    )

    print("--- Simulating Requests through Resilient Gateway ---")
    for i in range(1, 4):
        req = GatewayRequest(prompt=f"Explain vector search indexed documents step {i}")
        try:
            resp = gateway.generate(req)
            print(f"Request {i} SUCCESS: {resp.content}")
            print(f"   Provider: {resp.provider_used} | Latency: {resp.latency_ms:.1f}ms | Retries: {resp.retries}")
        except Exception as e:
            print(f"Request {i} FAILED: {e}")

    print("\n--- Testing Rate Limiting (Burst 4 requests) ---")
    for i in range(4, 8):
        req = GatewayRequest(prompt=f"Burst prompt {i}")
        try:
            resp = gateway.generate(req)
            print(f"Request {i} SUCCESS via {resp.provider_used}")
        except PermissionError as e:
            print(f"Request {i} BLOCKED: {e}")
        except Exception as e:
            print(f"Request {i} ERROR: {e}")
