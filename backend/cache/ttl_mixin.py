import time
from typing import Any, Tuple, Optional

from sortedcontainers import SortedList


class TTLCacheMixin:
    """
    Mixin to add TTL to any cache.
    Expects subclass to implement get/put/delete.
    """

    def __init__(self, *args, **kwargs):
        self._ttl_index: SortedList[Tuple[float, Any]] = SortedList()
        self._key_to_expiry = {}
        super().__init__(*args, **kwargs)

    def _purge_expired(self) -> None:
        now = time.time()
        while self._ttl_index:
            expiry, key = self._ttl_index[0]
            if expiry > now:
                break
            self._ttl_index.pop(0)
            if self._key_to_expiry.get(key) == expiry:
                self._key_to_expiry.pop(key, None)
                super().delete(key)

    def put_with_ttl(self, key: Any, value: Any, ttl_seconds: float) -> None:
        self._purge_expired()
        expiry = time.time() + ttl_seconds
        self._key_to_expiry[key] = expiry
        self._ttl_index.add((expiry, key))
        super().put(key, value)

    def get(self, key: Any) -> Optional[Any]:
        self._purge_expired()
        return super().get(key)

    def delete(self, key: Any) -> None:
        expiry = self._key_to_expiry.pop(key, None)
        if expiry is not None:
            self._ttl_index.discard((expiry, key))
        super().delete(key)
