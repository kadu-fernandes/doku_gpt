from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError


class IsChildValidator:

    @staticmethod
    def validate(parent: str | Path, child: str | Path) -> Path:
        parent = Path(str(parent).strip()).resolve(strict=False)
        child = Path(str(child).strip()).resolve(strict=False)

        try:
            child.relative_to(parent)
        except ValueError:
            raise InvalidPathError(
                f"The path '{str(child)}' is not a child of '{str(parent)}'!"
            )

        return child
