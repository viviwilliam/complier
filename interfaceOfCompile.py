import sys
import string
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import SFYX
import CFFX
import YFFX
import target
import LL1
from SFYX import VT


data =""
z =""
letters = string.ascii_letters + "_"
    # 空白字符
blank = " \n\r\t"
    # 保留字数组
reserved_words = ["char", "int", "if", "else", "var", "return", "break", "do", 
                    "while", "for", "double", "float", "short", "scanf", "case", "void"]
    # 符号表
signs = {"=": 27, "<=": 28, "<>": 29, "<": 30, ">=": 31, ">": 32, "+": 33, "-": 34, 
            "*": 35, "==": 53, "/": 36, "//": 37, ":": 38, ";": 39, "(": 40, ")": 41,
            "{": 42, "}": 43, "[": 44, "]": 45, "\"": 46, ",": 47, "'": 48, "!=": 49,
            "&": 50, "&&": 51, "||": 52, "==": 53, "|": 54, "%": 55, "?": 56}


keyward = set('')




class Example(QMainWindow):
    da = ""
    def __init__(self):
        super().__init__()

        self.initUI() #界面绘制交给InitUi方法
    
    def initUI(self):
        #设置窗口的标题
        self.setWindowTitle('Compiler')
        #设置窗口的图标,引用当前目录下的web.png图片
        self.setWindowIcon(QIcon('G:/Code/python/Complier/source/图片1.png'))
        #设置窗口和位置大小
        self.setFixedSize(800,800)
        self.add_menu()
        # self.add_layout()


    def add_menu(self):
        #------------------------布局---------------------
        #左侧

       
        #-------------------------工具栏------------------------------------
        #后退
       
        BackToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/撤回.png'),'&Back',self)
        #BackToolAction.setShortcut('ctrl+Q')
        BackToolAction.setStatusTip('back application')
        #BackToolAction.triggered.connect(qApp.quit)
        #前进
        ForwardToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/前进.png'),'&Forward',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        ForwardToolAction.setStatusTip('Forward application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #打印
        PrintToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/print.png'),'&Print',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        PrintToolAction.setStatusTip('Print application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #文件
        FoldToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/folder.png'),'&Fold',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        FoldToolAction.setStatusTip('Fold application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #保存
        SaveToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/edit-tools.png'),'&Save',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        SaveToolAction.setStatusTip('Save application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #搜索
        SearchToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/search.png'),'&Search',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        SearchToolAction.setStatusTip('Search application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #设置
        SetToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/setup.png'),'&Set',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        SetToolAction.setStatusTip('set application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #debug
        DebugToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/test.png'),'&Debug',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        DebugToolAction.setStatusTip('Debug application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #取消
        CancelToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/叉.png'),'&Cancel',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        CancelToolAction.setStatusTip('Cancel application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #数据
        DataToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/数据.png'),'&Data',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        DataToolAction.setStatusTip('Data application')
        #ForwardToolAction.triggered.connect(qApp.quit)
        #编译运行
        RunToolAction = QAction(QIcon('G:/Code/python/Complier/source/toor/对号.png'),'&Run',self)
        #ForwardToolAction.setShortcut('ctrl+Q')
        RunToolAction.setStatusTip('Run application')
        #ForwardToolAction.triggered.connect(qApp.quit)








        #--------------------------菜单栏----------------------------------
        #语法分析按钮
        DebugToolAction.triggered.connect(self.yufa)

        #打开文件选项
        openFileAction = QAction(QIcon('G:/Code/python/Complier/source/atm.png'),'&打开文件',self)
        openFileAction.setShortcut('ctrl+o')
        openFileAction.setStatusTip('打开文件')
        openFileAction.triggered.connect(self.funOpenFile)

        
        #退出选项
        exitAction = QAction(QIcon('G:/Code/python/Complier/source/退出 (2).png'),'&退出',self)
        exitAction.setShortcut('ctrl+Q')
        exitAction.setStatusTip('退出')
        exitAction.triggered.connect(qApp.quit)

        #------------------------词法分析栏---------------------------------
        NFAction = QAction('正规式转NFA',self)
        NFAction.setStatusTip('正规式转NFA')
        #NFAction
        
        #-----------------------语法分析栏-------------------------------
        LLAction = QAction('LL(1)',self)
        LLAction.setStatusTip('LL(1)')
        LLAction.triggered.connect(self.LLDage)

        SFAction = QAction('算符优先',self)
        SFAction.setStatusTip("算符优先分析法")
        SFAction.triggered.connect(self.SFDage)

        LRAction = QAction('LR',self)
        LRAction.setStatusTip("LR")


        self.statusBar()

        # self.setGeometry(100,100,800,900)
        #创建状态栏的小窗口,显示信息
        self.statusBar().showMessage('Ready')
        
        #创建一个菜单栏
        menubar = self.menuBar()
        #添加菜单,只添加菜单，未添加行为事件
        fileMenu = menubar.addMenu('&文件[F]')
        editMenu = menubar.addMenu('&退出[E]')
        lexMenu = menubar.addMenu('&词法分析[L]')
        synMenu = menubar.addMenu('&语法分析[S]')
        intMenu = menubar.addMenu('&中间代码生成[I]')
        objMenu = menubar.addMenu('&对象代码生成[O]')
        viewMenu = menubar.addMenu('&查看[V]')
        helpMenu = menubar.addMenu('&帮助[H]')
        #添加事件
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(exitAction)

        #语法分析按钮
        YFAction = QAction(QIcon('G:/Code/python/Complier/source/atm.png'),'&语法分析',self)
        YFAction.setShortcut('ctrl+o')
        YFAction.setStatusTip('语法分析')
        YFAction.triggered.connect(self.yufa)
        synMenu.addAction(YFAction)

        #语义分析按钮
        MiddleAction = QAction(QIcon('G:/Code/python/Complier/source/atm.png'),'&中间代码生成',self)
        MiddleAction.setShortcut('ctrl+o')
        MiddleAction.setStatusTip('中间代码生成')
        MiddleAction.triggered.connect(self.middle)
        intMenu.addAction(MiddleAction)

        #汇编代码
        objAction = QAction(QIcon('G:/Code/python/Complier/source/atm.png'),'&对象代码生成',self)
        objAction.setShortcut('ctrl+o')
        objAction.setStatusTip('对象代码生成')
        objAction.triggered.connect(self.obj)
        objMenu.addAction(objAction)
        

        #语法分析下面添加LL，算符优先和LR
        synMenu.addAction(LLAction)
        synMenu.addAction(SFAction)
        synMenu.addAction(LRAction)
        #词法分析下面添加从表达式到NFA

        lexMenu.addAction(NFAction)
#--------------------------状态栏------------------------------------
        # 状态栏1，有关文件
        toolbar1 = self.addToolBar('tool1')
        toolbar1.addAction(FoldToolAction)
        toolbar1.addAction(SaveToolAction)
        toolbar1.addAction(PrintToolAction)

        #状态栏2，前进后退
        toolbar2 = self.addToolBar('tool2')
        toolbar2.addAction(BackToolAction)
        toolbar2.addAction(ForwardToolAction)
        
        #状态栏3 编译运行
        toolbar3 = self.addToolBar('tool3')
        toolbar3.addAction(RunToolAction)
        toolbar3.addAction(DebugToolAction)
        toolbar3.addAction(CancelToolAction) 
        
        #状态栏4 数据
        toolbar4 = self.addToolBar('tool4')
        toolbar4.addAction(DataToolAction)
        toolbar4.addAction(SetToolAction)
        toolbar4.addAction(SearchToolAction)

        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        self.text3 = QTextEdit()

        #QMainWindow的中心窗口部件
        mainwidget = QWidget()
        #创建布局
        layout = QHBoxLayout()
        layout.addWidget(self.text1)
        self.text1.setMaximumWidth(600)
        vbox = QVBoxLayout()
        vbox.addWidget(self.text2)
        vbox.addWidget(self.text3)
        layout.addLayout(vbox)
        

        mainwidget.setLayout(layout)
        self.setCentralWidget(mainwidget)




    '''
    #右侧显示分词结果
    #预处理，将文件中的空格，换行等无关字符处理掉
    def output(self,_str):
        
        try: # 尝试是否能通过数字形式输出，如果能即为常数，否则为字符
            z = f"{int(_str)}\t26"+"\n"
        except ValueError:
            if _str in reserved_words: # 判断是否为保留字
                z =  f"{_str}\t{reserved_words.index(_str) + 1}\t保留字"+"\n"
                word = ""
            elif _str in signs: # 判断是否为符号
                z = f"{_str}\t{signs[_str]}"+"\n"
            else: # 否则为标识符
                z = f"{_str}\t25\t标识符"+"\n"
                word = ""
        self.da += z
    '''
    '''
    def LexicalAnalysis(self):
        if self.fname[0]:
            f = open(self.fname[0],'r')
            sign = 0
            with f:
                code = f.read()
        for line in code.split("\n"): # 按行迭代
            word = "" # 类似缓冲区的作用
            flag = False # 标记是否为123这类常数
            _pass = False # 标记是否跳过这一个字符
            for index, letter in enumerate(line):
                if _pass: # 判断是否跳过当前字符
                    _pass = False
                    continue
                if letter in string.digits: # 判断当前是否为数字
                    flag = not bool(word) # 如果word里没有字符，而当前又读到了数字，那么就打上标记
                    word += letter # 将字符加入缓冲区
                    continue
                elif letter in letters: # 判断当前是否为字母
                    if flag: # 如果打过了标记， 而此时读到了字母，标识符是不能以数字开头的，所以分开
                        self.output(word) # 输出数字
                        word = "" # 清空缓冲区
                        flag = False # 取消标记
                    word += letter # 将当前的字母加入缓冲区
                    continue
                else: # 此时当前字符既不是数字也不是字母，为符号或空白字符
                    if word: # 判断缓冲区内是否有字符，有则输出
                        self.output(word)
                        word = ""
                    if letter in blank: # 如果当前为空白字符（空格、回车）则跳过
                        continue
                    if line[index:index + 2] == "//": # 处理掉注释
                        break # 直接break，跳出行迭代
                    # 判断当前字符是否为最后一个以及和下一个字符能否组成一组符号
                    if index != len(line) - 1 and line[index:index + 2] in signs: 
                        self.output(line[index:index + 2]) # 输出组合的字符
                        _pass = True # 跳过下一个字符
                    else: # 输出单个字符
                        self.output(letter)
                    word = "" # 清空缓冲区
        
        
        self.text2.setText(self.da)
    '''
    windowList = []

    def LLDage(self):
        win = LL()
        self.windowList.append(win)
        self.close
        win.show()

    
    def SFDage(self):
        win = SF()
        self.windowList.append(win)
        self.close
        win.show()
    #左侧代码显示

    #对象代码生成
    def obj(self):
        target.read_quater()
        target.translate()
        target.modify_jmp()
        da4 =""
        for i in target.assemble:
            for j in i:
                da4 += j +'\n'

        self.text2.setText(da4)


    #中间代码生成
    def middle(self):
        da3 =""
        for i in range(len(YFFX.quaternion)):   #四元式
            da3 +=str(i)+'   '+str(YFFX.quaternion[i])+'\n'
        #print(da3)
        self.text3.setText(da3)

    #语法分析显示
    def yufa(self):
        YFFX.get_token()
        YFFX.parser()
        YFFX.write_quater()
        da2 = ""
        for i in YFFX.wrong:
            da2 += "语法错误"+' '+i+'\n'
        for i in YFFX.semAnalyse:
            da2 += "语义错误"+' '+i+'\n'
        
        da2 +="分析完成！"
        
        self.text3.setText(da2)



    def funOpenFile(self):
        self.fname = QFileDialog.getOpenFileName(self,'打开文件','*.c')
        if self.fname[0]:
            print("1111")
            content = CFFX.read_file(self.fname[0])
            CFFX.gettoken(content)
            f = open(self.fname[0], 'r',encoding='utf-8')
            with f:
                data = f.read()    
                self.text1.setText(data)
        da =""
        for i in CFFX.tokens:
            da += i.word + " " + str(i.code)+'\n'

        self.text2.setText(da)

        da1 = ""
        for i in CFFX.wrong:
            da1 += i+'\n'
        self.text3.setText(da1)
        #self.LexicalAnalysis()
        
    #def 

model3 = QStandardItemModel(20,3)
model5 = QStandardItemModel(20,3)

class LL(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('LL(1)')
        self.setFixedSize(1000,700)
        LL1.get_lan()
        LL1.get_first()
        LL1.get_follow()
        LL1.generate_table()
       
        self.box()
    
    
    def box(self):
        #设置主布局
        mainwidget = QWidget()

        #创建下面显示的水平布局
        textlayout = QVBoxLayout()

        
        mainwidget.setLayout(textlayout)

         #创建布局，水平布局下的顶部布局
        #layout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        #button
        self.readin = QPushButton('读入文法')
        self.confirm = QPushButton('确认文法')
        self.save = QPushButton('保存文法')
        


        textlayout.addLayout(buttonlayout)
        #layout.addLayout(buttonlayout)
        buttonlayout.addWidget(self.readin)
        buttonlayout.addWidget(self.confirm)
        buttonlayout.addWidget(self.save)

        #水平布局下的底部水平布局
        bottomlayout = QHBoxLayout()
        textlayout.addLayout(bottomlayout)
        #底部水平布局又分两个竖直布局
        leftlayout = QVBoxLayout()
        rightlayout = QVBoxLayout()
        bottomlayout.addLayout(leftlayout)
        bottomlayout.addLayout(rightlayout)

        
       

        #firstVT
        #SFYX.get_firstvt()
        #SFYX.get_lastvt()
        #SFYX.generate_table()
        #SFYX.analyse()
        #SFYX.
        #SFYX.startSFYX()
        self.lengthg = len(LL1.VT)
        self.lengthY = len(LL1.FIRST)
        self.lengthRight =len(LL1.FOLLOW)

        print(self.lengthg)
        print(self.lengthY)
        print(self.lengthRight)

        #左侧文本域
        #first表格
        self.model = QStandardItemModel(self.lengthY+1,self.lengthg+1)
        #self.model.setHorizontalHeaderLabels(['FirstVT','#','+','*',
        #                                    '-','(',')','i'])
        #self.model.setVerticalHeaderLabels(['S','E','T','F','F'])
        #循环设置follow显示的文字
        #横向
        m = 0
        item=QStandardItem('FIRST')
        self.model.setItem(0,0,item)
        for i in LL1.VT:
            m = m+1
            item=QStandardItem(str(i))
            self.model.setItem(0,m,item)

        m = 0
        for i in LL1.FIRST:
            m = m+1
            item=QStandardItem(str(i))
            self.model.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 1
        
        for i in LL1.FIRST:
            for j in LL1.FIRST[i]:
                print(j)
                n = 1
                for a in LL1.VT:
            #    print(a)
                    if a == j:
                        print(1)
                        item=QStandardItem("1")
                        self.model.setItem(m,n,item)
                    n = n+1
            m = m+1
        
        #-------------------Last表格----------------------------
        self.model1 = QStandardItemModel(self.lengthRight+1,self.lengthg+1)
        m = 0
        item=QStandardItem('LAST')
        self.model1.setItem(0,0,item)
        for i in LL1.VT:
            m = m+1
            item=QStandardItem(str(i))
            self.model1.setItem(0,m,item)

        m = 0
        for i in LL1.FOLLOW:
            m = m+1
            item=QStandardItem(str(i))
            self.model1.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 1
        
        for i in LL1.FOLLOW:
            for j in LL1.FOLLOW[i]:
                print(j)
                n = 1
                for a in LL1.VT:
            #    print(a)
                    if a == j:
                        print(1)
                        item=QStandardItem("1")
                        self.model1.setItem(m,n,item)
                    n = n+1
            m = m+1

        leng = len(LL1.Table)

        #优先表
        self.model2 = QStandardItemModel(leng+1,leng+1)
        m = 0
        item=QStandardItem('预测分析表')
        self.model2.setItem(0,0,item)
        for i in LL1.VT:
            m = m+1
            item=QStandardItem(str(i))
            self.model2.setItem(0,m,item)

        m = 0
        for i in LL1.Table:
            m = m+1
            item=QStandardItem(str(i))
            self.model2.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 0
        
        for i in LL1.Table:
           m = m+1
           for j in LL1.Table[i]:
                u = 1
                for h in LL1.VT:
                    if h == j:
                        item=QStandardItem(LL1.Table[i][h])
                        self.model2.setItem(m,u,item)
                    u = u+1

            



        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #-------------------写数据--------------------



        #last表格

        self.tableView1 = QTableView()
        self.tableView1.setModel(self.model1)
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        

        self.tableView2 = QTableView()
        self.tableView2.setModel(self.model2)
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setMinimumSize(400,250)
        self.langtext = QTextEdit()
        
        #获取文法
        #SFYX.get_lan()
        m = str(LL1.LAN)
        self.langtext.setText(m)


        self.langtext2 = QTextEdit()
        self.langtext3 = QTextEdit()
        leftlayout.addWidget(self.langtext)
        leftlayout.addWidget(self.tableView)
        leftlayout.addWidget(self.tableView1)
        #textlayout.addWidget(self.langtext)
        

        #优先表
        
        #self.model3.setVerticalHeaderLabels(['#','+','*','-','(',')','i'])
        #self.model3 = QStandardItemModel(20,3)
        model5.setHorizontalHeaderLabels(['符号栈','输入串',
                                            '所用产生式'])

        self.tableView3 = QTableView()
        self.tableView3.setModel(model5)
        self.tableView3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
        
        
        self.setCentralWidget(mainwidget)
        

        #右侧文本域
        self.langtext5 = QLineEdit()
        self.readstart = QPushButton('分析字符串')
        self.stringlayout = QHBoxLayout()
        self.stringlayout.addWidget(self.langtext5)
        self.stringlayout.addWidget(self.readstart)
        self.langtext5.setMaximumSize(300,50)
        rightlayout.addWidget(self.tableView2)
        rightlayout.addLayout(self.stringlayout)
        rightlayout.addWidget(self.tableView3)

        

        #button行为-----------------------------------
        self.readstart.clicked.connect(self.getText)
        

        
       
        #mainwidget.setGeometry(10,10,100,100)
    def getText(self):
        print(self.langtext5.text())
        LL1.analyze(self.langtext5.text())
        print(LL1.ProcessList)
        print(LL1.ProcessList[0][0])
        m = 0
        if LL1.errorflag == 1:
            item=QStandardItem("分析错误")
            model5.setItem(0,0,item)
        else:
            for i in LL1.ProcessList:
                item=QStandardItem(LL1.ProcessList[i][0])
                model5.setItem(m,0,item)
                item=QStandardItem(LL1.ProcessList[i][1])
                model5.setItem(m,1,item)
                item=QStandardItem(LL1.ProcessList[i][2])
                model5.setItem(m,2,item)
                m = m+1



class SF(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('算符优先分析法')
        self.setFixedSize(1000,700)
        SFYX.get_lan()
        SFYX.get_firstvt()
        SFYX.get_lastvt()
        SFYX.generate_table()
       
        self.box()
    
    
    def box(self):
        #设置主布局
        mainwidget = QWidget()

        #创建下面显示的水平布局
        textlayout = QVBoxLayout()

        
        mainwidget.setLayout(textlayout)

         #创建布局，水平布局下的顶部布局
        #layout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        #button
        self.readin = QPushButton('读入文法')
        self.confirm = QPushButton('确认文法')
        self.save = QPushButton('保存文法')
        


        textlayout.addLayout(buttonlayout)
        #layout.addLayout(buttonlayout)
        buttonlayout.addWidget(self.readin)
        buttonlayout.addWidget(self.confirm)
        buttonlayout.addWidget(self.save)

        #水平布局下的底部水平布局
        bottomlayout = QHBoxLayout()
        textlayout.addLayout(bottomlayout)
        #底部水平布局又分两个竖直布局
        leftlayout = QVBoxLayout()
        rightlayout = QVBoxLayout()
        bottomlayout.addLayout(leftlayout)
        bottomlayout.addLayout(rightlayout)

        
       

        #firstVT
        #SFYX.get_firstvt()
        #SFYX.get_lastvt()
        #SFYX.generate_table()
        #SFYX.analyse()
        #SFYX.
        #SFYX.startSFYX()
        self.lengthg = len(SFYX.VT)
        self.lengthY = len(SFYX.FIRSTVT)
        self.lengthRight =len(SFYX.LASTVT)

        print(self.lengthg)
        print(self.lengthY)
        print(self.lengthRight)

        #左侧文本域
        #first表格
        self.model = QStandardItemModel(self.lengthY+1,self.lengthg+1)
        #self.model.setHorizontalHeaderLabels(['FirstVT','#','+','*',
        #                                    '-','(',')','i'])
        #self.model.setVerticalHeaderLabels(['S','E','T','F','F'])
        #循环设置follow显示的文字
        #横向
        m = 0
        item=QStandardItem('FIRSTVT')
        self.model.setItem(0,0,item)
        for i in SFYX.VT:
            m = m+1
            item=QStandardItem(str(i))
            self.model.setItem(0,m,item)

        m = 0
        for i in SFYX.FIRSTVT:
            m = m+1
            item=QStandardItem(str(i))
            self.model.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 1
        
        for i in SFYX.FIRSTVT:
            for j in SFYX.FIRSTVT[i]:
                print(j)
                n = 1
                for a in SFYX.VT:
            #    print(a)
                    if a == j:
                        print(1)
                        item=QStandardItem("1")
                        self.model.setItem(m,n,item)
                    n = n+1
            m = m+1
        
        #-------------------Last表格----------------------------
        self.model1 = QStandardItemModel(self.lengthRight+1,self.lengthg+1)
        m = 0
        item=QStandardItem('LASTVT')
        self.model1.setItem(0,0,item)
        for i in SFYX.VT:
            m = m+1
            item=QStandardItem(str(i))
            self.model1.setItem(0,m,item)

        m = 0
        for i in SFYX.LASTVT:
            m = m+1
            item=QStandardItem(str(i))
            self.model1.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 1
        
        for i in SFYX.LASTVT:
            for j in SFYX.LASTVT[i]:
                print(j)
                n = 1
                for a in SFYX.VT:
            #    print(a)
                    if a == j:
                        print(1)
                        item=QStandardItem("1")
                        self.model1.setItem(m,n,item)
                    n = n+1
            m = m+1

        leng = len(SFYX.Table)

        #优先表
        self.model2 = QStandardItemModel(leng+1,leng+1)
        m = 0
        item=QStandardItem('优先表')
        self.model2.setItem(0,0,item)
        for i in SFYX.Table:
            m = m+1
            item=QStandardItem(str(i))
            self.model2.setItem(0,m,item)

        m = 0
        for i in SFYX.Table:
            m = m+1
            item=QStandardItem(str(i))
            self.model2.setItem(m,0,item)

        #-----------------------放整体数据------------------
        m = 0
        
        for i in SFYX.Table:
           m = m+1
           for j in SFYX.Table[i]:
                u = 1
                for h in SFYX.Table:
                    if h == j:
                        item=QStandardItem(SFYX.Table[i][h])
                        self.model2.setItem(m,u,item)
                    u = u+1

            



        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #-------------------写数据--------------------



        #last表格

        self.tableView1 = QTableView()
        self.tableView1.setModel(self.model1)
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        

        self.tableView2 = QTableView()
        self.tableView2.setModel(self.model2)
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setMinimumSize(400,250)
        self.langtext = QTextEdit()
        
        #获取文法
        #SFYX.get_lan()
        m = str(SFYX.LAN)
        self.langtext.setText(m)


        self.langtext2 = QTextEdit()
        self.langtext3 = QTextEdit()
        leftlayout.addWidget(self.langtext)
        leftlayout.addWidget(self.tableView)
        leftlayout.addWidget(self.tableView1)
        #textlayout.addWidget(self.langtext)
        

        #优先表
        
        #self.model3.setVerticalHeaderLabels(['#','+','*','-','(',')','i'])
        #self.model3 = QStandardItemModel(20,3)
        model3.setHorizontalHeaderLabels(['符号栈','输入串',
                                            '所用产生式'])

        self.tableView3 = QTableView()
        self.tableView3.setModel(model3)
        self.tableView3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
        
        
        self.setCentralWidget(mainwidget)
        

        #右侧文本域
        self.langtext5 = QLineEdit()
        self.readstart = QPushButton('分析字符串')
        self.stringlayout = QHBoxLayout()
        self.stringlayout.addWidget(self.langtext5)
        self.stringlayout.addWidget(self.readstart)
        self.langtext5.setMaximumSize(300,50)
        rightlayout.addWidget(self.tableView2)
        rightlayout.addLayout(self.stringlayout)
        rightlayout.addWidget(self.tableView3)

        

        #button行为-----------------------------------
        self.readstart.clicked.connect(self.getText)
        

        
       
        #mainwidget.setGeometry(10,10,100,100)
    def getText(self):
        print(self.langtext5.text())
        SFYX.analyse(self.langtext5.text())
        print(SFYX.ProcessList)
        print(SFYX.ProcessList[0][0])
        m = 0
        if SFYX.errorfalg == 1:
            item=QStandardItem("分析错误")
            model3.setItem(0,0,item)
        else:
            for i in SFYX.ProcessList:
                item=QStandardItem(SFYX.ProcessList[i][0])
                model3.setItem(m,0,item)
                item=QStandardItem(SFYX.ProcessList[i][1])
                model3.setItem(m,1,item)
                item=QStandardItem(SFYX.ProcessList[i][2])
                model3.setItem(m,2,item)
                m = m+1
        



        
        


if __name__ =='__main__':
    #创建应用程序和对象
    app=QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())