from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class IsWritableValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = IsWritableValidator._normalize_path(path)
        if not os.access(path, os.W_OK):
            IsWritableValidator._raise_error(path=path, suffix="is not writable!")

        return path
