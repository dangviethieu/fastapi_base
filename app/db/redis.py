from functools import lru_cache
import redis
import logging

from app.settings import RedisSetting

logger = logging.getLogger(__name__)


@lru_cache()
def _get_redis_settings():
    logger.info("Added redis to lru_cache")
    return RedisSetting()

redis_setting = _get_redis_settings()

pool = redis.ConnectionPool(
    host=redis_setting.redis_host,
    port=redis_setting.redis_port,
)

RedisSession = redis.Redis(
    connection_pool=pool,
)