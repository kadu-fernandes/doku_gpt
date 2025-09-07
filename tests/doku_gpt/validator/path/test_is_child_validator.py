from __future__ import annotations

from doku_gpt.error.invalid_path_error import InvalidPathError
from doku_gpt.validator.path.is_child_validator import IsChildValidator
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestIsChildValidator(AbstractFakeDokuTest):

    def test_is_child(self):
        self.assertEqual(self.file_valid(), IsChildValidator.validate(parent=self.tmp_root, child=self.file_valid()))

        self.assertEqual(
            self.folder_valid(), IsChildValidator.validate(parent=self.tmp_root, child=self.folder_valid())
        )

    def test_is_child_invalid_folder(self):
        parent = self.tmp_root.joinpath("one")
        self.assertEqual(self.file_valid(), IsChildValidator.validate(parent=self.tmp_root, child=self.file_valid()))

        with self.assertRaises(InvalidPathError) as context_error:
            IsChildValidator.validate(parent=parent, child=self.file_valid())

        self.assertEqual(
            "The path '/tmp/fake_doku/two/start.txt' is not a child of '/tmp/fake_doku/one'!",
            str(context_error.exception),
        )
