
class Config():
    configs = {
        # bert参数
        "config_path":'chinese_simbert_L-6_H-384_A-12/bert_config.json',
        "checkpoint_path":'chinese_simbert_L-6_H-384_A-12/bert_model.ckpt',
        "dict_path":'chinese_simbert_L-6_H-384_A-12/vocab.txt',

        # 模型参数
        "maxlen": 32,
        "with_pool":'linear', # with_pool:提取CLS向量，用CLS向量表示这句话的句向量 shape=(btz, 768)
        "application":'unilm',
        "return_keras_model":False,
        'save_name':'vec.npy',
        'data_name':'questions.csv'
    }