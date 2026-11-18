# 对应 Java: com.sky.interceptor.JwtTokenAdminInterceptor
from sky.constant.jwt_claims_constant import JwtClaimsConstant
from sky.context.base_context import BaseContext
from sky.properties.jwt_properties import JwtProperties
from sky.utils.jwt_util import JwtUtil


class HandlerMethod:
    """对应 Spring 的 HandlerMethod：只有落到 Controller 方法才验 JWT。"""


class SimpleResponse:
    def __init__(self) -> None:
        self.status = 200

    def setStatus(self, status: int) -> None:
        self.status = status

    def getStatus(self) -> int:
        return self.status


class JwtTokenAdminInterceptor:
    def __init__(self, jwtProperties: JwtProperties | None = None):
        self.jwtProperties = jwtProperties or JwtProperties()

    def preHandle(self, request_headers: dict, response: SimpleResponse, handler) -> bool:
        if not isinstance(handler, HandlerMethod):
            return True

        token = request_headers.get(self.jwtProperties.adminTokenName)
        try:
            claims = JwtUtil.parseJWT(self.jwtProperties.adminSecretKey, token)
            emp_id = int(claims[JwtClaimsConstant.EMP_ID])
            BaseContext.setCurrentId(emp_id)
            return True
        except Exception:
            response.setStatus(401)
            return False
