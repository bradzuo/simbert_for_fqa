# coding:utf-8
import os,sys,re
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import requests
import base64
import json


# 访问服务器端口，返回识别结果
def entity_rec(text):
    url = 'http://182.92.67.204:60063/simbert' # simbert

    data = {
        'text':text,
    }
    html = requests.post(url=url,data=data)
    return html

if __name__ == '__main__':

    print('-'*30)
    text = '你好'

    result = entity_rec(text)
    print(result.text)




