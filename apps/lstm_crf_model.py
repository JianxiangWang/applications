# coding=utf-8
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
"""
Authors: Wang Jianxiang (wangjianxing01@baidu.com)
"""
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import collections
import tensorflow as tf
from apps.interface import Inference
import logging
import json


LstmCrfModelMeta = collections.namedtuple("LstmCrfModelMeta",
                                          ["model_path", "word_path", "tag_path"])
LstmCrfInputPackage = collections.namedtuple("LstmCrfInputPackage", "query")


class LstmCrfInference(Inference):
    """
    The lstm plus crf model.
    """
    def __init__(self, lstm_crf_meta):
        super(LstmCrfInference, self).__init__()
        self.tokenize = True
        self.max_length = 100
        self.pad_tok = 'UNK'
        self.NONE = 'O'
        self.graph = self._load_graph(lstm_crf_meta.model_path)

        self.reverse_tag_dict, self.tag_num = self._load_dict(lstm_crf_meta.tag_path, reverse=True)
        self.tag_dict, self.tag_num = self._load_dict(lstm_crf_meta.tag_path, reverse=False)
        self.word_dict, self.word_num = self._load_dict(lstm_crf_meta.word_path, reverse=False)

        self.word_ids = self.graph.get_tensor_by_name('prefix/word_ids:0')
        self.sequence_lengths = self.graph.get_tensor_by_name('prefix/sequence_lengths:0')
        self.logits_out = self.graph.get_tensor_by_name('prefix/logits_out:0')
        self.trans_params_out = self.graph.get_tensor_by_name('prefix/trans_params_out:0')

        self.sess = tf.Session(graph=self.graph)

    def inference(self, lstm_crf_input):

        query = lstm_crf_input.query
        if self.tokenize:
            word_list = list(jieba.cut(query))
        else:
            word_list = list(query)

        logging.info(json.dumps(word_list, ensure_ascii=False))

        pad_word_list = word_list[:self.max_length]\
                        + [self.pad_tok] * max(self.max_length - len(word_list), 0)
        word_indexs = list(self.word_dict.get(x, self.word_num) for x in pad_word_list)

        seq_lengths = [len(word_list)]
        words = [word_indexs]

        logits, trans_params = self.sess.run([self.logits_out, self.trans_params_out], feed_dict={
            self.word_ids: words,
            self.sequence_lengths: seq_lengths,
        })

        # iterate over the sentences because no batching in vitervi_decode
        viterbi_sequences = []
        for logit, sequence_length in zip(logits, seq_lengths):
            logit = logit[:sequence_length]
            viterbi_seq, viterbi_score = tf.contrib.crf.viterbi_decode(
                logit, trans_params)

            lab_pred = viterbi_seq[:sequence_length]
            lab_pred_chunks = self._get_chunks(lab_pred, self.tag_dict)

            result_slots = []
            for chunk in lab_pred_chunks:
                result_slots.append(chunk[0])
                result_slots.append("".join(word_list[chunk[1]: chunk[2]]))
            viterbi_sequences += [result_slots]

        return query, viterbi_sequences, seq_lengths

    def _get_chunk_type(self, tok, idx_to_tag):
        """
        Args:
            tok: id of token, ex 4
            idx_to_tag: dictionary {4: "B-PER", ...}

        Returns:
            tuple: "B", "PER"

        """
        tag_name = idx_to_tag.get(tok, 'UNK')
        tag_class = tag_name.split('-')[0]
        tag_type = tag_name.split('-')[-1]
        return tag_class, tag_type

    def _get_chunks(self, seq, tags):
        """Given a sequence of tags, group entities and their position

        Args:
            seq: [4, 4, 0, 0, ...] sequence of labels
            tags: dict["O"] = 4

        Returns:
            list of (chunk_type, chunk_start, chunk_end)

        Example:
            seq = [4, 5, 0, 3]
            tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
            result = [("PER", 0, 2), ("LOC", 3, 4)]

        """
        default = tags[self.NONE]
        idx_to_tag = {idx: tag for tag, idx in tags.items()}
        chunks = []
        chunk_type, chunk_start = None, None
        for i, tok in enumerate(seq):
            # End of a chunk 1
            if tok == default and chunk_type is not None:
                # Add a chunk.
                chunk = (chunk_type, chunk_start, i)
                chunks.append(chunk)
                chunk_type, chunk_start = None, None

            # End of a chunk + start of a chunk!
            elif tok != default:
                tok_chunk_class, tok_chunk_type = self._get_chunk_type(tok, idx_to_tag)
                if chunk_type is None:
                    chunk_type, chunk_start = tok_chunk_type, i
                elif tok_chunk_type != chunk_type or tok_chunk_class == "B":
                    chunk = (chunk_type, chunk_start, i)
                    chunks.append(chunk)
                    chunk_type, chunk_start = tok_chunk_type, i
            else:
                pass

        # end condition
        if chunk_type is not None:
            chunk = (chunk_type, chunk_start, len(seq))
            chunks.append(chunk)

        return chunks

    def _load_dict(self, dict_path, reverse=False):
        result_dict = {}
        dict_num = 0
        with codecs.open(dict_path, 'r', encoding="utf-8") as dict_file:
            lines = dict_file.readlines()
            dict_num = int(lines[0])
            for line in lines[1:]:
                the_key, the_val = line.split('\t')
                if not reverse:
                    result_dict.setdefault(the_key, int(the_val))
                else:
                    result_dict.setdefault(int(the_val), the_key)
        return result_dict, dict_num


if __name__ == '__main__':
    inference = LstmCrfInference(LstmCrfModelMeta('frozen_models/slot_filling/model.pb',
                                                  'frozen_models/slot_filling/featureIdMap.word',
                                                  'frozen_models/slot_filling/featureIdMap.tag'))
    result = inference.inference(LstmCrfInputPackage('我想去香港大学～'))

    print result
