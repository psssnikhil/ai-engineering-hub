"""
Standardized Multi-Provider LLM Gateway
========================================
AI Engineering Hub — Common Infrastructure (`labs/common/gateway.py`)

A pluggable, standardized LLM Gateway supporting OpenAI and Anthropic out-of-the-box,
with automatic fallback chaining, rate limiting, and unified message formats.

Contributors can easily add new providers (Ollama, Gemini, Bedrock) by implementing
the `BaseProvider` interface.

Usage:
  from labs.common.gateway import LLMGateway, OpenAIProvider, AnthropicProvider

  gateway = LLMGateway(providers=[
      OpenAIProvider(model="gpt-4o-mini"),
      AnthropicProvider(model="claude-3-5-haiku-20241022"),
  ])

  response = gateway.generate(messages=[{"role": "user", "content": "Hello!"}])
"""

import os
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
    """Abstract base class for all LLM providers (OpenAI, Anthropic, Ollama, Gemini)."""

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


class OpenAIProvider(BaseProvider):
    """OpenAI API Provider implementation."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        super().__init__(name="OpenAI", model=model)
        from openai import OpenAI

        key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=key) if key else OpenAI()

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

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> ProviderResponse:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else anthropic.Anthropic()
        # Format messages for Anthropic (separate system prompt)
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
    """Unified Multi-Provider Gateway with automatic fallback routing."""

    def __init__(self, providers: Optional[List[BaseProvider]] = None):
        if providers:
            self.providers = providers
        else:
            # Default to OpenAI as primary
            self.providers = [OpenAIProvider()]

    def register_provider(self, provider: BaseProvider) -> None:
        """Register a new provider dynamically (e.g. Ollama, Gemini, Bedrock)."""
        self.providers.append(provider)

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        max_retries_per_provider: int = 2,
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
                    time.sleep(0.1 * (2 ** attempt))

        raise RuntimeError(f"All LLM providers failed in fallback chain. Last error: {last_error}")
