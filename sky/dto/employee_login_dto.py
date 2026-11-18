# 对应 Java: com.sky.dto.EmployeeLoginDTO
from dataclasses import dataclass


@dataclass
class EmployeeLoginDTO:
    username: str | None = None
    password: str | None = None
