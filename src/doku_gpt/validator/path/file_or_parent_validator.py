from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class FileOrParentValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = Path(path).resolve(strict=False)

        try:
            return path.resolve(strict=True)
        except FileNotFoundError:
            try:
                path.parent.resolve(strict=True)
                return path
            except FileNotFoundError:
                cls._raise_error(path=path, suffix="does not exist!")
