from functools import lru_cache
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.settings import MysqlDB

logger = logging.getLogger(__name__)


@lru_cache()
def _get_mysql_db_setting():
    logger.info("Added mysql to lru_cache")
    return MysqlDB()

mysql_setting = _get_mysql_db_setting()

DATABASE_URL = "mysql+mysqlconnector://{user}:{password}@{host}/{database}".format(
    user=mysql_setting.db_username,
    password=mysql_setting.db_password,
    host=mysql_setting.db_host,
    database=mysql_setting.db_database,
)
logger.info(f"Mysql URL: {DATABASE_URL}")

Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=Engine,
    )
)

Base = declarative_base()