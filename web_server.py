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
from flask import Flask, render_template, request, jsonify
from apps.tokenizer import Tokenizer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


tokenizer = Tokenizer()
@app.route("/tokenize", methods=['POST'])
def tokenize_app():
    input_data = request.form
    output_data = tokenizer.response(input_data)
    return jsonify(output_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
