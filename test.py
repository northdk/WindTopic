#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import multiprocessing
from multiprocessing import Queue
# import Queue
import threading
import time

s = 'here'

def printNum(n = 0):
    n = que.get()
    # print(que.empty())
    print(n+1)

def testGlobal():
    global s,d
    d = 'there'
    print(s)
    print(d)
    # d = "there"



if __name__ == '__haha__':
    global que
    que = Queue(maxsize=100)
    # que.put(n for n in range(100))
    # print(que.empty())
    for n in range(100):
        que.put(n)
    print(que.full())

    t = threading.Thread(target=printNum(), name='printNum')
    t.start()
    for n in range(100):
        t.join(10)
        # t.start()




class WorkManager(object):
    def __init__(self, work_num=1000, thread_num=2):
        self.work_queue = Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        初始化工作队列
    """

    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    """
        添加一项工作入队
    """

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))  # 任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive(): item.join()
        print("haha")


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                # print(do,args)
                do(args)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break

                # 具体要做的任务


def do_job(args):
    time.sleep(0.1)  # 模拟处理时间
    # print()
    print("hello!",list(args))


if __name__ == '__main__':
    start = time.time()
    work_manager = WorkManager(10000, 10)  # 或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    print("cost all time: %s" % (end - start))

