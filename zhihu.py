#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
# need to be refactored:
    * remove multi threads
    * just surport basic func with zhihu
    * the funcs should be in closed loop
'''

'''
#   Author: North D.K.
#                   to get millions zhihu usr,
#                   to find one person named ...
'''

import requests
import BeautifulSoup as bs
import json
import time
import os
import sys
import threading
# import pymysql
# import re
from urllib3 import request as urlReq
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

mutex = threading.Lock()

headers = {
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'Accept-Language: zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
}

login_data = {'phone_num': 'xxx',
             'password': 'xxx',
             'Referer': 'https://www.zhihu.com/',
             'remember_me': 'true',
              }

session = requests.session()
login_data = {'remember_me': 'true'}
captchaFile = os.path.join(sys.path[0], "captcha.jpg")
cookieFile = os.path.join(sys.path[0], "cookie")
host = "https://www.zhihu.com"

# authorization = ""


def loadFile(file,name):
    fileName = name+'.html'
    with open(fileName,"wb") as f:
        f.write(file.encode())
        f.close()


# def urlOpen(url, headers):
#     """打开网页，返回Response对象"""
#     print("haha")
#     print(url)
#     # if delay:
#     # time.sleep(delay)
#     return session.get(url, headers=headers, verify=False)

class Zhihu(object):
    api = "https://www.zhihu.com/api/v4/members/"
    homePage = ""
    authorization = ""
    def __init__(self,name,password,loginType='email'):
        self.__name = name
        self.__pwd = password
        self.cookie = None
        self.api = "https://www.zhihu.com/api/v4/members/"
        self.__openUrl = r'https://www.zhihu.com/people/coldnorth/activities'
        if loginType == "email":
            login_data['email'] = self.__name
            self.__loginUrl = "https://www.zhihu.com/login/email"
        elif loginType == "phone":
            login_data['phone_num'] = self.__name
            self.__loginUrl = "https://www.zhihu.com/login/phone_num"
        else:
            raise ValueError("账号类型错误")
        login_data['password'] = self.__pwd

    def isLogin(self):
        """通过页面访问确认是否已经登入，这里使用设置页面的链接，因为所有用户通用"""
        loginTestUrl = host+"/settings/profile"
        r = session.get(loginTestUrl,headers = headers,verify = False)
        print r
        if 200 == int(r.status_code):
            return True
        else:
            return False

    def login(self):
        """使用账号id及pwd登入"""
        response = session.get(host, headers=headers, verify=False)
        print(response.text.encode(response.encoding).decode('gbk2312'))
        soup = bs(response, "html.parser")
        print(soup)
        xsrf = soup.find('input', {'name': '_xsrf'})['value']
        # print(xsrf)
        login_data['_xsrf'] = xsrf
        login_data['captcha'] = self.getCaptcha()
        login_data['phone_num'] = input("please input your phone num:")
        login_data['password'] = input("please input your password:")
        responed = session.post(self.__loginUrl, headers=headers, data=login_data)
        if 0 == responed.json()['r']:
            self.saveCookie()
            print("login successfully!")
            # print(responed.text)
        else:
            print("login failed!")

    def getCaptcha(self):
        """获取验证码，后续考虑引入图片自动识别"""
        t = str(int(time.time() * 1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = session.get(captcha_url, headers=headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        captcha = input("please input the captcha:")
        os.remove(captchaFile)
        return captcha

    def saveCookie(self):
        """cookies 序列化到文件,即把dict对象转化成字符串保存"""
        with open(cookieFile, "w") as output:
            self.cookies = session.cookies.get_dict()
            json.dump(self.cookies, output)
            print("=" * 100)
            print("已在同目录下生成cookie文件：", cookieFile)

    def makeConnection(self):
        """与目标服务器取得连接"""
        if self.isLogin():
            print("is already login")
            return
        self.cookie = self.loadCookie()
        if self.cookie:
            print("检测到cookie文件，直接使用cookie登录")
            session.cookies.update(self.cookie)
            print(self.__openUrl)
            responsed = self.urlOpen("https://www.zhihu.com/",headers = headers)
            soup = bs(responsed.text, "html.parser")
            print("已登陆账号： %s" % soup.find("span", class_="name").getText())
            # self.homePage = soup.find("a",class_="zu-top-nav-userinfo")['href']
            self.homePage = "coldnorth"
            if self.homePage:
                print(self.homePage)
            # print("current user： %s" % soup.find("title", {"data-reactid": "4"}).getText()[:-4])
            # print(soup)
            # loadFile(soup,"soup")
        else:
            print("没有找到cookie文件，将调用login方法登录一次！")
            self.login()
        print("authorization:")
        self.authorization = self.getAuthorization(self)
        if self.authorization:
            print(self.authorization)

    def loadCookie(self):
        """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
        if os.path.exists(cookieFile):
            print("=" * 100)
            with open(cookieFile, "r") as f:
                self.cookie = json.load(f)
                return self.cookie
        return None

    @staticmethod
    def urlOpen(url,headers = headers,delay = 0):
        """打开网页，返回Response对象"""
        # print("haha")
        # print(url)
        # print("headers:")
        # print(headers)
        if delay:
            time.sleep(delay)
        return session.get(url, headers = headers, verify=False)

    @staticmethod
    def getAuthorization(self):
        """获取登陆身份信息，用以获得网站服务器授权"""
        print("here")
        if self.cookie:
            authorization = "Bearer" + " " + self.cookie["z_c0"][1:-1]
            return authorization
        else:
            return None

    def getHomePage(self):
        if self.homePage:
            return self.homePage
        else:
            return None

class Usr(Zhihu):
    headers = headers
    usrInfo = {}
    def __init__(self,url_token):
        self.__url_token = url_token
        self.__peopleUrl = "/people/"+self.__url_token
        self.__homeUrl = host+self.__peopleUrl
        self.headers['Referer'] = 'https://www.zhihu.com'+self.__url_token
        self.__followee_referer = self.__homeUrl+"/following"
        self.__followee_url = Zhihu.api+self.__url_token+"/followees"
        self.__follower_referer = self.__homeUrl+"/followers"
        self.__follower_url = Zhihu.api + self.__url_token + "/followers"

    def getUsrInfo(self):
        # print(self.__homeUrl)
        # print(self.__url_token)
        # print(self.headers)
        print(self.__homeUrl)
        global mutex
        mutex.acquire()
        try:
            responsed = Zhihu.urlOpen(self.__homeUrl,headers = headers)
        except:
            responsed = Zhihu.urlOpen(r'https://www.zhihu.com/people/coldnorth', headers=headers)
        mutex.release()
        print("response : %s" %responsed.status_code)
        # print(responsed)
        soup = bs(responsed.text,"html.parser")
        # print(soup)
        loadFile(soup,"testPage")
        # try:
        #     self.usrInfo['url_token'] = soup.find("a",class_="Tabs-link")['href'][8:-11]
        # except:
        #     self.usrInfo['url_token'] = 'unknown'
        try:
            self.usrInfo['name'] = soup.find("span",class_="ProfileHeader-name").getText()
        except:
            self.usrInfo['name'] = 'unknown'
        try:
            self.usrInfo['headline'] = soup.find("span",class_="RichText ProfileHeader-headline").getText()
        except:
            self.usrInfo['headline'] = 'unknown'
        try:
            self.usrInfo['headinfo'] = soup.find("div",class_="ProfileHeader-info").getText()
        except:
            self.usrInfo['headinfo'] = 'unknown'
        if soup.find("svg",class_="Icon Icon--female"):
            self.usrInfo['sex'] = 'female'
        elif soup.find("svg",class_="Icon Icon--male"):
            self.usrInfo['sex'] = 'male'
        else:
            self.usrInfo['sex'] = 'unknown'
        # print(self.__url_token+"/answers")
        try:
            self.usrInfo['answercount'] = int(soup.find("a",href=self.__peopleUrl+"/answers").find("span").getText())
        except:
            self.usrInfo['answercount'] = 'unknown'
        try:
            self.usrInfo['asks'] = int(soup.find("a",href=self.__peopleUrl+"/asks").find("span").getText())
        except:
            self.usrInfo['asks'] = 'unknown'
        try:
            self.usrInfo['collections'] = int(soup.find("a",href=self.__peopleUrl+"/collections").find("span").getText())
        except:
            self.usrInfo['collections'] = 'unknown'
        try:
            self.usrInfo['pins'] = int(soup.find("a", href=self.__peopleUrl + "/pins").find("span").getText())
        except:
            self.usrInfo['pins'] = 'unknown'
        try:
            self.usrInfo['following'] = int(soup.findAll("div",class_="NumberBoard-value")[0].string)
            # print(self.usrInfo['following'])
        except:
            self.usrInfo['following'] = 0
        try:
            self.usrInfo['follower'] = int(soup.findAll("div", class_="NumberBoard-value")[1].string)
        except:
            self.usrInfo['follower'] = 0
        return self.usrInfo

    # def getUsrName
    def  getFollowees(self,zhihu):
        if self.usrInfo['following'] == 0:
            return set()
        followees = set()
        offset = 0
        nextUrl = self.__followee_url
        self.headers['Referer'] = self.__followee_referer
        self.headers['authorization'] = zhihu.authorization
        while offset < self.usrInfo['following']:
            offset += 10
            resp = Zhihu.urlOpen(url = nextUrl,headers = self.headers)
            for user in resp.json()['data']:
                # time.sleep(0.1)
                followees.add(user['url_token'])
                print("%s----->%s" % (self.usrInfo['name'], user['url_token']))
            nextUrl = resp.json()['paging']['next']
        return followees

    def getFollowers(self,zhihu):
        if self.usrInfo['follower'] == 0:
            return set()
        followers = set()
        offset = 0
        nextUrl = self.__follower_url
        self.headers['Referer'] = self.__follower_referer
        self.headers['authorization'] = zhihu.authorization
        while offset < self.usrInfo['follower']:
            offset += 10
            resp = Zhihu.urlOpen(url = nextUrl,headers = self.headers)
            for user in resp.json()['data']:
                # time.sleep(0.1)
                followers.add(user['url_token'])
                print("%s<-----%s"%(self.usrInfo['name'],user['url_token']))
            nextUrl = resp.json()['paging']['next']
        return followers







