from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.not_hidden_validator import NotHiddenValidator
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestNotHiddenValidator(AbstractFakeDokuTest):

    def test_not_hidden_valid(self):
        self.assertEqual(self.file_valid(), NotHiddenValidator.validate(self.file_valid()))

    def test_not_hidden_invalid_file(self):
        with self.assertRaises(InvalidPathError) as context:
            NotHiddenValidator.validate(self.file_secret())

        self.assertEqual(
            "The given path '/tmp/fake_doku/two/.secret.txt' is hidden!",
            str(context.exception),
        )

    def test_not_hidden_invalid_folder(self):
        with self.assertRaises(InvalidPathError) as context:
            self.assertEqual(self.folder_secret(), NotHiddenValidator.validate(self.folder_secret()))

        self.assertEqual(
            "The given path '/tmp/fake_doku/.secret' is hidden!",
            str(context.exception),
        )
