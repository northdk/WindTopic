#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
#   FileName:testMySQL.py
#   Author: North D.K.
#                   to test mysql with module pymysql
'''

import pymysql
import time

if __name__ == '__main__':
    print("hello, mysql!")
    #建立数据库链接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='hellomysql')
    #创建游标对象
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute("USE hellomysql")
    print("e")
    id = 1
    name = 'hahaha'
    start = time.clock()
    while id < 0:
        try:
            cur.execute("INSERT INTO new_table (idnew_table,name) VALUE (%s,%s)",(id,name))
            cur.connection.commit()
        except pymysql.err.IntegrityError as e:
            print(e)
        id += 1
    # # SQL查询
    cur.execute("select* from new_table")
    # # 获取数据,fetchone,fetchmany,fetchall
    # row_1=cur.fetchmany(-5)
    # print(row_1)
    cur.scroll(9999,mode='relative')
    row_1 = cur.fetchall()
    print(type(row_1))#数据库查询返回的是一个list
    print(row_1)
    end = time.clock()
    print("use time : %f" %(end - start))
    print("now will close db!")
    cur.close()
    conn.close()

    a = 24
    print(type(a))
