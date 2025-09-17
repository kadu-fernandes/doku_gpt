from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_file_validator import PathIsFileValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsFileValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.file_valid, PathIsFileValidator.validate(self.file_valid))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathIsFileValidator.validate(self.file_invalid)

        self.assertEqual(
            "The given path '/tmp/fake_doku/two/file_does_not_exist.txt' is not a file!",
            str(context.exception),
        )
