from functools import lru_cache
from typing import Any

from pydantic import BaseSettings
from pydantic.types import constr


class Settings(BaseSettings):
    """Settings from environment variables."""

    class Config:
        """Config for custom settings."""

        env_prefix = "app"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Parse certain variables."""
            if field_name == "redis_addrs":
                return raw_val.split(",")
            return raw_val

    environment: constr(regex=r"^(dev|prod|stage|local)$") = "local"  # type: ignore
    loglevel: constr(  # type: ignore
        regex=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL|FATAL)$"
    ) = "DEBUG"
    redis_host: str = "log-farm"
    redis_username: str = "default"
    redis_password: str = "a1234a"
    stream_max_length = 100


@lru_cache
def init_settings() -> Settings:
    """Initialize settings from environment variables."""
    _env = Settings()
    return _env


env = init_settings()
