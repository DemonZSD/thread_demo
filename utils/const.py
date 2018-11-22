#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 13:59
# @Author  : Zhu Shidong
# @Site    : 
# @File    : const.py
# @Software: PyCharm
# @Function:
import os, time

time_str = time.strftime("%Y-%m-%d", time.localtime())
LOG_FILE = os.path.join(os.path.dirname(__file__), os.pardir, 'source', 'logs') + '/' + time_str + '.log'
IMAGES_CONF_FILE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'source', 'conf', 'images.json')