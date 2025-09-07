from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class IsFolderValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = IsFolderValidator._normalize_path(path)
        if not path.is_dir():
            IsFolderValidator._raise_error(path=path, suffix="is not a directory!")

        return path
