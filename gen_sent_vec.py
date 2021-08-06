"""
直接利用训练好的simbert去生成句子的句向量
@author:zuolong
"""

import numpy as np
import os
from utils import load_csv
os.environ['TF_KERAS'] = '1'
from model_net import simbert_net
from bert4keras.snippets import sequence_padding
import tqdm
from config import Config

configs = Config().configs
path = os.getcwd()

# 读取数据
data_path = os.path.join(os.getcwd(),'data',configs['data_name'])
questions = load_csv(filename=data_path,q_title='Questions',encoding='gbk')
print('共有问句：{}条'.format(len(questions)))

# 加载模型
tokenizer,encoder = simbert_net()

# 生成所有问句的vec
a_token_ids = []
for d in tqdm.tqdm(questions):
    token_ids = tokenizer.encode(d, maxlen=configs["maxlen"])[0] # 原始文本的token_id: CLS X X X X SEP;encode方法返回的是token_id，segment_id
    a_token_ids.append(token_ids)

a_token_ids = sequence_padding(a_token_ids)  # padding
a_vecs = encoder.predict([a_token_ids, np.zeros_like(a_token_ids)],verbose=True) # 根据padding后的token_id和segment_id来得到每个句子的CLS向量作为句向量

a_vecs = a_vecs / (a_vecs ** 2).sum(axis=1, keepdims=True) ** 0.5 # l2范数的归一化

print(type(a_vecs))
np.save(os.path.join(os.getcwd(),'result',configs['save_name']), a_vecs)
