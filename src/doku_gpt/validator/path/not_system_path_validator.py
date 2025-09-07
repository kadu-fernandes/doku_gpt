from __future__ import annotations

import os
from pathlib import Path

from doku_gpt.validator.path.abstract_path_validator import AbstractPathValidator


class NotSystemPathValidator(AbstractPathValidator):

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

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = NotSystemPathValidator._normalize_path(path)
        if path == Path("/"):
            NotSystemPathValidator._raise_error(path=path, suffix="is not allowed!")

        for forbidden in NotSystemPathValidator.__SYSTEM_PATHS:
            if str(path).startswith(forbidden + os.sep) or str(path) == forbidden:
                NotSystemPathValidator._raise_error(
                    path=path, suffix="is a system path and is not allowed!"
                )

        return path
