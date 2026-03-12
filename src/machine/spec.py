import re
from enum import Enum

from . import util


def _load_language_codes() -> list:
    codes = []
    for line in util.package_lines("languages.md"):
        if m := re.match(r"^\|\s+`(\w+)`\s+\|", line):
            codes.append(m.group(1))
    return sorted(codes)


LANGUAGE_CODES = _load_language_codes()


def _load_node_type_names() -> tuple[str, ...]:
    matches = (
        (int(m.group(1)), m.group(2).lower())
        for line in util.package_lines("machine.md")
        if (m := re.match(r"^###\s+4\.2\.(\d+)\.\s+([A-Za-z]+)", line))
    )
    return tuple(name for _, name in sorted(matches))


NodeType = Enum(
    "NodeType",
    {name: name for name in _load_node_type_names()},
    type=str,
)
