#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 9:24
# @Author  : Zhu Shidong
# @Site    : 
# @File    : coroutine_test_one.py
# @Software: PyCharm
# @Function: 测试协程

import gevent
from gevent import monkey;monkey.patch_all()
import urllib2

def get_body(i):
    print 'start %s' % i
    urllib2.urlopen("http://www.baidu.com")
    print 'end %s' % i

# spawn 启动协程：参数为函数名称get_body，参数名称i
tasks = [gevent.spawn(get_body, i) for i in range(3)]
# joinall 停止协程
gevent.joinall(tasks)

