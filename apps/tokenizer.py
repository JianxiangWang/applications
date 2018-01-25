# coding=utf-8
"""
The tokenizer file.

Authors: Wang Jianxiang (w51141201062@163.com)
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
