import os
from functools import lru_cache
from pydantic import BaseSettings


@lru_cache
class AppInfo(BaseSettings):
    app_env: str = "dev"
    app_url: str = "http://localhost"
    app_logo: str = "/public/images/logo.png"

    class Config:
        env_file = ".env"


@lru_cache()
class MysqlDB(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_database: str

    class Config:
        env_file = ".env"


@lru_cache()
class JWTSetting(BaseSettings):
    authjwt_secret_key: str = "MY_SECRET"
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 900
    authjwt_refresh_token_expires: int = 86400

    class Config:
        env_file = ".env"


@lru_cache()
class RedisSetting(BaseSettings):
    redis_host: str
    redis_port: int = 6379
    redis_prefix: str = "fastapi_base"
    redis_confirm_key: str = "REDIS_CONFIRM_KEY"

    class Config:
        env_file = ".env"


@lru_cache()
class RedisConfirmType:
    forgot_password: int = 1


@lru_cache()
class DocsURL(BaseSettings):
    docs_url: str = "docs"

    class Config:
        env_file = ".env"


@lru_cache()
class UserRoles:
    admin: int = 100
    user: int = 1