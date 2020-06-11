class token:
    def __init__(self,word,code,row,col):
        self.word = word
        self.code = code
        self.row = row
        self.col =  col
tokendic = {}
tokens = []
wrong = []
num_line = 1
def read_file(filepath):
    print(filepath)
    with open(filepath,encoding='utf-8') as f:
        content = f.read()
    return content

#识别标识符
def regid(content,index):
    state = 0
    word = ""
    while state!=2:
        if state==0:
            if content[index].isalpha() or content[index]=='_':
                word = word+content[index]
                state=1
        elif state==1:
            if content[index].isalpha() or content[index].isdigit() or content[index]=='_':
                word = word+content[index]
            else:
                state=2
        if state==2:
            index-=1
        index+=1
    if word in tokendic.keys():
        tokens.append(token(word,tokendic[word],num_line,0))
    else:
        tokens.append(token(word,800,num_line,0))
    return index
#识别数字
def regnum(content,index):
    yunsuan = ['+','-','*','/','&','|','!','>','<','=','[',']','(',')','%','\n','\t',';',',']
    state = 0
    word = ""
    while state not in [4,14]:
        if state==0:
            if content[index]=='0':
                state=2
            elif content[index].isdigit():
                state=1
            word+=content[index]
        elif state==1:
            if content[index]=='e' or content[index]=='E':
                state=10
                word+=content[index]
            elif content[index] in yunsuan:
                state=4
            elif content[index].isdigit():
                word+=content[index]
            elif content[index]=='.':
                word+=content[index]
                state=8
            else:
                state=14
                word+=content[index]
        elif state==2:
            if content[index]=='.':
                state=8
                word+=content[index]
            elif content[index]>='0' and content[index]<='7':
                word+=content[index]
                state=3
            elif content[index]=='x' or content[index]=='X':
                word+=content[index]
                state=5
            else:
                state=4
        elif state==3:
            if content[index]>='0' and content[index]<='7':
                word+=content[index]
            else:
                state=4
        elif state==5:
            if content[index].isdigit() or content[index].isalpha():
                word+=content[index]
                state=6
        elif state==6:
            if content[index].isdigit() or content[index].isalpha():
                word+=content[index]
            else:
                state=4
        elif state==8:
            if content[index].isdigit():
                state=9
            else:
                state=14
            word+=content[index]
        elif state==9:
            if content[index]=='e' or content[index]=='E':
                word+=content[index]
                state=10
            elif content[index].isdigit():
                word+=content[index]
            elif content[index] in yunsuan:
                state=4
            else:
                word+=content[index]
                state=14
        elif state==10:
            if content[index]=='+' or content[index]=='-':
                state=11
            elif content[index].isdigit():
                state=12
            else:
                state=14
            word+=content[index]
        elif state==11:
            word+=content[index]
            if content[index].isdigit():
                state=12
            else:
                state=14
        elif state==12:
            if content[index].isdigit():
                word+=content[index]
            elif content[index] in yunsuan:
                state=4
            else:
                word+=content[index]
                state=14
        if state==4:
            index-=1
        index+=1
    if state==4:
        tokens.append(token(word,500,num_line,0))
    else:
        wrong.append("line:"+str(num_line)+" "+word+"   实数结构错误")
    return index
#注释和除号
def regnode(content,index):
    global num_line
    state = 0
    word = ''
    while state not in [4,5,6]:
        if state==0:
            if content[index]=='/':
                word+=content[index]
                state=1
        elif state==1:
            if content[index]=='/':
                while content[index]!='\n':
                    index+=1
                num_line+=1
                state=4
            elif content[index]=='*':
                state=2
            elif content[index]=='=':
                word+=content[index]
                state=5
            else:
                state=6
        elif state==2:
            if content[index]=='*':
                state=3
            if content[index]=='\n':
                num_line+=1
        elif state==3:
            if content[index]=='/':
                state=4
            else:
                state=2
            if content[index]=='\n':
                num_line+=1
        if state==6:
            index-=1
        index+=1
    if state!=4:
        tokens.append(token(word,tokendic[word],num_line,0))
    return index
#字符常量
def regchar(content,index):
    zhuanyi = ['a','b','f','r','v','\\','\'','\"','?','t']
    state= 0
    word = ''
    while state not in [4,5]:
        if state==0:
            if content[index]=='\'':
                word+=content[index]
                state=1
        elif state==1:
            if content[index]=='\\':
                state=2
            else:
                state=3
            word+=content[index]
        elif state==2:
            word += content[index]
            if content[index] in zhuanyi:
                state=3
            else:
                state=5
        elif state==3:
            word += content[index]
            if content[index]=='\'':
                state=4
            else:
                state=5
        if state==5:
            index+=1
            while(content[index]!='\''):
                word+=content[index]
                index+=1
            index+=1
            break
        index += 1
    if state!=5:
        tokens.append(token(word,600,num_line,0))
    else:
        wrong.append("line:"+str(num_line)+" "+word+"\'"+"   字符常量不合法")
    return index
#字符串常量
def regstr(content,index):
    state = 0
    word = ""
    while state!=3:
        if state==0:
            if content[index]=="\"":
                word+=content[index]
                state = 1
        elif state==1:
            if content[index]=="\\":
                state=2
            elif content[index]=="\"":
                state=3
            word+=content[index]
        elif state==2:
            word+=content[index]
            state=1
        index+=1
    tokens.append(token(word,700,num_line,0))
    return index
#> >= >> >>= < <= << <<=
def regbs(content,index):
    state = 0
    word = ""
    while state not in [2,4,5,6]:
        if state==0:
            if content[index]=='>' or content[index]=='<':
                word+=content[index]
                state = 1
        elif state==1:
            if content[index]=='=':
                word+=content[index]
                state=2
            elif content[index]==word[0]:
                word+=content[index]
                state=3
            else:
                state=6
        elif state==3:
            if content[index]=='=':
                word+=content[index]
                state=4
            else:
                state=5
        if state==5 or state==6:
            index-=1
        index+=1
    tokens.append(token(word,tokendic[word],num_line,0))
    return index
#* ! ^ % = *= != ^= %= ==
def regae(content,index):
    state = 0
    word = ""
    zifu = ['*','!','^','%','=']
    while state!=2 and state!=3:
        if state==0:
            if content[index] in zifu:
                word+=content[index]
                state=1
        elif state==1:
            if content[index]=='=':
                word+=content[index]
                state=2
            else:
                state=3
        if state==3:
            index-=1
        index+=1
    tokens.append(token(word,tokendic[word],num_line,0))
    return index
#+ - & | += &= |= -= ++ -- && || ->
def regbe(content,index):
    state = 0
    word = ""
    while state not in [2,3,4]:
        if state==0:
            if content[index] in ['+','&','|','-']:
                word+=content[index]
                state=1
        elif state==1:
            if content[index]=='=':
                word+=content[index]
                state=2
            elif content[index]==word[0] or (content[index]=='>' and word[0]=='-'):
                word+=content[index]
                state=3
            else:
                state=4
        if state==4:
            index-=1
        index+=1
    tokens.append(token(word,tokendic[word],num_line,0))
    return index

# #include #define
def regde(content,index):
    if index+7<len(content) and content[index+1:index+8]=="include":
        tokens.append(token("#include",312,num_line,0))
        index+=8
    elif index+6<len(content) and content[index:index+7]=="define":
        tokens.append(token("#define",311,num_line,0))
        index+=7
    else:
        wrong.append("line:"+str(num_line)+" #  未识别")
        index+=1
    return index
#default
def regce(content,index):
    if content[index] in tokendic.keys():
        tokens.append(token(content[index],tokendic[content[index]],num_line,0))
    else:
        wrong.append("line:"+str(num_line)+" "+content[index]+"  未识别")
    index+=1
    return index

def gettoken(content):
    with open("./token.txt") as f:
        data = f.readlines()
    for i in data:
        temp = i.split('\t')
        tokendic[temp[0]] = temp[1][:-1]
    i = 0
    global num_line
    num_line = 1
    global wrong,tokens
    wrong = []
    tokens = []
    while (i < len(content)):
        while i<len(content) and (content[i] == ' ' or content[i] == '\n' or content[i] == '\t'):
            if content[i] == '\n':
                num_line += 1
            i += 1
        if i>=len(content):
                break
        if content[i].isalpha() or content[i] == '_':
            i = regid(content, i)
        elif content[i].isdigit():
            i = regnum(content, i)
        elif content[i] == '/':
            i = regnode(content, i)
        elif content[i] == '\'':
            i = regchar(content, i)
        elif content[i] == "\"":
            i = regstr(content, i)
        elif content[i] == '>' or content[i] == '<':
            i = regbs(content, i)
        elif content[i] in ['*', '!', '^', '%', '=']:
            i = regae(content, i)
        elif content[i] in ['+', '&', '|', '-']:
            i = regbe(content, i)
        elif content[i] == '#':
            i = regde(content, i)
        else:
            i = regce(content, i)
    for i in tokens:
        print(i.word + " " + str(i.code))

    with open('./tokenList.txt','w',encoding='utf-8') as f:
        f.write('')
        f.close()
    with open('./tokenList.txt','a',encoding='utf-8') as f:
        for i in tokens:
            f.write(i.word+' '+str(i.code)+' '+str(i.row)+'\n')
        f.write('# 100 '+str(tokens[-1].row))
        #错误
    for i in wrong:
        print(i)
    print(num_line)
    return tokens,wrong
if __name__ == '__main__':
    filepath = "./hello.c"
    content = read_file(filepath)
    gettoken(content)
