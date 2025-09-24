from __future__ import annotations

from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.path_extension_validator import PathExtensionValidator


class AbstractRootSanitizer(AbstractRootFolder):
    def __init__(self, root_folder: str | Path, page_path: str | Path):
        super().__init__(root_folder=root_folder)
        page_path = FileValidator.validate(page_path)
        self.page_path = PathExtensionValidator.validate(page_path)
