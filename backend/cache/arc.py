from collections import OrderedDict
from typing import Any, Optional

from .base import BaseCache


class ARCCache(BaseCache):
    """
    Simplified Adaptive Replacement Cache implementation.
    Uses four lists: T1, T2, B1, B2.
    """

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._T1 = OrderedDict()
        self._T2 = OrderedDict()
        self._B1 = OrderedDict()
        self._B2 = OrderedDict()
        self._p = 0  # target size for T1

    def get(self, key: Any) -> Optional[Any]:
        if key in self._T1:
            self.hits += 1
            value = self._T1.pop(key)
            self._T2[key] = value
            return value

        if key in self._T2:
            self.hits += 1
            value = self._T2.pop(key)
            self._T2[key] = value
            return value

        self.misses += 1
        return None

    def put(self, key: Any, value: Any) -> None:
        if self.capacity <= 0:
            return

        if key in self._T1:
            self._T1.pop(key)
            self._T2[key] = value
            return

        if key in self._T2:
            self._T2.pop(key)
            self._T2[key] = value
            return

        if key in self._B1:
            self._adapt(increase=True)
            self._replace(key)
            self._B1.pop(key)
            self._T2[key] = value
            return

        if key in self._B2:
            self._adapt(increase=False)
            self._replace(key)
            self._B2.pop(key)
            self._T2[key] = value
            return

        if len(self._T1) + len(self._B1) == self.capacity:
            if len(self._T1) < self.capacity:
                self._B1.popitem(last=False)
                self._replace(key)
            else:
                self._T1.popitem(last=False)
                self.evictions += 1
        else:
            total = len(self._T1) + len(self._T2) + len(self._B1) + len(self._B2)
            if total >= self.capacity:
                if total == 2 * self.capacity and self._B2:
                    self._B2.popitem(last=False)
                self._replace(key)

        self._T1[key] = value

    def _adapt(self, increase: bool) -> None:
        if increase:
            self._p = min(self._p + 1, self.capacity)
        else:
            self._p = max(self._p - 1, 0)

    def _replace(self, key: Any) -> None:
        if self._T1 and (len(self._T1) > self._p or (key in self._B2 and len(self._T1) == self._p)):
            old_key, _ = self._T1.popitem(last=False)
            self._B1[old_key] = None
            self.evictions += 1
        else:
            if self._T2:
                old_key, _ = self._T2.popitem(last=False)
                self._B2[old_key] = None
                self.evictions += 1

    def delete(self, key: Any) -> None:
        for d in (self._T1, self._T2, self._B1, self._B2):
            d.pop(key, None)

    def __len__(self) -> int:
        return len(self._T1) + len(self._T2)
