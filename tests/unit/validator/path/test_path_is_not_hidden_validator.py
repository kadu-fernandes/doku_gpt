from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_is_not_hidden_validator import PathIsNotHiddenValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsNotHiddenValidator(AbstractFakeDokuTest):
    def test_not_hidden_valid(self):
        self.assertEqual(self.file_valid, PathIsNotHiddenValidator.validate(self.file_valid))

    def test_not_hidden_invalid_file(self):
        with self.assertRaises(InvalidPathError) as context:
            PathIsNotHiddenValidator.validate(self.file_secret)

        self.assertEqual(
            "The given path '/tmp/fake_doku/two/.secret.txt' is hidden!",
            str(context.exception),
        )

    def test_not_hidden_invalid_folder(self):
        with self.assertRaises(InvalidPathError) as context:
            self.assertEqual(self.folder_secret, PathIsNotHiddenValidator.validate(self.folder_secret))

        self.assertEqual(
            "The given path '/tmp/fake_doku/.secret' is hidden!",
            str(context.exception),
        )
