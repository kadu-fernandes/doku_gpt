from doku_gpt.error.invalid_namespace_error import InvalidNamespaceError
from doku_gpt.resolver.namespace.prior_namespace_resolver import PriorNamespaceResolver
from tests.doku_gpt.abstract_fake_doku_test import AbstractFakeDokuTest


class TestPriorNamespaceResolver(AbstractFakeDokuTest):

    def test_explicit_prior_namespace_valid(self):
        validator = PriorNamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        self.assertEqual(":one:end", validator.resolve("..:one:end"))

    def test_explicit_prior_namespace_invalid(self):

        validator = PriorNamespaceResolver(root_folder=self.tmp_root, context=self.tmp_root.joinpath("two/start"))

        with self.assertRaises(InvalidNamespaceError) as context:
            validator.resolve("..:three:does_not_exist")

        self.assertEqual(
            "The given namespace '..:three:does_not_exist' does not exist!",
            str(context.exception),
        )
