from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_or_parent_validator import FileOrParentValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestFileOrParentValidator(AbstractFakeDokuTest):
    def test_valid(self):
        to_validade = self.tmp_root.joinpath("__some_file.txt")
        self.assertEqual(first=to_validade, second=FileOrParentValidator.validate(to_validade))

    def test_invalid(self):
        to_validade = self.tmp_root.joinpath("some_folder/__some_file.txt")

        with self.assertRaises(InvalidPathError) as context:
            FileOrParentValidator.validate(to_validade)

        self.assertEqual(
            "The given path '/tmp/fake_doku/some_folder/__some_file.txt' does not exist!",
            str(context.exception),
        )
