# coding:utf-8

import uuid, hashlib
class HashUtil(object):

    def __init__(self):
        super(HashUtil, self).__init__()

    def md5(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def uid(self):
        u = str(uuid.uuid1()).replace("-", "")
        m = self.md5(u)
        return m

hashUtil = HashUtil()