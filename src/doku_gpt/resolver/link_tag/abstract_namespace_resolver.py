from __future__ import annotations

from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.extractor.doku_page_extractor import DokuPageExtractor
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.sanitizer.doku.line.inline_markup_sanitizer import InlineMarkupSanitizer
from doku_gpt.sanitizer.doku.line.line_break_sanitizer import LinebreakSanitizer
from doku_gpt.sanitizer.doku.line.link_label_sanitizer import LinkLabelSanitizer
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator


class AbstractNamespaceResolver(AbstractRootFolder):
    def __init__(
        self,
        root_folder: str | Path,
        context: str | Path | None = None,
    ):
        super().__init__(root_folder=root_folder)
        self.context = context

    @property
    def context(self) -> Path | None:
        return self.__context

    @context.setter
    def context(self, context: str | Path | None) -> None:
        if context is None:
            self.__context = context
            return

        try:
            self.__context = FolderValidator.validate(context)
        except InvalidPathError as exception:
            try:
                self.__context = FileValidator.validate(context).parent
            except InvalidPathError:
                raise exception

    def _strip_relative_marker(self, raw: str) -> str:
        text = (raw or "").strip()
        if text.startswith(("~:", ".:")):
            return text[2:]
        if text.startswith(("~", ".")):
            return text[1:] if len(text) > 1 and text[1] != ":" else text[2:]
        raise InvalidNamespaceError(f"Not a relative namespace: '{raw}'")

    def _parse_prior_prefix(self, raw: str) -> tuple[int, str]:
        text = (raw or "").strip()
        levels_up = 0
        while True:
            if text.startswith("..:"):
                levels_up += 1
                text = text[3:]
                continue
            if text.startswith(".."):
                levels_up += 1
                text = text[2:]
                if text.startswith(":"):
                    text = text[1:]
                continue
            break
        if 1 > levels_up:
            raise InvalidNamespaceError(f"Not a prior namespace: '{raw}'")
        return levels_up, text

    def _resolve_page_path_from_context(
        self,
        base_folder: Path,
        remainder: str,
        root_folder: Path,
    ) -> Path:
        parts = [segment for segment in (remainder or "").split(":") if segment]
        if not parts:
            raise InvalidNamespaceError("Empty namespace remainder.")
        page_path = base_folder.joinpath(*parts).with_suffix(".txt")
        try:
            page_path.relative_to(root_folder)
        except ValueError:
            raise InvalidNamespaceError(f"Resolved path escapes root: '{page_path}'")
        return page_path

    def _absolute_page_path(self, target: str) -> Path:
        parts = [segment for segment in target.split(":") if segment]
        if not parts:
            raise InvalidNamespaceError("Empty absolute namespace.")
        page_path = Path(self.root_folder).joinpath(*parts).with_suffix(".txt")
        try:
            page_path.relative_to(self.root_folder)
        except ValueError:
            raise InvalidNamespaceError(f"Resolved path escapes root: '{page_path}'")
        return page_path

    def _validate_or_raise(self, path: Path) -> None:
        FileValidator.validate(path)

    def _absolute_namespace_from_path(self, page_path: str | Path) -> str:
        candidate_path = Path(page_path)

        try:
            relative_path = candidate_path.relative_to(self.root_folder)
        except ValueError:
            raise InvalidNamespaceError(f"Path is outside of root: '{candidate_path}'")

        if relative_path.suffix:
            if relative_path.suffix != ".txt":
                raise InvalidNamespaceError(f"Unsupported page suffix '{relative_path.suffix}'")
            relative_path = relative_path.with_suffix("")

        parts = [segment for segment in relative_path.parts if segment]
        if not parts:
            raise InvalidNamespaceError("Cannot derive namespace from the root folder itself.")

        return ":" + ":".join(parts)

    def _add_label(self, link_tag: LinkTag, page_path: Path) -> tuple[bool, LinkTag]:
        if link_tag.label is not None:
            return False, link_tag

        link_tag.label = DokuPageExtractor.extract_title(
            page_path=page_path,
            fragment=link_tag.target_fragment,
        )
        return True, link_tag

    def _add_excerpt(self, link_tag: LinkTag, page_path: Path) -> tuple[bool, LinkTag]:
        if link_tag.excerpt is not None:
            return False, link_tag

        excerpt = DokuPageExtractor.extract_excerpt(
            page_path=page_path,
            fragment=link_tag.target_fragment,
        )
        if excerpt is not None:
            excerpt = InlineMarkupSanitizer.sanitize(excerpt)
            excerpt = LinkLabelSanitizer.sanitize(excerpt)
            excerpt = LinebreakSanitizer.sanitize(excerpt)
        link_tag.excerpt = excerpt
        return True, link_tag
