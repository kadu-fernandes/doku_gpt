from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator


class ReadWriteHelper:

    @staticmethod
    def read_text(file_path: Path | str) -> str:
        file_path = FileValidator.validate(file_path)

        return file_path.read_text(encoding="utf-8")

    @staticmethod
    def read_text_lines(file_path: Path | str) -> list[str]:
        return ReadWriteHelper.read_text(file_path).splitlines()

    @staticmethod
    def write_text(file_path: Path | str, content: str) -> None:
        FolderValidator.validate(file_path.parent)
        file_path.write_text(data=content, encoding="utf-8")

    @staticmethod
    def write_text_lines(file_path: Path | str, lines: list[str]) -> None:
        FolderValidator.validate(file_path.parent)
        ReadWriteHelper.write_text(file_path=file_path, content="\n".join(lines))

    @staticmethod
    def read_json(file_path: Path | str) -> Any:
        json_text: str = ReadWriteHelper.read_text(file_path)

        return json.loads(json_text)

    @staticmethod
    def write_json(file_path: Path | str, content: Any) -> None:
        json_text: str = json.dumps(obj=content, ensure_ascii=False, indent=4, sort_keys=True)
        ReadWriteHelper.write_text(file_path=file_path, content=json_text)
