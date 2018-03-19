# coding:utf-8

import requests
import json
from utils.asynch import asynch
from utils.config import MUSIC_PATH
import random

p_d = [{
    "ip":"119.188.94.145",
    "port":"80"
},{
    "ip":"113.120.130.249",
    "port":"8080"
},{
    "ip":"210.72.14.142",
    "port":"80"
},{
    "ip":"113.204.136.50",
    "port":"8080"
},{
    "ip":"121.193.143.249",
    "port":"80"
}]

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

@asynch(False)
def download(url, name):
    if not (url.endswith("mp3") or url.endswith("wav")):
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
    }
    p=random.choice(p_d)
    proxies = {"http":p["ip"]+":"+p["port"]}
    r = requests.get(url, headers=headers, timeout=5, proxies=proxies)
    with open("".join([MUSIC_PATH, name.replace("/", "_"), url[-4:]]), "wb") as file:
        file.write(r.content)