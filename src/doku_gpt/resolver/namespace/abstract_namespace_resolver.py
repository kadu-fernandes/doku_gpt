from __future__ import annotations

import os
from abc import abstractmethod
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_validator import FileValidator
from doku_gpt.validator.path.folder_validator import FolderValidator
from doku_gpt.validator.path.is_child_validator import IsChildValidator


class AbstractNamespaceResolver(AbstractRootFolder):

    _START_ABSOLUTE = (":",)
    _START_RELATIVE = (".", "~")
    _START_PRIOR = ("..",)

    _INVALID_SEGMENTS = (".", "~", ">", ":", "|")

    def __init__(self, root_folder: str | Path, context: str | Path | None = None):
        super().__init__(root_folder=root_folder)
        self.context = context

    @property
    def context(self) -> Path | None:
        return self.__context

    @context.setter
    def context(self, context: str | Path | None) -> None:
        if context is None:
            self.__context = None
            return

        context = self._resolve_path(context)
        context = IsChildValidator.validate(parent=self.root_folder, child=context)
        self.__context = context if context.is_dir() else context.parent
        self.__context_namespace = self.path_to_absolute_namespace(self.__context).rstrip(":")

    @property
    def context_namespace(self) -> str | None:
        return self.__context_namespace

    @abstractmethod
    def can_resolve(self, namespace: str) -> bool:
        """
        Check if the namespace can be resolved by the validator.
        Example: '~:namespace:page' can be resolved by the 'RelativeNamespaceValidator'
        """
        pass

    @abstractmethod
    def resolve(self, namespace: str) -> str:
        """
        Validate the namespace and, if it's possible, try to resolve it to its absolute version.
        Example: '~:namespace:page' can be resolved by the 'RelativeNamespaceValidator' and be resolved to ':some:namespace:page'
        """
        pass

    def path_to_absolute_namespace(self, path: str | Path):
        to_resolve = self._resolve_path(path).with_suffix("")
        to_resolve = to_resolve.relative_to(self.root_folder)

        return ":" + str(to_resolve).strip(os.sep).replace(os.sep, ":")

    @staticmethod
    def _resolve_requirements(namespace: str) -> str:
        """
        Validate some common requirements for a namespace to be valid
        """
        to_resolve = namespace.strip()

        if "" == to_resolve:
            raise InvalidNamespaceError(f"The given namespace '{to_resolve}' is empty!")

        if to_resolve in AbstractNamespaceResolver._INVALID_SEGMENTS:
            raise InvalidNamespaceError(f"The given namespace '{to_resolve}' is only a marker, not a page/namespace.")

        if "::" in to_resolve:
            raise InvalidNamespaceError(f"The given '{to_resolve}' namespace contains '::'!")

        return to_resolve

    @staticmethod
    def _remove_prefixes(namespace: str) -> str:
        """
        Remove all leading prefix symbols ('.', '~', '>', '|', ':') and whitespace.
        This intentionally normalizes any absolute/relative/prior marker into a purely relative string.
        Examples:
          "~~~~something"   -> "something"
          ".....something"  -> "something"
          ">>>>>>something"  -> "something"
          "..:~|>a:b"       -> "a:b"
          "   :a:b"         -> "a:b"
        """
        if namespace is None:
            return ""
        text = namespace.strip()
        return text.lstrip(".~|:>")

    @staticmethod
    def _split_namespace(namespace: str) -> list[str]:
        """
        Split a namespace by the ":" and ensure none of them is empty or malformed.
        Note! It will change any namespace into a relative one.
        """
        segments = AbstractNamespaceResolver._remove_prefixes(namespace).split(":")
        for segment in segments:
            if ("" == segment) or (segment in AbstractNamespaceResolver._INVALID_SEGMENTS):
                raise InvalidNamespaceError(f"The given namespace '{namespace}' is malformed!")
        return segments

    @staticmethod
    def _resolve_path(path: str | Path) -> Path:
        """
        Check if a path is valid as a folder or as a file.
        Preference:
          1) Folder with the exact path
          2) File with the exact path (as-is)
          3) File with '.txt' suffix (fallback)
        Note: If both a folder and a file exist with the same stem, the folder wins.
        """
        try:
            return FolderValidator.validate(path)
        except InvalidPathError as folder_exc:
            try:
                return FileValidator.validate(path)
            except InvalidPathError:
                txt_candidate = path if path.suffix == ".txt" else path.with_suffix(".txt")
                if txt_candidate != path:
                    try:
                        return FileValidator.validate(txt_candidate)
                    except InvalidPathError:
                        pass
                raise folder_exc

    def _absolute_namespace_to_path(self, namespace: str):
        """
        Convert an absolute namespace to its real path
        """
        try:
            return self._resolve_path(self.root_folder.joinpath(namespace.strip(":").strip().replace(":", os.sep)))
        except InvalidPathError:
            raise InvalidNamespaceError(f"The given namespace '{namespace}' does not exist!")

    def _relative_namespace_to_path(self, namespace: str) -> Path:
        if self.context is None:
            raise RuntimeError("It's not possible to resolve a relative namespace without a context!")

        to_resolve = namespace.strip().rstrip(":")

        if to_resolve.startswith((".", "~")):
            if to_resolve.startswith(".."):
                raise InvalidNamespaceError(f"The namespace '{namespace}' is not a relative namespace!")

            to_resolve = AbstractNamespaceResolver._remove_prefixes(to_resolve).strip(":")

        to_resolve = self.context_namespace + ":" + to_resolve

        return self._absolute_namespace_to_path(to_resolve)

    def _prior_namespace_to_path(self, namespace: str) -> Path:
        """
        Convert a prior namespace to its real path.
        Note! As a rule, only one prior prefix is allowed in a namespace.
        """
        if self.context is None:
            raise RuntimeError("It's not possible to resolve a prior namespace without a context!")

        if not namespace.strip().startswith(".."):
            raise InvalidNamespaceError(f"The given namespace '{namespace}' is not a prior namespace!")

        to_resolve = AbstractNamespaceResolver._remove_prefixes(namespace)
        return AbstractNamespaceResolver._resolve_path(self.context.parent.joinpath(to_resolve.replace(":", os.sep)))
