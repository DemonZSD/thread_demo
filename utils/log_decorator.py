#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 13:52
# @Author  : Zhu Shidong
# @Site    : 
# @File    : log_decorator.py
# @Software: PyCharm
# @Function:
import logging
import const
from functools import wraps
import time


fmt = "%(asctime)s - %(levelname)s - %(message)s"
err_fmt = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
date_fmt = "%Y-%b-%d %H:%M:%S"

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt, date_fmt)
handler = logging.FileHandler(const.LOG_FILE)
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_decorator(func):
    """
    日志修饰器
    :param func:
    :return:
    """
    @wraps(func)
    def with_logger(*args, **kwargs):
        func_name = func.__name__
        arg_names = func.func_code.co_varnames[:func.func_code.co_argcount]  # 参数name
        params_str =  func_name + "(" + ', '.join(
            '%s=%r' % entry
            for entry in
            zip(arg_names, args[:len(arg_names)]) + [("args", list(args[len(arg_names):]))] + [("kwargs", kwargs)]) + ")"
        logger.debug(params_str)
        # print params_str
        try:
            out = func(*args, **kwargs)
            return out
        except:
            logger.exception(
                'exec func {func_name} failed'.format(func_name=func.__name__))
        logger.info('done exec func %s' % func.__name__)
    return with_logger


def exec_time_decorator(func):
    """
    日志修饰器
    :param func:
    :return:
    """
    @wraps(func)
    def time_logger(*args, **kwargs):
        func_name = func.__name__
        arg_names = func.func_code.co_varnames[:func.func_code.co_argcount]  # 参数name
        params_str =  func_name + "(" + ', '.join(
            '%s=%r' % entry
            for entry in
            zip(arg_names, args[:len(arg_names)]) + [("args", list(args[len(arg_names):]))] + [("kwargs", kwargs)]) + ")"
        logger.debug(params_str)
        # print params_str
        use_time = 0
        try:
            start_time = time.time()
            out = func(*args, **kwargs)
            end_time = time.time()
            use_time = str(end_time-start_time)
            logger.debug('exec func {params_str} with time: {exec_time}'.format(
                params_str=params_str, exec_time=use_time))
            return out
        except:
            logger.exception(
                'exec func {func_name} failed'.format(func_name=func.__name__))
        logger.debug('exec func {params_str} with time: {exec_time}'.format(
            params_str=params_str, exec_time=use_time))
    return time_logger


@log_decorator
def test(filename, *args, **kwargs):
    pass

if __name__ == '__main__':
    test('1.txt',(0,1,1,3), aa={'a':1, 'b':2})