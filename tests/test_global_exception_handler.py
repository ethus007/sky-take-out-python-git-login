# 对应 Java: GlobalExceptionHandlerTest
from sky.constant.message_constant import MessageConstant
from sky.exception.account_locked_exception import AccountLockedException
from sky.exception.account_not_found_exception import AccountNotFoundException
from sky.exception.duplicate_entry_exception import DuplicateEntryException
from sky.exception.password_error_exception import PasswordErrorException
from sky.handler.global_exception_handler import GlobalExceptionHandler


def test_account_not_found_becomes_result_error():
    handler = GlobalExceptionHandler()
    result = handler.exceptionHandler(
        AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND)
    )
    assert result.code == 0
    assert result.msg == MessageConstant.ACCOUNT_NOT_FOUND


def test_password_error_becomes_result_error():
    handler = GlobalExceptionHandler()
    result = handler.exceptionHandler(PasswordErrorException(MessageConstant.PASSWORD_ERROR))
    assert result.code == 0
    assert result.msg == MessageConstant.PASSWORD_ERROR


def test_account_locked_becomes_result_error():
    handler = GlobalExceptionHandler()
    result = handler.exceptionHandler(AccountLockedException(MessageConstant.ACCOUNT_LOCKED))
    assert result.code == 0
    assert result.msg == MessageConstant.ACCOUNT_LOCKED


def test_duplicate_username_becomes_already_exists():
    handler = GlobalExceptionHandler()
    ex = DuplicateEntryException("Duplicate entry 'zhangsan' for key 'employee.idx_username'")
    result = handler.exceptionHandler(ex)
    assert result.code == 0
    assert result.msg == "'zhangsan'已存在"
