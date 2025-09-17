from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_exists_validator import PathExistsValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathExistsValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.folder_valid, PathExistsValidator.validate(self.folder_valid))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathExistsValidator.validate(self.file_invalid)

        self.assertEqual(
            "The given path '/tmp/fake_doku/two/file_does_not_exist.txt' does not exist!",
            str(context.exception),
        )
