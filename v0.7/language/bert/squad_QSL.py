# coding=utf-8
# Copyright (c) 2020 NVIDIA CORPORATION. All rights reserved.
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), "DeepLearningExamples", "TensorFlow", "LanguageModeling", "BERT"))
sys.path.insert(0, os.getcwd())

from transformers import BertTokenizer
from utils.create_squad_data import read_squad_examples, convert_examples_to_features

import mlperf_loadgen as lg

max_seq_length = 384
max_query_length = 64
doc_stride = 128

class SQuAD_v1_QSL():
    def __init__(self, perf_count=None):
        print("Creating tokenizer...")
        tokenizer = BertTokenizer("build/data/bert_tf_v1_1_large_fp32_384_v2/vocab.txt")

        print("Reading examples...")
        eval_examples = read_squad_examples(input_file="build/data/dev-v1.1.json",
            is_training=False, version_2_with_negative=False)

        print("Converting examples to features...")
        eval_features = []
        def append_feature(feature):
            eval_features.append(feature)

        convert_examples_to_features(
            examples=eval_examples,
            tokenizer=tokenizer,
            max_seq_length=max_seq_length,
            doc_stride=doc_stride,
            max_query_length=max_query_length,
            is_training=False,
            output_fn=append_feature,
            verbose_logging=False)

        print("Constructing QSL...")
        self.eval_features = eval_features
        self.count = len(self.eval_features)
        self.perf_count = perf_count if perf_count is not None else self.count
        self.qsl = lg.ConstructQSL(self.count, self.perf_count, self.load_query_samples, self.unload_query_samples)
        print("Finished constructing QSL.")

    def load_query_samples(self, sample_list):
        pass

    def unload_query_samples(self, sample_list):
        pass

    def get_features(self, sample_id):
        return self.eval_features[sample_id]

    def __del__(self):
        lg.DestroyQSL(self.qsl)
        print("Finished destroying QSL.")

def get_squad_QSL():
    return SQuAD_v1_QSL()
