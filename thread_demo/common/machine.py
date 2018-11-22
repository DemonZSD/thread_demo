#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 13:43
# @Author  : Zhu Shidong
# @Site    : 
# @File    : machine.py.py
# @Software: PyCharm
# @Function:

from fabric.api import env

env.roledefs = {
    'host1':['root@192.168.0.115']
}


env.passwords = {
    'root@192.168.0.115:22':'123456'
}

REMOTE_UPLOAD_DIR = "/deploy/images"