from .lru import LRUCache
from .ttl_mixin import TTLCacheMixin


class LRUWithTTL(TTLCacheMixin, LRUCache):
    """
    LRU cache with TTL support.
    Policy name: "lru_ttl"
    """
    pass
