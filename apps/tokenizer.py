# coding=utf-8
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
"""
The XXX file.

Authors: Wang Jianxiang (wangjianxing01@baidu.com)
"""
from interface import AppInterface
import jieba
import json


class Tokenizer(AppInterface):

    def __init__(self):
        super(Tokenizer, self).__init__()

    def response(self, input_data):
        input_text = input_data.get("input", "")
        result = json.dumps(list(jieba.cut(input_text)), ensure_ascii=False)
        output = {
            "input": input_text,
            "output": result
        }
        return output
