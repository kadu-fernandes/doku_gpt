from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from slugify import slugify

from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.enum.valid_file import ValidFile
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.path_extension_validator import PathExtensionValidator


class DokuPageExtractor:
    __REGEX_TITLE = re.compile(
        r"^\s*={6}\s*(?P<title>.+?)\s*={6}\s*$",
        re.MULTILINE,
    )

    __REGEX_HEADERS = re.compile(
        r"^\s*(?P<eq>={1,6})\s+(?P<title>.+?)\s+(?P=eq)\s*$",
        re.MULTILINE,
    )

    @classmethod
    def can_fetch(cls, page_path: str | Path) -> bool:
        try:
            PathExtensionValidator.validate(path=page_path, extension=ValidFile.DOKU_WIKI)
            return True
        except InvalidPathError:
            return False

    @classmethod
    def file_exists(cls, page_path: str | Path) -> bool:
        try:
            FileValidator.validate(page_path)
            return True
        except InvalidPathError:
            return False

    @classmethod
    def extract_title(cls, page_path: str | Path, fragment: str | None = None) -> str | None:
        """
        If fragment is empty, return the first header in the file.
        If fragment is not empty, extract all headers to a list.
        For each extracted header, replace '-' and '_' for a space, and replace 2 or more consecutive spaces with only one.
        Using python-slugify, create 4 slugs in lowercase for each header:
            - romanized with '-'
            - romanized with '_'
            - deaccent-only with '-'
            - deaccent-only with '_'
        Compare these 4 slugs with the fragment (after trimming a leading '#', if present).
        If a slug is exactly the same as the fragment OR contains the fragment substring, return the respective header.
        If not, return None.
        """
        if not cls.can_fetch(page_path) or not cls.file_exists(page_path):
            return None

        page_adapter = PageAdapter(page_path)
        page_content = str(getattr(page_adapter, "content", "")) or ""

        if fragment is None or str(fragment).strip() == "":
            return cls.__handle_title_no_fragment(page_content)

        _, matched_title = cls.__handle_title_fragment(page_content, str(fragment))
        return matched_title

    @classmethod
    def extract_excerpt(cls, page_path: str | Path, fragment: str | None = None) -> str | None:
        """
        Extract the excerpt (body text) for the matched header, without spilling into the next header.
        - If fragment is None or empty: anchor on the first level-6 header (====== ... ======).
        - If fragment is provided: anchor on the header matched via the fragment logic (subsequence-in-order).
        The excerpt is built from the first paragraph; if it is too short, additional paragraphs are appended
        until a minimum size is reached, never crossing into the next header. If the first paragraph is too long,
        it is trimmed to the first 1–2 sentences that fit within the maximum target size.
        """
        if not cls.can_fetch(page_path) or not cls.file_exists(page_path):
            return None

        page_adapter = PageAdapter(page_path)
        content = str(getattr(page_adapter, "content", "")) or ""

        # Normalize line endings in-memory for consistent line math.
        content = content.replace("\r\n", "\n").replace("\r", "\n")

        header_match = None
        if fragment is None or str(fragment).strip() == "":
            found = cls.__REGEX_TITLE.search(content)
            if not found:
                return None
            header_match = found
        else:
            line_number, matched_title = cls.__handle_title_fragment(content, str(fragment))
            if line_number == -1 or matched_title is None:
                return None
            # Locate the concrete match object for the identified header line.
            for match in cls.__REGEX_HEADERS.finditer(content):
                title_text = match.group("title").strip()
                current_line = 1 + content.count("\n", 0, match.start())
                if current_line == line_number and title_text == matched_title:
                    header_match = match
                    break
            if header_match is None:
                return None

        # Delimit body: from end of this header to start of next header (or EOF).
        body_start_index = header_match.end()
        next_header_start = None
        for match in cls.__REGEX_HEADERS.finditer(content, pos=header_match.end()):
            next_header_start = match.start()
            break
        body_end_index = next_header_start if next_header_start is not None else len(content)
        body_slice = content[body_start_index:body_end_index]

        # Build paragraphs: blocks of non-empty lines separated by blank lines.
        lines = body_slice.split("\n")
        paragraphs: list[str] = []
        current_block: list[str] = []

        # Skip leading blank lines.
        index = 0
        while index < len(lines) and lines[index].strip() == "":
            index += 1

        while index < len(lines):
            line_text = lines[index]
            if line_text.strip() == "":
                if current_block:
                    joined = " ".join(part.strip() for part in current_block if part.strip())
                    joined = re.sub(r"\s{2,}", " ", joined).strip()
                    if joined:
                        paragraphs.append(joined)
                    current_block = []
                # Consume any additional blank lines between paragraphs.
                while index < len(lines) and lines[index].strip() == "":
                    index += 1
                continue
            current_block.append(line_text)
            index += 1

        if current_block:
            joined = " ".join(part.strip() for part in current_block if part.strip())
            joined = re.sub(r"\s{2,}", " ", joined).strip()
            if joined:
                paragraphs.append(joined)

        if not paragraphs:
            return ""

        # Goldilocks window.
        minimum_chars = 140
        minimum_words = 20
        maximum_chars = 450
        maximum_words = 80

        # Start with the first paragraph.
        excerpt_text = paragraphs[0]

        # If too long, trim by sentences (1–2 sentences that fit).
        if len(excerpt_text) > maximum_chars or len(excerpt_text.split()) > maximum_words:
            sentence_pattern = re.compile(r"(?<=[\.?!…])\s+")
            sentences = sentence_pattern.split(excerpt_text)
            assembled = ""
            for sentence in sentences:
                tentative = (assembled + " " + sentence).strip() if assembled else sentence.strip()
                if len(tentative) <= maximum_chars and len(tentative.split()) <= maximum_words:
                    assembled = tentative
                else:
                    if not assembled:
                        # If even the first sentence exceeds max, hard cut at max boundary by words.
                        words = sentence.strip().split()
                        safe_words: list[str] = []
                        for word in words:
                            candidate = (" ".join(safe_words + [word])).strip()
                            if len(candidate) <= maximum_chars and len(candidate.split()) <= maximum_words:
                                safe_words.append(word)
                            else:
                                break
                        assembled = " ".join(safe_words).strip()
                    break
            excerpt_text = assembled.strip()

        # If too short, append subsequent paragraphs until reaching the minimum (without crossing next header).
        para_index = 1
        while (len(excerpt_text) < minimum_chars or len(excerpt_text.split()) < minimum_words) and para_index < len(
            paragraphs
        ):
            tentative = (excerpt_text + " " + paragraphs[para_index]).strip()
            if len(tentative) <= maximum_chars and len(tentative.split()) <= maximum_words:
                excerpt_text = tentative
                para_index += 1
            else:
                break

        return excerpt_text.strip()

    @classmethod
    def __handle_title_no_fragment(cls, content: str) -> str | None:
        found = cls.__REGEX_TITLE.search(content)
        if not found:
            return None
        return found.group("title").strip()

    @classmethod
    def __handle_title_fragment(cls, content: str, fragment: str) -> tuple[int, str | None]:
        fragment_clean = str(fragment).strip()
        if fragment_clean.startswith("#"):
            fragment_clean = fragment_clean[1:]
        fragment_clean = fragment_clean.strip().casefold()

        if "_" in fragment_clean:
            fragment_separator = "_"
        elif "-" in fragment_clean:
            fragment_separator = "-"
        else:
            fragment_separator = "-"

        fragment_tokens_raw = [segment for segment in fragment_clean.split(fragment_separator) if segment]
        fragment_tokens_norm = [cls.__normalize_number_token(token) for token in fragment_tokens_raw]

        fragment_romanized = cls.__slug_to_tokens(" ".join(fragment_tokens_norm))
        fragment_deaccent = cls.__slug_to_tokens(cls.__deaccent_only(" ".join(fragment_tokens_norm)))

        best_line = -1
        best_title = None

        for match in cls.__REGEX_HEADERS.finditer(content):
            title_text = match.group("title").strip()
            line_index = 1 + content.count("\n", 0, match.start())

            title_tokens_source = cls.__neutralize_separators(title_text)
            title_tokens_romanized = cls.__slug_to_tokens(title_tokens_source)
            title_tokens_deaccent = cls.__slug_to_tokens(cls.__deaccent_only(title_tokens_source))

            if cls.__is_subsequence(fragment_romanized, title_tokens_romanized):
                best_line = line_index
                best_title = title_text
                break

            if cls.__is_subsequence(fragment_deaccent, title_tokens_deaccent):
                best_line = line_index
                best_title = title_text
                break

        return best_line, best_title

    @classmethod
    def __handle_headers(cls, page_content: str) -> str | None:
        matches = cls.__REGEX_HEADERS.findall(string=page_content)
        if not matches:
            return None
        return None

    @staticmethod
    def __neutralize_separators(value: str) -> str:
        replaced = value.replace("-", " ").replace("_", " ")
        collapsed = re.sub(r"\s{2,}", " ", replaced)
        return collapsed.strip().casefold()

    @staticmethod
    def __slug_to_tokens(value: str) -> list[str]:
        slug_as_spaces = slugify(value, separator=" ", lowercase=True)
        tokens = [token for token in slug_as_spaces.split(" ") if token]
        normalized_tokens = [DokuPageExtractor.__normalize_number_token(token) for token in tokens]
        return normalized_tokens

    @staticmethod
    def __normalize_number_token(token: str) -> str:
        if token.isdigit():
            try:
                number_value = int(token, 10)
                return str(number_value)
            except ValueError:
                return token
        return token

    @staticmethod
    def __deaccent_only(value: str) -> str:
        decomposed = unicodedata.normalize("NFKD", value)
        without_marks = "".join(character for character in decomposed if not unicodedata.combining(character))
        return without_marks

    @staticmethod
    def __is_subsequence(needles: list[str], haystack: list[str]) -> bool:
        if not needles:
            return False
        position = 0
        for needle in needles:
            found_index = -1
            for index in range(position, len(haystack)):
                if haystack[index] == needle:
                    found_index = index
                    break
            if found_index == -1:
                return False
            position = found_index + 1
        return True
