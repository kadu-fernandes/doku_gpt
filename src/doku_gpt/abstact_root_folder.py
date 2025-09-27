from abc import ABC
from pathlib import Path

from doku_gpt.validator.path.folder_validator import FolderValidator


class AbstractRootFolder(ABC):
    def __init__(
        self,
        root_folder: str | Path,
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ):
        self.root_folder = root_folder
        self.excluded_folders = excluded_folders
        self.excluded_files = excluded_files

    @property
    def root_folder(self) -> Path:
        return self.__root_folder

    @root_folder.setter
    def root_folder(self, root_folder: str | Path):
        self.__root_folder = FolderValidator.validate(root_folder)

    @property
    def settings_file(self) -> Path:
        return self.__root_folder.joinpath(".doku_gpt.json")

    @property
    def excluded_folders(self) -> list[str]:
        return self.__excluded_folders

    @excluded_folders.setter
    def excluded_folders(self, excluded_folders: list[str] | None) -> None:
        default: list[str] = ["playground", "wiki"]
        if excluded_folders:
            default.extend(excluded_folders)
        self.__excluded_folders = sorted(default)

    @property
    def excluded_files(self) -> list[str]:
        return self.__excluded_files

    @excluded_files.setter
    def excluded_files(self, excluded_files: list[str] | None) -> None:
        default: list[str] = ["sidebar"]
        if excluded_files:
            default.extend(excluded_files)
        self.__excluded_files = sorted(default)

    def _is_excluded_folder(self, path: Path) -> bool:
        if not path.is_dir():
            return False

        for part in path.relative_to(self.root_folder).parts:
            if part in self.excluded_folders:
                return True
        return False

    def _is_excluded_file(self, path: Path) -> bool:
        if not path.is_file():
            return False

        return path.with_suffix("").name in self.excluded_files
