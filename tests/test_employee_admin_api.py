# 对应 Java: EmployeeAdminApiTest
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from sky.config.web_mvc_configuration import create_app
from sky.constant.message_constant import MessageConstant
from sky.entity.employee import Employee
from sky.exception.account_locked_exception import AccountLockedException
from sky.exception.account_not_found_exception import AccountNotFoundException
from sky.exception.password_error_exception import PasswordErrorException
from sky.properties.jwt_properties import JwtProperties


@pytest.fixture
def employee_service():
    return Mock()


@pytest.fixture
def client(employee_service):
    jwt = JwtProperties(
        adminSecretKey="test-admin-secret",
        adminTtl=7_200_000,
        adminTokenName="token",
    )
    app = create_app(employee_service=employee_service, jwt_properties=jwt, enable_jwt=False)
    return TestClient(app)


def test_login_success_returns_token_in_result(client, employee_service):
    employee_service.login.return_value = Employee.builder(
        id=1, username="admin", name="管理员"
    )
    resp = client.post(
        "/admin/employee/login",
        json={"username": "admin", "password": "123456"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == 1
    assert body["data"]["id"] == 1
    assert body["data"]["userName"] == "admin"
    assert body["data"]["token"] is not None


@pytest.mark.parametrize("msg", ["账号不存在", "密码错误", "账号被锁定"])
def test_login_fail_returns_business_error(client, employee_service, msg):
    if msg == MessageConstant.ACCOUNT_NOT_FOUND:
        employee_service.login.side_effect = AccountNotFoundException(msg)
    elif msg == MessageConstant.PASSWORD_ERROR:
        employee_service.login.side_effect = PasswordErrorException(msg)
    else:
        employee_service.login.side_effect = AccountLockedException(msg)

    resp = client.post(
        "/admin/employee/login",
        json={"username": "admin", "password": "x"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == 0
    assert body["msg"] == msg
