from __future__ import annotations

import json
from pathlib import Path

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.factory.link_tag_factory import LinkTagFactory
from doku_gpt.finder.finder import Finder
from doku_gpt.functions import extract_link_tags
from doku_gpt.model.link_tag import LinkTag
from doku_gpt.resolver.link_tag.resolver import Resolver


class SettingsHandler(AbstractRootFolder):
    def __init__(
        self,
        root_folder: str | Path,
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ):
        super().__init__(root_folder=root_folder, excluded_folders=excluded_folders, excluded_files=excluded_files)
        self.__link_tags: dict[str, LinkTag] = {}
        self.__factory: LinkTagFactory = LinkTagFactory(root_folder)
        self.__resolver = Resolver(root_folder)
        self.__file = self.root_folder.joinpath(".doku_gpt.json")
        self.__adapter: PageAdapter = PageAdapter(self.__file)

    def create(self) -> None:
        if self.__file.exists():
            return
        self.__link_tags = {}
        self.__scan_and_merge()
        self.__save()

    def update(self) -> None:
        """Load current map (if any), rescan pages, and merge updates."""
        self.__link_tags = {}
        self.__load()
        self.__scan_and_merge()
        self.__save()

    def load(self) -> dict[str, LinkTag]:
        """
        Load the current .doku_gpt.json file (if any) and return link tags.
        """
        self.__link_tags = {}
        self.__load()
        return self.__link_tags

    def __scan_and_merge(self) -> None:
        finder = self.__create_finder()
        files = finder.find_files("*.txt")
        for file in files:
            adapter = PageAdapter(file)
            self.__create_file(adapter)

    def __load(self) -> None:
        if not self.__file.exists():
            return
        raw_text = self.__adapter.content or ""
        if not raw_text:
            try:
                raw_text = self.__file.read_text(encoding="utf-8")
            except FileNotFoundError:
                return
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError:
            return
        for target, data in payload.items():
            try:
                tag = LinkTag.model_validate(data)
            except AttributeError:
                tag = LinkTag.parse_obj(data)
            self.__link_tags[target] = tag

    def __save(self) -> None:
        serializable = {
            key: tag.model_dump(mode="json", by_alias=True, exclude_none=True) for key, tag in self.__link_tags.items()
        }
        self.__adapter.content = json.dumps(serializable, indent=2, ensure_ascii=False, sort_keys=True)

    def __create_file(self, adapter: PageAdapter) -> None:
        for line in adapter.lines:
            link_tags = extract_link_tags(line)
            for link_tag in link_tags:
                tag = self.__factory.get(link_tag)
                self.__resolver.context = adapter.page_path
                resolved, resolved_tag = self.__resolver.resolve(tag)
                if not resolved:
                    continue
                target = resolved_tag.target
                existing = self.__link_tags.get(target)
                if existing is None or not existing.is_valid:
                    self.__link_tags[target] = resolved_tag

    def __create_finder(self) -> Finder:
        default_excluded_folders: list[str] = ["playground", "wiki", "old_content"]
        self.excluded_folders.extend(default_excluded_folders)
        self.excluded_folders = sorted(self.excluded_folders)

        default_excluded_files: list[str] = ["sidebar"]
        self.excluded_files.extend(default_excluded_files)
        self.excluded_files = sorted(self.excluded_files)

        return Finder(
            root_folder=self.root_folder,
            excluded_folders=self.excluded_folders,
            excluded_files=self.excluded_files,
        )
