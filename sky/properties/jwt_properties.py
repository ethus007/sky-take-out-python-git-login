# 对应 Java: com.sky.properties.JwtProperties
from dataclasses import dataclass


@dataclass
class JwtProperties:
    adminSecretKey: str = "itcast"
    adminTtl: int = 7_200_000
    adminTokenName: str = "token"
    userSecretKey: str | None = None
    userTtl: int = 0
    userTokenName: str | None = None
