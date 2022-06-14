# 1. 상위 10개 opcode 추출(V) -> opcode 기반 앞뒤값을 index로서 사용(V)
# ex) A mov B -> A mov, mov B로 인덱스 구성(0x01 0x02 0x03)=> 0x0102 0x0203이 이름(V)
# 2. 구성한 BoW를 통해서 카운트 -> csv파일로 생성
# 3. 생성한 csv파일로 FeedForward에 넣음

import os, time, sys
from collections import deque

dir_base = os.getcwd()
data_offset = "/main"

cur_data_i = '' # 추출하고 있는 데이터폴더 위치 체크(인덱스)
cur_datas = []

init = 1
# 상위 10개
top10 = ['mov', 'push', 'call', 'lea', 'cmp', 'add', 'pop', 'test', 'jz', 'jmp', 'retn', 'xor', 'tes'] #13
# 전체 opcode
columns = top10.copy()
hex_d = {}
ngram = {}

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

def confirm_command(command, command_d):
    #print(command)
    if command in command_d:
        # 해당 키가 존재할 경우
        command_d[command] += 1
    elif not command in command_d:
        # 해당 키가 존재하지 않을 경우
        command_d[command] = 1
    #print(command, command_d[command])
    #time.sleep(1)
    return command_d

# opcode_count
#opcode_count()

# hex_d => opcode : hex값


# 상위 opcode hex index
for op in columns:
    num = str(init)
    num = "0x"+num.zfill(3)
    hex_d[op] = num
    init += 1
    
# main함수
# main폴더안에 데이터 폴더 이름 모아둠
main_l = os.listdir(dir_base+data_offset)
for l in main_l:
    if(len(l.split('.'))==1):
        cur_datas.append(l)
del main_l # 사용다한 main_l 삭제

# 폴더용(6개)
for cur_data_i in range(1): # TEST용
#for cur_data_i in range(len(cur_datas)):

    # init
    command_d = {}
    command_l = []

    print("["+cur_datas[cur_data_i]+" 진행중"+"]")
    # 윈도우 : \\ , 맥 : /
    cur_path = dir_base + data_offset + "/" + cur_datas[cur_data_i]
    data_l = os.listdir(cur_path)

    # 파일별로
    #for i in range(1): # test용도
    for i in range(len(data_l)):
        dq = deque([])
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
                
                # queue - opcode[A,command,B]
                if(len(dq)<3):
                    dq.append(command)
                else:
                    dq.popleft()
                    dq.append(command)
                
                # opcode : hex 제작
                if not command in columns:
                    columns.append(command)
                    # *
                    num = str(hex(init))[2:]
                    num = "0x"+num.zfill(3)
                    hex_d[command] = num
                    init += 1
                    #time.sleep(1)
                    
                # create index
                #center = dq[1] # 중앙의 Opcode
                # 중앙의  Opcode가 top10에 있다면
                if(len(dq)>2):
                    if dq[1] in top10:
                        h1 = hex_d[dq[0]] + hex_d[dq[1]][2:]
                        h2 = hex_d[dq[1]] + hex_d[dq[2]][2:]
                        if (h1 in ngram):
                            ngram[h1] += 1
                        else:
                            ngram[h1] = 1
                    
                        if(h2 in ngram):
                            ngram[h2] += 1
                        else:
                            ngram[h2] = 1
            
    #print(len(ngram.keys()))
            
    del dq

n_path = dir_base + "/n-gram.txt"
count = 1
n_key = list(ngram.keys())

c_ngram = ngram.copy() # copy본
c_ngram = sorted(c_ngram.items(), key=lambda x: x[1], reverse=True)
# => (2gram : count)

# ngram 상위60개 출력 - 5만개 이상
# 2gram top 60개 ','
string = ''
top60_2gram_path = dir_base + "/top60_2gram.txt"
with open(top60_2gram_path,'w') as f:
    for i in range(60):
        string = string + c_ngram[i][0] + ','
    string = string[:-1]+'\n'
    f.write(string)