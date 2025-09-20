from __future__ import annotations

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.extractor.web_page_extractor import WebPageExtractor
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.registry.interwiki_map_registry import InterwikiMapRegistry


class InterwikiResolver(AbstractRootFolder):
    def can_resolve(self, link_tag: LinkTag) -> bool:
        return link_tag.is_interwiki

    def resolve(self, link_tag: LinkTag) -> tuple[bool, LinkTag]:
        if not self.can_resolve(link_tag):
            return False, link_tag

        url = InterwikiMapRegistry.get(link_tag.target_prefix, link_tag.target_suffix)

        url_valid = False

        if link_tag.label is None:
            fetched_title = WebPageExtractor.extract_title(url)
            if fetched_title:
                link_tag.label = fetched_title
                link_tag.resolved = url
                url_valid = True

        if not url_valid:
            url_valid = WebPageExtractor.url_exists(url)

        if url_valid and link_tag.resolved is None:
            link_tag.resolved = url

        return (url_valid and link_tag.resolved is not None), link_tag
