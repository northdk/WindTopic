#!/usr/bin/evn python3
# -*-coding: utf-8 -*-

import logging
import requests
import BeautifulSoup as bs
import json
import time
import os
import sys
import threading

__author__ = 'NORTH D.K.'

from zhihu import Zhihu


# logging.basicConfig()
session = requests.session()

headers = {
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'Accept-Language: zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
}

login_data = {'phone_num': '18301691700',
             'password': 'north456123789',
             'Referer': 'https://www.zhihu.com/',
             'remember_me': 'true',
              }

def get_login_data():
    if not login_data['phone_num']:
        login_data['phone_num'] = input("phone num:")
    if not login_data['password']:
        login_data['password'] = input("password:")

def get_usr_info_from_topic(topic_url):
    print(topic_url)
    r = requests.get(topic_url)
    print r


if __name__ == '__main__':
    print(__author__)
    if not login_data['phone_num'] or not login_data['password']:
        get_login_data()
    zh = Zhihu(login_data['phone_num'],login_data['password'],'phone')
    zh.makeConnection()
    topic_url = 'www.zhihu.com/topic/19740929/followers?'
    r = zh.urlOpen(topic_url)
    # print(login_data)
