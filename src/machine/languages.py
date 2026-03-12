"""Language register — derived from ../../languages.md (rule 5)."""

import contextlib
import re
from importlib.resources import files
from pathlib import Path


def _read() -> str:

    # installed package resource (pip install / nix package).
    with contextlib.suppress(FileNotFoundError, TypeError):
        return files("machine").joinpath("languages.md").read_text(encoding="utf-8")

    # git root fallback (editable / dev).
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            candidate = parent / "languages.md"
            if candidate.exists():
                return candidate.read_text(encoding="utf-8")

    raise FileNotFoundError("languages.md not found as package resource or at git root")


def load_language_codes() -> frozenset[str]:
    codes: set[str] = set()
    for line in _read().splitlines():
        if m := re.match(r"^\|\s+`(\w+)`\s+\|", line):
            codes.add(m.group(1))
    return frozenset(codes)


LANGUAGE_CODES: frozenset[str] = load_language_codes()
