from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_excluded_folder_validator import PathIsExcludedFolderValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsExcludedFolderValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.folder_valid, PathIsExcludedFolderValidator.validate(self.folder_valid, ["three"]))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathIsExcludedFolderValidator.validate(self.folder_valid, ["two"])

        self.assertEqual(
            "The given folder '/tmp/fake_doku/two' is excluded!",
            str(context.exception),
        )
