"""
Exercise 01: Build a Resilient LLM Gateway with Fallbacks (Starter)
====================================================================
Course 12 — LLMOps & Production Systems

Goal: Implement an enterprise LLM Provider Gateway supporting primary-fallback
      routing, exponential backoff retries, and sliding-window rate limiting.

Instructions:
  1. Complete the TODO sections below.
  2. Run: python 01-starter.py
  3. Compare your output with 01-solution.py

Zero external dependencies required — standard library Python only.
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
        # Simulate network latency
        time.sleep(random.uniform(*self.latency_range))
        # Simulate random provider outage/error
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
        """
        TODO: Implement a sliding-window rate limiter.
        1. Remove timestamps older than 60.0 seconds from self.request_timestamps.
        2. If remaining count >= self.max_rpm, return False (rate limited).
        3. Otherwise, append time.time() to self.request_timestamps and return True.
        """
        pass  # Your code here

    def generate(self, request: GatewayRequest, max_retries_per_provider: int = 2) -> GatewayResponse:
        """
        TODO: Implement resilient request execution.
        1. Call _check_rate_limit(). Raise PermissionError if rate limit exceeded.
        2. Attempt primary provider first.
        3. Retry primary up to max_retries_per_provider times with exponential backoff (e.g. 0.1 * 2^attempt).
        4. If primary fails all retries, iterate through fallback_providers in order.
        5. Return a GatewayResponse capturing content, provider_used, latency_ms, and retry count.
        6. If ALL providers fail, raise RuntimeError("All LLM providers unavailable").
        """
        pass  # Your code here


# ── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Setup Primary (OpenAI) with high failure rate (70%) and Fallback (Anthropic, Google)
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
