"""
# 加载数据
"""
import pandas as pd


def load_txt(filename):
    """
    读取txt
    """
    D = []
    with open(filename,'r',encoding='utf-8') as f:
        for line in f:
            print(line)
            try:
                question,answer = line.split(' ')
            except:
                question, answer = line.split('\t')
            D.append(question)
    return D

def load_csv(filename,q_title,encoding):
    """
    读取csv
    """
    csv_data = pd.read_csv(filename,encoding=encoding)
    questions = csv_data[q_title].values.tolist()
    return questions


