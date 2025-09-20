from __future__ import annotations

import re

from doku_gpt.error.invalid_interwiki_error import InvalidInterwikiError


class InterwikiMapRegistry:
    __INTERWIKI_DEFAULTS: dict[str, str] = {
        "amazon": "https://www.amazon.com/dp/{to_replace}?tag=splitbrain-20",
        "amazon.de": "https://www.amazon.de/dp/{to_replace}?tag=splitbrain-21",
        "amazon.uk": "https://www.amazon.co.uk/dp/{to_replace}",
        "callto": "callto://{to_replace}",
        "go": "https://www.google.com/search?q={to_replace}&btnI=lucky",
        "google": "https://www.google.com/search?q={to_replace}",
        "google.de": "https://www.google.de/search?q={to_replace}",
        "imdb": "https://www.imdb.com/title/{to_replace}",
        "phpfn": "https://www.php.net/{to_replace}",
        "spotify": "https://open.spotify.com/track/{to_replace}",
        "sptf": "https://open.spotify.com/track/{to_replace}",
        "wp": "https://en.wikipedia.org/wiki/{to_replace}",
        "wpde": "https://de.wikipedia.org/wiki/{to_replace}",
        "wpes": "https://es.wikipedia.org/wiki/{to_replace}",
        "wpfr": "https://fr.wikipedia.org/wiki/{to_replace}",
        "wpjp": "https://ja.wikipedia.org/wiki/{to_replace}",
        "wpmeta": "https://meta.wikipedia.org/wiki/{to_replace}",
        "wppl": "https://pl.wikipedia.org/wiki/{to_replace}",
        "wppt": "https://pt.wikipedia.org/wiki/{to_replace}",
        "wpru": "https://ru.wikipedia.org/wiki/{to_replace}",
        "youtube": "https://youtu.be/{to_replace}",
    }

    @classmethod
    def get_map(cls) -> dict[str, str]:
        """
        Return a copy of the default interwiki map.
        Keys are interwiki prefixes (e.g. "wp", "imdb") and values are URL templates.
        This prevents accidental modification of the internal defaults.
        """
        return dict(cls.__INTERWIKI_DEFAULTS)

    @classmethod
    def exists(cls, interwiki: str) -> bool:
        """
        Check if a given interwiki prefix exists in the defaults.
        The prefix is stripped and lowercased before lookup.
        Returns True if the prefix is recognized, otherwise False.
        """
        interwiki_normalized = interwiki.strip().lower()
        return interwiki_normalized in cls.__INTERWIKI_DEFAULTS

    @classmethod
    def get(cls, interwiki: str, interwiki_id: str | None) -> str:
        """
        Resolve an interwiki prefix and optional identifier into a full URL.

        - If the prefix does not exist, raises InvalidInterwikiError.
        - If the template contains "{to_replace}" and no identifier is provided,
          raises InvalidInterwikiError.
        - The identifier is URL-encoded before being inserted into the template.
          (quote for path segments, quote_plus for query parameters.)
        - If the template has no "{to_replace}" placeholder, the raw template is returned.
        """
        interwiki_normalized = interwiki.strip().lower()

        if not cls.exists(interwiki_normalized):
            raise InvalidInterwikiError(f"The interwiki '{interwiki}' does not exist!")

        found = cls.__INTERWIKI_DEFAULTS[interwiki_normalized]

        if "{to_replace}" not in found:
            return found

        if interwiki_id is None or "" == interwiki_id:
            raise InvalidInterwikiError(f"The interwiki '{interwiki}' requires an id to replace.")

        return found.replace("{to_replace}", interwiki_id)

    @classmethod
    def get_by_target(cls, target: str) -> str:
        """
        Resolve a full target string like "wp>Python_(programming_language)" into a URL.

        - Splits the target into prefix and identifier via LinkTagHelper.split_interwiki().
        - Delegates to get() for resolution and validation.
        - Raises InvalidInterwikiError if the prefix does not exist or the identifier is missing
          when required.
        """
        interwiki, interwiki_id = cls.split_interwiki(target)
        return cls.get(interwiki, interwiki_id)

    @classmethod
    def split_interwiki(cls, target: str) -> tuple[str, str]:
        match = re.fullmatch(r"^([^>]+)>([^>]+)$", target.strip())
        if not match:
            raise InvalidInterwikiError(f"The given target '{target}' is not an interlink!")
        prefix, interwiki_id = match.groups()
        return prefix, interwiki_id
