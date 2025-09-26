from __future__ import annotations

import unittest

from doku_gpt.sanitizer.doku.line.image_sanitizer import ImageSanitizer


class TestDeletedSanitizer(unittest.TestCase):
    def test_sanitize(self) -> None:
        images: tuple[str, ...] = (
            "This {{ns:img.png}} was an image!",
            "This {{ ns:img.jpg?200x50&nolink }} was an image!",
            "This {{ https://host/path/img.gif?200x50 }} was an image!",
            "This {{ ns:img.webp |Caption}} was an image!",
            "This {{ :old:foo.jpg?direct&400| }} was an image!",
        )
        for image in images:
            self.assertEqual("This was an image!", ImageSanitizer.sanitize(image))
