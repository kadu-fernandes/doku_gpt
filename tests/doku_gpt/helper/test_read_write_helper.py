from __future__ import annotations

from doku_gpt.helper.read_write_helper import ReadWriteHelper
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestReadWriteHelper(AbstractFakeDokuTest):
    def test_read_text(self):
        content = ReadWriteHelper.read_text(self.file_valid())
        self.assertTrue(content.startswith("====== Start ======"))

    def test_write_text(self):
        content = ReadWriteHelper.read_text(self.file_valid())
        self.assertTrue(content.startswith("====== Start ======"))
        ReadWriteHelper.write_text(file_path=self.file_valid(), content="#### Xupex ####")
        content = ReadWriteHelper.read_text(self.file_valid())
        self.assertTrue(content.startswith("#### Xupex ####"))

    def test_read_text_lines(self):
        lines = ReadWriteHelper.read_text_lines(self.file_valid())
        self.assertEqual("  * [[~else]]", lines[3])

    def test_write_text_lines(self):
        lines = ReadWriteHelper.read_text_lines(self.file_valid())
        lines[3] = "This is Xupex"
        ReadWriteHelper.write_text_lines(self.file_valid(), lines)
        lines = ReadWriteHelper.read_text_lines(self.file_valid())
        self.assertEqual("This is Xupex", lines[3])

    def test_read_write_json(self):
        file = self.tmp_root.joinpath("the_file.json")
        ReadWriteHelper.write_json(file_path=file, content={"something": "else"})
        content = ReadWriteHelper.read_json(file)
        self.assertEqual("else", content["something"])
