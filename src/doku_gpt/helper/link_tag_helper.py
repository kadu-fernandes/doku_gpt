from __future__ import annotations

import re
from typing import Collection

from doku_gpt.dto.link_tag import LinkTag
from doku_gpt.enums.link_status import LinkStatus
from doku_gpt.enums.link_type import LinkType
from doku_gpt.enums.square_brackets import SquareBrackets
from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError


class LinkTagHelper:

    __LINK_TAG_PATTERN = re.compile(r"\[\[(.+?)]]")
    __REGEX_IS_LINK_TAG = re.compile(r"^(?!\|)([^]|]+)(\|[^]]*)?$")

    SQUARE_BRACKETS_AS_IT_IS = 0
    SQUARE_BRACKETS_YES = 1
    SQUARE_BRACKETS_NO = 2

    @staticmethod
    def is_link_tag(link_tag: str) -> bool:
        """
        Return True if `value` is a valid DokuWiki-style link tag:
          - [[target]]
          - [[target|label]]   (label may be empty)
        Invalid when:
          - target is empty
          - target starts with '|'
        """

        return bool(
            LinkTagHelper.__REGEX_IS_LINK_TAG.match(link_tag.strip().lstrip("[").rstrip("]").strip("|").strip())
        )

    @staticmethod
    def validate_link_tag(
        link_tag: str, square_brackets: SquareBrackets = SquareBrackets.SQUARE_BRACKETS_AS_IT_IS
    ) -> str:
        has_square_brackets = link_tag.strip().startswith("[")

        stripped_link_tag = link_tag.strip().lstrip("[").rstrip("]").strip("|").strip()
        if not LinkTagHelper.is_link_tag(stripped_link_tag):
            raise InvalidNamespaceError(f"The given link tag '{stripped_link_tag}' is invalid!")

        match square_brackets:
            case SquareBrackets.SQUARE_BRACKETS_YES:
                return f"[[{stripped_link_tag}]]"
            case SquareBrackets.SQUARE_BRACKETS_NO:
                return stripped_link_tag
            case _:
                return f"[[{stripped_link_tag}]]" if has_square_brackets else stripped_link_tag

    @staticmethod
    def split_link_tag(link_tag: str) -> tuple[str, str | None]:
        validated_link_tag = LinkTagHelper.validate_link_tag(
            link_tag=link_tag, square_brackets=SquareBrackets.SQUARE_BRACKETS_NO
        )

        if "|" not in validated_link_tag:
            return validated_link_tag, None

        target, label = validated_link_tag.split("|", 1)

        return target.strip(), label.strip() or None

    @staticmethod
    def create_link_tag(link_tag: str) -> LinkTag:
        validated_link_tag = LinkTagHelper.validate_link_tag(
            link_tag=link_tag, square_brackets=SquareBrackets.SQUARE_BRACKETS_NO
        )
        target, label = LinkTagHelper.split_link_tag(link_tag=validated_link_tag)

        return LinkTag(
            link_type=LinkTagHelper.classify_link_tag(link_tag),
            status=LinkStatus.NOT_VALIDATED,
            target=target,
            label=label,
        )

    @staticmethod
    def extract_link_tags(line: str) -> list[str]:
        return [f"[[{link_tag}]]" for link_tag in LinkTagHelper.__LINK_TAG_PATTERN.findall(line)]

    @staticmethod
    def classify_link_tag(link_tag: str) -> LinkType:
        if LinkTagHelper.is_external:
            return LinkType.EXTERNAL

        return LinkType.INTERWIKI if LinkTagHelper.is_interwiki(link_tag) else LinkType.INTERNAL

    @staticmethod
    def is_internal(
        link_tag: str,
        known_interwiki_prefixes: Collection[str] | None = None,
        treat_bare_domains_as_external: bool = False,
    ) -> bool:
        if LinkTagHelper.is_external(link_tag, treat_bare_domains_as_external):
            return False

        if LinkTagHelper.is_interwiki(link_tag, known_prefixes=known_interwiki_prefixes):
            return False

        target, _ = LinkTagHelper.split_link_tag(link_tag)
        return "" != target.strip()

    @staticmethod
    def is_interwiki(link_tag: str, known_prefixes: Collection[str] | None = None) -> bool:
        """
        Interwiki if target matches '<prefix>><rest>', with a sane prefix.
        If known_prefixes is provided, the prefix must be in that set (case-insensitive).
        """
        if LinkTagHelper.is_external(link_tag):
            return False

        target, _ = LinkTagHelper.split_link_tag(link_tag)
        target = target.strip()
        if "" == target:
            return False

        matches = re.match(r"^([a-z0-9][a-z0-9._-]*)>(.+)$", target, flags=re.IGNORECASE)
        if not matches:
            return False

        if known_prefixes is None:
            return True

        prefix = matches.group(1).lower()
        known = {p.lower() for p in known_prefixes}

        return prefix in known

    @staticmethod
    def split_interwiki(target: str) -> tuple[str, str | None]:
        interwiki, interwiki_id = target.strip().split(">", 1)
        if ">" not in target:
            interwiki = target.strip()
            interwiki_id = None

        if not interwiki_id:
            interwiki_id = None

        return interwiki, interwiki_id

    @staticmethod
    def is_external(link_tag: str, treat_bare_domains_as_external: bool = False) -> bool:
        """
        External if target starts with a known URL scheme (case-insensitive).
        Optionally treat bare domains like 'www.example.com' as external.
        """
        external_prefixes = (
            "http://",
            "https://",
            "ftp://",
            "ftps://",
            "smb://",
            "irc://",
            "ircs://",
            "mailto:",
            "tel:",
            "file://",
        )

        target, _ = LinkTagHelper.split_link_tag(link_tag)
        target_norm = target.strip()
        if "" == target_norm:
            return False

        target_lc = target_norm.lower()
        if any(target_lc.startswith(prefix) for prefix in external_prefixes):
            return True

        if treat_bare_domains_as_external:
            if re.match(r"^(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/|$)", target_lc):
                return True

        return False
