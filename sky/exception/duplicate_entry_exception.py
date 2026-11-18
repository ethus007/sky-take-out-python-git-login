# 对应 Java: java.sql.SQLIntegrityConstraintViolationException（用户名唯一索引冲突）


class DuplicateEntryException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.msg = message

    def getMessage(self) -> str:
        return self.msg
