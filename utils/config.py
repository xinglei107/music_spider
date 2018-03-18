# coding:utf-8

import sys
sys.path.append("/opt/kms/libs")
import kms

PROJECT_NAME = "music_spider"
LOG_PATH = "/opt/logs/music_spider/music_spider.log"

class Logger(object):
    
    @classmethod
    def get_logger(cls):
        import logging
        logger = logging.getLogger(PROJECT_NAME)
        logFileHandler = logging.FileHandler(LOG_PATH, "a")
        formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s [in %(filename)s : %(lineno)d]")
        logFileHandler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logFileHandler)
        return logger

logger = Logger.get_logger()
MYSQL_INFO = {
    "user" : kms.get(PROJECT_NAME, "mysql.user"),
    "pwd" : kms.get(PROJECT_NAME, "mysql.pwd"),
    "ip" : kms.get(PROJECT_NAME, "mysql.ip"),
    "port" : kms.get(PROJECT_NAME, "mysql.port"),
    "dbname" : kms.get(PROJECT_NAME, "mysql.dbname")
}
OK = 1
NOT_OK = 0