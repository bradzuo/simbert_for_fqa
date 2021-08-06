from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import urllib.parse
import requests
import json
import os,sys
rootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
print(rootPath)
sys.path.append(rootPath)
import pickle
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='view.log', level=logging.INFO, format=LOG_FORMAT)

def load_medpkl(pkl_path):
    """
    加载med的pkl文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path,'rb') as m:
        return pickle.load(m)

# 加载医疗qa数据
meddict = load_medpkl(pkl_path='/home/InfoRetrival/Bert_Faiss/meddata.pkl')
# meddict = load_medpkl(pkl_path=r'C:\files\LEARNING&DOING\DOING\InfoRetrival\Bert_Faiss\meddata.pkl')

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

def hello(request):
    context = {}
    context['hello'] = '医疗咨询FAQ'
    return render(request, 'index.html', context)

def recom_result(request):
    query = request.GET['query']
    # describe = eval(describe)
    # k = request.GET['k']
    print('query:',query)
    context = {}
    simbert_res = simbert_simi(text=query)
    if simbert_res:
        print('simbert返回文本匹配结果:', simbert_res.text)
        simbert_answer = meddict[eval(simbert_res.text)['data'][0][1]]
        print(simbert_answer)
        context['query'] = query
        context['res'] = simbert_answer[0].rstrip()
    else:
        print('没有相似的问句')
        context['query'] = query
        context['res'] = '没有相似的问句'
    return render(request, 'recom.html', context)




if __name__ == '__main__':
    pass