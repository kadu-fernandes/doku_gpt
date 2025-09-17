from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.path_extension_validator import PathExtensionValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsExtensionValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.file_valid, PathExtensionValidator.validate(path=self.file_valid, extension="txt"))

    def test_is_file_invalid(self):
        with self.assertRaises(InvalidPathError) as context:
            PathExtensionValidator.validate(path=self.file_pdf, extension="txt")

        self.assertEqual(
            "The extension '.txt' of the given file '/tmp/fake_doku/some_file.pdf' is not valid!",
            str(context.exception),
        )
