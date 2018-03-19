# coding:utf-8

from dao.DbHelper import session_scope
from model.comment import Comment
from utils.config import OK, NOT_OK

class CommentDao(object):

    def __init__(self):
        super(CommentDao, self).__init__()

    def add(self, Comment):
        with session_scope() as session:
            session.add(Comment)
            return (OK, "")
        return (NOT_OK, u"")

commentDao = CommentDao()