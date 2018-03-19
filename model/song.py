# coding:utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, TIMESTAMP, Column
import json

Base = declarative_base()

class Song(Base):

    __tablename__ = "song"

    sid = Column(String(64), primary_key=True)
    name = Column(String(128))
    singer = Column(String(128))
    album = Column(String(64))
    lyric = Column(String(1024))
    create = Column(TIMESTAMP)
    modified = Column(TIMESTAMP)
    comments = []


    def __repr__(self):
        return json.dumps({
            "sid":self.sid,
            "name":self.name,
            "singer":self.singer,
            "album":self.album,
            "lyric":self.lyric,
            "comments":self.comments
        }, indent=4, ensure_ascii=False)

        