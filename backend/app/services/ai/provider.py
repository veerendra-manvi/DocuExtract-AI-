import json
import logging
import time
from typing import Any, Dict, Tuple

import openai

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIProvider:
    """
    Abstracts API interactions with LLMs, seamlessly switching between OpenAI and Groq based on config.
    """

    def __init__(self):
        self.provider_name = settings.LLM_PROVIDER.lower()

        if self.provider_name == "groq":
            api_key = settings.GROQ_API_KEY or "dummy"
            self.base_url = "https://api.groq.com/openai/v1"
            self.client = openai.AsyncOpenAI(
                api_key=api_key, base_url=self.base_url, timeout=60.0, max_retries=2
            )
            # Use current supported Groq model
            self.model = "llama-3.3-70b-versatile"
        else:
            api_key = settings.OPENAI_API_KEY or "dummy"
            self.base_url = "https://api.openai.com/v1"
            self.client = openai.AsyncOpenAI(
                api_key=api_key, timeout=60.0, max_retries=2
            )
            # OpenAI standard fast model
            self.model = "gpt-4o-mini"

    async def generate_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.0
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Calls the LLM and returns (response_text, usage_metrics).
        Handles specific API exceptions gracefully.
        """
        start_time = time.time()

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        logger.info(
            f"AI Provider details - Provider: {self.provider_name}, Base URL: {self.base_url}, Model: {self.model}"
        )
        logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")

        try:
            response = await self.client.chat.completions.create(**payload)

            execution_time = time.time() - start_time
            content = response.choices[0].message.content or "{}"

            logger.debug(f"Response Received: {content}")

            usage = {}
            if response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }

            metrics = {
                "provider": self.provider_name,
                "execution_time_sec": round(execution_time, 2),
                "usage": usage,
            }

            return content, metrics

        except Exception as e:
            logger.error(
                f"AI Provider Error: Provider={self.provider_name}, Model={self.model}, URL={self.base_url}"
            )
            logger.exception(f"Full traceback for AI Provider Exception: {e}")
            # Raise the actual exception as a RuntimeError so it's not masked as Invalid API Key
            raise RuntimeError(str(e)) from e
