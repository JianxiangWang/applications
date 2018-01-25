# coding=utf-8
"""
The a file.

Authors: Wang Jianxiang (w51141201062@163.com)
"""

import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import json
from flask import Flask, render_template, request, jsonify
from apps.tokenizer import Tokenizer
from apps.model_proxy import SlotFillingProxy
import logging.config
import yaml

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
    logger.info('Output data: %s' % json.dumps(output_data, ensure_ascii=False))
    return jsonify(output_data)


''' Slot Filling'''
slot_filling_gproxy = SlotFillingProxy(model_dir="apps/frozen_models/slot_filling")


@app.route("/slot_filling", methods=['GET'])
def slot_filling():
    return render_template("slot_filling.html")


@app.route("/slot_filling/run", methods=['POST'])
def slot_filling_run():
    input_data = request.form
    logger.info('Input data = %s' % json.dumps(input_data, ensure_ascii=False))
    output_data = slot_filling_gproxy.response(input_data)
    logger.info('Output data: %s' % json.dumps(output_data, ensure_ascii=False))
    return jsonify(output_data)


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
        Setup logging configuration.
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    setup_logging()
    app.run(host="0.0.0.0", port=8888)
