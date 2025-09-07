from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError


class ExtensionValidator:

    EXT_DOKU_WIKI = "txt"
    EXT_MARKDOWN = "md"
    EXT_JSON = "json"

    @staticmethod
    def validate(path: str | Path, extension: str) -> Path:
        path = Path(str(path).strip()).resolve(strict=False)

        extension = "." + extension.strip().lstrip(".")

        if extension.strip().lower() != path.suffix.lower():
            raise InvalidPathError(f"The extension '{extension}' of the given file '{path}' is not valid!")

        return path
