# 对应 Java: com.sky.result.Result
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    code: int | None = None
    msg: str | None = None
    data: T | None = None

    @staticmethod
    def success(obj: Any = None) -> Result:
        result: Result = Result()
        result.code = 1
        if obj is not None:
            result.data = obj
        return result

    @staticmethod
    def error(msg: str) -> Result:
        result = Result()
        result.msg = msg
        result.code = 0
        return result
