from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathIsWritableValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = cls._normalize_path(path)
        if not os.access(path, os.W_OK):
            cls._raise_error(path=path, suffix="is not writable!")

        return path
