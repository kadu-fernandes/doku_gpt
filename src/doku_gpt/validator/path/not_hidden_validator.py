from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class NotHiddenValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = NotHiddenValidator._normalize_path(path)

        for segment in path.parts:
            if segment.startswith(".") and segment not in (".", ".."):
                NotHiddenValidator._raise_error(path=path, suffix="is hidden!")

        return path
