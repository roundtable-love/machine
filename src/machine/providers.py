"""LLM provider backends for transpilation."""

import asyncio
import os
import pathlib
from functools import cache, partial
from typing import Callable

from google import genai
from google.api_core import exceptions as google_exceptions
import tenacity
import anthropic
import openai

from .prompt import prompt

DEFAULT_PROVIDER = "gemini"

MODELS = dict(
    claude=os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5"),
    gemini=os.environ.get("GEMINI_MODEL", "gemini-3.0-flash"),
    openai=os.environ.get("OPENAI_MODEL", "gpt-5-mini"),
)

CLIENTS = dict(
    claude=cache(anthropic.AsyncAnthropic),
    gemini=cache(partial(genai.Client, api_key=os.environ["GEMINI_API_KEY"])),
    openai=cache(openai.AsyncOpenAI),
)


async def _claude(prompt: str) -> str:
    return (
        (
            await CLIENTS["claude"]().messages.create(
                model=MODELS["claude"],
                max_tokens=8096,
                messages=[{"role": "user", "content": prompt}],
            )
        )
        .content[0]
        .text
    )


async def _gemini(prompt: str) -> str:
    return (
        await CLIENTS["gemini"]().aio.models.generate_content(
            model=MODELS["gemini"],
            contents=prompt,
        )
    ).text


async def _openai(prompt: str) -> str:
    return (
        (
            await CLIENTS["openai"]().chat.completions.create(
                model=MODELS["openai"],
                messages=[{"role": "user", "content": prompt}],
            )
        )
        .choices[0]
        .message.content
    )


PROVIDERS = dict(
    claude=_claude,
    gemini=_gemini,
    openai=_openai,
)

RETRYABLE_ERRORS = (
    anthropic.RateLimitError,
    anthropic.InternalServerError,
    anthropic.APITimeoutError,
    google_exceptions.TooManyRequests,
    google_exceptions.InternalServerError,
    google_exceptions.ServiceUnavailable,
    openai.RateLimitError,
    openai.InternalServerError,
    openai.APITimeoutError,
)

semaphore = asyncio.Semaphore(int(os.environ.get("MODEL_CONCURRENCY", 10)))


@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(RETRYABLE_ERRORS),
)
async def transpile(
    target_node: str, lang: str, source: str, *, provider=DEFAULT_PROVIDER
):
    async with semaphore:
        return await PROVIDERS[provider](prompt(target_node, lang, source))
