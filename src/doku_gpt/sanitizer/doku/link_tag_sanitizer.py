from __future__ import annotations

import re
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.settings.settings_handler import SettingsHandler


class LinkTagSanitizer(AbstractRootFolder):
    """
    Replace all DokuWiki-style links [[target|Label]] in a page by either
    an excerpt or a label, according to the rules:

    - External or interwiki links: always replaced by excerpt (fallbacks applied).
    - Internal links: first occurrence replaced by excerpt (if present), subsequent by label.
      If excerpt is None/empty, use label even on the first occurrence.

    Replacements are plain text (the [[...]] markup is removed).
    """

    LINK_PATTERN = re.compile(r"\[\[(?P<target>[^\]|#]+)(?:#(?P<anchor>[^\]|]*))?(?:\|(?P<label>[^\]]*))?\]\]")

    def __init__(self, root_folder: str | Path):
        super().__init__(root_folder=root_folder)
        self._seen_internal_keys: set[str] = set()
        self._tags_map: dict[str, LinkTag] = {}
        self._factory: LinkTagFactory = LinkTagFactory(root_folder=self.root_folder)

    def load(self) -> None:
        handler = SettingsHandler(root_folder=self.root_folder)
        self._tags_map = handler.load()

    def sanitize(self, page: str) -> str:
        if not self._tags_map:
            self.load()
        return self.LINK_PATTERN.sub(self._replacement, page)

    def _replacement(self, match: re.Match) -> str:
        raw_link_tag = match.group(0)
        link_tag = self._factory.get(raw_link_tag)

        found_tag = self._tags_map.get(link_tag.target)
        if found_tag is None:
            return self._fallback_when_missing(link_tag)

        if link_tag.is_external or link_tag.is_interwiki:
            return self._choose_text(found_tag, preferred_excerpt=True, original=link_tag)

        internal_key = link_tag.target
        if self._is_seen_internal(internal_key):
            return self._choose_text(found_tag, preferred_excerpt=False, original=link_tag)

        self._mark_seen_internal(internal_key)
        return self._choose_text(found_tag, preferred_excerpt=True, original=link_tag)

    def _is_seen_internal(self, key: str) -> bool:
        return key in self._seen_internal_keys

    def _mark_seen_internal(self, key: str) -> None:
        self._seen_internal_keys.add(key)

    def _choose_text(self, canonical: LinkTag, preferred_excerpt: bool, original: LinkTag) -> str:
        canonical_excerpt = (canonical.excerpt or "").strip() if canonical.excerpt is not None else ""
        canonical_label = (canonical.label or "").strip() if canonical.label is not None else ""
        original_label = (original.label or "").strip() if original.label is not None else ""

        if preferred_excerpt:
            if 1 <= len(canonical_excerpt):
                return canonical_excerpt
            if 1 <= len(canonical_label):
                return canonical_label
            if 1 <= len(original_label):
                return original_label
            return self._title_from_target(original.target)

        if 1 <= len(canonical_label):
            return canonical_label
        if 1 <= len(original_label):
            return original_label
        if 1 <= len(canonical_excerpt):
            return canonical_excerpt
        return self._title_from_target(original.target)

    def _fallback_when_missing(self, original: LinkTag) -> str:
        original_label = (original.label or "").strip() if original.label is not None else ""
        if 1 <= len(original_label):
            return original_label
        return self._title_from_target(original.target)

    @staticmethod
    def _title_from_target(target: str) -> str:
        normalized = target.strip(":")
        if "/" in normalized:
            normalized = normalized.rsplit("/", 1)[-1]
        if ":" in normalized:
            normalized = normalized.rsplit(":", 1)[-1]
        return normalized.replace("_", " ").strip() or normalized
