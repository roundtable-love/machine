import contextlib
from importlib.resources import files
from functools import lru_cache
from pathlib import Path


@lru_cache
def package_path(path: str | Path) -> Path:
    # installed package resource
    with contextlib.suppress(FileNotFoundError, TypeError):
        return Path(str(files("machine").joinpath(path)))
    # git root fallback (editable / dev)
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            candidate = parent / path
            if candidate.exists():
                return candidate
    raise FileNotFoundError("machine.md not found as package resource or at git root")


@lru_cache
def package_text(path: str | Path) -> str:
    return package_path(path).read_text(encoding="utf-8")


@lru_cache
def package_lines(path: str | Path) -> list[str]:
    return package_text(path).splitlines()
