from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SenrenConfig(BaseSettings):
    REGISTRY_SERVICE_URL: str = "127.0.0.1:6391"
    LOG_LEVEL: str = "INFO"
    USER_REPO_PATH: str = "./user_repo"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_config() -> SenrenConfig:
    return SenrenConfig()


config = get_config()
