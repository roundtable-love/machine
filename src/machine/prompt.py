"""Prompt construction for MACHINE-1.0 transpilation."""

import contextlib
import re
from importlib.resources import files
from pathlib import Path

import langcodes


def _read() -> str:
    # 1. installed package resource (pip install / nix package).
    with contextlib.suppress(FileNotFoundError, TypeError):
        return files("machine").joinpath("machine.md").read_text(encoding="utf-8")

    # 2. git root fallback (editable / dev).
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            candidate = parent / "machine.md"
            if candidate.exists():
                return candidate.read_text(encoding="utf-8")

    raise FileNotFoundError("machine.md not found as package resource or at git root")


def _parse_rules(text: str) -> dict[str, str]:
    # extract transpilation rules from §4.2.x node sections.
    rules: dict[str, str] = {}
    for section in re.split(r"^###\s+4\.2\.\d+\.\s+", text, flags=re.MULTILINE)[1:]:
        name = re.match(r"(\w+)", section)
        if not name:
            continue
        t = re.search(
            r"-\s+\*\*Transpilation:\*\*\s+(.+?)(?=\n-\s|\n\n###|\n\n>|\Z)",
            section,
            re.DOTALL,
        )
        if t:
            rules[name.group(1).lower()] = re.sub(r"\s+", " ", t.group(1)).strip()
    return rules


_RULES: dict[str, str] = _parse_rules(_read())


def build_prompt(node_type: str, lang: str, source: str) -> str:
    lang_name = langcodes.get(lang).display_name()
    rules = _RULES[node_type]

    peer_warning = (
        "\n- Prepend a [!WARNING] callout stating that lossless parity cannot be "
        "guaranteed in non-English output at Peer density."
        if node_type == "peer" and lang != "en"
        else ""
    )

    return f"""\
You are a transpiler for Machine Lingua Franca 1.0 (MLF-1.0).

Transpile the specification below for a **{node_type}** node in **{lang_name}**.

Transpilation rules for `{node_type}` (from machine.md §4.2):
{rules}

Universal rules (normative):
- Output entirely in {lang_name}. All prose MUST be translated.
- Technical keywords (MUST, MAY, ASSERT, IRQ, SYN, DAMP, etc.) MUST NOT be translated.
- Structural syntax and keywords inside code blocks MUST NOT be translated.
- Mermaid diagram strings MUST be translated; node IDs and arrows MUST NOT.
- Crude language MUST NOT be softened for subject, student, or peer outputs.{peer_warning}

Output a complete Markdown document. No preamble or commentary outside the document.

---

{source}"""
