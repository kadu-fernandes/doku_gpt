from __future__ import annotations

from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathExistsValidator(AbstractPathValidator):
    @classmethod
    def validate(cls, path: str | Path) -> Path:
        to_validade = Path(str(path).strip())
        try:
            to_validade = to_validade.resolve(strict=True)  # exige que o path exista
        except FileNotFoundError:
            cls._raise_error(path=to_validade, suffix="does not exist!")
        return to_validade
