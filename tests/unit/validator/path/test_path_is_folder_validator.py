from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_folder_validator import PathIsFolderValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsFolderValidator(AbstractFakeDokuTest):
    def test_is_folder_valid(self):
        self.assertEqual(self.folder_valid, PathIsFolderValidator.validate(self.folder_valid))

    def test_is_folder_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathIsFolderValidator.validate(self.folder_invalid)

        self.assertEqual(
            "The given path '/tmp/fake_doku/two/folder_does_not_exist' is not a directory!",
            str(context.exception),
        )
