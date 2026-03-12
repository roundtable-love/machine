"""Prompt construction for MACHINE-1.0 transpilation."""

import langcodes

from . import util


def prompt(node_type: str, lang: str, text: str) -> str:
    lang_name = langcodes.get(lang).display_name()
    peer_warning = (
        "\n- Prepend a [!WARNING] callout stating that lossless parity cannot be "
        "guaranteed in non-English output at Peer density."
        if node_type == "peer" and lang != "en"
        else ""
    )

    return f"""
{util.package_text("machine.md")}

---

You are a transpiler for Machine 1.0 (MACHINE-1.0).

Transpile the below for a **{node_type}** node in **{lang_name}**.

Universal rules (normative):
- Output entirely in {lang_name}. All prose MUST be translated.
- Technical keywords (MUST, MAY, ASSERT, IRQ, SYN, DAMP, etc.) MUST NOT be translated.
- Structural syntax and keywords inside code blocks MUST NOT be translated.
- Mermaid diagram strings MUST be translated; node IDs and arrows MUST NOT.
- Crude language MUST NOT be softened for subject, student, or peer outputs.{peer_warning}

Output a complete Markdown document. No preamble or commentary outside the document.

---

{text}
"""
