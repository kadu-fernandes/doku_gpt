from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_file_validator import PathIsFileValidator


class PathIsExcludedFileValidator:
    @classmethod
    def validate(cls, file: str | Path, excluded_files: list[str]) -> Path:
        file = PathIsFileValidator.validate(file)

        if file.with_suffix("").name in excluded_files:
            raise InvalidPathError(f"The given file '{file}' is excluded!")

        return file
