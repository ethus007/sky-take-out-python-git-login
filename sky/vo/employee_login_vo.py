# 对应 Java: com.sky.vo.EmployeeLoginVO
from dataclasses import dataclass


@dataclass
class EmployeeLoginVO:
    id: int | None = None
    userName: str | None = None
    name: str | None = None
    token: str | None = None

    @classmethod
    def builder(cls, **kwargs) -> "EmployeeLoginVO":
        return cls(**kwargs)
