# 현재 할일 : 많은 쓴 opcode 상위 50개 추출

# main : 교수님이 원하는 실행형태 구축한 곳
import os, time, sys

dir_base = os.getcwd()
data_offset = "/main"
top100_report_offset = "/top100_report"
cur_data_i = '' # 추출하고 있는 데이터폴더 위치 체크(인덱스)
cur_datas = []

#command_l = [] # dir : 서로 다른 명령어 모아두는 곳
#command_d = {} # dic : 만약 빈도수까지 체크할경우 dictionary사용하여 체크

# dictionary key로 명령어가 존재하지 않을 경우
# => 존재한다면 그냥 value + 1 / 존재하지 않다면 추가하고 value + 1
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

def opcode_count():
    op = []
    opcode_path = dir_base + "/top100_report/opcode.txt"
    with open(opcode_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                opcode_l = line[:-1].split('_')
                for op_i in opcode_l:
                    if not op_i in op:
                        op.append(op_i)
    print(op)
    print(len(op))
    sys.exit(1)

# opcode_count
#opcode_count()

# main함수
# main폴더안에 데이터 폴더 이름 모아둠
main_l = os.listdir(dir_base+data_offset)
for l in main_l:
    if(len(l.split('.'))==1):
        cur_datas.append(l)
del main_l # 사용다한 main_l 삭제

# 폴더용(6개)
#for cur_data_i in range(1): # TEST용
for cur_data_i in range(len(cur_datas)):

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
                if not command in command_l:
                    command_l.append(command)
                
                command_d = confirm_command(command, command_d)
                        
    command_l = sorted(command_l)
    command_d = sorted(command_d.items(), key=lambda x: x[1], reverse=True)
    
    top100_path = dir_base + "/top100_report/" + cur_datas[cur_data_i] + ".txt" # 여기서부터 고침
    
    # 파일이 끝났을때 로깅해주는 코드
    # 상위 50개?
    test = []
    with open(top100_path, "w") as f:
        count = 0
        for i in range(50):
            count +=1
            string = "("+str(count)+") "+command_d[i][0]+" : "+str(command_d[i][1])+"\n"
            f.write(string)
            test.append(command_d[i][0])
        t = "_".join(test)+"\n"
        f.write(t)


'''
# opcode count
count = 0
for i in range(len(command_l)):
    command = command_l[i]
    # value가 1인것은 제외
    if(command_d[command] != 1):
        count += 1
        string = "(",count,") ",command," : ",command_d[command]
        print(str)
'''