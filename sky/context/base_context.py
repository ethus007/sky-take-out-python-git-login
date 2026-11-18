# 对应 Java: com.sky.context.BaseContext（ThreadLocal → contextvars）
from contextvars import ContextVar


class BaseContext:
    _current_id: ContextVar[int | None] = ContextVar("current_id", default=None)

    @classmethod
    def setCurrentId(cls, id: int | None) -> None:
        cls._current_id.set(id)

    @classmethod
    def getCurrentId(cls) -> int | None:
        return cls._current_id.get()

    @classmethod
    def removeCurrentId(cls) -> None:
        cls._current_id.set(None)
