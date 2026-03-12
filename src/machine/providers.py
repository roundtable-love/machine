"""LLM provider backends for transpilation."""

import os
from typing import Callable

Provider = Callable[[str], str]

DEFAULT_PROVIDER = "gemini"


def claude(prompt: str) -> str:
    import anthropic
    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def gemini(prompt: str) -> str:
    from google import genai
    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return client.models.generate_content(model=model, contents=prompt).text


def openai(prompt: str) -> str:
    import openai as _openai
    model = os.environ.get("OPENAI_MODEL", "gpt-4o")
    client = _openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


PROVIDERS: dict[str, Provider] = {
    "claude": claude,
    "gemini": gemini,
    "openai": openai,
}
