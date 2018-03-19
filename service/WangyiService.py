# ecoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from parser import extract
from collections import deque
from utils.asynch import asynch
from utils.config import logger
from utils.config import WANGYI_LINK_TYPE
from service.SongService import songService
import re

subHtmlUrlQueue = deque()
songUrlQueue = deque()
visitedUrl = {}

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

chrome_options = webdriver.ChromeOptions()  
chrome_options.add_argument(('--proxy-server=http://' + p_d[1]["ip"]+":"+p_d[1]["port"]))  
main_driver = webdriver.Chrome(chrome_options=chrome_options)
chrome_options.add_argument(('--proxy-server=http://' + p_d[0]["ip"]+":"+p_d[0]["port"]))  
song_driver = webdriver.Chrome(chrome_options=chrome_options)

def crawl():
    subHtmlUrlQueue.append("http://music.163.com/")
    __crawl(main_driver)

def __crawl(driver):
    while True:
        while len(subHtmlUrlQueue) > 0:
            url = subHtmlUrlQueue.popleft()
            if url in visitedUrl:
                continue
            try:
                visitedUrl[url] = 1
                logger.info("visit page %s" % url)
                driver.get(url)
                WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_tag_name("script"))
                driver.switch_to.frame("contentFrame")
                atags = driver.find_elements_by_tag_name("a");
                hrefs = [a.get_attribute("href") for a in atags]
                links = filter_link(hrefs)
                song_links = get_song_link(links)
                logger.debug("get song_links %s" % len(song_links))
                notsong_links = get_nonsong_link(links)
                songUrlQueue.extend(song_links)
                subHtmlUrlQueue.extend(notsong_links)
            except Exception as e:
                logger.error("", exc_info=True)
                continue
        else:
            logger.info("empty page queue")
            time.sleep(1)

@asynch(True)
def crawl_songs():
    while True:
        while len(songUrlQueue) > 0:
            song_link = songUrlQueue.popleft()
            if song_link in visitedUrl:
                continue
            logger.info("visit song %s" % song_link)
            try:
                visitedUrl[song_link] = 1
                sid = song_link[song_link.find("=")+1:]
                if songService.is_existed(sid):
                    logger.info("%s has existed" % sid)
                    continue
                info = extract.getSongInfo(song_link, song_driver)
                if not info:
                    continue
                songService.add(info)
            except Exception as e:
                logger.error("", exc_info=True)
                continue
        else:
            logger.info("empty song queue")
            time.sleep(1)

def filter_link(hrefs):
    pat = re.compile("https?:\/\/music\.163\.com\/")
    links = [str(href) for href in hrefs if pat.search(str(href))]
    return links

def get_song_link(links):
    pat = re.compile("song\?id=")
    song_links = [str(link) for link in links if pat.search(str(link))]
    return song_links

def get_nonsong_link(links):
    notsong_links = []
    for key in WANGYI_LINK_TYPE.iterkeys():
        pat = re.compile(key + "\?id=")
        notsong_links.extend([str(link) for link in links if pat.search(str(link))])
    return notsong_links
