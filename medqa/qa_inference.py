# coding:utf-8
import os,sys,re
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import requests
import base64
import json

# 访问服务器端口，返回识别结果
def entity_rec(text):
    url = 'http://localhost:8056/medicalqa'
    data = {
        'text':text,
    }
    # html = requests.get(url=url,params=data)
    html = requests.post(url=url,data=data)
    return html


if __name__ == '__main__':

    print('-'*30)
    text = '头昏眼花'
    for i in range(1):
        result = entity_rec(text)
        print(result.text)
        if result.text == '':
            print('为空')
        print(json.loads(result.text))




