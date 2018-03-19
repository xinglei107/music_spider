# coding:utf-8

from dao.SongDao import songDao
from model.song import Song
from model.comment import Comment
from utils.HashUtil import hashUtil
from utils.config import logger
from parser.MediaProcess import download
import datetime

class SongService(object):

    def __init__(self):
        super(SongService, self).__init__()

    def add(self, songDict):
        download(songDict["url"], songDict["name"]+"_"+songDict["singer"])
        song = self.__trans_dict_to_song(songDict)
        commentsDict = songDict["comments"]
        comments = []
        for com in commentsDict:
            comment = self.__trans_dict_to_comment(com)
            comment.sid = song.sid
            comments.append(comment)
        songDao.add(song, comments)

    def is_existed(self, id):
        return songDao.is_existed(id)

    def __trans_dict_to_song(self, songDict):
        return Song(
                sid = songDict["id"],
                name = songDict["name"],
                singer = songDict["singer"],
                album = songDict["album"],
                lyric = "\\n".join(songDict["lyric"]),
                create = datetime.datetime.now(),
                modified = datetime.datetime.now()
            )

    def __trans_dict_to_comment(self, commentDict):
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
        
songService = SongService()