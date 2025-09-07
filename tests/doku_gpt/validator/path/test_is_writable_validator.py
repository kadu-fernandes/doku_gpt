from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.is_writable_validator import IsWritableValidator
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestIsWritableValidator(AbstractFakeDokuTest):

    def test_is_writable_valid(self):
        self.assertEqual(self.file_valid(), IsWritableValidator.validate(self.file_valid()))

    def test_is_writable_invalid(self):
        file = Path("/etc/hosts")
        with self.assertRaises(InvalidPathError) as context:
            IsWritableValidator.validate(file)

        self.assertEqual(
            "The given path '/etc/hosts' is not writable!",
            str(context.exception),
        )
