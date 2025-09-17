from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_excluded_file_validator import PathIsExcludedFileValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsExcludedFileValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.file_valid, PathIsExcludedFileValidator.validate(self.file_valid, ["three"]))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathIsExcludedFileValidator.validate(self.file_valid, ["start"])

        self.assertEqual(
            "The given file '/tmp/fake_doku/two/start.txt' is excluded!",
            str(context.exception),
        )
