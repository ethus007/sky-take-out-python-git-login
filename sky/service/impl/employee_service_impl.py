# 对应 Java: com.sky.service.impl.EmployeeServiceImpl
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
from sky.mapper.employee_mapper import EmployeeMapper
from sky.result.page_result import PageResult
from sky.utils.json_util import md5_hex


class EmployeeServiceImpl:
    """对应 Java 的 EmployeeServiceImpl：员工登录/增删改查的业务实现（不是 HTTP 入口）。"""

    def __init__(self, employeeMapper: EmployeeMapper):
        # 对应 Java @Autowired EmployeeMapper：查库的对象，测试时换成 Mock
        self.employeeMapper = employeeMapper

    def login(self, employeeLoginDTO: EmployeeLoginDTO) -> Employee:
        """员工登录。入参是前端 JSON 反序列化后的 DTO（username + password）。"""
        username = employeeLoginDTO.username  # 从 DTO 取出用户名
        password = employeeLoginDTO.password  # 从 DTO 取出前端传来的明文密码

        # 1、根据用户名查询数据库中的数据
        employee = self.employeeMapper.getByUsername(username)  # 没有这条记录就返回 None

        # 2、处理各种异常情况（用户名不存在、密码不对、账号被锁定）
        if employee is None:  # 库里查不到这个用户名
            # 账号不存在。抛业务异常，不在这里 return，交给 GlobalExceptionHandler 打成 Result.error
            raise AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND)

        # 密码比对：明文 → MD5 十六进制，和库里存的 password 哈希对齐
        password = md5_hex(password or "")
        if password != employee.password:  # 刚算出的哈希 ≠ 表里的 password
            raise PasswordErrorException(MessageConstant.PASSWORD_ERROR)

        if employee.status == StatusConstant.DISABLE:  # 禁用常量 0（ENABLE 是 1）
            # 账号被禁用，不允许登录
            raise AccountLockedException(MessageConstant.ACCOUNT_LOCKED)

        # 3、三关都过：把 Employee 对象交回 Controller，后面用它发 JWT
        return employee

    def save(self, employeeDTO: EmployeeDTO) -> None:
        employee = Employee()
        employee.copy_from(employeeDTO)
        employee.status = StatusConstant.ENABLE
        employee.password = md5_hex(PasswordConstant.DEFAULT_PASSWORD)
        self.employeeMapper.insert(employee)

    def pageQuery(self, employeePageQueryDTO: EmployeePageQueryDTO) -> PageResult:
        page = self.employeeMapper.pageQuery(employeePageQueryDTO)
        return PageResult(total=page.getTotal(), records=page.getResult())

    def startOrStop(self, status: int, id: int) -> None:
        employee = Employee.builder(status=status, id=id)
        self.employeeMapper.update(employee)

    def getById(self, id: int) -> Employee:
        employee = self.employeeMapper.getById(id)
        employee.password = "****"
        return employee

    def update(self, employeeDTO: EmployeeDTO) -> None:
        employee = Employee()
        employee.copy_from(employeeDTO)
        self.employeeMapper.update(employee)
