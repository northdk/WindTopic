#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
引入自定义模块的两种方式
from getSources import myPrint
import getSources -> getSources.myPrint()
'''

__author__ = 'North D.K.'

import requests
from bs4 import BeautifulSoup as bs
import json
import time
import os
import sys
import pymysql
import re
from urllib import request as urlReq
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

captchaFile = os.path.join(sys.path[0], "captcha.jpg")
cookieFile = os.path.join(sys.path[0], "cookie")
session = requests.session()
headers = {
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'Accept-Language: zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.zhihu.com',
}

login_data = {'phone_num': '18681821674',
             'password': 'north456123789',
             'Referer': 'https://www.zhihu.com/',
             'remember_me': 'true',
              }

def zhihuOpen(url,headers,delay=0):
    """打开网页，返回Response对象"""
    if delay:
        time.sleep(delay)
    return session.get(url, headers = headers, verify=False)

def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    captcha = input("please input the captcha:")
    os.remove(captchaFile)
    return captcha

def loadCookie():
    """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
    if os.path.exists(cookieFile):
        print("=" * 100)
        with open(cookieFile, "r") as f:
            cookie = json.load(f)
            return cookie
    return None

def saveCookie():
    """cookies 序列化到文件
    即把dict对象转化成字符串保存
    """
    global session
    with open(cookieFile, "w") as output:
        cookies = session.cookies.get_dict()
        json.dump(cookies, output)
        print("=" * 100)
        print("已在同目录下生成cookie文件：", cookieFile)

def zhihuLogin():
    response = session.get('http://www.zhihu.com', headers=headers, verify=False).text
    print(response)
    soup = bs(response, "html.parser")
    xsrf = soup.find('input', {'name': '_xsrf'})['value']
    print(xsrf)
    login_data['_xsrf'] = xsrf
    login_data['captcha'] = get_captcha()
    responed = session.post('https://www.zhihu.com/login/phone_num', headers=headers, data=login_data)
    if 0 == responed.json()['r']:
        saveCookie()
        print(responed.text)
    else:
        print("login failed!")

def getFollowing(url,hearders,folder):#the url should be usr homepage
    host = "https://www.zhihu.com/api/v4/members/"
    referer = "https://www.zhihu.com/people/"
    usrHomeUrl = host+url+"?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"
    headers['Referer'] = referer+url
    startUrl = host + url + "/followees?offset={0}"
    usrHomeJson = zhihuOpen(usrHomeUrl,headers).json()
    followee_num = usrHomeJson['following_count']
    if followee_num:
        print(followee_num)
    workFolder = folder+'%s.jpg'%usrHomeJson['name']
    print(workFolder)
    urlReq.urlretrieve(usrHomeJson['avatar_url'], workFolder)
    headers['Referer'] = host+url+"/following"
    offset = 0
    nextUrl = startUrl.format(str(offset))
    while offset < int(followee_num):
        # nextUrl = startUrl.format(str(offset))
        tmpResp = zhihuOpen(nextUrl,headers)
        # print(tmpResp.json()['data'])
        respList = tmpResp.json()['data']
        if respList==None:
            return
        for usrInfo in respList:
            print("save %s pic" % usrInfo['name'])
            try:
                urlReq.urlretrieve(usrInfo['avatar_url'], folder+"%s-%s.jpg" %(usrInfo['name'],usrInfo['url_token']))
            except:
                print("the usr url is invalid!")
            time.sleep(1)
        offset += 10
        nextUrl = tmpResp.json()['paging']['next']
        print("nextGetUrl is:"+nextUrl)



    # following = zhihuOpen(followingUrl,headers=headers)
    # # print(soupFollowing)
    # imgList = soupFollowing.findAll("img")
    # print(imgList)
    # for img in imgList:
    #     if 'alt' in img.attrs:
    #         print("haha")
    #         print(img.attrs['src'])
    #         imgFile = img.attrs['alt']
    #         urlReq.urlretrieve(img.attrs['src'], '%s.jpg' % imgFile)
    # else:
    #         print("eee")
    #         print(img)

# headers2 = {
#     'Connection': 'keep-alive',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'Accept-Language: zh-CN,zh;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Host': 'www.zhihu.com',
#     'Referer':'https://www.zhihu.com/people/coldnorth/following'
# }


if __name__ == '__main__':
    # global session
    cookie = loadCookie()
    if cookie:
        print("检测到cookie文件，直接使用cookie登录")
        session.cookies.update(cookie)
        responsed = zhihuOpen("https://www.zhihu.com/people/coldnorth/", headers)
        # with open("zhihu_loginPage.html",'wb') as f:
        #     f.write(responsed.content)
        soup = bs(responsed.text, "html.parser")
        # with open("soup.html", 'wb') as f:
        #     f.write(soup.encode())
        #     f.close()
        # print("已登陆账号： %s" % soup.find("span", class_="name").getText())
        print("current user： %s" % soup.find("title", {"data-reactid":"4"}).getText()[:-4])
        # usrUrl = "http://www.zhihu.com"+soup.find("div",class_="top-nav-profile").find("a").attrs['href']
        # usrResp = zhihuOpen(usrUrl,headers)
        # usrSoup = bs(usrResp.text,"html.parser")
        # print("准备获取 %s 的关注列表" % usrSoup.find("title").getText()[:-4])
    else:
        print("没有找到cookie文件，将调用login方法登录一次！")
        zhihuLogin()

    r = zhihuOpen("https://www.zhihu.com/api/v4/members/coldnorth/followees?offset=0",headers=headers)
    print(r.status_code)

    r = zhihuOpen("https://www.zhihu.com/api/v4/members/ze.ran/followers",headers=headers)
    totals = int(r.json()['paging']['totals'])
    print(totals)
    offset = 0
    usrCount = 0
    startUrl = "https://www.zhihu.com/api/v4/members/ze.ran/followers?offset={0}&limit=20"
    with open("zeran.txt","a") as f:
        beginTime1 = time.clock()
        beginTime2 = time.time()
        while offset < totals:
            nextUrl = startUrl.format(str(offset))
            r = zhihuOpen(nextUrl,headers=headers)
            f.write(" %d:" % offset)
            # f.write(type(r.json()['data']))
            for u in r.json()['data']:
                usrCount += 1
                print(usrCount)
                f.write("%s," %u['url_token'])
            f.write('\n')
            offset += 20
        endTime1 = time.clock()
        endTime2 = time.time()
        print(endTime1 - beginTime1)
        print(endTime2 - beginTime2)
        f.close()



    """


    headers["Referer"] = "https://www.zhihu.com/?next=/people/coldnorth/following"
    following = zhihuOpen("https://www.zhihu.com/people/coldnorth/following",headers)


    headers2 = headers
    headers2["Referer"] = "https://www.zhihu.com/people/coldnorth/following"
    headers2["authorization"] = "Bearer"+" "+cookie["z_c0"][1:-1]
    print(headers2["authorization"])

    startUrl = "https://www.zhihu.com/api/v4/members/coldnorth/followees?offset={0}"
    offset = 0
    nextUrl = startUrl.format(str(offset))
    usrList = dict()
    while nextUrl:
        tmpResp = zhihuOpen(nextUrl, headers2)
        print(tmpResp.json()["data"])
        respList = tmpResp.json()["data"]
        for usrInfo in respList:
            print("save %s pic" %usrInfo['name'])
            urlReq.urlretrieve(usrInfo['avatar_url'],"picture\%s-%s.jpg" \
                               %(usrInfo['name'],usrInfo['url_token']))
            usrList[usrInfo['name']] = usrInfo['url_token']
            try:
                os.mkdir('picture\%s-%s' %(usrInfo['name'],usrInfo['url_token']))
            except:
                print("folder %s:%s is already exists!"%(usrInfo['name'],usrInfo['url_token']))
            # try:
            #     os.mkdir('picture\%s' %usrInfo['name'])
            # except:
            #     os.mkdir('picture\%s' % usrInfo['name']+"-s")
        offset += 10
        if offset > 28:
            nextUrl = None
        else:
            nextUrl = startUrl.format(str(offset))
        print("next is:",nextUrl)
    print(usrList)
    for usr in usrList.keys():
        print("visit "+usr)
        folder = "picture\\"+usr+"-"+usrList[usr]+"\\"
        # print(folder)
        getFollowing(usrList[usr],headers2,folder)
    """


    # tmpH = session.get("https://www.zhihu.com/people/coldnorth/followees",headers=headers,verify=False)
    #
    # sp = bs(tmpH.content, "lxml")



    # ne = sp.find("div",attrs={'data-reactid':'18'})["data-state"]
    # # if ne:
    # #     print(ne)
    # dicttt = json.loads(ne)
    # if dicttt:
    #     print(dicttt)
    # print(dicttt["people"]["followingByUser"]["coldnorth"]["next"])










#print(responed)


# soup = bs(zhihuOpen(r"https://www.zhihu.com/people/coldnorth/activities",headers).text,"html.parser")
# startData = zhihuOpen("https://www.zhihu.com/people/coldnorth/activities",headers)
#print(soup)

# 直接这么调用会需要身份验证
# apiUrl = "https://www.zhihu.com/api/v4/members/coldnorth/followees?per_page=5&include=data%5B%2A%5D.answer_count%2Carticles_count%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=25"
# print(apiUrl)
# newSoup = bs(zhihuOpen(apiUrl,headers).text,"html.parser")
# print(newSoup)




# with open("zhihuFollowing.html","w",encoding='utf-8') as f:
#     f.write(str(soupFollowing))
#     f.close()