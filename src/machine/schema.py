"""Generate standard.schema.json from standard/standard.md."""

import json
import re
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer(help=__doc__)

_default_source = Path(__file__).parents[3] / "standard" / "standard.md"


def _enum(text: str, heading: str) -> list[str]:
    # extract sorted backtick-quoted values from the first table column under a heading.
    m = re.search(
        rf"###\s+{heading}.*?\n(.*?)(?=^##|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not m:
        return []
    return sorted(
        vm.group(1)
        for line in m.group(1).splitlines()
        if (vm := re.match(r"\|\s+`([^`]+)`", line))
    )


def generate(text: str) -> dict:
    base_class = _enum(text, r"[\d.]+\s+`base_class`")
    status     = _enum(text, r"[\d.]+\s+`metadata\.status`")
    level      = _enum(text, r"[\d.]+\s+`compliance_matrix`\s+`level`")

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "machine/standard.schema.json",
        "title": "Standard",
        "description": "Engineering standard document.",
        "type": "object",
        "required": ["metadata", "standard"],
        "additionalProperties": False,
        "properties": {
            "compliance_matrix": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "l1_physical": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "forbidden":   {"type": "array", "items": {"type": "string"}},
                            "level":       {"type": "string", "enum": level},
                            "requirement": {"type": "string"},
                        },
                    },
                    "l2_data_link": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "action":    {"type": "string"},
                            "interrupt": {"type": "string"},
                            "trigger":   {"type": "string"},
                        },
                    },
                    "l3_network": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "integrity": {"type": "string"},
                            "protocol":  {"type": "string"},
                        },
                    },
                },
            },
            "logic_gate": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "input":    {"type": "string"},
                    "output_0": {"type": "string"},
                    "output_1": {"type": "string"},
                    "process":  {"type": "string"},
                },
            },
            "metadata": {
                "type": "object",
                "required": ["custodian", "status"],
                "additionalProperties": False,
                "properties": {
                    "custodian": {"type": "string"},
                    "origin":    {"type": "string"},
                    "source":    {"type": "string"},
                    "status":    {"type": "string", "enum": status},
                },
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["quote", "source"],
                    "additionalProperties": False,
                    "properties": {
                        "quote":  {"type": "string"},
                        "ref":    {"type": "string", "format": "uri"},
                        "source": {"type": "string"},
                    },
                },
            },
            "standard": {
                "type": "object",
                "required": ["base_class", "philosophy", "uid", "version"],
                "additionalProperties": False,
                "properties": {
                    "alias":      {"type": "array", "items": {"type": "string"}},
                    "base_class": {"type": "string", "enum": base_class},
                    "philosophy": {"type": "string"},
                    "uid":        {"type": "string", "pattern": "^[A-Z]+-[0-9]+$"},
                    "version":    {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+"},
                },
            },
        },
    }


@app.command()
def main(
    source: Annotated[
        Optional[Path],
        typer.Argument(help="Path to standard.md"),
    ] = None,
) -> None:
    path = source or _default_source
    typer.echo(json.dumps(generate(path.read_text()), indent=2))


if __name__ == "__main__":
    app()
