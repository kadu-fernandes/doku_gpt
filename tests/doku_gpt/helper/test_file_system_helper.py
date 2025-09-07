from __future__ import annotations

import shutil
from pathlib import Path

from doku_gpt.helper.file_system_helper import FileSystemHelper
from doku_gpt.helper.read_write_helper import ReadWriteHelper
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestFileSystemHelper(AbstractFakeDokuTest):
    def test_copy_file(self):
        destination = self.tmp_root.joinpath("dont_exist.txt")
        destination.unlink(missing_ok=True)
        self.assertFalse(destination.exists())
        FileSystemHelper.copy_file(source=self.file_valid(), destination=destination)
        self.assertTrue(destination.exists())
        content_one = ReadWriteHelper.read_text(self.file_valid())
        content_two = ReadWriteHelper.read_text(destination)
        self.assertEqual(content_one, content_two)

    def test_copy_folder(self):
        destination = Path("/tmp/DoesNotExists")
        if destination.exists():
            shutil.rmtree(destination, ignore_errors=True)
        destination_two = destination.joinpath("two")
        self.assertFalse(destination.exists())
        self.assertFalse(destination_two.exists())
        self.assertTrue(self.tmp_root.exists())
        FileSystemHelper.simple_copy_folder(source=self.tmp_root, destination=destination)
        self.assertTrue(destination.exists())
        self.assertTrue(destination_two.exists())
