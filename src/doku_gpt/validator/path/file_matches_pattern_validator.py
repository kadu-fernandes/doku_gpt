from __future__ import annotations

import fnmatch
from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_file_validator import PathIsFileValidator


class FileMatchesPatternValidator:
    @classmethod
    def validate(cls, file: str | Path, pattern: str) -> Path:
        file_path = PathIsFileValidator.validate(file)
        normalized_pattern = pattern.strip()

        if not fnmatch.fnmatchcase(file_path.name, normalized_pattern):
            raise InvalidPathError(f"The given file '{file_path}' does not match the pattern('{normalized_pattern}')!")

        return file_path
