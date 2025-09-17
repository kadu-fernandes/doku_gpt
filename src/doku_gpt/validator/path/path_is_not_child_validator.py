from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError


class PathIsNotChildValidator:
    @classmethod
    def validate(cls, parent: str | Path, other: str | Path) -> Path:
        parent = Path(str(parent).strip()).resolve(strict=False)
        other = Path(str(other).strip()).resolve(strict=False)

        try:
            other.relative_to(parent)

            raise InvalidPathError(f"The path '{str(other)}' must not be a child of '{str(parent)}'!")
        except ValueError:
            return other
