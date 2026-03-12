"""MACHINE-1.0 transpiler CLI.

Environment:
  MODEL_PROVIDER      gemini (default) | claude | openai
  CLAUDE_MODEL  default: claude-sonnet-4-6
  OPENAI_MODEL  default: gpt-4o
  GEMINI_MODEL  default: gemini-2.0-flash
  GEMINI_API_KEY  required for gemini provider
"""

import os
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from .languages import LANGUAGE_CODES
from .prompt import build_prompt
from .providers import DEFAULT_PROVIDER, PROVIDERS

app = typer.Typer(help=__doc__)

_default_source = Path(__file__).parents[2] / "machine.md"


def _languages_callback(value: bool) -> None:
    if value:
        typer.echo(" ".join(sorted(LANGUAGE_CODES)))
        raise typer.Exit()


class NodeType(str, Enum):
    newborn = "newborn"
    infant = "infant"
    child = "child"
    subject = "subject"
    student = "student"
    peer = "peer"


@app.command()
def main(
    node_type: Annotated[NodeType, typer.Argument(help="Target node type")],
    lang: Annotated[str, typer.Argument(help="ISO 639-1/3 language code")],
    source: Annotated[Path, typer.Option(help="Path to machine.md")] = _default_source,
    languages: Annotated[
        bool,
        typer.Option(
            "--languages",
            help="Print supported language codes and exit.",
            callback=_languages_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    if lang not in LANGUAGE_CODES:
        typer.echo(
            f"Unknown language '{lang}'. Registered codes: {', '.join(sorted(LANGUAGE_CODES))}",
            err=True,
        )
        raise typer.Exit(code=1)

    # newborn: L1 signal only — no L3 text output.
    if node_type is NodeType.newborn:
        typer.echo("N/A")
        return

    provider_name = os.environ.get("MODEL_PROVIDER", DEFAULT_PROVIDER).lower()
    if provider_name not in PROVIDERS:
        typer.echo(
            f"Unknown model provider '{provider_name}'. Choose from: {', '.join(PROVIDERS)}",
            err=True,
        )
        raise typer.Exit(code=1)

    prompt = build_prompt(node_type.value, lang, source.read_text())
    typer.echo(PROVIDERS[provider_name](prompt))


if __name__ == "__main__":
    app()
