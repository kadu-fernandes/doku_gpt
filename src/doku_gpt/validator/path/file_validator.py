from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator
from doku_gpt.validator.path.is_file_validator import IsFileValidator
from doku_gpt.validator.path.is_readable_validator import IsReadableValidator
from doku_gpt.validator.path.is_writable_validator import IsWritableValidator
from doku_gpt.validator.path.not_hidden_validator import NotHiddenValidator
from doku_gpt.validator.path.not_system_path_validator import NotSystemPathValidator
from doku_gpt.validator.path.path_exists_validator import PathExistsValidator


class FileValidator(AbstractPathValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = PathExistsValidator.validate(path)
        path = IsFileValidator.validate(path)
        path = NotSystemPathValidator.validate(path)
        path = IsReadableValidator.validate(path)
        path = IsWritableValidator.validate(path)
        path = NotHiddenValidator.validate(path)

        return path
