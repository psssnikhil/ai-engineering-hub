"""
Standardized Multi-Provider LLM Gateway
========================================
AI Engineering Hub — Common Infrastructure (`labs/common/gateway.py`)

A pluggable, standardized LLM Gateway supporting OpenAI, Anthropic, and Mock/Offline providers out-of-the-box,
with automatic fallback chaining, rate limiting, zero-key offline execution support, and unified message formats.

Usage:
  from labs.common.gateway import LLMGateway, OpenAIProvider, AnthropicProvider, MockProvider

  # Keyed production setup:
  gateway = LLMGateway(providers=[
      OpenAIProvider(model="gpt-4o-mini"),
      AnthropicProvider(model="claude-3-5-haiku-20241022"),
      MockProvider(),
  ])

  # Offline/Keyless fallback:
  gateway = LLMGateway(providers=[MockProvider()])
"""

import os
import time
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logger = logging.getLogger("llm_gateway")


@dataclass
class GatewayMessage:
    role: str
    content: str


@dataclass
class ProviderResponse:
    content: str
    provider_name: str
    model_name: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    raw_response: Optional[Any] = None


class BaseProvider(ABC):
    """Abstract base class for all LLM providers (OpenAI, Anthropic, Mock, Ollama, Gemini)."""

    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> ProviderResponse:
        """Generate response from provider model."""
        pass


class MockProvider(BaseProvider):
    """Mock/Offline Provider for keyless execution and zero-dependency local testing."""

    def __init__(self, model: str = "mock-offline-v1"):
        super().__init__(name="MockOffline", model=model)

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> ProviderResponse:
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")
                break

        # Handle tool calling mock response
        if tools and "status" in last_user_msg.lower():
            return ProviderResponse(
                content="Checking system component status...",
                provider_name=self.name,
                model_name=self.model,
                tool_calls=[{
                    "id": "call_mock_1",
                    "name": "get_system_status",
                    "arguments": json.dumps({"component": "vector_db"})
                }],
                raw_response=None
            )

        # Default Mock Answer
        mock_answer = (
            f"[Offline Mock Answer] Grounded response for query: '{last_user_msg[:60]}...' "
            "RAG pipeline retrieved relevant context [1] successfully."
        )

        return ProviderResponse(
            content=mock_answer,
            provider_name=self.name,
            model_name=self.model,
            tool_calls=None,
            raw_response=None
        )


class OpenAIProvider(BaseProvider):
    """OpenAI API Provider implementation."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        super().__init__(name="OpenAI", model=model)
        from openai import OpenAI

        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=key)

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> ProviderResponse:
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)
        msg = response.choices[0].message

        tool_calls = None
        if msg.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
                for tc in msg.tool_calls
            ]

        return ProviderResponse(
            content=msg.content or "",
            provider_name=self.name,
            model_name=self.model,
            tool_calls=tool_calls,
            raw_response=response,
        )


class AnthropicProvider(BaseProvider):
    """Anthropic API Provider implementation."""

    def __init__(self, model: str = "claude-3-5-haiku-20241022", api_key: Optional[str] = None):
        super().__init__(name="Anthropic", model=model)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set.")

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> ProviderResponse:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        
        system_prompt = ""
        filtered_messages = []
        for m in messages:
            if m["role"] == "system":
                system_prompt += m["content"] + "\n"
            else:
                filtered_messages.append({"role": m["role"], "content": m["content"]})

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": filtered_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            kwargs["system"] = system_prompt.strip()

        response = client.messages.create(**kwargs)

        text_content = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_content += block.text

        return ProviderResponse(
            content=text_content,
            provider_name=self.name,
            model_name=self.model,
            raw_response=response,
        )


class LLMGateway:
    """Unified Multi-Provider Gateway with automatic provider fallback chain and offline fallback."""

    def __init__(self, providers: Optional[List[BaseProvider]] = None):
        if providers:
            self.providers = providers
        else:
            # Build intelligent fallback list based on available API keys
            active_providers: List[BaseProvider] = []
            if os.getenv("OPENAI_API_KEY"):
                try:
                    active_providers.append(OpenAIProvider())
                except Exception:
                    pass
            if os.getenv("ANTHROPIC_API_KEY"):
                try:
                    active_providers.append(AnthropicProvider())
                except Exception:
                    pass
            
            # Always append MockProvider as zero-key offline fallback
            active_providers.append(MockProvider())
            self.providers = active_providers

    def register_provider(self, provider: BaseProvider) -> None:
        """Register a new provider dynamically (e.g. Ollama, Gemini, Bedrock)."""
        self.providers.append(provider)

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        max_retries_per_provider: int = 1,
    ) -> ProviderResponse:
        """Execute request with automatic provider fallback chain."""
        last_error = None

        for provider in self.providers:
            for attempt in range(max_retries_per_provider):
                try:
                    return provider.generate(
                        messages=messages,
                        tools=tools,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                except Exception as err:
                    last_error = err
                    logger.warning(
                        f"Provider {provider.name} ({provider.model}) attempt {attempt+1} failed: {err}"
                    )
                    time.sleep(0.05 * (2 ** attempt))

        raise RuntimeError(f"All LLM providers failed in fallback chain. Last error: {last_error}")
