from fastapi import APIRouter
from random import randint, random
from time import sleep

from .models import PutRequest, GetResponse, StatsResponse, DemoTrafficRequest
from .dependencies import get_cache

router = APIRouter()


@router.get("/{policy}/get", response_model=GetResponse)
def cache_get(policy: str, key: str):
    cache = get_cache(policy)
    value = cache.get(key)
    return GetResponse(key=key, value=value, hit=(value is not None))


@router.post("/{policy}/put")
def cache_put(policy: str, body: PutRequest):
    cache = get_cache(policy)

    if body.ttl is not None:
        if not hasattr(cache, "put_with_ttl"):
            return {"error": "Policy does not support TTL"}
        cache.put_with_ttl(body.key, body.value, ttl_seconds=body.ttl)
    else:
        cache.put(body.key, body.value)

    return {"status": "ok"}


@router.delete("/{policy}/delete")
def cache_delete(policy: str, key: str):
    cache = get_cache(policy)
    cache.delete(key)
    return {"status": "ok"}


@router.get("/{policy}/stats", response_model=StatsResponse)
def cache_stats(policy: str):
    cache = get_cache(policy)
    return StatsResponse(stats=cache.stats())


@router.post("/{policy}/demo-traffic", response_model=StatsResponse)
def cache_demo_traffic(policy: str, body: DemoTrafficRequest):
    """
    Generate some synthetic traffic to see hits/misses move in real time.
    """
    cache = get_cache(policy)

    for _ in range(body.writes):
        key = f"user:{randint(1, body.key_space)}"
        value = {"balance": randint(0, 1000), "score": random()}
        cache.put(key, value)

    for _ in range(body.reads):
        key = f"user:{randint(1, body.key_space)}"
        cache.get(key)

    # optional tiny sleep to simulate realistic workload
    sleep(0.01)

    return StatsResponse(stats=cache.stats())
