# 对应 Java: com.sky.config.WebMvcConfiguration + SkyApplication
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sky.controller.admin.employee_controller import EmployeeController
from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.exception.base_exception import BaseException
from sky.exception.duplicate_entry_exception import DuplicateEntryException
from sky.handler.global_exception_handler import GlobalExceptionHandler
from sky.interceptor.jwt_token_admin_interceptor import (
    HandlerMethod,
    JwtTokenAdminInterceptor,
    SimpleResponse,
)
from sky.mapper.memory_employee_mapper import MemoryEmployeeMapper
from sky.properties.jwt_properties import JwtProperties
from sky.service.impl.employee_service_impl import EmployeeServiceImpl
from sky.utils.json_util import to_jsonable

LOGIN_PATH = "/admin/employee/login"
SKIP_PREFIXES = ("/docs", "/redoc", "/openapi.json")


def create_app(
    employee_service=None,
    jwt_properties: JwtProperties | None = None,
    enable_jwt: bool = True,
) -> FastAPI:
    jwt_properties = jwt_properties or JwtProperties()
    if employee_service is None:
        employee_service = EmployeeServiceImpl(MemoryEmployeeMapper())
    controller = EmployeeController(employee_service, jwt_properties)
    interceptor = JwtTokenAdminInterceptor(jwt_properties)
    handler = GlobalExceptionHandler()

    app = FastAPI(title="苍穹外卖-员工管理接口文档", version="2.0")
    app.state.employee_controller = controller
    app.state.jwt_properties = jwt_properties

    def result_response(result, status_code: int = 200) -> JSONResponse:
        return JSONResponse(status_code=status_code, content=to_jsonable(result))

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        if not enable_jwt:
            return await call_next(request)
        path = request.url.path
        if path == LOGIN_PATH or path.startswith(SKIP_PREFIXES):
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

    @app.post("/admin/employee/login")
    def login(body: dict):
        dto = EmployeeLoginDTO(
            username=body.get("username"),
            password=body.get("password"),
        )
        return result_response(controller.login(dto))

    @app.post("/admin/employee/logout")
    def logout():
        return result_response(controller.logout())

    @app.post("/admin/employee")
    def save(body: dict):
        dto = EmployeeDTO(
            id=body.get("id"),
            username=body.get("username"),
            name=body.get("name"),
            phone=body.get("phone"),
            sex=body.get("sex"),
            idNumber=body.get("idNumber"),
        )
        return result_response(controller.save(dto))

    @app.get("/admin/employee/page")
    def page(name: str | None = None, page: int = 1, pageSize: int = 10):
        dto = EmployeePageQueryDTO(name=name, page=page, pageSize=pageSize)
        return result_response(controller.page(dto))

    @app.post("/admin/employee/status/{status}")
    def start_or_stop(status: int, id: int):
        return result_response(controller.startOrStop(status, id))

    @app.get("/admin/employee/{id}")
    def get_by_id(id: int):
        return result_response(controller.getById(id))

    @app.put("/admin/employee")
    def update(body: dict):
        dto = EmployeeDTO(
            id=body.get("id"),
            username=body.get("username"),
            name=body.get("name"),
            phone=body.get("phone"),
            sex=body.get("sex"),
            idNumber=body.get("idNumber"),
        )
        return result_response(controller.update(dto))

    return app
