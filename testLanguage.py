#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
#   FileName:testMySQL.py
#   Author: North D.K.
#                   to test python language,
#                   to learn how to use python more easily
'''

class Tdk(object):
    id = 1
    def __init__(self):
        self.name = "dukun"

class Demo(Tdk):
    id = 9
    def __init__(self):
        Tdk.__init__(Tdk)
        self.__sex = "male"
        self.__id = id
    def printInfo(self):
        print(Tdk.name)
        print(self.__sex)

if __name__ == '__main__':
    demo = Demo()
    tdk = Tdk()
    demo.printInfo()
