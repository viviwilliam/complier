import json
quaternion = []
assemble = []
t_var = 0
def newt():
    global t_var
    t_var+=1
    return '_t'+str(t_var)

def read_quater():
    global quaternion
    with open('中间代码.txt','r',encoding='utf-8') as f:
        quaternion = json.loads(f.read())

def translate():
    for i in quaternion:
        t = []
        if i[0]=='=':
            t.append('MOV AX,'+i[1])
            t.append('MOV '+i[3]+',AX')
            assemble.append(t)
        elif i[0]=='++':
            t.append('MOV AX,' + i[1])
            t.append('ADD AX,1')
            t.append('MOV ' + i[3] + ',AX')
            assemble.append(t)
        elif i[0]=='--':
            t.append('MOV AX,' + i[1])
            t.append('SUB AX,1')
            t.append('MOV ' + i[3] + ',AX')
            assemble.append(t)
        elif i[0]=='+':
            t.append('MOV AX,'+i[1])
            t.append('ADD AX,' + i[2])
            t.append('MOV '+i[3]+',AX')
            assemble.append(t)
        elif i[0]=='-':
            t.append('MOV AX,' + i[1])
            t.append('SUB AX,' + i[2])
            t.append('MOV ' + i[3] + ',AX')
            assemble.append(t)
        elif i[0]=='*':
            t.append('MOV AX,' + i[1])
            t.append('MOV BX,' + i[2])
            t.append('MUL BX')
            t.append('MOV ' + i[3] + ',AX')
            assemble.append(t)
        elif i[0]=='/':
            t.append('MOV AX,' + i[1])
            t.append('MOV DX,0')
            t.append('MUL AX,'+i[2])
            t.append('DIV BX')
            t.append('MOV ' + i[3] + ',AX')
            assemble.append(t)
        elif i[0]=='%':
            t.append('MOV AX,' + i[1])
            t.append('MOV DX,0')
            t.append('MUL AX,' + i[2])
            t.append('DIV BX')
            t.append('MOV ' + i[3] + ',DX')
            assemble.append(t)
        elif i[0] in ['>','>=','<','<=','==','!=']:
            judge_size(i[0],i)
        elif i[0]=='&&':
            t.append('MOV DX,0')
            t.append('MOV AX,'+i[1])
            t.append('CMP AX,0')
            temp = newt()
            t.append('JE '+temp)
            t.append('MOV AX,'+i[2])
            t.append('CMP AX,0')
            t.append('JE ' + temp)
            t.append('MOV DX,1')
            t.append(temp+':MOV '+i[3]+',DX')
            assemble.append(t)
        elif i[0]=='||':
            t.append('MOV DX,1')
            t.append('MOV AX,' + i[1])
            t.append('CMP AX,0')
            temp = newt()
            t.append('JNE ' + temp)
            t.append('MOV AX,' + i[2])
            t.append('CMP AX,0')
            t.append('JNE ' + temp)
            t.append('MOV DX,0')
            t.append(temp + ':MOV ' + i[3] + ',DX')
            assemble.append(t)
        elif i[0]=='!':
            t.append('MOV DX,1')
            t.append('MOV AX,' + i[1])
            t.append('CMP AX,0')
            temp = newt()
            t.append('JE ' + temp)
            t.append('MOV DX,' + i[2])
            t.append(temp + ':MOV ' + i[3] + ',DX')
            assemble.append(t)
        elif i[0]=='j':
            t.append('JMP far ptr '+str(i[3]))
            assemble.append(t)
        elif i[0]=='jz':
            t.append('MOV AX,'+i[1])
            t.append('CMP AX,0')
            temp = newt()
            t.append('JNE '+temp)
            t.append('JMP far ptr '+str(i[3]))
            t.append(temp+':NOP')
            assemble.append(t)
        elif i[0]=='jnz':
            t.append('MOV AX,' + i[1])
            t.append('CMP AX,0')
            temp = newt()
            t.append('JE ' + temp)
            t.append('JMP far ptr ' + str(i[3]))
            t.append(temp + ':NOP')
            assemble.append(t)
def judge_size(symbol,i):
    global assemble
    t = []
    t.append('MOV AX,' + i[1])
    t.append('CMP AX,' + i[2])
    if symbol=='<':
        t.append('JB ' + str(i[3]))
    elif symbol=='>=':
        t.append('JNB ' + str(i[3]))
    elif symbol == '>':
        t.append('JA ' + str(i[3]))
    elif symbol == '<=':
        t.append('JNA ' + str(i[3]))
    elif symbol == '==':
        t.append('JE ' + str(i[3]))
    elif symbol == '!=':
        t.append('JNE ' + str(i[3]))
    assemble.append(t)

def isinjump(s):
    jmp = ['JMP far ptr','JA','JNA','JB','jNB']
    for i in jmp:
        if i in s:
            return True
    return False

def modify_jmp():
    for i in assemble:
        for j in range(len(i)):             #每个汇编代码
            if isinjump(i[j]):
                num = i[j].split(' ')[-1]
                if num.isdigit():
                    id = int(num)
                    temp = newt()
                    assemble[id][0] = temp+':'+assemble[id][0]
                    i[j] = i[j].replace(num,temp)

if __name__ == '__main__':
    read_quater()
    translate()
    for i in range(len(quaternion)):
        print(i,'   ',quaternion[i])
    modify_jmp()
    for i in assemble:
        for j in i:
            print(j)
