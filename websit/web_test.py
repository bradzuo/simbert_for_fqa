import requests

def comp_kg(query):
    # 访问服务器端口，返回结果
    url = 'http://localhost:8088/compkg'
    data = {
        'query': query,  # 微博情感分析,实体识别,敏感词过滤,文本摘要参数
    }
    # html = requests.get(url=url,params=data)
    html = requests.post(url=url, data=data)
    return html

query = '广东省有多少家上市公司'
res = comp_kg(query=query).text
print(res)
res = eval(res)
print(res)
