"""OpenAI provider implementation."""

import os
from typing import Optional

import openai
from openai import OpenAI

from docsync.core.llm import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLMProvider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key. If None, tries to get from env var OPENAI_API_KEY.
            model: Model to use. Defaults to "gpt-4o-mini".
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please provide it or set OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate text using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            
            content = response.choices[0].message.content or ""
            usage = response.usage.model_dump() if response.usage else {}

            return LLMResponse(
                content=content,
                model=self.model,
                usage=usage,
            )
        except openai.APIError as e:
            raise RuntimeError(f"OpenAI API error: {e}") from e
