# coding:utf-8

from asynch import asynch
from bs4 import BeautifulSoup
from collections import deque
import requests
import json
import re
import signal

subHtmlUrlQueue = deque()
mediaUrlQueue = deque()
visitedUrlDict = {}
host = "http://www.kuwo.cn"


def save():
    with open("history.txt", "w") as file:
        file.write(visitedUrlDict)

def index(url):
    response = requests.get(url)
    if response.status_code == 200 and response.headers.get("Content-Type").find("text/html") >= 0:
        getHrefs(response.text)

def getHrefs(html):
    soup = BeautifulSoup(html, "lxml")
    atags = soup.find_all("a")
    for atag in atags:
        href = atag.get("href")
        if href in visitedUrlDict or not href:
            continue
        visitedUrlDict[href] = 1
        print href
        id = getIdFromHref(href)
        if id == href:
            url = getFullUrl(href)
            subHtmlUrlQueue.append(url)
        else:
            url = getRealMediaUrl(id)
            print url
            mediaUrlQueue.append((url, atag.get_text()))
    while len(subHtmlUrlQueue):
        url = subHtmlUrlQueue.popleft()
        index(url)

def getIdFromHref(href):
    pat = re.search(r"yinyue/([0-9]\d*)", href)
    if pat:
        return pat.group(1)
    return href

def getFullUrl(href):
    pat = re.match("https?://", href)
    if pat:
        return href
    return host + href

def getRealMediaUrl(id):
    return "http://antiserver.kuwo.cn/anti.s?format=mp3&rid=MUSIC_{0}&type=convert_url&response=res".format(id)

def downloadMedia(url, title):
    headers = {
        "Referer":"http://www.kuwo.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=5)
    with open("/Users/xinglei/Desktop/musics/" + title + ".mp3", "wb") as file:
        file.write(r.content)

@asynch(False)
def download():
    while True:
        while len(mediaUrlQueue):
            url, title = mediaUrlQueue.popleft()
            #print "#############", url, title
            downloadMedia(url, title)

def receive_signal(signum, stack):
    print signum

signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

if __name__ == '__main__':
    download()
    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        print "exit"
    #index(host)