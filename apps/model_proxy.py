# coding=utf-8
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
"""
The XXX file.

Authors: Wang Jianxiang (wangjianxing01@baidu.com)
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import json
from interface import AppInterface
from apps.lstm_crf_model import LstmCrfInference, LstmCrfModelMeta, LstmCrfInputPackage


class SlotFillingProxy(AppInterface):

    def __init__(self, model_dir):
        super(SlotFillingProxy, self).__init__()
        self.model_path = os.path.join(model_dir, 'model.pb')
        self.word_path = os.path.join(model_dir, 'featureIdMap.word')
        self.tag_path = os.path.join(model_dir, 'featureIdMap.tag')
        self.inference = LstmCrfInference(
                            LstmCrfModelMeta(self.model_path, self.word_path, self.tag_path))

    def response(self, input_data):
        query = input_data.get("input", "")
        _, viterbi_sequences, seq_lengths = self.inference.inference(LstmCrfInputPackage(query))
        output = {
            "input": query,
            "output": json.dumps(viterbi_sequences, ensure_ascii=False)
        }
        return output


if __name__ == '__main__':
    proxy = SlotFillingProxy(model_dir="frozen_models/slot_filling")
    input_data = {"input": u"学费大概多少呢？?医学"}
    print proxy.response(input_data)