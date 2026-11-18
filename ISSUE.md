# 员工管理（含登录）尚未实现

对应讲义 `苍穹外卖/讲义/day02` 前四条，以及登录前置。

请实现下列接口（`EmployeeController` / `EmployeeServiceImpl`），使 `tests/test_employee_admin_api.py` 与 `tests/test_employee_service_impl.py` 通过。

| 方法 | 路径 | 做什么 |
|---|---|---|
| POST | `/admin/employee/login` | 登录（放行，不校验 JWT）；成功返回 token；失败返回业务错误 msg |
| POST | `/admin/employee/logout` | 退出 |
| POST | `/admin/employee` | 新增员工 |
| GET | `/admin/employee/page` | 分页 |
| POST | `/admin/employee/status/{status}` | 启用/禁用 |
| GET | `/admin/employee/{id}` | 按 id 查（编辑回显，密码脱敏） |
| PUT | `/admin/employee` | 编辑 |

登录规则与 Java 切片一致：用户名不存在 / 密码错误（MD5 比对）/ 账号禁用 分别抛业务异常，由全局异常处理打成 `Result.code=0`。
