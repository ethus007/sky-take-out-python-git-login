# 对应 Java: com.sky.utils.JwtUtil
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt


class JwtUtil:
    @staticmethod
    def createJWT(secretKey: str, ttlMillis: int, claims: dict[str, Any]) -> str:
        payload = dict(claims)
        exp = datetime.now(timezone.utc) + timedelta(milliseconds=ttlMillis)
        payload["exp"] = exp
        return jwt.encode(payload, secretKey.encode("utf-8"), algorithm="HS256")

    @staticmethod
    def parseJWT(secretKey: str, token: str | None) -> dict[str, Any]:
        return jwt.decode(
            token or "",
            secretKey.encode("utf-8"),
            algorithms=["HS256"],
        )
