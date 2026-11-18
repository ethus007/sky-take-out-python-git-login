# 对应 Java: com.sky.mapper.EmployeeMapper
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.entity.employee import Employee


@dataclass
class Page:
    """对应 PageHelper 的 Page<Employee>"""
    total: int = 0
    records: list[Employee] = field(default_factory=list)

    def add(self, employee: Employee) -> None:
        self.records.append(employee)

    def setTotal(self, total: int) -> None:
        self.total = total

    def getTotal(self) -> int:
        return self.total

    def getResult(self) -> list[Employee]:
        return self.records


@runtime_checkable
class EmployeeMapper(Protocol):
    def getByUsername(self, username: str | None) -> Employee | None: ...

    def insert(self, employee: Employee) -> None: ...

    def pageQuery(self, dto: EmployeePageQueryDTO) -> Page: ...

    def update(self, employee: Employee) -> None: ...

    def getById(self, id: int | None) -> Employee | None: ...
