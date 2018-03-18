# ecoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys 
import time
from parser import extract

driver = webdriver.Chrome()

driver.get("http://music.163.com/")
driver.switch_to.frame("contentFrame")
atags = driver.find_elements_by_tag_name("a");
for a in atags:
    print a.get_attribute("href")

driver.quit()