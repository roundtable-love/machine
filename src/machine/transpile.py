"""MACHINE-1.0 transpiler CLI.

Environment:
  MODEL_PROVIDER      gemini (default) | claude | openai
  CLAUDE_MODEL  default: claude-sonnet-4-6
  OPENAI_MODEL  default: gpt-4o
  GEMINI_MODEL  default: gemini-2.0-flash
  GEMINI_API_KEY  required for gemini provider
"""

import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated, Literal

import typer

from .providers import DEFAULT_PROVIDER, PROVIDERS, transpile
from .spec import LANGUAGE_CODES, NodeType

main = typer.Typer(help=__doc__)


def _languages_callback(value: bool) -> None:
    if value:
        typer.echo(" ".join(LANGUAGE_CODES))
        raise typer.Exit()


def _node_types_callback(value: bool) -> None:
    if value:
        typer.echo(" ".join((node.value for node in NodeType)))
        raise typer.Exit()


@main.command()
def _main(
    node_type: Annotated[NodeType, typer.Argument(help="Target node type")],
    lang: Annotated[
        Literal[*LANGUAGE_CODES], typer.Argument(help="ISO 639-1/3 language code")
    ],
    source: Annotated[Path, typer.Argument(help="Source")],
    provider: Annotated[
        Literal[*PROVIDERS.keys()], typer.Argument(help="Provider name")
    ] = DEFAULT_PROVIDER,
    languages: Annotated[
        bool,
        typer.Option(
            "--languages",
            help="Print supported language codes and exit.",
            callback=_languages_callback,
            is_eager=True,
        ),
    ] = False,
    node_types: Annotated[
        bool,
        typer.Option(
            "--node-types",
            help="Print supported node types and exit.",
            callback=_node_types_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    if node_type is NodeType.newborn:
        # newborn: L1 signal only — no L3 text output.
        typer.echo("N/A")
    else:
        typer.echo(
            asyncio.run(
                transpile(
                    node_type.value,
                    lang,
                    source,
                    provider=provider,
                )
            )
        )


if __name__ == "__main__":
    main()
