# main : 교수님이 원하는 실행형태 구축한 곳
import os

dir_base = os.getcwd()
data_offset = "\main"
cur_data_i = '' # 추출하고 있는 데이터폴더 위치 체크(인덱스)
cur_datas = []

command_l = [] # dir : 서로 다른 명령어 모아두는 곳
command_d = {} # dic : 만약 빈도수까지 체크할경우 dictionary사용하여 체크

# main폴더안에 데이터 폴더 이름 모아둠
main_l = os.listdir(dir_base+data_offset)
for l in main_l:
    if(len(l.split('.'))==1):
        cur_datas.append(l)
del main_l # 사용다한 main_l 삭제

#for cur_data_i in range(1): # TEST용
for cur_data_i in range(len(cur_datas)):
    print("["+cur_datas[cur_data_i]+" 진행중"+"]")
    cur_path = dir_base + data_offset + "\\" + cur_datas[cur_data_i]
    data_l = os.listdir(cur_path)
    for i in range(len(data_l)):
        if(i%100==0):
            print(str(i)+" - ",data_l[i])
            #print(command_l)
        data_path = cur_path + "\\" + data_l[i]
        with open(data_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                command = line.split(' ')[0]
                if command.find('\n') != -1:
                    command = command[:-1]
                if not command in command_l:
                        command_l.append(command)

command_l = sorted(command_l)
#print(command_l)
#print(len(command_l))

# 알파벳별로 명령어 분류
al_l = [[] for i in range(26)] # 알파벳 26 / a(0x61) - z(0x7A)
ci = 0x61
i = 0
file_name = 'command.txt'
file_path = dir_base + '\\' + file_name
with open(file_path,'w') as f:
    for w in command_l:
        wi = w[0]
        while(True):
            if(chr(ci) != wi):
                ci += 1
                i += 1
            else:
                break
        al_l[i].append(w)
    
    ai = 0x61
    for al in al_l:
        f.write("[" + chr(ai) + "] commands\n")
        for a in al:
            f.write(a+'\n')
        f.write('\n')
        ai += 1


# 
