# 对应 Java: com.sky.entity.Employee
from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import datetime
from typing import Any


@dataclass
class Employee:
    id: int | None = None
    username: str | None = None
    name: str | None = None
    password: str | None = None
    phone: str | None = None
    sex: str | None = None
    idNumber: str | None = None
    status: int | None = None
    createTime: datetime | None = None
    updateTime: datetime | None = None
    createUser: int | None = None
    updateUser: int | None = None

    @classmethod
    def builder(cls, **kwargs: Any) -> "Employee":
        """对应 Lombok @Builder"""
        return cls(**kwargs)

    def copy_from(self, other: Any) -> None:
        """对应 BeanUtils.copyProperties：同名字段有值才拷"""
        for f in fields(self):
            if hasattr(other, f.name):
                value = getattr(other, f.name)
                if value is not None:
                    setattr(self, f.name, value)
