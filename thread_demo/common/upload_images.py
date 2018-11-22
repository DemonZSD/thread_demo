#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 13:42
# @Author  : Zhu Shidong
# @Site    : 
# @File    : upload_images.py
# @Software: PyCharm
# @Function:
from fabric.api import put, sudo, cd
import os
from upload_base import UploadBase
from utils.log_decorator import exec_time_decorator


class UploadImages(UploadBase):
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

    # @exec_time_decorator
    def upload_images(self, image_name):
        local_path = os.path.join(os.path.dirname(__file__),
                                  os.pardir, os.pardir, 'source', 'images', image_name)
        sudo('mkdir -p %s' % self._remote_path)
        with cd(self._remote_path):
            print self._remote_path
            put(local_path=local_path, remote_path=self._remote_path, use_sudo=True)


