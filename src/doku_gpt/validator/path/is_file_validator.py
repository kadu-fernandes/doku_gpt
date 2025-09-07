from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class IsFileValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = IsFileValidator._normalize_path(path)
        if not path.is_file():
            IsFileValidator._raise_error(path=path, suffix="is not a file!")

        return path
