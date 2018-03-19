# coding:utf-8

from utils.config import MYSQL_INFO, logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

mysql_path = "mysql+pymysql://{user}:{pwd}@{ip}:{port}/{dbname}?charset=utf8".format(**MYSQL_INFO)
engine = create_engine(mysql_path, pool_size=10, pool_recycle=3600, max_overflow=5, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    try:
        session = Session()
        yield session
        session.commit()
    except Exception as e:
        logger.error("", exc_info=True)
        session.rollback()
    finally:
        session.close()
