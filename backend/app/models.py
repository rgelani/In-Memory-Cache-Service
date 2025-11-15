from pydantic import BaseModel
from typing import Any, Optional, Dict


class PutRequest(BaseModel):
    key: str
    value: Any
    ttl: Optional[int] = None


class GetResponse(BaseModel):
    key: str
    value: Optional[Any]
    hit: bool


class StatsResponse(BaseModel):
    stats: Dict[str, Any]


class DemoTrafficRequest(BaseModel):
    reads: int = 100
    writes: int = 20
    key_space: int = 50
