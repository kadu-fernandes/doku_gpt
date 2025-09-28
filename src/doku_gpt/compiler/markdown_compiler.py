from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.error.invalid_value_error import InvalidValueError


class MarkdownCompiler:
    COMPILE_DESTINATION = Path("/tmp/doku_gpt_prepare")
    HEADER = re.compile(r"^\#\s{1}(.*)$")

    def compile(self) -> None:
        self.__convert_to_markdown()
        self.__add_header()

    def __convert_to_markdown(self) -> None:
        pandoc = self.__pandoc()
        for txt_file in self.COMPILE_DESTINATION.glob("gpt_00*.txt"):
            md_file = txt_file.with_suffix(".md")
            subprocess.run(
                [str(pandoc), "-f", "dokuwiki", "-t", "markdown", str(txt_file), "-o", str(md_file)],
                check=True,
            )
            txt_file.unlink(missing_ok=True)

    def __add_header(self) -> None:
        md_files = list(self.COMPILE_DESTINATION.glob("gpt_00*.md"))
        if 1 > len(md_files):
            return

        filename_regex = re.compile(r"^(?P<base>(?:gpt(?:_\d{2})+))(?:_(?P<slug>[^.]+))?\.md$")

        id_to_file: dict[str, Path] = {}
        id_to_slug: dict[str, str] = {}
        parent_to_children: dict[str, list[str]] = {}

        for markdown_file in md_files:
            filename = markdown_file.name
            match = filename_regex.match(filename)
            if not match:
                raise InvalidValueError(f"Invalid filename format: {filename}")

            file_id = match.group("base")
            file_slug = match.group("slug") or ""

            id_to_file[file_id] = markdown_file
            id_to_slug[file_id] = file_slug

        for file_id in id_to_file.keys():
            id_segments = file_id.split("_")
            if 2 >= len(id_segments):
                continue
            parent_id = "_".join(id_segments[:-1])
            parent_children = parent_to_children.get(parent_id, [])
            parent_children.append(file_id)
            parent_to_children[parent_id] = parent_children

        today_string = date.today().isoformat()

        for file_id, markdown_file in id_to_file.items():
            title_text = self.__fetch_header(markdown_file)

            id_segments = file_id.split("_")
            parent_id: str | None = None
            if 2 < len(id_segments):
                parent_id = "_".join(id_segments[:-1])

            ancestor_ids: list[str] = []
            if 2 < len(id_segments):
                for index in range(1, len(id_segments)):
                    candidate_id = "_".join(id_segments[: index + 1])
                    ancestor_ids.append(candidate_id)

            namespace_slugs: list[str] = []
            for ancestor_id in ancestor_ids:
                ancestor_slug = id_to_slug.get(ancestor_id, "")
                if 1 > len(ancestor_slug):
                    continue
                namespace_slugs.append(ancestor_slug)

            own_slug = id_to_slug.get(file_id, "")
            if 1 > len(own_slug):
                namespace_path = namespace_slugs
            else:
                if 1 > len(namespace_slugs):
                    namespace_path = [own_slug]
                else:
                    namespace_path = namespace_slugs

            children_ids = parent_to_children.get(file_id, [])

            header_lines: list[str] = []
            header_lines.append("---")
            header_lines.append('world: "Väinela"')
            header_lines.append(f'id: "{file_id}"')
            header_lines.append(f'title: "{title_text}"')
            if 1 > len(namespace_path):
                header_lines.append("namespace_path: []")
            else:
                namespace_joined = ", ".join([f'"{slug}"' for slug in namespace_path])
                header_lines.append(f"namespace_path: [{namespace_joined}]")
            header_lines.append('type: "worldbuilding"')
            header_lines.append("fictional: true")
            header_lines.append('language: "pt-PT"')
            header_lines.append('source: "compiled namespace"')
            header_lines.append(f'version: "{today_string}"')
            if parent_id is not None:
                header_lines.append(f'parent: "{parent_id}"')
            if 1 > len(children_ids):
                header_lines.append("children: []")
            else:
                children_joined = "\n  - ".join(['"{}"'.format(child_id) for child_id in sorted(children_ids)])
                header_lines.append("children:\n  - " + children_joined)
            header_lines.append("---")
            header_string = "\n".join(header_lines) + "\n\n"

            original_text = markdown_file.read_text(encoding="utf-8")
            if original_text.lstrip().startswith("---"):
                raise InvalidValueError(f"YAML frontmatter already present: {markdown_file.name}")

            new_text = header_string + original_text
            markdown_file.write_text(new_text, encoding="utf-8")

    def __fetch_header(self, file: Path) -> str:
        adapter = PageAdapter(file)
        for line in adapter.lines:
            match = self.HEADER.match(line)
            if match:
                return match.group(1).strip()
        raise InvalidValueError("The file does not have a header!")

    def __pandoc(self) -> Path:
        try:
            return Path("/usr/bin/pandoc").resolve(strict=True)
        except FileNotFoundError:
            raise InvalidPathError("Please ensure you have pandoc installed")
