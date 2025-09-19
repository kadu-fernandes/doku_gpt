from __future__ import annotations

import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from doku_gpt.extractor.normalizer.imdb_title_normalizer import ImdbTitleNormalizer
from doku_gpt.extractor.normalizer.wikipedia_title_normalizer import WikipediaTitleNormalizer


class WebPageExtractor:
    __HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    }

    @classmethod
    def can_fetch(cls, url: str) -> bool:
        scheme = urlparse(url).scheme.lower()
        return scheme in ("http", "https")

    @classmethod
    def url_exists(cls, url: str) -> bool:
        if not WebPageExtractor.can_fetch(url):
            return True

        try:
            status_code = cls.__head(url).status_code < 400
            return status_code
        except requests.RequestException:
            return False

    @classmethod
    def __handle_og_title(cls, soup: BeautifulSoup, property: str) -> str | None:
        og_title = soup.find("meta", attrs={"property": property})
        if not isinstance(og_title, Tag):
            return None

        value = str(og_title.get("content") or "").strip()
        if value != "":
            return WebPageExtractor.__clean(value)

        return None

    @classmethod
    def __handle_title(cls, soup: BeautifulSoup) -> str | None:
        title = soup.find(attrs={"property": "title"})
        if not isinstance(title, Tag):
            return None

        value = str(title.get("content") or "").strip()
        if value != "":
            return WebPageExtractor.__clean(value)

        return None

    @classmethod
    def extract_title(cls, url: str) -> str | None:
        if not WebPageExtractor.can_fetch(url):
            return None

        try:
            soup = WebPageExtractor.__fetch(url)
        except requests.exceptions.RequestException:
            return None

        og_title = cls.__handle_og_title(soup=soup, property="og:title")
        if og_title is not None:
            return og_title

        og_title = cls.__handle_og_title(soup=soup, property="twitter:title")
        if og_title is not None:
            return og_title

        return cls.__handle_title(soup=soup)

    @classmethod
    def __head(cls, url: str):
        return requests.head(url=url.strip(), headers=cls.__HEADERS, allow_redirects=True, timeout=5)

    @classmethod
    def __fetch(cls, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=cls.__HEADERS, timeout=10.0)
        response.raise_for_status()
        return BeautifulSoup(response.text or "", "html.parser")

    @classmethod
    def __clean(cls, value: str) -> str | None:
        normalized_spaces_value = re.sub(r"\s+", " ", value).strip()
        if normalized_spaces_value:
            normalized_value = WikipediaTitleNormalizer.normalize(normalized_spaces_value)
            normalized_value = ImdbTitleNormalizer.normalize(normalized_value)
            return normalized_value or None
        return None
