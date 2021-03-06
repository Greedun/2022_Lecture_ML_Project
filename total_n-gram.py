import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from keras import layers
from sklearn.model_selection import train_test_split

import os, time, sys
from collections import deque

global d_op_hex

dir_base = os.getcwd()
data_offset = "/main"

datas = []

# 상위 10개
top10 = ['mov', 'push', 'call', 'lea', 'cmp', 'add', 'pop', 'test', 'jz', 'jmp', 'retn', 'xor', 'tes'] #13
# 전체 opcode
l_opcode_list = top10.copy()
opcode_c = 1
d_op_hex = {}
ngram = {}
n_gram = {}

ltop60_2gram = []
dtop60_2gram = {}

ltop60 = []

def create_top60_csv(datas_i, tmp_ll):
    
    string = ''
    top60_csv_path = dir_base + "/dataset/" + str(datas_i) + ".csv"
    
    with open(top60_csv_path,'w') as f:
        for t in tmp_ll:
            string = ",".join(t) + "\n"
            f.write(string)
            #time.sleep(1)

def read_opcode_hex():
    global n_gram
    
    ngram_hex_path = dir_base + "/n-gram_hex.txt"
    with open(ngram_hex_path,'r') as f :
        lines = f.readlines()
        for line in lines:
            tmp = line.split(",")
            s = len(tmp)
            tmp[s-1] = tmp[s-1][:-1]
            for n in tmp:
                tmp_i = n.split("_")
                n_gram[tmp_i[0]] = tmp_i[1]
    #print(n_gram)

def read_top60_2gram():
    global ltop60_2gram
    
    top60_2gram_path = dir_base + "/top60_2gram.txt"
    with open(top60_2gram_path,"r") as f:
        lines = f.readlines()
        for line in lines:
            l = list(line.split(','))
            size = len(l)
            end = l[size-1][:-1]
            l = list(l[:size-1])
            l.append(end)
        ltop60_2gram = l.copy()

def read_asm(dq,data_path):
    global d_op_hex
    
    with open(data_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            command = line.split(' ')[0]
            if command.find('\n') != -1:
                    # 명령어가 단일 명령어인 경우
                    command = command[:-1]
                    
            # queue - opcode[A,command,B]
            if(len(dq)<3):
                dq.append(command)
            else:
                dq.popleft()
                dq.append(command)
            
            # opcode : hex 제작후 저장
            save_opcode_hex(command)
            # create 2gram of opcode_hex
            # 중앙의 opcode가 top10일때 2gram추출
            # center = dq[1]
            if(len(dq)>2):
                if dq[1] in top10:
                    h1 = d_op_hex[dq[0]] + d_op_hex[dq[1]][2:]
                    h2 = d_op_hex[dq[1]] + d_op_hex[dq[2]][2:]
                    if (h1 in ngram):
                        ngram[h1] += 1
                    else:
                        ngram[h1] = 1
                    
                    if(h2 in ngram):
                        ngram[h2] += 1
                    else:
                        ngram[h2] = 1


def write_top60_2gram(c_ngram):
    global ltop60
    
    # c_ngram : 2gram의 횟수를 카운팅한 딕셔너리
    # ngram 상위60개 출력 - 5만개 이상
    # 2gram top 60개 ','로 구분자
    string = ''
    top60_2gram_path = dir_base + "/top60_2gram.txt"
    with open(top60_2gram_path,'w') as f:
        for i in range(60):
            ltop60.append(c_ngram[i][0])
            string = string + c_ngram[i][0] + ','
        string = string[:-1]+'\n'
        f.write(string)

def save_opcode_hex(command):
    global l_opcode_list
    global opcode_c
    global d_op_hex
    
        # opcode리스트에 opcode가 존재하는가?
    if not command in l_opcode_list:
        l_opcode_list.append(command)
        
        # opcode : hex
        num = str(hex(opcode_c))[2:] 
        d_op_hex[command] = "0x"+num.zfill(3)
        opcode_c += 1
    #print(d_op_hex)

    #print("save_opcode_hex : ",tmp_d)


def opcode_count():
    op = []
    opcode_path = dir_base + "/opcode.txt"
    with open(opcode_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                opcode_l = line[:-1].split('_')
                for op_i in opcode_l:
                    if not op_i in op:
                        op.append(op_i)
    #print(op)
    #print(len(op))
    sys.exit(1)
    
# normalization을 했을때 정확도가가 어떻게 변화하는지 학습습
def normalization(total_data):
    total_data = np.float64(total_data)
    for index in range(len(total_data)):
        total_data[index] = (total_data[index] - total_data[index].min()) / (total_data[index].max() - total_data[index].min())
    return total_data

def __main__():
    global d_op_hex
    global opcode_c
    '''
    print("[import 완료후 main 시작]")
    
    # dataset폴더가 없다면 생성해주는 기능
    if not os.path.exists(dir_base+'/dataset/'):
        os.mkdir(dir_base+'/dataset/')

    # opcode 전체 갯수 count
    #opcode_count()   
    
    # top10 opcode
    for op in l_opcode_list:
        # opcode : hex
        num = str(hex(opcode_c))[2:] 
        d_op_hex[op] = "0x"+num.zfill(3)
        opcode_c += 1
    
    # [main]
    # 폴더안에 데이터를 전부 돌면서 2gram 추출
    # 데이터 폴더 이름 추출
    l_folder = os.listdir(dir_base)
    for f in l_folder:
        if(len(f.split('.'))==1):
            if f != "dataset":
                datas.append(f) #데이터 폴더들 저장
    del l_folder
    
    print("[데이터전처리 시작]")
    # 폴더용(6개)
    #for cur_data_i in range(1): # TEST용
    for cur_data_i in range(len(datas)):

        # init
        command_l = []
        
        # 어떤 데이터 폴더가 진행중인가?
        print("["+datas[cur_data_i]+" 데이터 진행중"+"]")
        # 윈도우 : \\ , 맥 : /
        cur_path = dir_base + "/" + datas[cur_data_i]
        l_asm = os.listdir(cur_path)
        
        # 파일별로
        #for i in range(1): # test용도
        for i in range(len(l_asm)):
            dq = deque([])
            # 100개마다 중간 진행사항 확인
            if(i%100==0):
                print(str(i)+"번째 asm파일 진행중")
            
            data_path = cur_path + "/" + l_asm[i]
            
            # asm파일 읽는 부분
            read_asm(dq,data_path)
        del dq
    
    # 2gram을 카운팅한 것을 카운팅수로 정렬한다.(큰수 -> 작은수)
    # => (2gram : count)
    c_ngram = ngram.copy() # copy본
    c_ngram = sorted(c_ngram.items(), key=lambda x: x[1], reverse=True)
    
    # ltop60값
    write_top60_2gram(c_ngram)
    
    print("[데이터 전처리 완료]\n\n")
    
    # -------------------------
    # top60 2gram 가져오기
    #/ read_top60_2gram()
    
    tmp = ''

    n_gram = {}
    # d_op_hex값
    #/ read_opcode_hex()
    
    # hex값 초기화 => 사용X (d_op_hex로 대체)
    # 딕셔너리 값초기화
    for i in range(len(ltop60)):
        dtop60_2gram[ltop60[i]] = 0
    #print(dtop60_2gram)
    
    print("[csv파일 생성 시작]")
    k_top60 = ltop60.copy()
    # 폴더용(6개)
    #for cur_data_i in range(1): # TEST용
    for cur_data_i in range(len(datas)):
        # init
        command_d = {}
        command_l = []
        tmp_ll = list()
        
        print("["+datas[cur_data_i]+" 진행중"+"]")
        # 윈도우 : \\ , 맥 : /
        cur_path = dir_base + "/" + datas[cur_data_i]
        l_asm = os.listdir(cur_path)
        
        # 파일별로
        #for i in range(1): # test용도
        for i in range(len(l_asm)):
            dq = deque([])
            tmp_l = list()
            c_dtop60_2gram = dtop60_2gram.copy()
            if(i%100==0):
                print(str(i)+"번째 asm파일 진행중")
                #print(command_l)
            
            data_path = cur_path + "/" + l_asm[i]
            
            # asm파일을 읽는 부분
            with open(data_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    command = line.split(' ')[0]
                    if command.find('\n') != -1:
                        # 명령어가 단일 명령어인 경우
                        command = command[:-1]
                    #print(list(command)) # 여기까지는 이상 없음
                
                    if(len(dq)<3):
                        dq.append(command)
                    else:
                        dq.popleft()
                        dq.append(command)
                
                    op_h = d_op_hex[command]
                    #print(command,op_h)
                
                    #dtop60_2gram
                
                    # create index
                    #center = dq[1] # 중앙의 Opcode
                    # 중앙의  Opcode가 top10에 있다면
                    if(len(dq)>2):
                        if dq[1] in top10:
                            h1 = d_op_hex[dq[0]] + d_op_hex[dq[1]][2:]
                            h2 = d_op_hex[dq[1]] + d_op_hex[dq[2]][2:]
                            if (h1 in c_dtop60_2gram):
                                c_dtop60_2gram[h1] += 1
                    
                            if(h2 in c_dtop60_2gram):
                                c_dtop60_2gram[h2] += 1               
                for k in k_top60:
                    tmp_l.append(str(c_dtop60_2gram[k]))
                tmp_ll.append(tmp_l)
            del tmp_l

        create_top60_csv(datas[cur_data_i], tmp_ll)
        
        del tmp_ll
        del dq
        del c_dtop60_2gram
        print(datas[cur_data_i],".csv파일 생성 완료\n")
    print("[csv파일 생성 완료]\n")
    '''
    # --------------------------
    # [ngram model]
    # ltop60
    # d_op_hex
    print("[model 시작]")
    read_top60_2gram()
    
    # test
    be_test = pd.read_csv("dataset/test_benign.csv",names=ltop60_2gram)
    be_test.insert(0,'label',[0 for i in range(200)])
    mal_test = pd.read_csv("dataset/test_malware.csv",names=ltop60_2gram)
    mal_test.insert(0, 'label',[1 for i in range(200)])

    op_test = pd.concat([be_test,mal_test], ignore_index=True)
    print("=> test데이터 입력 완료")
    
    # train
    be_train = pd.read_csv("dataset/train__benign.csv",names=ltop60_2gram)
    be_train.insert(0,'label',[0 for i in range(1000)])
    mal_train = pd.read_csv("dataset/train__malware.csv",names=ltop60_2gram)
    mal_train.insert(0, 'label',[1 for i in range(1000)])

    op_train = pd.concat([be_train,mal_train], ignore_index=True)
    print("=> train데이터 입력 완료")
    
    # validate
    be_val = pd.read_csv("dataset/valid__benign.csv",names=ltop60_2gram)
    be_val.insert(0,'label',[0 for i in range(200)])
    mal_val = pd.read_csv("dataset/valid__malware.csv",names=ltop60_2gram)
    mal_val.insert(0, 'label',[1 for i in range(200)])

    op_val = pd.concat([be_val,mal_val], ignore_index=True)
    print("=> valid데이터 입력 완료")
    
    
    # shuffle
    op_train = shuffle(op_train , random_state=1000)
    op_val = shuffle(op_val, random_state=1000)
    op_test = shuffle(op_test, random_state=1000)
    print("=> 데이터 셔플")
    
    # split data, label
    train_data, train_label = op_train.iloc[:, 1:], op_train['label']
    val_data, val_label = op_val.iloc[:, 1:], op_val['label']
    test_data, test_label = op_test.iloc[:, 1:], op_test['label']
    print("=> label, data분리")
    
    # bring data
    train_data = train_data.values
    train_label = train_label.values

    val_data = val_data.values
    val_label = val_label.values

    test_data = test_data.values
    test_label = test_label.values
    
    '''
    # confirm shape
    print(F"train_data shape : {train_data.shape}")
    print(F"train_label shape : {train_label.shape}")
    print(F"valid_data shape : {val_data.shape}")
    print(F"valid_label shape : {val_label.shape}")
    '''

    # create model
    model = tf.keras.models.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(60,)))
    model.add(layers.Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='rmsprop',
            loss='binary_crossentropy',
            metrics = ['accuracy'])
    print("=> 모델 생성 및 컴파일")
    
    # 정규화
    n_train_data = normalization(train_data)
    n_valid_data = normalization(val_data)
    n_test_data = normalization(test_data)
    print("=> 데이터 정규화")
    
    hist = model.fit(train_data,train_label, epochs = 500 ,validation_data = (val_data, val_label))
    score = model.evaluate(test_data,test_label)
    print('정답률 = ', score[1],'loss=', score[0])
    
    # model.predict(test_data)
    
    # visualization
    plt.plot(hist.history['accuracy'])
    plt.plot(hist.history['val_accuracy'])
    plt.title('Accuracy')
    plt.legend(['train','test'], loc='upper left')
    plt.show()
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.title('Loss')
    plt.legend(['train','test'], loc='upper left')
    plt.show()
    
    
__main__()