from __future__ import annotations

import fnmatch
from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_folder_validator import PathIsFolderValidator


class FolderMatchesPatternValidator:
    @classmethod
    def validate(cls, folder: str | Path, pattern: str) -> Path:
        folder = PathIsFolderValidator.validate(folder)
        pattern_prepared = "*" + pattern.strip().lstrip("*").strip()
        if not fnmatch.fnmatchcase(str(folder), pattern_prepared):
            raise InvalidPathError(f"The given folder '{folder}' does not match the pattern('{pattern}')!")

        return folder
