# -*- coding:utf-8 -*-
import os
import re
import json
import itchat
from itchat.content import *

from flask import Flask
from flask import request
import hashlib
import receive
import reply
import os,sys
import os, base64
import requests as req
from PIL import Image
from io import BytesIO
sys.path.append('..')
app = Flask(__name__)
import pickle,requests

@app.route("/")
def index():
    return "Hello World!"

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
    url = 'http://182.92.67.204:60063/simbert'  # simbert

    data = {
        'text': text,
    }
    html = requests.post(url=url, data=data)
    return html

meddict = load_medpkl(pkl_path='meddata.pkl')

# 公众号后台消息路由入口
@app.route("/chat", methods=["GET", "POST"])
def wechat():
    # 验证使用的GET方法
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = "880130"

        # 进行排序
        dataList = [token, timestamp, nonce]
        dataList.sort()
        result = "".join(dataList)

        #哈希加密算法得到hashcode
        sha1 = hashlib.sha1()
        sha1.update(result.encode("utf-8"))
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr
        else:
            return ""
    else:
        recMsg = receive.parse_xml(request.data)
        print('recMsg:',recMsg)
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            print('输入信息类别：',recMsg.MsgType)
            if recMsg.MsgType == 'text':
                content = recMsg.Content  # 获取到的用户信息
                print('用户输入：', content)

                simbert_res = simbert_simi(text=content)
                if simbert_res:
                    print('simbert返回文本匹配结果:', simbert_res.text)
                    simbert_answer = meddict[eval(simbert_res.text)['data'][0][1]]
                    answer = simbert_answer[0]
                else:
                    answer = '没有相似的问句'

                replyMsg = reply.TextMsg(toUser, fromUser, answer)
                return replyMsg.send()
            elif recMsg.MsgType == 'image':
                replyMsg = reply.TextMsg(toUser, fromUser, '你发的都是些啥啊...')
                return replyMsg.send()
            elif recMsg.MsgType == 'voice':
                replyMsg = reply.TextMsg(toUser, fromUser, '对不起，还没把讯飞小哥哥融入我的身体里...')
                return replyMsg.send()
            else:
                return reply.Msg().send()
        else:
            return reply.Msg().send()

if __name__ == "__main__":
    # app.run(host='192.168.3.14', port=80)
    app.run(host='182.92.67.204', port=80)
    # app.run(host='0.0.0.0', port=80)
    # app.run(host='172.21.139.36', port=80)



