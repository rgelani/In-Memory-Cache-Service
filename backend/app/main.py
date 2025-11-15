from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as cache_router

app = FastAPI(
    title="In-Memory Cache Service",
    description="FastAPI service exposing LRU, LFU, ARC, LRU+TTL caches",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(cache_router, prefix="/cache", tags=["cache"])
