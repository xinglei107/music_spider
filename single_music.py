# coding:utf-8

from parser import extract
import json
from service.SongService import songService


info = extract.getSongInfo("http://music.163.com/#/song?id=386538")
print json.dumps(info, indent=4, ensure_ascii=False)
songService.add(info)