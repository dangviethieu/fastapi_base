import logging

from fastapi import Request

from .mysql import SessionLocal
from app.db.redis import RedisSession
from app.utils.http_exception import raise_exception

logger = logging.getLogger(__name__)


def get_mysql_db(request: Request) -> SessionLocal:
    return request.state.db

def get_redis_db() -> RedisSession:
    try:
        db = RedisSession
        logger.debug("Start db session {}".format(RedisSession))
        return db
    except Exception as e:
        print(e)
        raise_exception(e)