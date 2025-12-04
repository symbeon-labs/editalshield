"""Anthropic Claude provider implementation."""

import os
from typing import Optional

import anthropic
from anthropic import Anthropic

from docsync.core.llm import LLMProvider, LLMResponse


class ClaudeProvider(LLMProvider):
    """Anthropic Claude implementation of LLMProvider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-haiku-20241022"):
        """Initialize Claude provider.

        Args:
            api_key: Anthropic API key. If None, tries to get from env var ANTHROPIC_API_KEY.
            model: Model to use. Defaults to "claude-3-5-haiku-20241022".
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Please provide it or set ANTHROPIC_API_KEY environment variable."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate text using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text if response.content else ""
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            }

            return LLMResponse(
                content=content,
                model=self.model,
                usage=usage,
            )
        except anthropic.APIError as e:
            raise RuntimeError(f"Anthropic API error: {e}") from e
