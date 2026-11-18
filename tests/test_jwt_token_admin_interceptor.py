# 对应 Java: JwtTokenAdminInterceptorTest
from sky.interceptor.jwt_token_admin_interceptor import (
    HandlerMethod,
    JwtTokenAdminInterceptor,
    SimpleResponse,
)
from sky.properties.jwt_properties import JwtProperties


def interceptor() -> JwtTokenAdminInterceptor:
    jwt = JwtProperties(adminSecretKey="test-admin-secret", adminTokenName="token")
    return JwtTokenAdminInterceptor(jwt)


def test_missing_or_invalid_token_returns_401():
    it = interceptor()
    handler = HandlerMethod()
    response = SimpleResponse()
    assert it.preHandle({}, response, handler) is False
    assert response.getStatus() == 401

    response = SimpleResponse()
    assert it.preHandle({"token": "not-a-jwt"}, response, handler) is False
    assert response.getStatus() == 401


def test_static_resource_is_skipped():
    it = interceptor()
    response = SimpleResponse()
    assert it.preHandle({}, response, object()) is True
    assert response.getStatus() == 200
