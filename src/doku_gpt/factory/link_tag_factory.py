from __future__ import annotations

import re
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.enum.link_type import LinkType
from doku_gpt.model.link_tag import LinkTag


class LinkTagFactory(AbstractRootFolder):
    REGEX_QUERY_FRAGMENT = re.compile(
        r"""
            ^(?P<base>[^?#]*)
            (?:\?(?P<query>[^#]*))?
            (?:\#(?P<fragment>.*))?
            $""",
        re.VERBOSE,
    )

    def __init__(
        self,
        root_folder: str | Path,
    ):
        super().__init__(root_folder=root_folder)

    def get(self, link_tag: str) -> LinkTag:
        self.__link_tag: LinkTag = LinkTag()
        self.__link_tag.attach_root(self.root_folder)

        cleaned_link_tag = link_tag.strip().lstrip("[").rstrip("]").strip()
        if "" == cleaned_link_tag:
            raise ValueError("Empty link tag after trimming brackets.")

        cleaned_link_tag = self.__extract_label(cleaned_link_tag)
        cleaned_link_tag = self.__extract_query_and_fragment(cleaned_link_tag)
        if "" == cleaned_link_tag:
            raise ValueError("Empty target after removing query and fragment.")

        self.__extract_target(cleaned_link_tag)
        self.__classify()
        return self.__link_tag

    def __extract_label(self, link_tag: str) -> str:
        if "|" not in link_tag:
            return link_tag

        target_part, label_part = link_tag.split(sep="|", maxsplit=1)
        self.__link_tag.label = None if "" == label_part.strip() else label_part.strip()
        return target_part.strip()

    def __extract_query_and_fragment(self, target: str) -> str:
        regex_match = self.REGEX_QUERY_FRAGMENT.match(target)
        if not regex_match:
            return target.strip()

        groups = regex_match.groupdict()

        if groups.get("query"):
            self.__link_tag.target_query = groups["query"]
        if groups.get("fragment"):
            self.__link_tag.target_fragment = groups["fragment"]

        base_part = str(groups["base"]).strip()
        return base_part

    def __extract_target(self, target: str) -> None:
        if ">" not in target:
            self.__link_tag.target_prefix = target.strip()
            if "" == self.__link_tag.target_prefix:
                raise ValueError("Target prefix cannot be empty.")
            return

        prefix_part, suffix_part = target.split(sep=">", maxsplit=1)
        self.__link_tag.target_prefix = prefix_part.strip()
        self.__link_tag.target_suffix = suffix_part.strip()

        if "" == self.__link_tag.target_prefix or "" == self.__link_tag.target_suffix:
            raise ValueError("Interwiki links require both non-empty prefix and suffix.")

    def __classify(self) -> None:
        if self.__link_tag.target_suffix is not None:
            self.__link_tag.link_type = LinkType.INTERWIKI
            return

        if "://" in self.__link_tag.target_prefix:
            self.__link_tag.link_type = LinkType.EXTERNAL
            return

        if self.__link_tag.target_prefix.startswith(("..")):
            self.__link_tag.link_type = LinkType.INTERNAL_PRIOR
            return

        if self.__link_tag.target_prefix.startswith((".", "~")):
            self.__link_tag.link_type = LinkType.INTERNAL_RELATIVE
            return

        if self.__link_tag.target_prefix.startswith((":")):
            self.__link_tag.link_type = LinkType.INTERNAL_ABSOLUTE
            return

        self.__link_tag.link_type = LinkType.INTERNAL
