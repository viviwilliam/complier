import copy
import wx
import wx.grid
import time
 
 
grammar = []
itemSet = []
DFA = []
Vn = []
Vt = []
 
 
def closure(item):
    global itemSet
    dot = []
    dot.append(item)
    olddot = []
    while len(dot) != len(olddot):
        olddot = copy.deepcopy(dot)
        temp = []
        for i in range(len(dot)):
            for j in range(len(itemSet)):
                if dot[i].index('·')+1 < len(dot[i]) and dot[i][dot[i].index('·')+1] == itemSet[j][0] and itemSet[j][itemSet[j].index('>')+1] == '·':
                    temp.append(itemSet[j])
        for k in range(len(temp)):
            if temp[k] not in dot:
                dot.append(temp[k])
    return dot
 
 
def goto(item, a):
    global itemSet
    for i in range(len(item)):
        if item[i] == '·' and i!= len(item)-1:
            if item[i+1] == a:
                item2 = item[:i]+item[i+1]+'·'+item[i+2:]
                if item2 in itemSet:
                    return item2
    return -1
 
 
def findItem(item):
    global DFA
    for i in range(len(DFA)):
        if item in DFA[i]:
            return i
    return -1
 
 
n = int(input('输入个数'))
for i in range(n):
    temp = input()
    if i == 0:
        grammar.append('S\'->'+temp[0])
    grammar.append(temp)
    for j in range(len(temp)):
        if temp[j].isupper() and temp[j] not in Vn:
            Vn.append(temp[j])
        elif temp[j].islower() and temp[j] not in Vt:
            Vt.append(temp[j])
Vn.sort()
Vt.sort()
 
for i in range(len(grammar)):
    flag = 0
    for j in range(len(grammar[i])):
        if grammar[i][j] == '>':
            flag = 1
        if flag == 1 and grammar[i][j] != '>':
            temp = grammar[i][:j]+'·'+grammar[i][j:]
            itemSet.append(temp)
    itemSet.append(grammar[i]+'·')
 
 
print(grammar)
DFA.append(closure(itemSet[0]))
 
oldDFA = []
 
while len(oldDFA) != len(DFA):
    oldDFA = copy.deepcopy(DFA)
    temp = []
    tDFA = []
    for i in range(len(DFA)):
        for j in range(len(DFA[i])):
            position = DFA[i][j].index('·')
            if position != len(DFA[i][j]) - 1:
                # print('@',goto(DFA[i][j], DFA[i][j][position+1]))
                tDFA.append(closure(goto(DFA[i][j], DFA[i][j][position+1])))
    for k in range(len(tDFA)):
        if tDFA[k] not in DFA:
            DFA.append(tDFA[k])
 
 
print(DFA)
 
for i in range(len(DFA)):
    for j in range(len(DFA[i])):
        if len(DFA[i][j][-1]) == '·' and len(DFA[i]) != 1:
            print('非LR(0)文法')
            break
 
print(len(DFA))
DFAtable = []
 
for i in range(len(DFA)):
    table = []
    for j in range(len(DFA[i])):
        position = DFA[i][j].index('·')
        if position == len(DFA[i][j])-1:
            temp = DFA[i][j][:-1]
 
            table = [grammar.index(temp)]*(len(Vt)+1)
            break
        for k in range(len(Vt)):
            if DFA[i][j][position+1] == Vt[k]:
                temp = Vt[k]+'S'+str(findItem(goto(DFA[i][j], Vt[k])))
                table.append(temp)
        for m in range(len(Vn)):
            if DFA[i][j][position+1] == Vn[m]:
                temp = Vn[m]+str(findItem(goto(DFA[i][j], Vn[m])))
                table.append(temp)
    DFAtable.append(table)
 
 
# 判断是否为LR(0)文法
flag = 0
for i in range(len(DFAtable)):
    for j in range(len(DFAtable)):
        if len(DFA[i][j]) > 2:
            print('非LR(0)文法')
            flag = 1
            break
    if flag == 1:
        break
 
print(DFAtable)
 
VtVn = Vt + ['#'] + Vn
LR0TABLE = [[' ' for col in range(len(VtVn))] for row in range(len(DFA)+1)]
 
print('------------------------------------------------')
print('状态\t\t\t\tAction\t\t\t\t GOTO')
 
for i in range(len(VtVn)):
    LR0TABLE[0][i] = VtVn[i]+' '
 
 
for i in range(len(DFAtable)):
    if 0 in DFAtable[i]:
        LR0TABLE[2][VtVn.index('#')] = 'acc'
        continue
    for j in range(len(DFAtable[i])):
        try:
            LR0TABLE[i+1][VtVn.index(DFAtable[i][j][0])] = DFAtable[i][j][1:]
        except:
            for k in range(len(Vt)+1):
                LR0TABLE[i+1][k] = 'r'+str(DFAtable[i][j])
 
print('     ')
for i in range(len(LR0TABLE)):
    print('    ',end=' ')
    for j in range(len(LR0TABLE[i])):
        print(LR0TABLE[i][j], end='     ')
    print('')
 
 
class GridFrame(wx.Frame):
    def __init__(self, parent):
        global LR0TABLE
 
        wx.Frame.__init__(self, parent)
 
        # Create a wxGrid object
        grid = wx.grid.Grid(self, -1)
 
        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        grid.CreateGrid(len(LR0TABLE)+5, len(VtVn)+5)
 
        # We can set the sizes of individual rows and columns
        # in pixels
 
        grid.SetCellValue(0, 0, '状态')
        grid.SetCellValue(0, 1, '-')
        grid.SetCellValue(0, 2, 'ACTION')
        grid.SetCellValue(0, 3, '-')
        grid.SetCellValue(0, 4, '-')
        grid.SetCellValue(0, 5, '-')
        grid.SetCellValue(0, 6, 'GOTO')
        grid.SetCellValue(0, 7, '-')
        grid.SetCellValue(0, 8, '-')
 
        for i in range(len(LR0TABLE)):
            grid.SetCellValue(i+2, 0, str(i))
            for j in range(len(LR0TABLE[i])):
                grid.SetCellValue(i+1, j+1, LR0TABLE[i][j])
 
        self.Show()
 
 
app = wx.App(0)
frame = GridFrame(None)
app.MainLoop()
 
string = input('输入一个句子：')
string += '#'
status = [0]
oper = ['#']
action = []
 
flag = 0
while flag != 1:
    symbol = string[0]
    try:
        if LR0TABLE[status[-1] + 1][VtVn.index(symbol)] != ' ' and LR0TABLE[status[-1] + 1][VtVn.index(symbol)][
            0] != 'r':
            if LR0TABLE[status[-1] + 1][VtVn.index(symbol)] == 'acc':
                flag = 1
                print('接受！')
                break
            status.append(int(LR0TABLE[status[-1] + 1][VtVn.index(symbol)][-1]))
            oper.append(symbol)
            string = string[1:]
            # action.append(LR0TABLE[status[-1] + 1][VtVn.index(symbol)])
            print(status)
            print(oper)
            print('')
 
        elif LR0TABLE[status[-1] + 1][VtVn.index(symbol)][0] == 'r':
            position = int(LR0TABLE[status[-1] + 1][VtVn.index(symbol)][1])
            Vnc = grammar[position][0]
            Grlen = len(grammar[position]) - grammar[position].index('>') - 1
            status = status[:-Grlen]
            oper = oper[:-Grlen]
            oper.append(Vnc)
            addx = int(LR0TABLE[status[-1] + 1][VtVn.index(Vnc)])
            status.append(int(addx))
            print(status)
            print(oper)
            print('')
            # action.append(str(LR0TABLE[status[-1] + 1][VtVn.index(symbol)]))
        else:
            print('错误')
            break
    except ValueError as e:
        print('错误')
 
 
'''
E->aA
E->bB
A->cA
A->d
B->cB
B->d
'''
 
'''
S->rD
D->D,i
D->i
'''


'''
bccd
'''