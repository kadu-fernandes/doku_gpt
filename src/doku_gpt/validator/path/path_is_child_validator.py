from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError


class PathIsChildValidator:
    @classmethod
    def validate(cls, parent: str | Path, child: str | Path) -> Path:
        parent_path = Path(str(parent).strip())
        child_path = Path(str(child).strip())

        try:
            parent_resolved = parent_path.resolve(strict=True)
        except FileNotFoundError:
            raise InvalidPathError(f"The path '{parent_path}' is not a valid parent since it does not exist!")

        relation_check_path: Path
        try:
            child_resolved = child_path.resolve(strict=True)
            relation_check_path = child_resolved
        except FileNotFoundError:
            try:
                relation_check_path = child_path.parent.resolve(strict=True)
            except FileNotFoundError:
                raise InvalidPathError(f"The path '{child_path}' is not a valid child since it does not exist!")

        try:
            relation_check_path.relative_to(parent_resolved)
        except ValueError:
            raise InvalidPathError(f"The path '{child_path}' is not a child of '{parent_path}'!")

        return child_path.resolve(strict=False)
