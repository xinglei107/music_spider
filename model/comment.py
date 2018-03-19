# coding:utf-8


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import json

Base = declarative_base()

class Comment(Base):

    __tablename__ = "comment"

    cid = Column(String(64), primary_key=True)
    sid = Column(String(64))
    whoId = Column(String(64))
    whoName = Column(String(128))
    what = Column(String(1024))
    when = Column(String(32))
    like = Column(Integer)
    create = Column(TIMESTAMP)
    modified = Column(TIMESTAMP)


    def __repr__(self):
        return json.dumps({
            "cid":self.cid,
            "sid":self.sid,
            "whoId":self.whoId,
            "whoName":self.whoName,
            "what":self.what,
            "when":self.when,
            "like":self.like
        }, indent=4, ensure_ascii=False)
