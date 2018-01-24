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
sys.setdefaultencoding("utf-8")
import logging
import json
from flask import Flask, render_template, request, jsonify
from apps.tokenizer import Tokenizer
from apps.model_proxy import SlotFillingProxy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


''' Tokenizer '''
tokenizer = Tokenizer()


@app.route("/tokenizer", methods=['GET'])
def tokenizer_index():
    return render_template("tokenizer.html")


@app.route("/tokenizer/run", methods=['POST'])
def tokenizer_run():
    input_data = request.form
    logger.info('Input data: %s' % json.dumps(input_data, ensure_ascii=False))
    output_data = tokenizer.response(input_data)
    return jsonify(output_data)


''' Slot Filling'''
slot_filling_gproxy = SlotFillingProxy(model_dir="apps/frozen_models/slot_filling")


@app.route("/slot_filling", methods=['GET'])
def slot_filling():
    return render_template("slot_filling.html")


@app.route("/slot_filling/run", methods=['POST'])
def slot_filling_run():
    input_data = request.form
    logger.info('Input data: %s' % json.dumps(input_data, ensure_ascii=False))
    output_data = slot_filling_gproxy.response(input_data)
    return jsonify(output_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
