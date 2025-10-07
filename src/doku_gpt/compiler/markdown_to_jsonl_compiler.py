from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Tuple

from doku_gpt.error.invalid_value_error import InvalidValueError


class MarkdownToJsonlCompiler:
    SOURCE_DIRECTORY = Path("/tmp/doku_gpt_prepare")
    OUTPUT_FILE = SOURCE_DIRECTORY.joinpath("gpt_dataset.jsonl")

    FRONTMATTER_BORDER = re.compile(r"^\s*---\s*$")
    HEADER_H1 = re.compile(r"^\s{0,3}\#\s{1}(.+?)\s*$")
    ANY_HEADER = re.compile(r"^\s{0,3}\#{1,6}\s+")
    FILENAME_ID = re.compile(r"^(?P<base>(?:gpt(?:_\d{2})+))(?:_(?P<slug>[^.]+))?\.md$")

    def compile(self) -> Path:
        if not self.SOURCE_DIRECTORY.is_dir():
            raise InvalidValueError(f"Invalid source directory: {self.SOURCE_DIRECTORY}")

        markdown_files = sorted(self.SOURCE_DIRECTORY.glob("gpt_*.md"))
        if 1 > len(markdown_files):
            raise InvalidValueError("No Markdown files found to compile.")

        if self.OUTPUT_FILE.exists():
            self.OUTPUT_FILE.unlink(missing_ok=True)

        with self.OUTPUT_FILE.open("w", encoding="utf-8") as output_stream:
            for markdown_file in markdown_files:
                try:
                    json_line = self.__convert_file_to_jsonl_line(markdown_file)
                except InvalidValueError:
                    continue
                output_stream.write(json_line + "\n")

        return self.OUTPUT_FILE

    def __convert_file_to_jsonl_line(self, file_path: Path) -> str:
        text = file_path.read_text(encoding="utf-8")
        frontmatter_text, body_text = self.__read_frontmatter_and_body(text)

        metadata = self.__parse_flat_yaml(frontmatter_text)
        world = metadata.get("world", "").strip()
        language = metadata.get("language", "").strip() or "pt-PT"
        title_from_yaml = metadata.get("title", "").strip()
        if 1 > len(world) or 1 > len(title_from_yaml):
            raise InvalidValueError(f"Missing required YAML keys in {file_path.name}")

        h1_title, first_section = self.__extract_h1_and_first_section(body_text)
        assistant_text = first_section.strip()
        if 1 > len(assistant_text):
            raise InvalidValueError(f"Empty main section in {file_path.name}")

        system_prompt = (
            f"You are a helpful assistant specialized in the fictional world '{world}'. "
            f"Answer in {language}. Base your answers strictly on the provided documents."
        )

        user_prompt = f"Describe: {title_from_yaml}"

        json_object = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": assistant_text},
            ]
        }

        return json.dumps(json_object, ensure_ascii=False)

    def __read_frontmatter_and_body(self, text: str) -> Tuple[str, str]:
        lines = text.splitlines()
        if 1 > len(lines) or not self.FRONTMATTER_BORDER.match(lines[0]):
            raise InvalidValueError("Missing YAML frontmatter start '---' on first line.")
        end_index = None
        for index in range(1, len(lines)):
            if self.FRONTMATTER_BORDER.match(lines[index]):
                end_index = index
                break
        if end_index is None:
            raise InvalidValueError("Missing YAML frontmatter closing '---'.")
        frontmatter_text = "\n".join(lines[1:end_index]).strip()
        body_text = "\n".join(lines[end_index + 1 :]).lstrip("\n")
        return frontmatter_text, body_text

    def __parse_flat_yaml(self, frontmatter_text: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for raw in frontmatter_text.splitlines():
            line = raw.strip()
            if 1 > len(line) or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key_normalized = key.strip()
            value_normalized = value.strip().strip('"').strip("'")
            if key_normalized in parsed:
                continue
            parsed[key_normalized] = value_normalized
        return parsed

    def __extract_h1_and_first_section(self, body_text: str) -> Tuple[str, str]:
        lines = body_text.splitlines()
        total = len(lines)
        index = 0

        h1_title: str | None = None
        while index < total:
            line = lines[index]
            if line.strip():
                match_h1 = self.HEADER_H1.match(line)
                if not match_h1:
                    raise InvalidValueError("First non-empty line after YAML must be an H1 '# Title'.")
                h1_title = match_h1.group(1).strip()
                index += 1
                break
            index += 1

        if h1_title is None:
            raise InvalidValueError("H1 title not found.")

        while index < total and not lines[index].strip():
            index += 1

        section_lines: list[str] = []
        while index < total:
            current_line = lines[index]
            if self.ANY_HEADER.match(current_line):
                break
            section_lines.append(current_line)
            index += 1

        section_text = "\n".join(section_lines).strip()
        return h1_title, section_text
