# 对应 Java: com.sky.service.impl.EmployeeServiceImpl
from sky.dto.employee_dto import EmployeeDTO
from sky.dto.employee_login_dto import EmployeeLoginDTO
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.entity.employee import Employee
from sky.mapper.employee_mapper import EmployeeMapper
from sky.result.page_result import PageResult


class EmployeeServiceImpl:
    """员工登录/增删改查。base 提交里尚未实现，见 ISSUE.md。"""

    def __init__(self, employeeMapper: EmployeeMapper):
        self.employeeMapper = employeeMapper

    def login(self, employeeLoginDTO: EmployeeLoginDTO) -> Employee:
        raise NotImplementedError("员工登录尚未实现")

    def save(self, employeeDTO: EmployeeDTO) -> None:
        raise NotImplementedError("新增员工尚未实现")

    def pageQuery(self, employeePageQueryDTO: EmployeePageQueryDTO) -> PageResult:
        raise NotImplementedError("员工分页尚未实现")

    def startOrStop(self, status: int, id: int) -> None:
        raise NotImplementedError("启用/禁用员工尚未实现")

    def getById(self, id: int) -> Employee:
        raise NotImplementedError("按 id 查询员工尚未实现")

    def update(self, employeeDTO: EmployeeDTO) -> None:
        raise NotImplementedError("编辑员工尚未实现")
