# 内存实现，对应 MyBatis EmployeeMapper + EmployeeMapper.xml；测试可 Mock 本接口
from __future__ import annotations

from copy import deepcopy
from dataclasses import fields
from datetime import datetime

from sky.aspect.auto_fill_aspect import AutoFillAspect
from sky.dto.employee_page_query_dto import EmployeePageQueryDTO
from sky.entity.employee import Employee
from sky.enumeration.operation_type import OperationType
from sky.exception.duplicate_entry_exception import DuplicateEntryException
from sky.mapper.employee_mapper import Page
from sky.utils.json_util import md5_hex


class MemoryEmployeeMapper:
    def __init__(self) -> None:
        admin = Employee(
            id=1,
            name="管理员",
            username="admin",
            password=md5_hex("123456"),
            phone="13812312312",
            sex="1",
            idNumber="110101199001010047",
            status=1,
        )
        self._rows: list[Employee] = [admin]
        self._next_id = 2

    def getByUsername(self, username: str | None) -> Employee | None:
        for row in self._rows:
            if row.username == username:
                return deepcopy(row)
        return None

    def insert(self, employee: Employee) -> None:
        AutoFillAspect.autoFill(employee, OperationType.INSERT)
        if any(row.username == employee.username for row in self._rows):
            raise DuplicateEntryException(
                f"Duplicate entry '{employee.username}' for key 'employee.idx_username'"
            )
        employee.id = self._next_id
        self._next_id += 1
        self._rows.append(deepcopy(employee))

    def pageQuery(self, dto: EmployeePageQueryDTO) -> Page:
        matched = list(self._rows)
        if dto.name:
            matched = [e for e in matched if e.name and dto.name in e.name]
        matched.sort(key=lambda e: e.createTime or datetime.min, reverse=True)
        total = len(matched)
        start = (dto.page - 1) * dto.pageSize
        end = start + dto.pageSize
        page = Page(total=total, records=[deepcopy(e) for e in matched[start:end]])
        return page

    def update(self, employee: Employee) -> None:
        AutoFillAspect.autoFill(employee, OperationType.UPDATE)
        for i, row in enumerate(self._rows):
            if row.id != employee.id:
                continue
            merged = deepcopy(row)
            for f in fields(Employee):
                value = getattr(employee, f.name)
                if value is not None:
                    setattr(merged, f.name, value)
            self._rows[i] = merged
            return

    def getById(self, id: int | None) -> Employee | None:
        for row in self._rows:
            if row.id == id:
                return deepcopy(row)
        return None
