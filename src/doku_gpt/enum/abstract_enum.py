from __future__ import annotations

from enum import Enum


class AbstractEnum(str, Enum):
    @classmethod
    def all(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    def validate(cls, value: str) -> str:
        normalized_value = value.strip().lower().lstrip(".")
        if normalized_value not in cls.all():
            raise ValueError(f"{value} is not valid {cls.__name__}!")
        return normalized_value
