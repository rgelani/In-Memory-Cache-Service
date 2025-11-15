from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    @abstractmethod
    def get(self, key: Any) -> Optional[Any]:
        ...

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        ...

    @abstractmethod
    def delete(self, key: Any) -> None:
        ...

    def __len__(self) -> int:
        raise NotImplementedError

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "capacity": self.capacity,
            "current_size": len(self),
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": self.hits / total if total > 0 else 0.0,
        }
