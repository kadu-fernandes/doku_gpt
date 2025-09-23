from __future__ import annotations

from pathlib import Path

from doku_gpt.enum.link_status import LinkStatus
from doku_gpt.enum.link_type import LinkType
from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.abstract_namespace_resolver import AbstractNamespaceResolver


class InternalImplicitResolver(AbstractNamespaceResolver):
    def can_resolve(self, link_tag: LinkTag) -> bool:
        if not link_tag.is_internal:
            return False
        if (
            link_tag.link_type is LinkType.INTERNAL_ABSOLUTE
            or link_tag.link_type is LinkType.INTERNAL_PRIOR
            or link_tag.link_type is LinkType.INTERNAL_RELATIVE
        ):
            return False
        return True

    def resolve(self, link_tag: LinkTag) -> tuple[bool, LinkTag]:
        if not self.can_resolve(link_tag):
            return False, link_tag

        if link_tag.link_status is LinkStatus.VALID:
            return True, link_tag

        if self.context is None:
            raise InvalidNamespaceError("No context given!")

        link_tag.attach_root(self.root_folder)

        raw_target = (link_tag.target_prefix or "").strip()
        if not raw_target:
            raise InvalidNamespaceError("Empty implicit namespace.")

        page_path: Path

        if ":" in raw_target:
            page_path = self._absolute_page_path(raw_target)
            self._validate_or_raise(page_path)
        else:
            try:
                relative_candidate = self._resolve_page_path_from_context(
                    base_folder=self.context,
                    remainder=raw_target,
                    root_folder=self.root_folder,
                )
                self._validate_or_raise(relative_candidate)
                page_path = relative_candidate
            except InvalidPathError:
                absolute_candidate = self._absolute_page_path(raw_target)
                self._validate_or_raise(absolute_candidate)
                page_path = absolute_candidate
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
