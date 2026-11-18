# 对应 Java: com.sky.dto.EmployeeDTO
from dataclasses import dataclass


@dataclass
class EmployeeDTO:
    id: int | None = None
    username: str | None = None
    name: str | None = None
    phone: str | None = None
    sex: str | None = None
    idNumber: str | None = None
