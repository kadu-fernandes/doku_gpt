from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.absolute_namespace_resolver import AbsoluteNamespaceResolver
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestAbsoluteNamespaceResolver(AbstractFakeDokuTest):

    def test_explicit_absolute_namespace_valid(self):
        validator = AbsoluteNamespaceResolver(self.tmp_root)

        self.assertEqual(":two:three:end", validator.resolve(":two:three:end"))

    def test_explicit_absolute_namespace_invalid(self):

        validator = AbsoluteNamespaceResolver(self.tmp_root)
        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve(":two:three:does_not_exist")

        self.assertEqual(
            "The given namespace 'two:three:does_not_exist' does not exist!",
            str(context.exception),
        )

    def test_implicit_absolute_namespace_valid(self):
        validator = AbsoluteNamespaceResolver(self.tmp_root)

        self.assertEqual(":two:three:end", validator.resolve("two:three:end"))

    def test_implicit_absolute_namespace_invalid(self):
        validator = AbsoluteNamespaceResolver(self.tmp_root)
        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve(":two:three:does_not_exist")

        self.assertEqual(
            "The given namespace 'two:three:does_not_exist' does not exist!",
            str(context.exception),
        )
