from __future__ import annotations

import shutil
import unittest
from pathlib import Path


class AbstractFakeDokuTest(unittest.TestCase):
    @property
    def fake_doku(self) -> Path:
        script_path = Path(__file__).resolve()

        for parent in script_path.parents:
            if parent.name == "tests":
                project_root = parent.parent

                return project_root.joinpath("data/fake_doku")

        raise RuntimeError("Could not find the 'fake_doku_path' path!")

    @property
    def file_valid(self) -> Path:
        return self.tmp_root.joinpath("two/start.txt")

    @property
    def file_invalid(self) -> Path:
        return self.tmp_root.joinpath("two/file_does_not_exist.txt")

    @property
    def file_secret(self) -> Path:
        return self.tmp_root.joinpath("two/.secret.txt")

    @property
    def folder_valid(self) -> Path:
        return self.tmp_root.joinpath("two")

    @property
    def folder_invalid(self) -> Path:
        return self.tmp_root.joinpath("two/folder_does_not_exist")

    @property
    def file_pdf(self):
        file = self.tmp_root.joinpath("some_file.pdf")
        file.write_text("Something")

        return file

    @property
    def folder_secret(self) -> Path:
        return self.tmp_root.joinpath(".secret")

    def setUp(self):
        self.tmp_root = Path("/tmp/fake_doku")
        self._copy_folder_fake_data()

    def tearDown(self):
        if self.tmp_root.exists():
            shutil.rmtree(self.tmp_root, ignore_errors=True)

    def _copy_folder_fake_data(self) -> None:
        source_path = self.fake_doku
        destination_path = self.tmp_root

        if destination_path.exists():
            shutil.rmtree(destination_path)

        shutil.copytree(src=source_path, dst=destination_path, dirs_exist_ok=False)
        self.assertTrue(destination_path.exists())
