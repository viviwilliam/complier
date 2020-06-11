
FIRST = dict()  # FIRST集
FOLLOW = dict()  # FOLLOW集
LAN = dict()  # 文法
Table = dict()  # 分析表
VT = set()  # 终结符
ProcessList = dict()
errorflag = 0
def get_lan():
    with open('./ll1文法测试.txt',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            splitlist = line[3:].replace("\n", "").split("|")
            LAN[line[0]] = splitlist

def get_first():
    length = {}
    for k in LAN:
        FIRST[k]= []
        length[k] = 0
    flag = True
    while flag==True:
        for k in LAN:
            l = LAN[k]
            for s in l:
                if not (s[0].isupper()) or s[0]=='ε':   #规则2
                    FIRST[k].append(s[0])
                elif s[0].isupper():                   #规则3.1
                    temp = FIRST[s[0]][:]
                    if 'ε' in temp:
                        temp.remove('ε')
                    FIRST[k].extend(temp)
                    for i in range(len(s) - 1):         #规则3.2.1
                        if s[i].isupper() and 'ε' in FIRST[s[i]]:
                            if s[i + 1].isupper():
                                t = FIRST[s[i + 1]][:]
                                if 'ε' in t:
                                    t.remove('ε')
                                FIRST[k].extend(t)
                            else:
                                FIRST[k].append(s[i + 1])
                                break
                        else:
                            break
                    ft = 0                                  #规则3.2.2
                    for i in s:
                        if i.isupper() and 'ε' in FIRST[i]:
                            continue
                        else:
                            ft=1
                            break
                    if ft==0:
                        FIRST[k].append('ε')
                FIRST[k] = list(set(FIRST[k]))
        fg = 0
        for k in LAN:
            if length[k]!=len(FIRST[k]):
                length[k]=len(FIRST[k])
                fg=1
        if fg==0:
            flag=False
    print("文法为：%s" % LAN)
    print("FIRST集为：%s" % FIRST)

def get_follow():
    condition = lambda t: t != 'ε'  # 过滤器用于过滤空串
    for k in LAN:  # 新建list
        FOLLOW[k] = list()
        if k == list(LAN.keys())[0]:
            FOLLOW[k].append('#')
    for i in range(2):
        for k in LAN:
            l = LAN[k]
            for s in l:
                if s[len(s) - 1].isupper():
                    FOLLOW[s[len(s) - 1]].extend(FOLLOW[k])  # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中
                    FOLLOW[s[len(s) - 1]] = list(filter(condition, FOLLOW[s[len(s) - 1]]))  # 去除空串
                for index in range(len(s) - 1):
                    if s[index].isupper():
                        if s[index + 1].isupper():  # 若A→αBβ是一个产生式，则把FIRST(β)\{ε}加至FOLLOW(B)中；
                            FOLLOW[s[index]].extend(FIRST[s[index + 1]])
                            FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串
                        if not (s[index + 1].isupper()) and (s[index + 1] != 'ε'):
                            FOLLOW[s[index]].append(s[index + 1])
                        emptyflag = 1
                        for i in range(index + 1, len(s)):
                            if not (s[i].isupper()) or (s[i].isupper() & ('ε' not in FIRST[s[i]])):
                                emptyflag = 0
                                break
                        if emptyflag == 1:
                            FOLLOW[s[index]].extend(FOLLOW[k])  # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                            FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串
    for k in FOLLOW:  # 去重
        FOLLOW[k] = list(set(FOLLOW[k]))
    print('FOLLOW集为：%s' % FOLLOW)

def get_VT():
    VT.add('#')
    for l in LAN.values():
        for s in l:
            for c in s:
                if not (c.isupper()) and (c != 'ε'): VT.add(c)
    print('终结符为：%s' % VT)

def generate_table():
    get_VT()
    for k in LAN:  # 初始化分析表
        Table[k] = dict()
        for e in VT:
            Table[k][e] = None
    for k in LAN:
        l = LAN[k]
        for s in l:
            if s[0].isupper():
                for e in VT:
                    fg = 0
                    for j in s:
                        if e in FIRST[j]:
                            Table[k][e] = s
                        if 'ε' not in FIRST[j]:
                            fg=1
                            break
                    if fg==0:
                        for c in FOLLOW[k]:
                            Table[k][c] = s
            if s[0] in VT:
                Table[k][s[0]] = s
            if s=='ε':
                for c in FOLLOW[k]:
                    Table[k][c] = s
    print('分析表为：%s' % Table)

def analyze(inputstr1):
    global errorflag
    inputstr = inputstr1+'#'  # 输入任意字符串
    inputstr = list(inputstr[::-1])
    stack = list()
    stack.append('#')  # "#"入栈
    stack.append(list(LAN.keys())[0])  # 开始符入栈
    errorflag = 0  # 出错标识
    count = 0  # 插入列表时的索引
    ProcessList.clear()
    ProcessList[count] = (''.join(stack), ''.join(inputstr), ' ')
    while True:
        for i in inputstr:
            if i not in VT:
                errorflag = 1
                break
        if errorflag==1:
            break
        count += 1
        current = stack.pop()
        if current in VT and current!='#':
            if current == inputstr[-1]:
                inputstr.pop()
            else:
                errorflag=1
                break
        elif current=='#':
            if current!=inputstr[-1]:
                errorflag=1
            break
        elif Table[current][inputstr[-1]] !=None:
            if Table[current][inputstr[-1]]!='ε':
                temp = list(Table[current][inputstr[-1]][::-1])
                stack.extend(temp)
                ProcessList[count] = (''.join(stack), ''.join(inputstr), current + '->' + Table[current][inputstr[-1]])
            else:
                ProcessList[count] = (''.join(stack), ''.join(inputstr), current + '->ε')
        else:
            errorflag=1
            break
    if errorflag==1:
        print('分析失败')
    else:
        print('分析成功')
        print('步骤\t符号栈\t输入串\t所用产生式')
        for i in ProcessList.keys():
            print(str(i)+'\t\t'+ProcessList[i][0]+'\t\t'+ProcessList[i][1][::-1]+'\t\t'+ProcessList[i][2])
if __name__ == '__main__':
    get_lan()
    get_first()
    get_follow()
    generate_table()
    analyze(input())
