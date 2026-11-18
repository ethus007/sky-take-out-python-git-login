# 对应 Java: com.sky.exception.BaseException


class BaseException(Exception):
    def __init__(self, msg: str | None = None):
        super().__init__(msg or "")
        self.msg = msg or ""

    def getMessage(self) -> str:
        return self.msg
