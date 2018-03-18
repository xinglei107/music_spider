# coding:utf-8

from utils.config import MYSQL_INFO, logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

class DbHelper(object):
    """
        操作数据库
    """
    def __init__(self, arg):
        super(DbHelper, self).__init__()
        self.arg = arg

mysql_path = "mysql+pymysql://{user}:{pwd}@{ip}:{port}/{dbname}?charset=utf-8".format(MYSQL_INFO)
engine = create_engine(mysql_path, pool_size=10, pool_recycle=3600, max_overflow=5, pool_pre_ping=True)
Session = sessionmaker(bind=engine)



@contextmanager
def session_scope():
    try:
        session = Session()
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
