# coding:utf

from utils.config import OK, NOT_OK, logger

def protector(realf):
    def execute(*args, **kws):
        try:
            return realf(*args, **kws)
        except Exception as e:
            logger.error(repr(e), exc_info=True)
        return None
    return execute