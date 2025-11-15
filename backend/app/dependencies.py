from fastapi import HTTPException

from cache import LRUCache, LFUCache, ARCCache, LRUWithTTL
from .config import settings

cache_instances = {}


def get_cache(policy: str):
    policy = policy.lower()

    if policy not in cache_instances:
        if policy == "lru":
            cache_instances[policy] = LRUCache(settings.DEFAULT_CACHE_CAPACITY)
        elif policy == "lfu":
            cache_instances[policy] = LFUCache(settings.DEFAULT_CACHE_CAPACITY)
        elif policy == "arc":
            cache_instances[policy] = ARCCache(settings.DEFAULT_CACHE_CAPACITY)
        elif policy == "lru_ttl":
            cache_instances[policy] = LRUWithTTL(settings.DEFAULT_CACHE_CAPACITY)
        else:
            raise HTTPException(status_code=400, detail="Invalid cache policy")

    return cache_instances[policy]
