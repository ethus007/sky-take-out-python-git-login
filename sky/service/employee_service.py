# 对应 Java: com.sky.service.EmployeeService
from typing import Protocol, runtime_checkable

from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.entity.employee import Employee
from sky.result.page_result import PageResult


@runtime_checkable
class EmployeeService(Protocol):
    def login(self, employeeLoginDTO: EmployeeLoginDTO) -> Employee: ...

    def save(self, employeeDTO: EmployeeDTO) -> None: ...

    def pageQuery(self, employeePageQueryDTO: EmployeePageQueryDTO) -> PageResult: ...

    def startOrStop(self, status: int, id: int) -> None: ...

    def getById(self, id: int) -> Employee: ...

    def update(self, employeeDTO: EmployeeDTO) -> None: ...
