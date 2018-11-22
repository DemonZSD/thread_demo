#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 13:46
# @Author  : Zhu Shidong
# @Site    : 
# @File    : docker_load.py
# @Software: PyCharm
# @Function:

from fabric.api import cd, sudo
import machine
from utils.log_decorator import exec_time_decorator


class ImageLoad():
    """
    镜像上传tag push
    """
    @staticmethod
    # @exec_time_decorator
    def docker_load(docker_images):
        with cd(machine.REMOTE_UPLOAD_DIR):
            print "docker load {docker_images}".format(docker_images=docker_images)
            sudo('docker load < {docker_images}'.format(docker_images=docker_images))

    @staticmethod
    # @exec_time_decorator
    def docker_tag(old_tag, new_tag):
        print "docker tag {old_tag} {new_tag}".format(old_tag=old_tag, new_tag=new_tag)
        sudo('docker tag {old_tag} {new_tag}'.format(old_tag=old_tag, new_tag=new_tag))

    @staticmethod
    # @exec_time_decorator
    def docker_push(docker_images):
        print "docker push {docker_images}".format(docker_images=docker_images)
        sudo('docker push {docker_images}'.format(docker_images=docker_images))