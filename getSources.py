#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS
import requests

def myPrint() -> object:
    print("hello, DK!")

"""
to get url source
"""
class GetSource(object):

    def __init__(self,url):
        print("we are trying to create a GetSource instance!")
        self.__url = url
        try:
            self.__html = urlopen(self.__url)
            self.__html_data = self.__html.read()
            self.__bsObj = BS(self.__html_data,"html.parser")
            print("created a GetSource instance!")
        except (HTTPError,URLError) as e:
            print(e)
            print("input url is invalid!")
            self.__html = None
            self.__html_data = None

    def writeHtml(self,fileName):
        if self.__html_data:
            with open(fileName,"wb") as f:
                f.write(self.__html_data)
        else:
            print("cannot write the html file!")

    def printest(self):
        print(self.__bsObj)

    def getTitle(self):
        print(u'self.__bsObj.find("title").get_text()')

