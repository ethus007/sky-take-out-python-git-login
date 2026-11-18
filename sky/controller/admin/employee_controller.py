# 对应 Java: com.sky.controller.admin.EmployeeController
from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.properties.jwt_properties import JwtProperties
from sky.result.result import Result
from sky.service.employee_service import EmployeeService


class EmployeeController:
    def __init__(self, employeeService: EmployeeService, jwtProperties: JwtProperties):
        self.employeeService = employeeService
        self.jwtProperties = jwtProperties

    def login(self, employeeLoginDTO: EmployeeLoginDTO) -> Result:
        raise NotImplementedError("员工登录接口尚未实现")

    def logout(self) -> Result:
        raise NotImplementedError("退出接口尚未实现")

    def save(self, employeeDTO: EmployeeDTO) -> Result:
        raise NotImplementedError("新增员工接口尚未实现")

    def page(self, employeePageQueryDTO: EmployeePageQueryDTO) -> Result:
        raise NotImplementedError("员工分页接口尚未实现")

    def startOrStop(self, status: int, id: int) -> Result:
        raise NotImplementedError("启用/禁用接口尚未实现")

    def getById(self, id: int) -> Result:
        raise NotImplementedError("按 id 查询接口尚未实现")

    def update(self, employeeDTO: EmployeeDTO) -> Result:
        raise NotImplementedError("编辑员工接口尚未实现")
