
import flask
import json
from flask import request,Response
from bert4keras.backend import keras, K
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding
import numpy as np
from utils import load_data
a_vecsss = np.load(r"loan_sim_all_datas.npy")
import tensorflow as tf
global graph,model,sess
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)


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

# 测试相似度效果
data = datas_all

def most_similar(text, topn=2):
    """检索最相近的topn个句子
    """
    token_ids, segment_ids = tokenizer.encode(text, max_length=maxlen)
    print(token_ids, segment_ids)
    vec = encoder.predict([[token_ids], [segment_ids]])[0]
    vec /= (vec ** 2).sum() ** 0.5
    sims = np.dot(a_vecsss, vec)
    return [(int(i), datas_all[i], str(sims[i])) for i in sims.argsort()[::-1][:topn]]
print('测试数据')
print(most_similar('前列腺炎的自我治疗'))

if __name__ == '__main__':
    app = flask.Flask(__name__)

    def response_headers(content):
        resp = Response(content)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    @app.route("/simbert",methods=["GET","POST"])
    def bert_intent_recognize():
        data = {"sucess":0}
        result = None
        if request.method == "POST":
            text = request.form.get("text")
        else:
            text = request.args.get("text")
        print('对比文本：',text)
        if text:
            with graph.as_default():
                set_session(sess)
                results = most_similar(text)
                print(result)
                data["data"] = results
                data["sucess"] = 1
                # print(data)
            content = json.dumps(data, ensure_ascii=False)
        else:
            content = json.dumps({'error': 'no text'}, ensure_ascii=False)

        resp = response_headers(content)
        return resp

    app.run(host='0.0.0.0', port=60063)
    # text = '神经性皮炎怎么治'
    # print(most_similar(text))