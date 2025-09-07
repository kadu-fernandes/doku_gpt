import sys
from pprint import pprint


class DebugHelper:

    @staticmethod
    def dump(to_dump) -> None:
        print("\n\n")
        pprint(object=to_dump, indent=4)
        print("\n\n")

    @staticmethod
    def dump_die(to_dump) -> None:
        DebugHelper.dump(to_dump)
        sys.exit(1)
