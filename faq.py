
"""
基于es+esim做信息检索，用于医疗咨询
"""
import json
import requests
import pickle

# coding:utf-8
import os,sys,re
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import requests
import base64
import json

def load_medpkl(pkl_path):
    """
    加载med的pkl文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path,'rb') as m:
        return pickle.load(m)

def simbert_simi(text):
    """
    用simbert做文本匹配
    :param query:
    :param candi_sent:
    :return:
    """
    url = 'http://localhost:60063/simbert'  # simbert

    data = {
        'text': text,
    }
    html = requests.post(url=url, data=data)
    return html

if __name__ == '__main__':

    # 加载医疗qa数据
    meddict = load_medpkl(pkl_path='meddata.pkl')
    while True:
        inp = input('您要查询: ')
        simbert_res = simbert_simi(text=inp)
        if simbert_res:
            print('simbert返回文本匹配结果:',simbert_res.text)
            simbert_answer = meddict[eval(simbert_res.text)['data'][0][1]]
            print(simbert_answer)
        else:
            print('没有相似的问句')