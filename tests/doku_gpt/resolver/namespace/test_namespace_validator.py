from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.namespace_resolver import NamespaceResolver
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestNamespaceResolver(AbstractFakeDokuTest):

    def test_explicit_absolute_namespace_valid(self):
        validator = NamespaceResolver(self.tmp_root)

        self.assertEqual(":two:three:end", validator.resolve(":two:three:end"))

    def test_explicit_absolute_namespace_invalid(self):

        validator = NamespaceResolver(self.tmp_root)
        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve(":two:three:does_not_exist")

        self.assertEqual(
            "The given namespace 'two:three:does_not_exist' does not exist!",
            str(context.exception),
        )

    def test_implicit_absolute_namespace_valid(self):
        validator = NamespaceResolver(self.tmp_root)

        self.assertEqual(":two:three:end", validator.resolve("two:three:end"))

    def test_implicit_absolute_namespace_invalid(self):
        validator = NamespaceResolver(self.tmp_root)
        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve(":two:three:does_not_exist")

        self.assertEqual(
            "The given namespace 'two:three:does_not_exist' does not exist!",
            str(context.exception),
        )

    def test_explicit_prior_namespace_valid(self):
        validator = NamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        self.assertEqual(":one:end", validator.resolve("..:one:end"))

    def test_explicit_prior_namespace_invalid(self):

        validator = NamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve("..:three:does_not_exist")

        self.assertEqual(
            "The given namespace '..:three:does_not_exist' does not exist!",
            str(context.exception),
        )

    def test_explicit_relative_namespace_valid_tilde(self):
        validator = NamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        self.assertEqual(":two:three:end", validator.resolve("~three:end"))

    def test_explicit_relative_namespace_invalid(self):

        validator = NamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve("~:does_not_exist")

        self.assertEqual(
            "The given namespace ':two:does_not_exist' does not exist!",
            str(context.exception),
        )
