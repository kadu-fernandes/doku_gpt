from __future__ import annotations

from doku_gpt.validator.path.path_is_valid_for_namespace_validator import PathIsValidForNamespaceValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPathIsValidForNamespaceValidator(AbstractFakeDokuTest):
    def test_is_folder_valid(self):
        self.assertEqual(self.folder_valid, PathIsValidForNamespaceValidator.validate(self.folder_valid))

    def test_is_file_valid(self):
        self.assertEqual(self.file_valid, PathIsValidForNamespaceValidator.validate(self.file_valid.with_suffix("")))
