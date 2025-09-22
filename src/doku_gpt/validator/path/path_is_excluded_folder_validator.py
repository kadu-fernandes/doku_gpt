from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_child_validator import PathIsChildValidator
from doku_gpt.validator.path.path_is_folder_validator import PathIsFolderValidator


class PathIsExcludedFolderValidator:
    @classmethod
    def validate(cls, folder: str | Path, excluded_folders: list[str], root_folder: str | Path | None = None) -> Path:
        folder = PathIsFolderValidator.validate(folder)
        to_validate = folder.resolve()

        if root_folder is not None:
            root_folder = PathIsFolderValidator.validate(root_folder)
            to_validate = PathIsChildValidator.validate(parent=root_folder, child=to_validate)
            to_validate = to_validate.relative_to(root_folder)

        segments = list(to_validate.parts)
        for segment in segments:
            if segment in excluded_folders:
                raise InvalidPathError(f"The given folder '{to_validate}' is excluded!")

        return folder
