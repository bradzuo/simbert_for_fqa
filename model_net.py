"""
simbert模型结构
"""

from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
import os
from config import Config
from keras.models import Model

path = os.getcwd()
configs = Config().configs

# bert配置
bert_config_path = os.path.join(path, configs['config_path'])
bert_checkpoint_path = os.path.join(configs['checkpoint_path'])
bert_dict_path = os.path.join(configs['dict_path'])

def simbert_net():

    # 建立分词器
    tokenizer = Tokenizer(bert_dict_path, do_lower_case=True)  # 建立分词器

    # 建立模型
    bert = build_transformer_model(
        bert_config_path,
        bert_checkpoint_path,
        with_pool=configs['with_pool'],
        application=configs['application'],  # simbert是用unilm来生成句向量的
        return_keras_model=configs['return_keras_model'],
    )

    # 编码器
    encoder = Model(bert.model.inputs, bert.model.outputs[0])  # 用cls对应的向量作为句子的句向量
    return tokenizer,encoder