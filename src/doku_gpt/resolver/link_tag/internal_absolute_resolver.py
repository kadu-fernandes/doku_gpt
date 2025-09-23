from __future__ import annotations

import os

from doku_gpt.enum.link_status import LinkStatus
from doku_gpt.enum.link_type import LinkType
from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.abstract_namespace_resolver import AbstractNamespaceResolver
from doku_gpt.validator.path.file_validator import FileValidator


class InternalAbsoluteResolver(AbstractNamespaceResolver):
    def can_resolve(self, link_tag: LinkTag) -> bool:
        return link_tag.is_internal and (link_tag.link_type is LinkType.INTERNAL_ABSOLUTE)

    def resolve(self, link_tag: LinkTag) -> tuple[bool, LinkTag]:
        if not self.can_resolve(link_tag):
            return False, link_tag

        if self.context is None:
            raise InvalidNamespaceError("No context given!")

        if link_tag.link_status is LinkStatus.VALID:
            return True, link_tag

        link_tag.attach_root(self.root_folder)

        raw_target = (link_tag.target_prefix or "").strip()
        if not raw_target:
            raise InvalidNamespaceError("Empty relative namespace.")

        page_path = self.root_folder.joinpath(raw_target.lstrip(":").replace(":", os.sep)).with_suffix(".txt")

        try:
            FileValidator.validate(page_path)
        except InvalidPathError:
            raise
        link_tag.target_prefix = self._absolute_namespace_from_path(page_path)

        changed_any_field = False
        changed, link_tag = self._add_label(link_tag=link_tag, page_path=page_path)
        if changed:
            changed_any_field = True

        changed, link_tag = self._add_excerpt(link_tag=link_tag, page_path=page_path)
        if changed:
            changed_any_field = True

        if changed_any_field and link_tag.link_status is not LinkStatus.NOT_VALIDATED:
            link_tag.link_status = LinkStatus.NOT_VALIDATED

        return True, link_tag
