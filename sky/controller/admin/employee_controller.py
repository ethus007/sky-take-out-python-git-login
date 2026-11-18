# 对应 Java: com.sky.controller.admin.EmployeeController
from sky.constant.jwt_claims_constant import JwtClaimsConstant
from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.properties.jwt_properties import JwtProperties
from sky.result.result import Result
from sky.service.employee_service import EmployeeService
from sky.utils.jwt_util import JwtUtil
from sky.vo.employee_login_vo import EmployeeLoginVO


class EmployeeController:
    def __init__(self, employeeService: EmployeeService, jwtProperties: JwtProperties):
        self.employeeService = employeeService
        self.jwtProperties = jwtProperties

    def login(self, employeeLoginDTO: EmployeeLoginDTO) -> Result:
        employee = self.employeeService.login(employeeLoginDTO)
        claims = {JwtClaimsConstant.EMP_ID: employee.id}
        token = JwtUtil.createJWT(
            self.jwtProperties.adminSecretKey,
            self.jwtProperties.adminTtl,
            claims,
        )
        employeeLoginVO = EmployeeLoginVO.builder(
            id=employee.id,
            userName=employee.username,
            name=employee.name,
            token=token,
        )
        return Result.success(employeeLoginVO)

    def logout(self) -> Result:
        return Result.success()

    def save(self, employeeDTO: EmployeeDTO) -> Result:
        self.employeeService.save(employeeDTO)
        return Result.success()

    def page(self, employeePageQueryDTO: EmployeePageQueryDTO) -> Result:
        pageResult = self.employeeService.pageQuery(employeePageQueryDTO)
        return Result.success(pageResult)

    def startOrStop(self, status: int, id: int) -> Result:
        self.employeeService.startOrStop(status, id)
        return Result.success()

    def getById(self, id: int) -> Result:
        employee = self.employeeService.getById(id)
        return Result.success(employee)

    def update(self, employeeDTO: EmployeeDTO) -> Result:
        self.employeeService.update(employeeDTO)
        return Result.success()
