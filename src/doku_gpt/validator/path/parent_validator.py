from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class ParentValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = Path(path).resolve(strict=False)

        try:
            return path.parent.resolve(strict=True)
        except FileNotFoundError:
            cls._raise_error(path=path, suffix="parent does not exist!")
