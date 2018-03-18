# coding:utf-8

import requests
import json

def get_info_by_enc(enc):
    data = {
            "params": enc["encText"],
            "encSecKey": enc["encSecKey"]
        }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post("http://music.163.com/weapi/song/enhance/player/url?csrf_token=", data=data, headers=headers)
    urlDict = json.loads(res.text)
    return urlDict