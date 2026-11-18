# 对应 Java: com.sky.handler.GlobalExceptionHandler
from sky.constant.message_constant import MessageConstant
from sky.exception.base_exception import BaseException
from sky.exception.duplicate_entry_exception import DuplicateEntryException
from sky.result.result import Result


class GlobalExceptionHandler:
    def exceptionHandler(self, ex) -> Result:
        if isinstance(ex, BaseException):
            return Result.error(ex.getMessage())
        if isinstance(ex, DuplicateEntryException):
            message = ex.getMessage()
            if "Duplicate entry" in message:
                username = message.split(" ")[2]
                return Result.error(username + MessageConstant.ALREADY_EXISTS)
            return Result.error(MessageConstant.UNKNOWN_ERROR)
        raise ex
