#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 16:42
# @Author  : Zhu Shidong
# @Site    : 
# @File    : unit_test.py
# @Software: PyCharm
# @Function:
from fabric.api import put, sudo, execute, roles, cd
import os
from thread_demo.common import machine
from fabric.api import env
from utils.log_decorator import  exec_time_decorator
from thread_demo.common.upload_images import UploadImages
from thread_demo.common.docker_load import ImageLoad
import threading
import json, time
from utils.const import IMAGES_CONF_FILE_PATH
from utils.log_decorator import logger


def images_conf_parse():
    with open(IMAGES_CONF_FILE_PATH, 'r') as f:
        images_version = json.load(f)
        return images_version


def common_upload_image(
        up_image, image_load, docker_images_key, docker_images_value, regist_url):
    """

    :param up_image: UploadImages instance
    :param image_load: ImageLoad instance
    :param docker_images:
    :param regist_url:
    :return:
    """
    origin_hub = "192.168.0.124:80"
    old_docker_image = "{origin_hub}/{name}".format(
        name=docker_images_value,
        origin_hub=origin_hub
    )
    new_docker_image = "{registry_url}/{name}".format(
        registry_url=regist_url,
        name=docker_images_value
    )
    image_file_name = "{name}.tar".format(
        name=docker_images_key
    )
    up_image.upload_images(image_file_name)
    image_load.docker_load(image_file_name)
    image_load.docker_tag(old_docker_image, new_docker_image)
    image_load.docker_push(new_docker_image)
    return "new_docker_image"

@roles('host1')
@exec_time_decorator
def upload_images_with_no_paraller(regist_url):
    up_image = UploadImages()
    image_load = ImageLoad()
    # docker_images = 'test1.tar'

    remote_path_str = machine.REMOTE_UPLOAD_DIR
    up_image.remote_path = remote_path_str
    images_versions = images_conf_parse()

    for images_key, images_value in images_versions.items():
        common_upload_image(up_image, image_load, images_key, images_value, regist_url)

@roles('host1')
@exec_time_decorator
def upload_thread_pool(regist_url, worker_count):
    import concurrent.futures
    images_versions = images_conf_parse()
    up_image = UploadImages()
    image_load = ImageLoad()
    remote_path_str = machine.REMOTE_UPLOAD_DIR
    up_image.remote_path = remote_path_str
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(
            common_upload_image, *(up_image, image_load, images_key, images_value, regist_url)
        ) for images_key, images_value in images_versions.items()]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


@roles('host1')
@exec_time_decorator
def upload_image_with_coroutine(regist_url, split_num):
    import gevent
    # from gevent import monkey
    # monkey.patch_all()
    up_image = UploadImages()
    image_load = ImageLoad()
    remote_path_str = machine.REMOTE_UPLOAD_DIR
    up_image.remote_path = remote_path_str

    images_versions = images_conf_parse()

    images_list = dict()
    images_count = 0
    for images_key, images_value in images_versions.items():
        if str(images_count % split_num) not in images_list.keys():
            images_list[str(images_count % split_num)] = []
        images_list[str(images_count % split_num)].append(images_key)
        images_count += 1
    for key, value in images_list.items():
        # spawn 启动协程：参数为函数名称 upload_image，参数名称up_image, image_load, i, regist_url
        tasks = [gevent.spawn(common_upload_image,
                              up_image, image_load,
                              images_key, images_versions.get(images_key),
                              regist_url) for images_key in value]
        # joinall 停止协程
        gevent.joinall(tasks)

@roles('host1')
@exec_time_decorator
def upload_images_with_thread(regist_url, split_num):
    up_image = UploadImages()
    image_load = ImageLoad()
    remote_path_str = machine.REMOTE_UPLOAD_DIR
    up_image.remote_path = remote_path_str

    images_versions = images_conf_parse()

    images_list = dict()
    images_count=0
    for images_key, images_value in images_versions.items():
        if str(images_count % split_num) not in images_list.keys():
            images_list[str(images_count % split_num)] = []
        images_list[str(images_count % split_num)].append(images_key)
        images_count+=1

    # print images_list
    threads = []
    for key, value in images_list.items():
        for images_key in value:
            threads.append(threading.Thread(
                target=common_upload_image, args=(
                    up_image, image_load,
                    images_key,
                    images_versions.get(images_key),
                    regist_url)))

        for thread_item in threads:
            thread_item.start()

        for thread_item in threads:
            thread_item.join()
        threads = []

    print 'upload_images_with_thread done'

@roles('host1')
def delete_registry():
    with cd('/deploy'):
        sudo("docker stop $(docker ps -a | grep registry | awk '{print $1}') && \
              docker rm $(docker ps -a | grep registry | awk '{print $1}') && \
              rm -rf /mnt/docker && \
              docker run -d --restart=always --name registry -v $PWD/certs:/certs -v /mnt:/var/lib/registry \
	          -e REGISTRY_HTTP_ADDR=0.0.0.0:443\
	          -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt \
	          -e REGISTRY_HTTP_TLS_KEY=/certs/registry.key  \
	          -p 443:443 registry:2")
        sudo('rm -rf /deploy/images/*')



def count_time_use(func,try_time, *args):
    total_time_thread = 0
    min_time_thread = 9999999
    max_time_thread = 0
    for i in range(try_time):
        time_thread_start = time.time()
        execute(func, *args)
        max_time_thread = max((time.time() - time_thread_start), max_time_thread)
        min_time_thread = min((time.time() - time_thread_start), min_time_thread)
        total_time_thread = total_time_thread + (time.time() - time_thread_start)
        execute(delete_registry)
    logger.info("average_time_thread: {value} ".format(value=float(total_time_thread) / try_time))
    logger.info("max_time_thread: {value} ".format(value=max_time_thread))
    logger.info("min_time_thread: {value} ".format(value=min_time_thread))


if __name__ == '__main__':
    registry_url = '192.168.0.115'
    try_time = 10
    worker_count = 3
    count_time_use(upload_thread_pool, try_time, *(registry_url, worker_count))
    count_time_use(upload_images_with_thread, try_time, *(registry_url, worker_count))
