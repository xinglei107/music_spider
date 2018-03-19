# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
import re

from selenium import webdriver
from parser import MediaProcess

from utils.config import logger
from utils.decorater import protector


@protector
def getSongInfo(url, driver=None):
    """
    返回歌曲的基本信息，包括：
        id：str，歌曲id，必选，
        url：str，歌曲真实地址，可选，
        name：str，歌曲名称，必选，
        singer：str，歌手，可选，
        album：str，专辑，可选，
        lyrice：str，歌词，可选，
        comments：json，歌曲评论，可选，包括：
            whoId：int，评论人id，
            whoName：str，评论人昵称，
            what：str，评论内容，
            when：str，评论时间，xxxx年x月x日
            like：int，点赞数
    """
    info = {}
    exit = False
    if not driver:
        driver = webdriver.Chrome()
        exit = True
    driver.get(url)
    driver.switch_to_frame("contentFrame")

    info["id"] = __get_id_from_url(driver.current_url)

    music_element = __get_music_element(driver)
    info["name"] = __get_song_title(music_element)
    info["singer"] = __get_song_singer(music_element)
    info["album"] = __get_song_ablum(music_element)

    info["lyric"] = __get_song_lyric(driver)

    comment_elements = __get_comment_elements(driver)
    info["comments"] = __get_song_comments(comment_elements)

    info["url"] = __get_song_url(driver)
    
    if exit:
        driver.quit()
    return info

def __get_id_from_url(url):
    id = url[url.find("=")+1:]
    return id

def __get_music_element(driver):
    return driver.find_element_by_xpath("//div[@class='f-cb']//div[@class='cnt']")

def __get_song_title(element):
    return element.find_element_by_xpath(".//div[@class='tit']").text

def __get_song_singer(element):
    p = element.find_elements_by_tag_name("p")
    if len(p) > 0:
        return p[0].find_element_by_tag_name("a").text
    return ""

def __get_song_ablum(element):
    p = element.find_elements_by_tag_name("p")
    if len(p) > 1:
        return p[1].find_element_by_tag_name("a").text
    return ""

def __get_song_lyric(driver):
    element = __get_music_element(driver)
    lyricDiv = element.find_element_by_xpath(".//div[@id='lyric-content']")
    lyric = driver.execute_script('var arr = document.getElementById("lyric-content").innerHTML.replace(\'<div id="flag_more" class="f-hide">\', "").split("<br>"); arr.pop();return arr', lyricDiv)
    return lyric

def __get_url_info(driver):
    """
        获取加密信息后，构造表单，请求url信息，
        注意：返回的并不一定是当前歌曲的信息，所以还需要进一步判断
    """
    songId = __get_id_from_url(driver.current_url)
    enc = driver.execute_script('var c7f=NEJ.P;eo9f=c7f("nej.g");v7o=c7f("nej.j");k7d=c7f("nej.u");TY1x=c7f("nm.x.ek");l7e=c7f("nm.x");window.GEnc=true;var bsL0x=function(czZ5e){var o7h=[];k7d.bd7W(czZ5e,function(czX5c){o7h.push(TY1x.emj[czX5c])});return o7h.join("")};var czW5b=v7o.bn7g;v7o.bn7g=function(Y7R,e7d){var j7c={},e7d=NEJ.X({},e7d),lx1x=Y7R.indexOf("?");if(window.GEnc&&/(^|\.com)\/api/.test(Y7R)&&!(e7d.headers&&e7d.headers[eo9f.zI5N]==eo9f.Ff7Y)&&!e7d.noEnc){if(lx1x!=-1){j7c=k7d.hu0x(Y7R.substring(lx1x+1));Y7R=Y7R.substring(0,lx1x)}if(e7d.query){j7c=NEJ.X(j7c,k7d.fH9y(e7d.query)?k7d.hu0x(e7d.query):e7d.query)}if(e7d.data){j7c=NEJ.X(j7c,k7d.fH9y(e7d.data)?k7d.hu0x(e7d.data):e7d.data)}j7c["csrf_token"]=v7o.gy0x("__csrf");Y7R=Y7R.replace("api","weapi");e7d.method="post";delete e7d.query;var bBU3x=window.asrsea(JSON.stringify(j7c),bsL0x(["流泪","强"]),bsL0x(TY1x.md),bsL0x(["爱心","女孩","惊恐","大笑"]));e7d.data=k7d.cC8u({params:bBU3x.encText,encSecKey:bBU3x.encSecKey});return bBU3x}};f=function(){};var p={type:"json",query:{ids:"[' + 
        songId + ']",br:128000},onload:f,onerror:f};real=v7o.bn7g("/api/song/enhance/player/url",p);return real')
    urlDict = MediaProcess.get_info_by_enc(enc)
    return urlDict

def __get_song_url(driver):
    songId = __get_id_from_url(driver.current_url)
    url_info = __get_url_info(driver)
    url = __get_url_by_id(songId, url_info)
    return url

def __get_song_comments(elements):
    comments = []
    for itm in elements:
        whoInfo = __get_comment_who_info(itm)
        comments.append({
            "whoId" : whoInfo["whoId"],
            "whoName" : whoInfo["who"],
            "what" : __get_comment_what(itm),
            "when" : __get_comment_when(itm),
            "like" : __get_comment_like(itm)
        })
    return comments

def __get_comment_elements(driver):
    return driver.find_elements_by_xpath("//div[@class='itm' and @id]//div[@class='cntwrap']")

def __get_comment_who_info(element):
    cnt = element.find_element_by_xpath(".//div[contains(@class, 'cnt')]")
    coma = cnt.find_element_by_xpath(".//a")
    who = coma.text
    whoId = __get_id_from_url(coma.get_attribute("href"))
    return {
        "who" : who,
        "whoId" : whoId
    }

def __get_comment_what(element):
    cnt = element.find_element_by_xpath(".//div[contains(@class, 'cnt')]")
    index = cnt.text.find("：")
    if index >= 0:
        return cnt.text[index+1:]
    return cnt.text

def __get_comment_when(element):
    rp = element.find_element_by_xpath(".//div[@class='rp']")
    when = rp.find_element_by_xpath(".//div[contains(@class, 'time')]").text
    when = __format_time(when)
    return when

def __get_comment_like(element):
    rp = element.find_element_by_xpath(".//div[@class='rp']")
    like = rp.find_element_by_xpath(".//a").text
    return __get_num(like)

def __format_time(when):
    """
        只返回xxxx年x月x日
    """
    if u"年" in when:
        return when
    current = time.localtime()
    year = time.strftime("%Y", current)
    month = time.strftime("%m", current)
    day = time.strftime("%d", current)
    if u"日" in when:
        return u"{0}年".format(year) + when[0:when.find(u"日")+1]
    return (u"{0}年{1}月{2}日".format(year, int(month), int(day)))

def __get_num(like):
    """
        从文本中提取数字
    """
    pat = re.compile("\d+")
    num = pat.search(like)
    if num:
        return int(num.group(0))
    return 0

def __get_url_by_id(current_id, urlDict):
    """
        提取当前歌曲的真实地址。
        urlDict中存放的可能不是当前歌曲的信息，
        需要与当前歌曲id进行对比
    """
    if len(urlDict.get("data", [])) > 0:
        real_id = urlDict["data"][0]["id"]
        if str(real_id) == str(current_id):
            return urlDict["data"][0]["url"]
    return ""