# 对应 Java DigestUtils.md5DigestAsHex + Jackson 把对象打成 JSON
from dataclasses import asdict, is_dataclass
from datetime import datetime
from hashlib import md5
from typing import Any


def md5_hex(raw: str) -> str:
    return md5(raw.encode("utf-8")).hexdigest()


def to_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M")
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if hasattr(obj, "__dict__"):
        return {k: to_jsonable(v) for k, v in vars(obj).items() if not k.startswith("_")}
    return obj
