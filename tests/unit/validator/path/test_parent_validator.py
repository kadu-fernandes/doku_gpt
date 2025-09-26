from __future__ import annotations

from doku_gpt.validator.path.path_exists_validator import PathExistsValidator
from tests.unit.abstract_fake_doku_test import AbstractFakeDokuTest


class TestParentValidator(AbstractFakeDokuTest):
    def test_is_file_valid(self):
        self.assertEqual(self.folder_valid, PathExistsValidator.validate(self.folder_valid))
