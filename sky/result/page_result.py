# 对应 Java: com.sky.result.PageResult
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PageResult:
    total: int = 0
    records: list[Any] = field(default_factory=list)
