# 对应 Java: com.sky.dto.EmployeePageQueryDTO
from dataclasses import dataclass


@dataclass
class EmployeePageQueryDTO:
    name: str | None = None
    page: int = 1
    pageSize: int = 10
