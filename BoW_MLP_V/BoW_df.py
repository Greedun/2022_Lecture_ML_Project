# BoW

# shuffle : https://www.delftstack.com/ko/howto/python/python-shuffle-array/

columns = ['mov', 'push', 'call', 'lea', 'cmp', 'add', 'pop', 'test', 'jz', 'jmp', 'jnz', 'sub', 'retn', 'xor', 'and', 'inc', 'movzx', 'or', 'jge', 'movsx', 'jnb', 'fnclex', 'shl', 'fld', 'dec', 'fstp', 'imul', 'jb', 'jl', 'jle', 'shr', 'movsd', 'rep', 'adc', 'sbb', 'neg', 'sar', 'setnz', 'jg', 'lock', 'movss', 'nop', 'ja', 'jbe', 'xchg', 'leave', 'fmul', 'movq', 'fxch', 'cdq', 'idiv', 'movaps', 'movd', 'paddw', 'pxor', 'paddusw', 'punpcklbw', 'jns', 'setalc', 'std', 'jnp', 'not', 'fadd', 'rol', 'js', 'setz', 'fild', 'paddd', 'pmullw', 'no']
init = [0 for i in range(len(columns))]

# main : 교수님이 원하는 실행형태 구축한 곳
import os,time

dir_base = os.getcwd()
data_offset = "/main"
cur_data_i = '' # 추출하고 있는 데이터폴더 위치 체크(인덱스)
cur_datas = []

command_l = [] # dir : 서로 다른 명령어 모아두는 곳
command_d = {} # dic : 만약 빈도수까지 체크할경우 dictionary사용하여 체크
t_l = []

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
    t_l = []

    print("["+cur_datas[cur_data_i]+" 진행중"+"]")
    # 윈도우 : \\ , 맥 : /
    cur_path = dir_base + data_offset + "/" + cur_datas[cur_data_i]
    data_l = os.listdir(cur_path)

    # 파일별로
    #for i in range(1): # test용도
    for i in range(len(data_l)):
        op_l = init.copy()
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
                
                if command in columns:
                    index = columns.index(command)
                    op_l[index] += 1
        t_l.append(op_l)
    
    # csv파일 생성
    csv_path = dir_base + "/dataset/" + str(cur_datas[cur_data_i]) + ".csv"
    with open(csv_path, 'w') as f:
        for i in range(len(t_l)):
            string = str(t_l[i])[1:-1].replace(" ","")+"\n"
            f.write(string)
                        
    command_l = sorted(command_l)