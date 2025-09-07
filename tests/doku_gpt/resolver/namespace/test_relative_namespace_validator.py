from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.relative_namespace_resolver import RelativeNamespaceResolver
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestRelativeNamespaceResolver(AbstractFakeDokuTest):

    def test_explicit_relative_namespace_valid_tilde(self):
        validator = RelativeNamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        self.assertEqual(":two:three:end", validator.resolve("~three:end"))

    def test_explicit_relative_namespace_invalid(self):

        validator = RelativeNamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve("~:does_not_exist")

        self.assertEqual(
            "The given namespace ':two:does_not_exist' does not exist!",
            str(context.exception),
        )
