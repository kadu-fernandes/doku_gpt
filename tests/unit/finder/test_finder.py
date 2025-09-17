from __future__ import annotations

from doku_gpt.finder.finder import Finder
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestFinder(AbstractFakeDokuTest):
    def test_find_folders(self):
        finder = self.__create_finder()
        folders = finder.find_folders()
        self.assertEqual(3, len(folders))

    def test_find_folders_pattern(self):
        finder = self.__create_finder()
        folders = finder.find_folders("two*")
        self.assertEqual(2, len(folders))

    def test_find_folders_excluded_folders(self):
        finder = self.__create_finder(excluded_folders=["two"])
        folders = finder.find_folders()
        self.assertEqual(1, len(folders))

    def test_find_folder_children(self):
        finder = self.__create_finder()
        folders = finder.find_folder_children()
        self.assertEqual(2, len(folders))

    def test_find_files(self):
        finder = self.__create_finder()
        files = finder.find_files()
        self.assertEqual(12, len(files))

    def test_find_files_pattern(self):
        finder = self.__create_finder()
        files = finder.find_files("end*")
        self.assertEqual(4, len(files))

    def test_find_files__excluded_files(self):
        finder = self.__create_finder(excluded_files=["start", "end"])
        files = finder.find_files()
        for file in files:
            print(str(file) + "\n\n")
        self.assertEqual(4, len(files))

    def test_find_files_children(self):
        finder = self.__create_finder()
        files = finder.find_file_children()
        self.assertEqual(3, len(files))

    def __create_finder(
        self,
        excluded_folders: list[str] | None = None,
        excluded_files: list[str] | None = None,
    ) -> Finder:
        return Finder(root_folder=self.fake_doku, excluded_folders=excluded_folders, excluded_files=excluded_files)
