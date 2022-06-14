#구성한 BoW를 통해서 카운트 -> csv파일로 생성

import os, time, sys
from collections import deque

dir_base = os.getcwd()
data_offset = "/main"

cur_data_i = '' # 추출하고 있는 데이터폴더 위치 체크(인덱스)
cur_datas = []

init = 1
top10 = ['mov', 'push', 'call', 'lea', 'cmp', 'add', 'pop', 'test', 'jz', 'jmp', 'retn', 'xor', 'tes'] #13
n_path = dir_base + "/n-gram.txt" # 100개씩 ,를 구분자로 나눔 줄바꿈(\n)
hex_d = {}
ngram = {}

tl_ngram = []
td_ngram = {}

ltop60_2gram = []
dtop60_2gram = {}

# top60 2gram 가져오기
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
#print(top60_2gram)

tmp = ''

n_gram = {}

# opcode : hex값 을 DB화 시키기
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
        
        
# 딕셔너리 값초기화
for i in range(len(ltop60_2gram)):
    dtop60_2gram[ltop60_2gram[i]] = 0
#print(dtop60_2gram)
# -----------------------------------------

# main함수
# main폴더안에 데이터 폴더 이름 모아둠
main_l = os.listdir(dir_base+data_offset)
for l in main_l:
    if(len(l.split('.'))==1):
        cur_datas.append(l)
del main_l # 사용다한 main_l 삭제


k_top60 = list(dtop60_2gram.keys())
# 폴더용(6개)
#for cur_data_i in range(1): # TEST용
for cur_data_i in range(len(cur_datas)):
    # init
    command_d = {}
    command_l = []
    tmp_ll = list()

    print("["+cur_datas[cur_data_i]+" 진행중"+"]")
    # 윈도우 : \\ , 맥 : /
    cur_path = dir_base + data_offset + "/" + cur_datas[cur_data_i]
    data_l = os.listdir(cur_path)
    
    # 파일별로
    #for i in range(1): # test용도
    for i in range(len(data_l)):
        dq = deque([])
        tmp_l = list()
        c_dtop60_2gram = dtop60_2gram.copy()
        if(i%100==0):
            print(str(i)+" - ",data_l[i])
            #print(command_l)
        data_path = cur_path + "/" + data_l[i]
        
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
                
                op_h = n_gram[command]
                #print(command,op_h)
                
                #dtop60_2gram
                
                # create index
                #center = dq[1] # 중앙의 Opcode
                # 중앙의  Opcode가 top10에 있다면
                if(len(dq)>2):
                    if dq[1] in top10:
                        h1 = n_gram[dq[0]] + n_gram[dq[1]][2:]
                        h2 = n_gram[dq[1]] + n_gram[dq[2]][2:]
                        if (h1 in c_dtop60_2gram):
                            c_dtop60_2gram[h1] += 1
                    
                        if(h2 in c_dtop60_2gram):
                            c_dtop60_2gram[h2] += 1
            for k in k_top60:
                tmp_l.append(str(c_dtop60_2gram[k]))
            tmp_ll.append(tmp_l)
        del tmp_l
            
    string = ''
    # csv파일 생성
    top60_csv_path = dir_base + "/dataset/" + str(cur_datas[cur_data_i]) + ".csv"
    
    with open(top60_csv_path,'w') as f:
        for t in tmp_ll:
            string = ",".join(t) + "\n"
            f.write(string)
            #time.sleep(1)

    del tmp_ll
    del dq
    del c_dtop60_2gram

