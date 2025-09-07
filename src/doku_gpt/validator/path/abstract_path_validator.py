from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError


class AbstractPathValidator(ABC):

    @staticmethod
    @abstractmethod
    def validate(path: str | Path) -> Path:
        pass

    @staticmethod
    def _normalize_path(path: str | Path) -> Path:
        return Path(str(path).strip()).resolve(strict=False)

    @staticmethod
    def _raise_error(path: Path, suffix: str) -> None:
        raise InvalidPathError(f"The given path '{path}' {suffix.strip()}")
