from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator
from doku_gpt.validator.path.path_is_file_validator import PathIsFileValidator
from doku_gpt.validator.path.path_is_folder_validator import PathIsFolderValidator


class PathIsValidForNamespaceValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        try:
            return PathIsFolderValidator.validate(path)
        except InvalidPathError:
            try:
                return PathIsFileValidator.validate(Path(path).with_suffix(".txt"))
            except InvalidPathError:
                cls._raise_error(path=Path(path), suffix="is not valid for a namespace!")
