# coding:utf-8

from dao.DbHelper import session_scope
from model.song import Song
from model.comment import Comment
from utils.config import OK, NOT_OK

class SongDao(object):

    def __init__(self):
        super(SongDao, self).__init__()

    def add(self, song, comments):
        with session_scope() as session:
            session.add(song)
            session.add_all(comments)
            return (OK, "")
        return (NOT_OK, u"")

    def is_existed(self, id):
        with session_scope() as session:
            existed = session.query(Song).filter(Song.sid == id).first()
            if existed:
                return True
        return False

songDao = SongDao()