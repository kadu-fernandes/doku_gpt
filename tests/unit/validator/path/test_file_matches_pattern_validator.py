from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.file_matches_pattern_validator import FileMatchesPatternValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestFileMatchesPatternValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.file_valid, FileMatchesPatternValidator.validate(self.file_valid, "*.txt"))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            FileMatchesPatternValidator.validate(self.file_valid, "*.md")

        self.assertEqual(
            "The given file '/tmp/fake_doku/two/start.txt' does not match the pattern('*.md')!",
            str(context.exception),
        )
