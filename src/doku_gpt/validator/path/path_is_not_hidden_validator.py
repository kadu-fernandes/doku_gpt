from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathIsNotHiddenValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = cls._normalize_path(path)

        for segment in path.parts:
            if segment.startswith(".") and segment not in (".", ".."):
                cls._raise_error(path=path, suffix="is hidden!")

        return path
