from __future__ import annotations

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.extractor.web_page_extractor import WebPageExtractor
from doku_gpt.model.link_tag import LinkTag


class ExternalResolver(AbstractRootFolder):
    def can_resolve(self, link_tag: LinkTag) -> bool:
        return link_tag.is_external

    def resolve(self, link_tag: LinkTag) -> tuple[bool, LinkTag]:
        if not self.can_resolve(link_tag):
            return False, link_tag

        core_url = (link_tag.core or "").strip()
        if not core_url or not WebPageExtractor.can_fetch(core_url):
            return False, link_tag

        url_valid = WebPageExtractor.url_exists(core_url)

        if link_tag.label is None and url_valid:
            fetched_title = WebPageExtractor.extract_title(core_url)
            if fetched_title:
                link_tag.label = fetched_title

        if link_tag.resolved is None and url_valid:
            link_tag.resolved = core_url

        return (url_valid and link_tag.resolved is not None), link_tag
