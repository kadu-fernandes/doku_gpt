from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator
from doku_gpt.validator.path.path_exists_validator import PathExistsValidator
from doku_gpt.validator.path.path_is_file_validator import PathIsFileValidator
from doku_gpt.validator.path.path_is_not_hidden_validator import PathIsNotHiddenValidator
from doku_gpt.validator.path.path_is_not_system_path_validator import PathIsNotSystemPathValidator
from doku_gpt.validator.path.path_is_readable_validator import PathIsIsReadableValidator
from doku_gpt.validator.path.path_is_writable_validator import PathIsWritableValidator


class FileValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = PathExistsValidator.validate(path)
        path = PathIsFileValidator.validate(path)
        path = PathIsNotSystemPathValidator.validate(path)
        path = PathIsIsReadableValidator.validate(path)
        path = PathIsWritableValidator.validate(path)
        path = PathIsNotHiddenValidator.validate(path)

        return path
