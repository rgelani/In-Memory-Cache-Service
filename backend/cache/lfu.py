from collections import defaultdict, OrderedDict
from typing import Any, Optional

from .base import BaseCache


class LFUCache(BaseCache):
    """
    Least Frequently Used cache.
    Evicts the key with the lowest access frequency.
    Ties are broken by recency within the same frequency bucket.
    """

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._values = {}                    # key -> value
        self._freq = {}                      # key -> frequency
        self._buckets = defaultdict(OrderedDict)  # freq -> OrderedDict(key -> None)
        self._min_freq = 0

    def _touch(self, key: Any) -> None:
        freq = self._freq[key]
        bucket = self._buckets[freq]
        if key in bucket:
            del bucket[key]
        if not bucket:
            del self._buckets[freq]
            if self._min_freq == freq:
                self._min_freq += 1

        new_freq = freq + 1
        self._freq[key] = new_freq
        self._buckets[new_freq][key] = None

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._values:
            self.misses += 1
            return None
        self.hits += 1
        self._touch(key)
        return self._values[key]

    def put(self, key: Any, value: Any) -> None:
        if self.capacity <= 0:
            return

        if key in self._values:
            self._values[key] = value
            self._touch(key)
            return

        if len(self._values) >= self.capacity:
            bucket = self._buckets[self._min_freq]
            evict_key, _ = bucket.popitem(last=False)
            del self._values[evict_key]
            del self._freq[evict_key]
            if not bucket:
                del self._buckets[self._min_freq]
            self.evictions += 1

        self._values[key] = value
        self._freq[key] = 1
        self._buckets[1][key] = None
        self._min_freq = 1

    def delete(self, key: Any) -> None:
        if key not in self._values:
            return
        freq = self._freq[key]
        bucket = self._buckets[freq]
        del bucket[key]
        if not bucket:
            del self._buckets[freq]
            if self._min_freq == freq:
                self._min_freq = min(self._buckets.keys()) if self._buckets else 0

        del self._values[key]
        del self._freq[key]

    def __len__(self) -> int:
        return len(self._values)
