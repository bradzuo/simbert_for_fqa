# coding:utf-8

import requests
import json

# 访问服务器端口，返回识别结果
def faq(query):
    # url = 'http://192.168.161.112:102/faq' # simbert
    url = 'http://localhost:102/faq' # simbert

    data = {
        'query':query,
    }
    data = json.dumps(data)
    response = requests.post(url=url,data=data)
    return response

if __name__ == '__main__':

    query = '心情不好'
    response = faq(query)
    if response.status_code == 200:
        print(response.text)
    else:
        print('response.status_code is not 200')





