#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 11:27
# @Author  : zhushidong
# @Site    : 
# @File    : threading_demo.py
# @Software: PyCharm
# @Function:

import threading
import time

exitFlag = 0

class MyThread(threading.Thread):

    def __init__(self, thread_id, thread_name, delay):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.delay = delay

    def run(self):
        print("Starting" +  self.thread_name)
        # TODO do something
        print_time(self.thread_name, 5, self.delay)
        print ("End" + self.thread_name)


def print_time(thread_name, counter, delay):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


if __name__ == '__main__':
    thread1 = MyThread(1, 'thread-1', 1)
    thread2 = MyThread(1, 'thread-2', 2)
    thread1.start()
    thread2.start()
    print("Exiting Main Thread")

