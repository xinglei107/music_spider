# coding:utf-8

from dao.CommentDao import commentDao
from model.comment import Comment
from utils.HashUtil import hashUtil
import datetime

class cCommentService(object):

    def __init__(self):
        super(cCommentService, self).__init__()

    def add(commentDict):
        comment = self.__trans_dict_to_object(commentDict)
        commentDao.add(comment)


    def __trans_dict_to_object(self, commentDict):
        return Comment(
                cid = hashUtil.uid(),
                whoId = commentDict["whoId"],
                whoName = commentDict["whoName"],
                what = commentDict["what"],
                when = commentDict["when"],
                like = commentDict["like"],
                create = datetime.datetime.now(),
                modified = datetime.datetime.now()
            )
        
commentService = CommentService()