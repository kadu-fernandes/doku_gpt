from __future__ import annotations

import unittest
from pathlib import Path

from doku_gpt.adapter.page_adapter import PageAdapter
from doku_gpt.extractor.doku_page_extractor import DokuPageExtractor


class TestDokuPageExtractor(unittest.TestCase):
    def test_can_fetch_valid(self) -> None:
        page_path = self.__test_path()
        self.assertTrue(DokuPageExtractor.can_fetch(page_path))

    def test_extract_title_no_fragmente(self) -> None:
        page_path = self.__test_path()
        self.assertEqual(
            "A Origem das Raças e os Conflitos Antigos",
            DokuPageExtractor.extract_title(page_path),
        )

    def test_fragment_full_slug_of_main_header(self) -> None:
        page_path = self.__test_path()
        fragment = "a-origem-das-racas-e-os-conflitos-antigos"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("A Origem das Raças e os Conflitos Antigos", extracted)

    def test_fragment_with_hash_and_deaccent_intro(self) -> None:
        page_path = self.__test_path()
        fragment = "#introducao"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("Introdução", extracted)

    def test_fragment_subsequence_parte_1(self) -> None:
        page_path = self.__test_path()
        fragment = "parte-1"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("Coração de Pedra (Parte 1)", extracted)

    def test_fragment_hyphen_and_deaccent_veroes(self) -> None:
        page_path = self.__test_path()
        fragment = "ritos-de-inverno-e-veroes"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("Ritos-de-inverno e verões", extracted)

    def test_fragment_underscore_variant(self) -> None:
        page_path = self.__test_path()
        fragment = "linha_do_tempo"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("Linha_do_tempo", extracted)

    def test_fragment_number_normalization(self) -> None:
        page_path = self.__test_path()
        fragment = "coracao-de-pedra-001"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("Coração de Pedra #001", extracted)

    def test_fragment_cjk_with_romanized_parentheses(self) -> None:
        page_path = self.__test_path()
        fragment = "neko-no-shinwa"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertEqual("猫の神话 (Neko no shinwa)", extracted)

    def test_fragment_wrong_order_returns_none(self) -> None:
        page_path = self.__test_path()
        fragment = "metodologicas-notas"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertIsNone(extracted)

    def test_fragment_unknown_returns_none(self) -> None:
        page_path = self.__test_path()
        fragment = "this-fragment-does-not-exist"
        extracted = DokuPageExtractor.extract_title(page_path, fragment)
        self.assertIsNone(extracted)

    def test_extract_excerpt_without_fragment_uses_first_section_only(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path)
        self.assertEqual(
            "Este documento descreve, de forma resumida, várias tradições e conflitos antigos.",
            excerpt,
        )

    def test_extract_excerpt_fragment_intro_deaccent_with_hash(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "#introducao")
        self.assertEqual(
            "Aqui vai um parágrafo introdutório. Fragmentos típicos: #introducao, #a-origem-das-racas-e-os-conflitos-antigos.",
            excerpt,
        )

    def test_extract_excerpt_fragment_parte_1_subsequence(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "parte-1")
        self.assertEqual(
            "Sequência relacionada, mesma família de títulos mas sem marcador #001.",
            excerpt,
        )

    def test_extract_excerpt_fragment_number_normalization(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "coracao-de-pedra-001")
        self.assertEqual(
            "Texto relativo à crônica “Coração de Pedra”, primeira entrada numerada.",
            excerpt,
        )

    def test_extract_excerpt_fragment_em_dash_notas_metodologicas(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "notas-metodologicas")
        self.assertEqual(
            "Aqui usamos em dash (—) em vez de hífen, para testar normalização.",
            excerpt,
        )

    def test_extract_excerpt_fragment_cjk_with_romanized_parentheses(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "neko-no-shinwa")
        self.assertEqual(
            "Seção com CJK + transliteração/romanização no parêntesis.",
            excerpt,
        )

    def test_extract_excerpt_fragment_underscore_section_with_empty_body(self) -> None:
        page_path = self.__test_path()
        excerpt = DokuPageExtractor.extract_excerpt(page_path, "linha_do_tempo")
        self.assertEqual("Este título usa underscores.", excerpt)

    def __test_path(self) -> Path:
        path = Path("/tmp/doku_page_extractor.txt")
        adapter = PageAdapter(path)
        adapter.content = """
====== A Origem das Raças e os Conflitos Antigos ======

Este documento descreve, de forma resumida, várias tradições e conflitos antigos.

===== Introdução =====
Aqui vai um parágrafo introdutório. Fragmentos típicos: #introducao, #a-origem-das-racas-e-os-conflitos-antigos.

==== Coração de Pedra #001 ====
Texto relativo à crônica “Coração de Pedra”, primeira entrada numerada.

==== Coração de Pedra (Parte 1) ====
Sequência relacionada, mesma família de títulos mas sem marcador #001.

==== A. B: C — Tradição oral ====
Os sinais “.” e “:” aparecem aqui; também um em dash (—).

=== Ritos-de-inverno e verões ===
Título com hífen simples, e com acento em “verões”.

=== Notas—metodológicas ===
Aqui usamos em dash (—) em vez de hífen, para testar normalização.

== Linha_do_tempo ==
Este título usa underscores.

==== Parte 001: Fundos ====
Comparação de números: “001” deve casar com fragmentos que usem “1” ou “001”.

==== 猫の神话 (Neko no shinwa) ====
Seção com CJK + transliteração/romanização no parêntesis.

= Apêndice: Tabelas =
Assumimos que “= título =” é nível 6 para efeitos de teste.

            """
        return path

    def tearDown(self) -> None:
        path = Path("/tmp/doku_page_extractor.txt")
        if path.exists():
            path.unlink(missing_ok=True)
