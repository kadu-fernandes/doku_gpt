from __future__ import annotations

from pathlib import Path

from doku_gpt.helper.finder_helper import FinderHelper
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestFinderHelper(AbstractFakeDokuTest):
    def test_find_folder_children(self):
        found = FinderHelper.find_folder_children(folder=self.tmp_root)
        self.assertEqual(2, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

    def test_find_folder_children_excluded_folder(self):
        found = FinderHelper.find_folder_children(folder=self.tmp_root, excluded_folders=["two"])
        self.assertEqual(1, len(found))

        actual = found[0]
        expected = Path("/tmp/fake_doku/one")
        self.assertEqual(expected, actual)

    def test_find_folder_children_pattern(self):
        found = FinderHelper.find_folder_children(folder=self.tmp_root, pattern="o*")
        self.assertEqual(1, len(found))

        actual = found[0]
        expected = Path("/tmp/fake_doku/one")
        self.assertEqual(expected, actual)

    def test_find_folders(self):
        found = FinderHelper.find_folders(folder=self.tmp_root)
        self.assertEqual(3, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

    def test_find_folders_excluded_folder(self):
        found = FinderHelper.find_folders(folder=self.tmp_root, excluded_folders=["one"])
        self.assertEqual(2, len(found))

        actual = found[0]
        expected = Path("/tmp/fake_doku/two")
        self.assertEqual(expected, actual)

        actual = found[1]
        expected = Path("/tmp/fake_doku/two/three")
        self.assertEqual(expected, actual)

    def test_find_folders_excluded_pattern(self):
        found = FinderHelper.find_folders(folder=self.tmp_root, pattern="t*")
        self.assertEqual(2, len(found))

        actual = found[0]
        expected = Path("/tmp/fake_doku/two")
        self.assertEqual(expected, actual)

        actual = found[1]
        expected = Path("/tmp/fake_doku/two/three")
        self.assertEqual(expected, actual)

    def test_find_file_children(self):
        found = FinderHelper.find_file_children(folder=self.tmp_root)
        self.assertEqual(3, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

    def test_find_file_children_excluded_files(self):
        found = FinderHelper.find_file_children(folder=self.tmp_root, excluded_files=["else"])
        self.assertEqual(2, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

        actual = found[0]
        expected = Path("else.txt")
        self.assertNotEqual(expected, actual.name)

    def test_find_file_children_pattern(self):
        found = FinderHelper.find_file_children(folder=self.tmp_root, pattern="els*")
        self.assertEqual(1, len(found))

        actual = found[0]
        expected = Path("else.txt")
        self.assertNotEqual(expected, actual.name)

    def test_find_files(self):
        found = FinderHelper.find_files(folder=self.tmp_root)
        self.assertEqual(12, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

    def test_find_files_excluded_files(self):
        found = FinderHelper.find_files(folder=self.tmp_root, excluded_files=["start"])
        self.assertEqual(8, len(found))

        actual = str(found[0])
        self.assertFalse(actual.startswith("."))

        expected = Path("start.txt")
        for actual in found:
            self.assertNotEqual(expected, actual.name)

    def test_find_files_pattern(self):
        found = FinderHelper.find_files(folder=self.tmp_root, pattern="els*")
        self.assertEqual(4, len(found))

        expected = Path("else.txt")
        for actual in found:
            self.assertNotEqual(expected, actual.name)
