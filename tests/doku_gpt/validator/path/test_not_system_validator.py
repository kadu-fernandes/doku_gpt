from __future__ import annotations

from pathlib import Path

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.not_system_path_validator import NotSystemPathValidator
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestNotSystemValidator(AbstractFakeDokuTest):

    def test_not_system_valid(self):
        self.assertEqual(self.file_valid(), NotSystemPathValidator.validate(self.file_valid()))

    def test_not_system_invalid(self):
        file = Path("/etc/hosts")
        with self.assertRaises(InvalidPathError) as context:
            NotSystemPathValidator.validate(file)

        self.assertEqual(
            "The given path '/etc/hosts' is a system path and is not allowed!",
            str(context.exception),
        )
