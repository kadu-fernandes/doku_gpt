from __future__ import annotations

import re
from pathlib import Path
from typing import List

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.settings.settings_handler import SettingsHandler


class LinkTagSanitizer(AbstractRootFolder):
    """
    Replace every DokuWiki link [[target|Label]] by:
      - First occurrence of the same target in the page:  Label (Label é "Excerpt")
      - Subsequent occurrences:                           Label

    If no canonical data is found for a target, falls back to the link's own label
    or a title derived from the target, and skips the excerpt annotation.
    """

    LINK_PATTERN = re.compile(r"\[\[[^\]]+]]")

    def __init__(self, root_folder: str | Path):
        super().__init__(root_folder=root_folder)
        self.__seen_targets: set[str] = set()
        self.__settings: dict[str, LinkTag] = {}
        self._factory: LinkTagFactory = LinkTagFactory(root_folder=self.root_folder)

    def sanitize(self, page: str) -> str:
        if not self.__settings:
            self.__settings = SettingsHandler(root_folder=self.root_folder).load()

        self.__seen_targets.clear()

        lines = page.splitlines(keepends=True)
        sanitized_lines: List[str] = []

        for line in lines:
            if "" == line.strip():
                sanitized_lines.append(line)
                continue

            tags_in_line = self.LINK_PATTERN.findall(line)
            for raw_tag in tags_in_line:
                link_tag = self._factory.get(raw_tag)
                replacement = self.__fetch_label_or_excerpt(link_tag=link_tag)
                line = line.replace(raw_tag, replacement, 1)

            sanitized_lines.append(line)

        return "".join(sanitized_lines)

    def __fetch_label_or_excerpt(self, link_tag: LinkTag) -> str:
        default_return: str = link_tag.label or link_tag.target

        found_setting = self.__settings.get(link_tag.target)
        if found_setting is None:
            return default_return

        found_label = found_setting.label or default_return

        if link_tag.target in self.__seen_targets:
            return found_label

        self.__seen_targets.add(link_tag.target)

        if found_setting.excerpt is None:
            return found_label

        return f'{found_label} ("{found_setting.excerpt}")'
