#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 15:52
# @Author  : Zhu Shidong
# @Site    : 
# @File    : upload_base.py
# @Software: PyCharm
# @Function:

class UploadBase(object):
    def __init__(self):
        self._remote_path = ''

    @property
    def remote_path(self):
        return self._remote_path

    @remote_path.setter
    def remote_path(self, value):
        if not isinstance(value, str):
            raise ValueError('remote_path must be a string!')
        if value and len(value) > 0:
            self._remote_path = value
        else:
            raise ValueError('remote_path can not be None')