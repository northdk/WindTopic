#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'North D.K.'
"""                                                * * * * *
//                            _ooOoo_              * 佛曰: *
//                           o8888888o             * * * * *
//                           88" . "88                      ~ 写字楼里写字间，写字间里程序员；
//                           (| -_- |)                      ! 程序人员写程序，又拿程序换酒钱.
//                            O\ = /O                       @ 酒醒只在网上游，酒醉还来网下眠；
//                        ____/`---'\____                   # 醉醉醒醒日复日，改改写写年复年。
//                      .   ' \ | | / `.                    $ 唯愿老死键盘前，不敢栖身迭代间；
//                       / \||| : |||/  \                   % 奔驰宝马贵者趣，公交自行程序员。
//                     / _||||| -:- |||||- \                ^ 运营笑我太疯癫，我笑产品看不穿；
//                       | | \ \ - / / | |                  & 不见满城温柔乡，何处容得程序员？
//                     | \_| ''\---/'' | |
//                      \ .-\__ `-` ___/-. /
//                   ___`. .' /--.--\ `. . __
//                ."" '< `.___\_<|>_/___.' >'"".
//               | | : `- \`.;`\ _ /`;.`/ - ` : | |
//                 \ \ `-. \_ __\ /__ _/ .-` / /
//         ======`-.____`-.___\_____/___.-`____.-'======
//                            `=---='
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    佛祖保佑             永无BUG

"""

"""
#   FileName    : spider.py
#   Description : use zhihu module to get data
#                  use mysql with pymysql to store (millions usr data,in a big table)
"""
from zhihu import  Zhihu
from zhihu import Usr

import threading
import time

usr_name = '18681821674'
pswd = 'north456123789'
zh = Zhihu(usr_name,pswd,loginType='phone')

testCount = -1

# fileNum = 0
# usrIndex = 0
# fileCount = 0
usrQueue = set()    #待爬取用户队列
everQueue = set()   #已爬取用户队列
tmpUsr = set()      #爬取信息缓存
everInfo = set()    #已爬取信息队列
usrStore = list()   #待存储队列
tmpStore = list()   #存储缓存队列

mutex = threading.Lock()

saveFile = "usersData4\{0}.text" #存储文件
saveOffset = 0                  #存储文件命名偏移

class Spider(object):
    usr_name = ''
    pswd = ''  # use getpass.getpass to get password，to avoid back echo
    users = set()
    uQueue = set()
    usrIndex = 0
    usrSaveFile = 'usersData\{0}.text'
    fileNume = 0
    workFile = ''
    def __init__(self):
        self.__zh = Zhihu(self.usr_name, self.pswd, loginType='phone')
        self.__zh.makeConnection()
        firstUsrUrl =  self.__zh.getHomePage()
        firstUsr = Usr(firstUsrUrl)
        fInfo = firstUsr.getUsrInfo()
        # print(fInfo)
        self.workFile = self.usrSaveFile.format(str(self.fileNume))
        with open(self.workFile,"w") as f:
            f.write('('+str(self.usrIndex)+')')
            self.usrIndex += 1
            for key in fInfo:
                f.write(key)
                f.write(':')
                f.write(str(fInfo[key]))
                f.write('; ')
            f.write('\n')
            f.close()
        # print(firstUsr.getFollowees(self.__zh))
        for usr in firstUsr.getFollowees(self.__zh):
            self.users.add(usr)
        print(self.users)

    def getUsrs(self):
        for u in self.users:
            self.uQueue.add(u)
        self.users.clear()
        self.reFreshUsrs()

    def reFreshUsrs(self):
        for u in self.uQueue:
            newU = Usr(u)
            followees = newU.getFollowees(self.__zh)
            if followees != None:
                for newuu in followees:
                    self.users.add(newuu)
            followers = newU.getFollowers(self.__zh)
            if followers != None:
                for newu in followers:
                    self.users.add(newu)

    def writeUsrs(self):
        print('now write %d' %self.usrIndex)
        if len(self.uQueue) == 0:
            print('e')
            self.getUsrs()
            # yield self.writeUsrs()
            return
        for u in self.uQueue:
            print('index is:%d' % self.usrIndex)
            print(u)
            newuu = Usr(u)
            fInfo = newuu.getUsrInfo()
            if self.usrIndex > 1000:
                self.fileNume += 1
                self.usrIndex = 0
            self.usrIndex += 1
            self.workFile = self.usrSaveFile.format(str(self.fileNume))
            with open(self.workFile,'a') as f:
                f.write('('+str(self.usrIndex)+')')
                self.usrIndex += 1
                for key in fInfo:
                    try:
                        f.write(key)
                        f.write(':')
                        f.write(str(fInfo[key]))
                        f.write(' ')
                    except:
                        print("cannot write file")
                f.write('\n')
                f.close()
        # yield self.writeUsrs()

def saveData():
    global  saveFile,saveOffset,usrStore
    saveOffset += 1
    tmpIndex = 0
    workFile = saveFile.format(str(saveOffset))
    with open(workFile,"a") as f:
        for uInfo in usrStore:
            tmpIndex += 1
            print("wrintting info~~~~~~~~~~~~")
            print(uInfo)
            try:
                f.write('(' + str(tmpIndex) + ')')
                for key in uInfo.keys():
                    f.write("%s:%s," %(key,uInfo[key]))
                f.write('\n')
            except:
                continue
        f.close()
    usrStore.clear()

def getInfo():
    global mutex,zh
    while True:
        global tmpUsr
        print(threading.current_thread().name)
        # time.sleep(1)
        # uQueue = set()
        # if uQueue == None:
        if len(tmpUsr) == 0:
            time.sleep(1)
            continue
        mutex.acquire()
        print("tmp length is:%d" %len(tmpUsr))
        uQueue = tmpUsr.copy()
        print("in %s uQueue length is:%d" %(threading.current_thread().name,len(uQueue)))
        print(uQueue)
        tmpUsr.clear()
        mutex.release()
        # if len(everInfo) > 20000:
        #     everInfo.clear()
        for u in uQueue:
            print("parse usr with:%s" %u)
            # if u in everInfo:
            #     continue
            # try:
            newu = Usr(u)
            uInfo = dict()
            # uInfo = newu.getUsrInfo()
            uInfo['url_token'] = u
            try:
                uInfo.update(newu.getUsrInfo())
            except:
                uInfo['info'] = "uknown"
            print(uInfo)
            mutex.acquire()
            tmpStore.append(uInfo)
            mutex.release()
        uQueue.clear()
        time.sleep(0.1)

def getUsr(delay = 1):
    # if delay:
    #     time.sleep(delay)
    # if len(usrStore) > 10000:
    #     return
    global  mutex,zh
    while True:
        global usrQueue,tmpUsr
        tmpQueue = set()
        print(threading.current_thread().name)
        print("usrQueue length is:%d" %len(usrQueue))
        # if len(everQueue) > 20000:
        #     everQueue.clear()
        # if len(usrQueue)>1000:
        #     continue
        if len(usrQueue) == 0:
            usrQueue.add("nordenbox")#防止队列为空
        for u in usrQueue:
            # if u in everQueue:
            #     continue
            try:
                newusr = Usr(u)
                newusr.getUsrInfo()
                # everQueue.add(u)
                tmpQueue = tmpQueue | newusr.getFollowees(zh) | newusr.getFollowers(zh)
                print(tmpQueue)
                mutex.acquire()
                tmpUsr = tmpQueue | tmpUsr
                print("tmpUsr length is:%d" % len(tmpUsr))
                mutex.release()
                # print(newusr.getFollowees(zh))
            finally:
                time.sleep(10)
        usrQueue.clear()
        usrQueue = usrQueue | tmpQueue
        # tmpQueue.clear()
        print("usrQueue length:%d" %len(usrQueue))
        # time.sleep(delay)

def saveUsr(delay = 0):
    # if delay:
    #     time.sleep(dealy)
    global mutex,testCount
    countTime = 0
    # pFlag = 1
    while True:
        global usrIndex,usrStore,tmpStore
        print(threading.current_thread().name)
        time.sleep(1)
        print("usrStore length is %d" %len(usrStore))
        if len(usrStore) > 999:
            saveData()
        mutex.acquire()
        for uInfo in tmpStore:
            usrStore.append(uInfo)
            tmpStore.clear()
        mutex.release()
        # print(usrIndex)


def working():
    global mutex, usrIndex
    while True:
        print(threading.current_thread().name)
        # if n%2 == 0:
        #     print(n)
        mutex.acquire()
        usrIndex += 1
        mutex.release()
        print(usrIndex)
        time.sleep(1)


if __name__ == '__main__':
    print(__author__)

    zh.makeConnection()
    usrQueue.add(zh.getHomePage())#自己的url_token作为第一个元素加入用户队列
    print(usrQueue)
    # testThread = threading.Thread(target=working, name='testThread')
    getThread = threading.Thread(target=getUsr,name='getThread')
    saveThread = threading.Thread(target=saveUsr,name='savaThread')
    # getInfoThread = threading.Thread(target=getInfo,name='getInfoThread')

    dkThreads = list()
    dkThreads.append(saveThread)
    dkThreads.append(getThread)
    # dkThreads.append(getInfoThread)

    getInfoThread = "getInfoThread{0}"
    getInfoThreadOffset = 0
    for n in range(50):
        getInfoThread_t = getInfoThread.format(str(getInfoThreadOffset))
        getInfoThread_t = threading.Thread(target=getInfo,name=getInfoThread_t)
        dkThreads.append(getInfoThread_t)
        getInfoThreadOffset += 1


    for t in dkThreads:
        t.start()









