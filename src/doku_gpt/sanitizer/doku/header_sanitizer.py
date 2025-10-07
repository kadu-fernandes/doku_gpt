from pathlib import Path, PurePosixPath

from doku_gpt.abstact_root_folder import FolderValidator
from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.extractor.doku_page_extractor import FileValidator


class HeaderSanitizer:
    def sanitize(self, root_folder: str | Path, page: str | Path) -> str:
        root_folder = FolderValidator.validate(root_folder)
        page = FileValidator.validate(page)

        relative_path = page.relative_to(root_folder).with_suffix("")
        parts = PurePosixPath(relative_path.as_posix()).parts
        context = " › ".join(parts[:-1])

        adapter = PageAdapter(page)
        first_line = adapter.lines[0].strip()

        if not first_line.startswith("="):
            raise ValueError(f"First line of '{page}' must start with '='")

        header_content = first_line.strip("= ").strip()
        if context:
            new_header = f"====== {context} › {header_content} ======"
        else:
            new_header = f"====== {header_content} ======"

        return new_header
