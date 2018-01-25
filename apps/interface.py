# coding=utf-8
"""
The interface file.

Authors: Wang Jianxiang (w51141201062@163.com)
"""

import abc
import tensorflow as tf


class AppInterface(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def response(self, input_data):
        pass


class Inference(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def inference(self, input_package):
        """
        Do inference.
        """
        pass

    def _load_graph(self, frozen_graph_filename):
        """
        Load graph from frozen graph.
        Args:
            frozen_graph_filename: The file name
        Returns:
            graph: The tensorflow graph.
        """
        with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(
                graph_def,
                input_map=None,
                return_elements=None,
                name="prefix",
                op_dict=None,
                producer_op_list=None
            )
        return graph


if __name__ == '__main__':
    a = AppInterface()