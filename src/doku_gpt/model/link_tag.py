from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, PrivateAttr, ValidationInfo, model_validator

from doku_gpt.enum.link_status import LinkStatus
from doku_gpt.enum.link_type import LinkType
from doku_gpt.error.invalid_value_error import InvalidValueError


class LinkTag(BaseModel):
    link_status: LinkStatus = LinkStatus.NOT_VALIDATED
    link_type: LinkType | None = None
    target_prefix: str = ""
    target_suffix: str | None = None
    target_fragment: str | None = None
    target_query: str | None = None
    resolved: str | None = None
    label: str | None = None
    excerpt: str | None = None

    _root_folder: Path | None = PrivateAttr(default=None)

    @property
    def is_external(self) -> bool:
        if self.link_type is None:
            raise InvalidValueError("Link type is not set!")
        return self.link_type == LinkType.EXTERNAL

    @property
    def is_internal(self) -> bool:
        if self.link_type is None:
            raise InvalidValueError("Link type is not set!")
        return self.link_type in (
            LinkType.INTERNAL,
            LinkType.INTERNAL_ABSOLUTE,
            LinkType.INTERNAL_PRIOR,
            LinkType.INTERNAL_RELATIVE,
        )

    @property
    def is_interwiki(self) -> bool:
        if self.link_type is None:
            raise InvalidValueError("Link type is not set!")
        return self.link_type == LinkType.INTERWIKI

    @property
    def is_valid(self) -> bool:
        return LinkStatus.VALID == self.link_status

    @property
    def target(self) -> str:
        target = self.target_prefix
        if self.is_interwiki:
            if self.target_suffix is None:
                raise InvalidValueError(f"The interwiki '{target}' must have a suffix!")
            target += f">{self.target_suffix}"
        return target

    @property
    def core(self) -> str:
        core = self.target
        if self.target_query:
            core += f"?{self.target_query}"
        if self.target_fragment:
            core += f"#{self.target_fragment}"
        return core

    @property
    def content(self) -> str:
        content = self.core
        if self.label is not None:
            content += f"|{self.label}"
        return content

    @property
    def link_tag(self) -> str:
        return f"[[{self.content}]]"

    def __can_return_path(self) -> Path | None:
        if self._root_folder is None:
            return None

        if not self.is_internal:
            return self._root_folder

        if LinkType.INTERNAL_ABSOLUTE != self.link_type and self.resolved is not None:
            raise InvalidValueError("Only absolute namespaces can have resolved paths!")

        if LinkType.INTERNAL_ABSOLUTE != self.link_type:
            if self.resolved is not None:
                raise InvalidValueError("Only absolute namespaces can have resolved paths!")
            return self._root_folder

        return self._root_folder

    @property
    def path(self) -> Path | None:
        root_folder = self.__can_return_path()
        if root_folder is None:
            return None

        if self.resolved is None:
            return None

        if LinkType.INTERNAL_ABSOLUTE != self.link_type:
            raise InvalidValueError(f"Non absolute namespaces '{self.target_prefix}' cannot have resolved paths!    ")

        return root_folder.joinpath(self.resolved)

    @property
    def relative_path(self) -> Path | None:
        root_folder = self.__can_return_path()
        if root_folder is None:
            return None

        to_resolve = str(self.target_prefix).lstrip(":").replace(":", os.sep)
        to_resolve_path = root_folder.joinpath(to_resolve)
        try:
            return to_resolve_path.resolve(True)
        except FileNotFoundError:
            try:
                return to_resolve_path.with_suffix("*.txt").resolve(True)
            except FileNotFoundError:
                return None

    @property
    def url(self) -> str | None:
        if self.is_internal:
            return None
        if self.resolved is None:
            return None
        return self.resolved

    def attach_root(self, root_folder: str | Path) -> None:
        self._root_folder = Path(root_folder)

    @model_validator(mode="after")
    def _attach_root_from_context(self, info: ValidationInfo):
        if info.context and "root_folder" in info.context:
            self.attach_root(info.context["root_folder"])
        return self
