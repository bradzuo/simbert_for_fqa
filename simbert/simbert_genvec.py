"""
直接利用训练好的simbert权重去生成句子的句向量
"""

import numpy as np
import os
from collections import Counter
from utils import load_data

os.environ['TF_KERAS'] = '1'
from bert4keras.backend import keras, K
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding
from keras.models import Model
import tqdm

maxlen = 32

# bert配置
# bert配置
config_path = 'chinese_simbert_L-6_H-384_A-12/chinese_simbert_L-6_H-384_A-12/bert_config.json'
checkpoint_path = 'chinese_simbert_L-6_H-384_A-12/chinese_simbert_L-6_H-384_A-12/bert_model.ckpt'
dict_path = 'chinese_simbert_L-6_H-384_A-12/chinese_simbert_L-6_H-384_A-12/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False,
)

encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])

datas1 = load_data('loan.txt')
datas_all = datas1

print('共有问句：{}条'.format(len(datas_all)))
# 测试相似度效果
data = datas_all
a_token_ids, b_token_ids, labels = [], [], []
texts = []

for d in tqdm.tqdm(data):
    token_ids = tokenizer.encode(d, max_length=maxlen)[0]
    a_token_ids.append(token_ids)
    #     token_ids = tokenizer.encode(d[1], maxlen=maxlen)[0]
    #     b_token_ids.append(token_ids)
    #     labels.append(d[2])
    texts.append(d)

a_token_ids = sequence_padding(a_token_ids)
# b_token_ids = sequence_padding(b_token_ids)
a_vecs = encoder.predict([a_token_ids, np.zeros_like(a_token_ids)],
                         verbose=True)
# b_vecs = encoder.predict([b_token_ids, np.zeros_like(b_token_ids)],
#                          verbose=True)
# labels = np.array(labels)

a_vecs = a_vecs / (a_vecs ** 2).sum(axis=1, keepdims=True) ** 0.5

print(type(a_vecs))
np.save("loan_sim_all_datas.npy", a_vecs)
