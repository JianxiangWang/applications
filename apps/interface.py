# coding=utf-8
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
"""
Authors: Wang Jianxiang (wangjianxing01@baidu.com)
"""
import abc


class AppInterface(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def response(self, input_data):
        pass


if __name__ == '__main__':
    a = AppInterface()