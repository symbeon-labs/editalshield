"""Google Gemini provider implementation."""

import os
from typing import Optional

import google.generativeai as genai

from docsync.core.llm import LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):
    """Google Gemini implementation of LLMProvider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        """Initialize Gemini provider.

        Args:
            api_key: Google API key. If None, tries to get from env var GOOGLE_API_KEY.
            model: Model to use. Defaults to "gemini-2.0-flash-exp".
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Please provide it or set GOOGLE_API_KEY environment variable."
            )
        genai.configure(api_key=self.api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate text using Gemini API."""
        try:
            # Combine system prompt with user prompt if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.model.generate_content(full_prompt)

            # Estimate tokens (Gemini doesn't provide exact counts in all cases)
            usage = {
                "total_tokens": len(full_prompt.split()) + len(response.text.split()),
            }

            return LLMResponse(
                content=response.text,
                model=self.model_name,
                usage=usage,
            )
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}") from e
