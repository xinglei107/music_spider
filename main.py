#coding:utf-8

import time
from utils.asynch import asynch

@asynch
def add1(a, b):
    time.sleep(2)
    return a+b

@asynch
def add2(a, b):
    time.sleep(4)
    return a+b


if __name__ == '__main__':
   ha = add1(1,2)
   hb = add2(2,3)
   print ha.get_result()
   print hb.get_result()