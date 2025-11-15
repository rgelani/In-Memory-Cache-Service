from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEFAULT_CACHE_CAPACITY: int = 1000


settings = Settings()
