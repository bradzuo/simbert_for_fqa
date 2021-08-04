# -*-coding:utf-8-*-
import os,re,json,sys
import keras
rootPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(rootPath)
keras.backend.clear_session()
import tensorflow as tf
import sys
import jieba
from flask import request,jsonify,render_template,Response,Flask
import numpy as np
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='../../comp_kg_interface.log', level=logging.INFO, format=LOG_FORMAT)
app = Flask(__name__)
app.config['DEBUG'] = False

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/compkg", methods=["GET", "POST"])
def ComKG():

    content = ""
    if request.method == "POST":
        # versionCode = request.form.get("version")
        query = request.form.get("query")
    else:
        # versionCode = request.args.get("version")
        query = request.args.get("query")
    logging.info('用户查询：{}'.format(query))
    rec_res,res,code = begin(query=query)
    # print("rec_res:",rec_res)
    # print("res:",res)
    if res:
        if code != '01':
            if not res[0].empty or not res[1].empty or not res[2].empty:
                result_operation, result_roe, result_dayfreval = res
                oper_res = []
                roe_res = []
                day_res = []
                if not result_roe.empty:
                    ROE_date = result_roe['statDate'].values.tolist()
                    ROE_value = result_roe['dupontROE'].values.tolist()
                    # print("ROE_date:", ROE_date)
                    # print("ROE_value:", ROE_value)
                    year1 = []
                    year2 = []
                    year3 = []
                    for index, d in enumerate(ROE_date):
                        if d.startswith('2019'):
                            year1.append(ROE_value[index])
                        elif d.startswith('2020'):
                            year2.append(ROE_value[index])
                        elif d.startswith('2021'):
                            year3.append(ROE_value[index])

                    roe_res.append(year1)
                    roe_res.append(year2)
                    roe_res.append(year3)
                    # print("pro_res:",pro_res)
                if not result_dayfreval.empty:
                    day_res.append(result_dayfreval['date'].values.tolist())
                    day_res.append(result_dayfreval['peTTM'].values.tolist())
                    day_res.append(result_dayfreval['close'].values.tolist())

                if not result_operation.empty:
                    # ['code','statDate','INVTurnRatio','CATurnRatio','AssetTurnRat
                    oper_res.append(result_operation['code'].values.tolist())
                    oper_res.append(result_operation['statDate'].values.tolist())
                    oper_res.append(result_operation['INVTurnRatio'].values.tolist())
                    oper_res.append(result_operation['CATurnRatio'].values.tolist())
                    oper_res.append(result_operation['AssetTurnRatio'].values.tolist())

                final_res = []
                final_res.append(oper_res)
                final_res.append(roe_res)
                final_res.append(day_res)
                # print('code:',code)
                # print("final_res:",final_res)
                content = json.dumps({'res':final_res,'rec_res':rec_res,'code':code},ensure_ascii=False)
                resp = Response_headers(content)
            else:
                content = json.dumps({'res': [], 'rec_res': rec_res, 'code': code}, ensure_ascii=False)
                resp = Response_headers(content)
        else:
            content = json.dumps({'res':res,'rec_res':rec_res,'code':code},ensure_ascii=False)
            resp = Response_headers(content)
    else:
        # print('没有收录当前问句的答案')
        content = json.dumps({'error':'没有相关数据,请确保输入的企业名称正确并在沪深上市'})
        resp = Response_headers(content)
    # print("content:",content)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=False)
