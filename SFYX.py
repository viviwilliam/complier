FIRSTVT = dict()  # FIRST集
LASTVT = dict()  # FOLLOW集
LAN = dict()  # 文法
VT = set()  # 终结符
stack = list()  #栈
S = list()   #符号栈
Table = dict()  #优先关系表
ProcessList = dict()
errorfalg = 0

def get_lan():
    with open('./算符文法测试.txt',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            splitlist = line[3:].replace("\n", "").split("|")
            LAN[line[0]] = splitlist
    print('文法为', LAN)

def get_VT():
    VT.add('#')
    for l in LAN.values():
        for s in l:
            for c in s:
                if not (c.isupper()) and (c != 'ε'): VT.add(c)
    print('终结符为：%s' % VT)

def insert(F,p,a):
    if not F[p][a]:
        F[p][a] = True
        stack.append((p,a))
def get_firstvt():
    F = {}
    get_VT()
    for k in LAN:  # 初始化
        F[k] = dict()
        for e in VT:
            F[k][e] = False
    for k in LAN:       #规则1
        l = LAN[k]
        for s in l:
            if not s[0].isupper():
                insert(F,k,s[0])
            elif len(s)>=2 and s[0].isupper() and (not s[1].isupper()):
                insert(F,k,s[1])
    while len(stack)!=0:    #规则2
        (Q,a) = stack.pop()
        for k in LAN:
            l = LAN[k]
            for s in l:
                if s[0]==Q:
                    insert(F,k,a)
    for k in F:
        l = F[k]
        FIRSTVT[k] = []
        for s in l:
            if F[k][s]==True:
                FIRSTVT[k].append(s)
    print('FIRSTVT为',FIRSTVT)

def get_lastvt():
    F = {}
    for k in LAN:  # 初始化
        F[k] = dict()
        for e in VT:
            F[k][e] = False
    for k in LAN:  # 规则1
        l = LAN[k]
        for s in l:
            if not s[-1].isupper():
                insert(F, k, s[-1])
            elif len(s) >= 2 and s[-1].isupper() and (not s[-2].isupper()):
                insert(F, k, s[1])
    while len(stack) != 0:  # 规则2
        (Q, a) = stack.pop()
        for k in LAN:
            l = LAN[k]
            for s in l:
                if s[-1] == Q:
                    insert(F, k, a)
    for k in F:
        l = F[k]
        LASTVT[k] = []
        for s in l:
            if F[k][s] == True:
                LASTVT[k].append(s)
    print('LASTVT为', LASTVT)

def generate_table():
    for k in VT:
        Table[k] = {}
        for j in VT:
            Table[k][j] = None
    for k in LAN:
        l = LAN[k]
        for s in l:
            for i in range(len(s)-1):
                if s[i] in VT and s[i+1] in VT:
                    Table[s[i]][s[i+1]] = '='
                if i<len(s)-2 and s[i] in VT and s[i+1] not in VT and s[i+2] in VT:
                    Table[s[i]][s[i+2]] = '='
                if s[i] in VT and s[i+1] not in VT:
                    for j in FIRSTVT[s[i+1]]:
                        Table[s[i]][j] = '<'
                if s[i] not in VT and s[i+1] in VT:
                    for j in LASTVT[s[i]]:
                        Table[j][s[i+1]] = '>'
    #单独处理   #E#
    E = list(LAN.keys())[0]
    for j in FIRSTVT[E]:
        Table['#'][j] = '<'
    for j in LASTVT[E]:
        Table[j]['#'] = '>'
    Table['#']['#'] = '='

    for i in Table:
        print(i+'   ',Table[i])

def analyse(inputstr1):
    global errorfalg
    for i in range(100):
        S.append('')
    errorfalg = 0
    inputstr = inputstr1+'#'
    inputstr = list(inputstr[::-1])
    k = 0           #栈顶指针
    S[k] = '#'
    count = 0
    ProcessList.clear()
    ProcessList[count] = (''.join(S[0:k+1]), ''.join(inputstr), ' ')
    while True:
        for i in inputstr:
            if i not in VT:
                errorfalg = 1
                break
        if errorfalg==1:
            break
        a = inputstr[-1]
        if S[k] in VT:
            j = k
        else:
            j = k-1
        while Table[S[j]][a] == '>':
            while True:
                Q = S[j]
                if S[j-1] in VT:
                    j = j-1
                else:
                    j=j-2
                if Table[S[j]][Q] == '<':
                    break

            # 把S[j+1]....S[k]归约为某个N
            for m in LAN:
                n = LAN[m]
                for i in n:
                    flag = 0
                    if len(i)!=k-j:
                        flag = 1
                        continue
                    for coun in range(len(i)):
                        if S[j+1+coun] != i[coun]:
                            if S[j+1+coun] not in VT and i[coun] not in VT:
                                continue
                            else:
                                flag=1
                                break
                    if flag==0:
                        N = m
                        temp = i
                        break
                if flag==0:
                    break
            k = j+1
            S[k] = N
            count+=1
            ProcessList[count] = (''.join(S[0:k+1]), ''.join(inputstr), '规约，用'+N+'->'+temp)
            #print(str(count)+'\t\t'+ProcessList[count][0]+'\t\t'+ProcessList[count][1][::-1]+'\t\t'+ProcessList[count][2])
        if Table[S[j]][a] == '<' or Table[S[j]][a]== '=':  #移入操作
            k=k+1
            S[k] = a
            inputstr.pop()
            count+=1
            ProcessList[count] = (''.join(S[0:k+1]),''.join(inputstr), '移进')
            #print(str(count) + '\t\t' + ProcessList[count][0] + '\t\t' + ProcessList[count][1][::-1] + '\t\t' +
                  #ProcessList[count][2])
        else:
            errorfalg = 1
            break
        if a=='#':
            break
    if errorfalg==1:
        print('分析失败')
    else:
        print('分析成功')
        print('步骤\t符号栈\t输入串\t所用产生式')
        for i in ProcessList.keys():
            print(str(i)+'\t\t'+ProcessList[i][0]+'\t\t'+ProcessList[i][1][::-1]+'\t\t'+ProcessList[i][2])

if __name__ =='__main__':
    get_lan()
    get_firstvt()
    get_lastvt()
    generate_table()
    analyse()