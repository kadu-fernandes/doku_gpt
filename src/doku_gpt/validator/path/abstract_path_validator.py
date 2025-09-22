from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import NoReturn

from doku_gpt.error.invalid_path_error import InvalidPathError


class AbstractPathValidator(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, path: str | Path) -> Path:
        pass

    @classmethod
    def _normalize_path(cls, path: str | Path) -> Path:
        original_path = Path(str(path).strip())

        try:
            return original_path.resolve(strict=True)
        except FileNotFoundError:
            parent_path = original_path.parent
            try:
                parent_path.resolve(strict=True)
            except FileNotFoundError:
                cls._raise_error(path=original_path, suffix="does not exist!")

        return original_path.resolve(strict=False)

    @classmethod
    def _raise_error(cls, path: str | Path, suffix: str) -> NoReturn:
        raise InvalidPathError(f"The given path '{str(path)}' {suffix.strip()}")
