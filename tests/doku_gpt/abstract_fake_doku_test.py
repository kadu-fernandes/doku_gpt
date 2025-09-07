from __future__ import annotations

import shutil
import unittest
from abc import ABC
from pathlib import Path

from doku_gpt.helper.file_system_helper import FileSystemHelper


class AbstractFakeDokuTest(unittest.TestCase, ABC):

    @staticmethod
    def fake_doku_path() -> Path:
        script_path = Path(__file__).resolve()

        for parent in script_path.parents:
            if parent.name == "tests":
                project_root = parent.parent

                return project_root.joinpath("data/fake_doku")

        raise RuntimeError("Could not find the 'fake_doku_path' path!")

    def file_valid(self) -> Path:
        return self.tmp_root.joinpath("two/start.txt")

    def file_invalid(self) -> Path:
        return self.tmp_root.joinpath("two/file_does_not_exist.txt")

    def file_secret(self) -> Path:
        return self.tmp_root.joinpath("two/.secret.txt")

    def folder_valid(self) -> Path:
        return self.tmp_root.joinpath("two")

    def folder_invalid(self) -> Path:
        return self.tmp_root.joinpath("two/folder_does_not_exist")

    def file_pdf(self):
        file = self.tmp_root.joinpath("some_file.pdf")
        file.write_text("Something")

        return file

    def folder_secret(self) -> Path:
        return self.tmp_root.joinpath(".secret")

    def setUp(self):
        self.tmp_root = Path("/tmp/fake_doku")
        FileSystemHelper.copy_folder(source=AbstractFakeDokuTest.fake_doku_path(), destination=self.tmp_root)

    def tearDown(self):
        if self.tmp_root.exists():
            shutil.rmtree(self.tmp_root, ignore_errors=True)
