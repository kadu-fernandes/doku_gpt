from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathIsFolderValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        try:
            path = cls._normalize_path(path=path)
        except FileNotFoundError:
            cls._raise_error(path=path, suffix="does not exist!")
        if not path.is_dir():
            cls._raise_error(path=path, suffix="is not a directory!")

        return path
