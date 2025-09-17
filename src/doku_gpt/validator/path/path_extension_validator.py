from __future__ import annotations

from pathlib import Path

from doku_gpt.enum.valid_file_enum import ValidFileEnum
from doku_gpt.error.invalid_path_error import InvalidPathError


class PathExtensionValidator:
    @classmethod
    def validate(cls, path: str | Path, extension: str | ValidFileEnum | None = None) -> Path:
        file_path = Path(str(path).strip()).resolve(strict=False)
        suffix = file_path.suffix.lstrip(".").lower()

        if extension is not None:
            expected = (
                extension.value if isinstance(extension, ValidFileEnum) else ValidFileEnum.validate(str(extension))
            )
            if suffix != expected:
                raise InvalidPathError(f"The extension '.{expected}' of the given file '{file_path}' is not valid!")
            return file_path

        # Sem parâmetro `extension`: apenas verifica se o ficheiro tem uma extensão reconhecida
        try:
            ValidFileEnum.validate(suffix)
        except ValueError:
            raise InvalidPathError(f"The given file '{file_path}' does not have a valid extension!")

        return file_path
