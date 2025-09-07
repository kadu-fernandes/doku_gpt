from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class IsReadableValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = IsReadableValidator._normalize_path(path)
        if not os.access(path, os.R_OK):
            IsReadableValidator._raise_error(path=path, suffix="is not readable!")

        return path
