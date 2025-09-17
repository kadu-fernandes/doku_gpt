from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class PathIsNotSystemPathValidator(AbstractPathValidator):
    __SYSTEM_PATHS = {
        "/bin",
        "/boot",
        "/dev",
        "/etc",
        "/home",
        "/lib",
        "/lib64",
        "/media",
        "/mnt",
        "/opt",
        "/proc",
        "/root",
        "/run",
        "/sbin",
        "/srv",
        "/sys",
        "/usr",
        "/var",
    }

    @classmethod
    def validate(cls, path: str | Path) -> Path:
        path = cls._normalize_path(path)
        if path == Path("/"):
            cls._raise_error(path=path, suffix="is not allowed!")

        for forbidden in cls.__SYSTEM_PATHS:
            if str(path).startswith(forbidden + os.sep) or str(path) == forbidden:
                cls._raise_error(path=path, suffix="is a system path and is not allowed!")

        return path
