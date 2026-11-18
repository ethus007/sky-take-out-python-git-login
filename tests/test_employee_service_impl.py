# 对应 Java: EmployeeServiceImplTest
from unittest.mock import Mock

import pytest

from sky.constant.message_constant import MessageConstant
from sky.constant.password_constant import PasswordConstant
from sky.constant.status_constant import StatusConstant
from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.entity.employee import Employee
from sky.exception.account_locked_exception import AccountLockedException
from sky.exception.account_not_found_exception import AccountNotFoundException
from sky.exception.password_error_exception import PasswordErrorException
from sky.mapper.employee_mapper import Page
from sky.service.impl.employee_service_impl import EmployeeServiceImpl
from sky.utils.json_util import md5_hex


def login_dto(username: str, password: str) -> EmployeeLoginDTO:
    return EmployeeLoginDTO(username=username, password=password)


def admin_employee(**kwargs) -> Employee:
    data = dict(
        id=1,
        username="admin",
        name="管理员",
        password=md5_hex("123456"),
        status=StatusConstant.ENABLE,
    )
    data.update(kwargs)
    return Employee.builder(**data)


@pytest.fixture
def mapper():
    return Mock()


@pytest.fixture
def service(mapper):
    return EmployeeServiceImpl(mapper)


@pytest.mark.parametrize(
    "name,dto,mapper_returns,expected_type,expected_msg",
    [
        ("成功", login_dto("admin", "123456"), admin_employee(), None, None),
        (
            "用户名不存在",
            login_dto("ghost", "123456"),
            None,
            AccountNotFoundException,
            MessageConstant.ACCOUNT_NOT_FOUND,
        ),
        (
            "密码错误",
            login_dto("admin", "wrong"),
            admin_employee(),
            PasswordErrorException,
            MessageConstant.PASSWORD_ERROR,
        ),
        (
            "账号禁用",
            login_dto("locked", "123456"),
            admin_employee(id=2, username="locked", status=StatusConstant.DISABLE),
            AccountLockedException,
            MessageConstant.ACCOUNT_LOCKED,
        ),
    ],
)
def test_login_covers_success_and_three_failures(
    service, mapper, name, dto, mapper_returns, expected_type, expected_msg
):
    mapper.getByUsername.return_value = mapper_returns
    if expected_type is None:
        result = service.login(dto)
        assert result.id == 1
        assert result.username == "admin"
        return
    with pytest.raises(expected_type) as exc:
        service.login(dto)
    assert exc.value.getMessage() == expected_msg


def test_disable_employee_then_login_fails_with_locked(service, mapper):
    enabled = admin_employee()
    mapper.getByUsername.return_value = enabled
    service.startOrStop(StatusConstant.DISABLE, 1)
    updated = mapper.update.call_args[0][0]
    assert updated.status == StatusConstant.DISABLE
    enabled.status = StatusConstant.DISABLE
    with pytest.raises(AccountLockedException):
        service.login(login_dto("admin", "123456"))


def test_create_employee_then_get_by_id_masks_password(service, mapper):
    dto = EmployeeDTO(
        username="zhangsan",
        name="张三",
        phone="13800000000",
        sex="1",
        idNumber="110101199001011234",
    )
    service.save(dto)
    inserted = mapper.insert.call_args[0][0]
    assert inserted.status == StatusConstant.ENABLE
    assert inserted.password == md5_hex(PasswordConstant.DEFAULT_PASSWORD)

    mapper.getById.return_value = admin_employee()
    viewed = service.getById(1)
    assert viewed.password == "****"


def test_page_query_and_update_name(service, mapper):
    query = EmployeePageQueryDTO(page=1, pageSize=10)
    page = Page()
    page.add(admin_employee())
    page.setTotal(1)
    mapper.pageQuery.return_value = page

    result = service.pageQuery(query)
    assert result.total == 1

    edit = EmployeeDTO(id=1, name="管理员改名", username="admin")
    service.update(edit)
    updated = mapper.update.call_args[0][0]
    assert updated.name == "管理员改名"
