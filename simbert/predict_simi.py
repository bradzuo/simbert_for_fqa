from bert4keras.backend import keras, K
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding
import numpy as np
from utils import load_data
a_vecsss = np.load(r"sim_all_datas_6.npy")


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

datas1 = load_data('medical_data.txt')
datas_all = datas1

# 测试相似度效果
data = datas_all

import functools,time
def time_cost(func):
    @functools.wraps(func)
    def wrapped(*args,**kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        end_time = time.time()
        cost_time = end_time - start_time
        print('耗时：',cost_time)
        return res
    return wrapped

@time_cost
def most_similar(text, topn=5):
    """检索最相近的topn个句子
    """
    token_ids, segment_ids = tokenizer.encode(text, max_length=maxlen)
    print(token_ids, segment_ids)
    vec = encoder.predict([[token_ids], [segment_ids]])[0]
    vec /= (vec ** 2).sum() ** 0.5
    sims = np.dot(a_vecsss, vec)
    return [(i, datas_all[i], sims[i]) for i in sims.argsort()[::-1][:topn]]

kk = ["神经性皮炎怎么治"]
mmm = []
for i in kk:
    results = most_similar(i, 10)
    mmm.append([i, results])
    print(i, results)