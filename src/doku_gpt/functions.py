from __future__ import annotations

import re
import sys
from pprint import pprint
from typing import List, NoReturn


@staticmethod
def dump(object) -> None:
    print("\n\n")
    pprint(object=object, indent=4)
    print("\n\n")


@staticmethod
def dump_die(object) -> NoReturn:
    dump(object)
    sys.exit(1)


@staticmethod
def extract_link_tags(line: str) -> List[str]:
    """Return all link_tags-like paths found inside [[...]] on this line."""
    compiled = re.compile(r"(?P<token>\[\[(?P<path>[^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]*)?\]\])")
    return [path.strip() for path, _ in compiled.findall(line)]
