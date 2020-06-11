'''
算术表达式改进文法：
    E -> TE1
    E1 -> +TE1|-TE1|&
    T -> FT1
    T1 -> *FT1|/FT1|%FT1|&
    F -> (E)|DIGIT|ID

布尔表达式改进文法：
    B -> HB1
    B1 -> && B | &
    H -> GH1
    H1 -> || H | &
    G -> F G1 | !B | (B)
    G1->ROP F|$
    ROP -> < | > | == | !=|>=|<=

声明语句文法：
    X -> YZ;
    Y -> int|char|bool
    Z -> MZ1
    Z1 -> ,Z|&
    M -> ID M1
    M1 -> = E|&

赋值语句文法：
    R -> R1R2;
    R1->ID = ER2
    R2->,R1 | $
语句文法：
    Q->idO | $
    O->++|--|$
    I -> if(B){A}ELSE | while(B){A} | for(RB;Q){A}
    ELSE->else{A}|$
    A -> CA|&
    C -> X|R|I


main函数文法：
    S->void main ( ) { A }
'''
import json
token_list = []
token_index = 0
token = []
wrong = []
#语义
variable_table = []
semAnalyse = []
variable_type = ''
#四元式
temp_var = 0
NXQ = 0
quaternion = []   #四元式列表
def newtemp():
    global temp_var
    temp_var+=1
    return 'T'+str(temp_var)

def GETCODE(OP,ARG1,ARG2,RESULT):
    global NXQ
    quaternion.insert(NXQ,[OP,ARG1,ARG2,RESULT])
    NXQ+=1


def lookup(varname):
    for i in variable_table:
        if i[0]==varname:
            return True
    return False


def clear():
    global token_list,token_index,token,wrong,variable_table,semAnalyse
    global variable_type,temp_var,NXQ,quaternion
    token_list = []
    token_index = 0
    token = []
    wrong = []
    #语义
    variable_table = []
    semAnalyse = []
    variable_type = ''
    #四元式
    temp_var = 0
    NXQ = 0
    quaternion = []   #四元式列表

def get_token():
    clear()
    with open('./tokenList.txt',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            token_list.append(line.replace('\n','').split(' '))
    print(token_list)

def GetNextToken():
    global token_index
    if token_index>=len(token_list):
        return
    token_index+=1
    return token_list[token_index-1]

def error(st = ''):
    global token_index
    if st!='':
        token_index -= 1
        line = int(token_list[token_index][2])-1
        wrong.append('line:'+str(line)+'   缺少'+st)
    else:
        wrong.append('错误')


def A():
    global token
    if token[0] in ['int','char','bool','if','while','for'] or token[1]=='800':
        C()
        A()
def C():
    global token
    if token[0] in ['int','char','bool']:
        X()
    elif token[0] in ['if','while','for']:
        I()
    elif token[1]=='800':
        R()
    else:
        error()
def X():
    global token
    if token[0] in ['int','char','bool']:
        Y()
        Z()
        if token[0]!=';':
            error(';')
        token=GetNextToken()
    else:
        error('关键声明语句')
def Y():
    global token,variable_type
    if token[0] in ['int','char','bool']:
        variable_type = token[0]
        token = GetNextToken()
    else:
        error('关键声明语句')

def Z():
    global token
    if token[1]!='800':
        error('标识符')
    M()
    Z1()

def M():
    global token,variable_type
    if token[1]=='800':
        id = token[0]
        if not lookup(token[0]):
            variable_table.append([token[0],variable_type])
        else:
            semAnalyse.append('line: '+str(token[2])+'    重定义变量'+token[0])
        token = GetNextToken()
        M1(id)
    else:
        error('标识符')

def M1(id):
    global token
    if token[0]=='=':
        token = GetNextToken()
        es = E()
        GETCODE('=',es,'',id)

def E():
    global token
    if token[0] =='(' or token[1] in ['800','500']:
        e1i = T()
        es = E1(e1i)
        return es
    else:
        error()
def T():
    global token
    if token[0] =='(' or token[1] in ['800','500']:
        t1i = F()
        ts = T1(t1i)
        return ts
    else:
        error()

def F():
    global token
    if token[0]=='(':
        token = GetNextToken()
        fval = E()
        if token[0]!=')':
            error(')')
        token = GetNextToken()
        return fval
    elif token[1] in ['800','500']:
        fval = token[0]
        token = GetNextToken()
        return fval
    else:
        error('数字标识符或左括号')

def T1(t11i):
    global token
    if token[0] in ['*','/','%']:
        temp = token[0]
        if token[0]!='*':
            token = GetNextToken()
            if token[0]=='0':
                semAnalyse.append('line: '+str(token[2])+'    除数为0')
        else:
            token = GetNextToken()
        fval = F()
        t1i = newtemp()
        if temp=='*':
            GETCODE('*',t11i,fval,t1i)
        elif temp=='/':
            GETCODE('/',t11i,fval,t1i)
        else:
            GETCODE('%',t11i,fval,t1i)
        t1s = T1(t1i)
        return t1s
    else:
        return t11i
def E1(e11i):
    global token
    if token[0] in ['+','-']:
        temp = token[0]
        token = GetNextToken()
        tval = T()
        e1i = newtemp()
        if temp=='+':
            GETCODE('+',e11i,tval,e1i)
        else:
            GETCODE('-',e11i,tval,e1i)
        es = E1(e1i)
        return es
    else:
        return e11i
def Z1():
    global token
    if token[0]==',':
        token = GetNextToken()
        Z()
def R():
    global token
    R1()
    R2()
    if token[0] != ';':
        error(';')
    token = GetNextToken()
def R1():
    global token
    if token[1]!='800':
        error('标识符')
    else:
        if not lookup(token[0]):
            semAnalyse.append('line: '+str(token[2])+'    变量未定义'+token[0])
    id = token[0]
    token = GetNextToken()
    if token[0]!='=':
        error('=')
    token = GetNextToken()
    es = E()
    GETCODE('=',es,'',id)
    R2()
def R2():
    global token
    if token[0]==',':
        token = GetNextToken()
        R1()


def I():
    global token
    if token[0]=='if':
        token = GetNextToken()
        if token[0]!='(':
            error('(')
        token = GetNextToken()
        val = B()

        GETCODE('jnz',val,'',NXQ+2)
        GETCODE('j','_','_',0)

        if token[0]!=')':
            error(')')
        token = GetNextToken()
        if token[0]!='{':
            error('{')
        token = GetNextToken()
        A()

        GETCODE('j','_','_',-1)

        if token[0]!='}':
            error('}')
        token = GetNextToken()
        ELSE()
    elif token[0]=='while':
        token = GetNextToken()
        if token[0]!='(':
            error('(')
        token = GetNextToken()
        temp = NXQ
        bval = B()

        GETCODE('jnz',bval,'_',NXQ+2)
        GETCODE('j','_','_',-2)


        if token[0]!=')':
            error(')')
        token = GetNextToken()
        if token[0]!='{':
            error('{')
        token = GetNextToken()
        A()

        GETCODE('j','_','_',temp)

        if token[0]!='}':
            error('}')
        token = GetNextToken()

        for i in reversed(quaternion):
            if i[3]==-2:
                i[3] = NXQ
                break
    elif token[0]=='for':
        token = GetNextToken()
        if token[0]!='(':
            error('(')
        token = GetNextToken()
        R()
        temp1 = NXQ
        bval = B()
        GETCODE('jnz',bval,'_',-1)  #真
        GETCODE('j','_','_',-2)  #假

        if token[0]!=';':
            error(';')
        token = GetNextToken()
        temp2 = NXQ
        Q()
        GETCODE('j', '_', '_', temp1)
        for i in reversed(quaternion):  # 找真出口
            if i[3] == -1:
                i[3] = NXQ
                break

        if token[0]!=')':
            error(')')
        token = GetNextToken()
        if token[0]!='{':
            error('{')
        token = GetNextToken()
        A()

        GETCODE('j','_','_',temp2)
        for i in reversed(quaternion):  # 找假出口
            if i[3] == -2:
                i[3] = NXQ
                break

        if token[0]!='}':
            error('}')
        token = GetNextToken()
    else:
        error('控制语句')

def Q():
    global token
    if token[1]=='800':
        val = token[0]
        token = GetNextToken()
        O(val)

def O(val):
    global token
    if token[0] in ['++','--']:
        GETCODE(token[0],val,'_',val)
        token = GetNextToken()
    elif token[0] =='=':
        token = GetNextToken()
        eval = E()
        GETCODE('=',eval,'_',val)

def ELSE():
    global token
    if token[0]=='else':
        token = GetNextToken()
        if token[0]!='{':
            error('{')
        token = GetNextToken()
        for i in reversed(quaternion):  #假出口
            if i[3]==0:
                i[3] = NXQ
                break
        A()
        for i in reversed(quaternion):  # goto
            if i[3] == -1:
                i[3] = NXQ
                break
        if token[0]!='}':
            error('}')
        token = GetNextToken()
    else:
        for i in reversed(quaternion):  #假出口
            if i[3]==0:
                i[3] = NXQ
                break
        for i in reversed(quaternion):  #goto
            if i[3] == -1:
                i[3] = NXQ
                break
def B():
    hval = H()
    b1val = B1(hval)
    return b1val
def H():
    gval = G()
    h1val = H1(gval)
    return h1val
def G():
    global token
    if token[0]=='!':
        token = GetNextToken()
        temp = newtemp()
        bval = B()
        GETCODE('!',bval,'_',temp)
        return temp
    elif token[0]=='(':
        token = GetNextToken()
        bval = B()
        if token[0]!=')':
            error()
        token = GetNextToken()
        return bval
    elif token[1]=='800' or token[1]=='500':
        fval = F()
        g1val = G1(fval)
        return g1val
    else:
        error('布尔表达式')
def G1(fval):
    global token
    if token[0] in ['<','>','==','!=','>=','<=']:
        op = ROP()
        f1val = F()
        temp = newtemp()
        GETCODE(op,fval,f1val,NXQ+3)
        GETCODE('=','0','_',temp)
        GETCODE('j','_','_',NXQ+2)
        GETCODE('=','1','_',temp)
        return temp
    else:
        return fval
def ROP():
    global token
    if token[0] in ['<','>','==','!=','>=','<=']:
        temp = token[0]
        token = GetNextToken()
        return temp
    else:
        error('操作符')

def H1(gval):
    global token
    if token[0]=='&&':
        token = GetNextToken()
        hval = H()
        temp = newtemp()
        GETCODE('&&',gval,hval,temp)
        return temp
    else:
        return gval
def B1(hval):
    global token
    if token[0] == '||':
        token = GetNextToken()
        temp = newtemp()
        bval = B()
        GETCODE('||',hval,bval,temp)
        return temp
    else:
        return hval
def parser():
    global token
    token = GetNextToken()
    if token[0]!='void':
        error('void')
    token = GetNextToken()
    if token[0]!='main':
        error('main')
    token = GetNextToken()
    if token[0]!='(':
        error('(')
    token = GetNextToken()
    if token[0]!=')':
        error(')')
    token = GetNextToken()
    if token[0] != '{':
        error('{')
    token = GetNextToken()
    A()
    if token[0] != '}':
        error('}')
    token = GetNextToken()

    if token[0] =='#':
        print('分析完成！')
    else:
        error()


def write_quater():
    with open('中间代码.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(quaternion))
        f.close()



if __name__ == '__main__':
    
    get_token()
    parser()
    write_quater()
    #for i in variable_table:
        #print(i)
    for i in wrong:     #语法错误
        print(i)
    for i in semAnalyse:    #语义错误
        print(i)
    for i in range(len(quaternion)):   #四元式
        print(i,'   ',quaternion[i])