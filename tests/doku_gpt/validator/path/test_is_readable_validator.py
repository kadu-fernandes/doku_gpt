from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.is_writable_validator import IsWritableValidator
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestIsReadableValidator(AbstractFakeDokuTest):

    def test_is_writable_valid(self):
        self.assertEqual(self.file_valid(), IsWritableValidator.validate(self.file_valid()))

    def test_is_writable_invalid(self):
        file = Path("/root")
        with self.assertRaises(InvalidPathError) as context:
            IsWritableValidator.validate(file)

        self.assertEqual(
            "The given path '/root' is not writable!",
            str(context.exception),
        )
