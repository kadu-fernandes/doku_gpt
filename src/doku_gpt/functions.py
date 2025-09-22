from __future__ import annotations

import sys
from pprint import pprint
from typing import NoReturn


@staticmethod
def dump(object) -> None:
    print("\n\n")
    pprint(object=object, indent=4)
    print("\n\n")


@staticmethod
def dump_die(object) -> NoReturn:
    dump(object)
    sys.exit(1)
