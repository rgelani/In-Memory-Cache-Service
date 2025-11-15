from collections import OrderedDict
from typing import Any, Optional

from .base import BaseCache


class LRUCache(BaseCache):
    """
    Least Recently Used cache.
    Evicts the key that was not used for the longest time.
    """

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._data = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._data:
            self.misses += 1
            return None
        self.hits += 1
        self._data.move_to_end(key, last=True)
        return self._data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self._data:
            self._data.move_to_end(key, last=True)
            self._data[key] = value
            return

        if len(self._data) >= self.capacity:
            self._data.popitem(last=False)
            self.evictions += 1

        self._data[key] = value

    def delete(self, key: Any) -> None:
        self._data.pop(key, None)

    def __len__(self) -> int:
        return len(self._data)
