# 对应 Java: com.sky.config.WebMvcConfiguration + SkyApplication
# base：应用能启动，JWT 拦截和全局异常在；员工 HTTP 路由尚未挂上。
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sky.exception.base_exception import BaseException
from sky.exception.duplicate_entry_exception import DuplicateEntryException
from sky.handler.global_exception_handler import GlobalExceptionHandler
from sky.interceptor.jwt_token_admin_interceptor import (
    HandlerMethod,
    JwtTokenAdminInterceptor,
    SimpleResponse,
)
from sky.properties.jwt_properties import JwtProperties
from sky.utils.json_util import to_jsonable

SKIP_PREFIXES = ("/docs", "/redoc", "/openapi.json")


def create_app(
    employee_service=None,
    jwt_properties: JwtProperties | None = None,
    enable_jwt: bool = True,
) -> FastAPI:
    jwt_properties = jwt_properties or JwtProperties()
    interceptor = JwtTokenAdminInterceptor(jwt_properties)
    handler = GlobalExceptionHandler()

    app = FastAPI(title="苍穹外卖-员工管理接口文档", version="2.0")
    app.state.jwt_properties = jwt_properties

    def result_response(result, status_code: int = 200) -> JSONResponse:
        return JSONResponse(status_code=status_code, content=to_jsonable(result))

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        if not enable_jwt:
            return await call_next(request)
        path = request.url.path
        if path.startswith(SKIP_PREFIXES):
            return await call_next(request)
        if not path.startswith("/admin"):
            return await call_next(request)
        response = SimpleResponse()
        headers = {k: v for k, v in request.headers.items()}
        ok = interceptor.preHandle(headers, response, HandlerMethod())
        if not ok:
            return JSONResponse(status_code=response.getStatus(), content={"code": 0, "msg": "未登录"})
        return await call_next(request)

    @app.exception_handler(BaseException)
    async def base_exception_handler(_, exc: BaseException):
        return result_response(handler.exceptionHandler(exc))

    @app.exception_handler(DuplicateEntryException)
    async def duplicate_handler(_, exc: DuplicateEntryException):
        return result_response(handler.exceptionHandler(exc))

    return app
