"""
sanic 接口
"""
import numpy as np
import os
from utils import load_csv
from config import Config
import functools,time
from model_net import simbert_net
from sanic import Sanic,request
from sanic.response import json
import traceback


app = Sanic('simbert')

configs = Config().configs
path = os.getcwd()

# 加载保存的问答对的所有问题的vec
a_vecsss = np.load(os.path.join(os.getcwd(),'result',configs['save_name']))

# 加载模型
tokenizer,encoder = simbert_net()

# 加载数据
data_path = os.path.join(os.getcwd(),'data',configs['data_name'])
questions = load_csv(filename=data_path,q_title='Questions',encoding='gbk')

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
    token_ids, segment_ids = tokenizer.encode(text, maxlen=configs['maxlen'])
    vec = encoder.predict([[token_ids], [segment_ids]])[0]
    vec /= (vec ** 2).sum() ** 0.5
    sims = np.dot(a_vecsss, vec)
    return [(i, questions[i], sims[i]) for i in sims.argsort()[::-1][:topn]]

@app.route('/faq',methods=['POST'])
async def question_similarity(request):
    try:
        json_data = request.json
        query = json_data['query']
        most_simi = most_similar(query)
        response = {
            'question':most_simi[0][1],
            'confidence':str(most_simi[0][2])
        }
        print('response:',response)
    except Exception as e:
        print('error:',e)
        response = {}
        response["error"]=traceback.format_exc()
    return json(response,ensure_ascii=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=102)