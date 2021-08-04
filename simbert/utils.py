
def load_data(filename):
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

def load_title(filename):
    D = []
    with open(filename,'r',encoding='utf-8')as f,open('titles.txt','w',encoding='utf-8') as t:
        for line in f:
            question,answer = line.split('\t')
            t.write(question + '\n')

if __name__ == '__main__':
    load_title(filename=r'C:\files\LEARNING&DOING\DOING\InfoRetrival\ES_ESIM\utils\medical_data.txt')

