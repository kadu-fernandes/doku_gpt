from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathExistsValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = PathExistsValidator._normalize_path(path)

        if not path.exists():
            PathExistsValidator._raise_error(path=path, suffix="does not exist!")

        return path
