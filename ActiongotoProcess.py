#from main import  firstSet
#from main import  grammar
#from main import keywordsList
import copy

firstSet={}#从main中复制过来的，会进行更改
grammar ={}#main中grammar的复本

Start_symbol=""#初始符号
All_symbol=set()#所有符号的集合
Terminal_symbol=set()#终结符
nonTerminal_symbol=set()#非终结符

grammar_point=[]#包含point的项目，key为‘l’对应左端，‘r’对应右端，‘point’对应点的位置,'finish':点的位置是否在最后
accept_grammar_point=[]#含终结符的项目，在grammer_point的基础上增加了‘forward’，展望符号
First_start={}#对应accept_grammer_point中point=0的项目编号
CLOSURE=[]#每个项目的闭包
CLOSURESET=[]#LR（1）项目族群
ACTION_GOTO=[]#ACTION_GOTO表，ACTION_GO[状态i][符号j]，0为acc，x为移进，-x为用产生式x规约（这个产生式下标为accept_grammar_point的下标号
empty_first=[]#first集中含有空的非终结符

#求项目x的CLOSURE,y是最初的项目来源
def GET_CLOSURE(x,y):
    global CLOSURE,accept_grammar_point,firstSet,First_start
    item = accept_grammar_point[x]#以其为中心扩展得到
    if(item["point"]<len(item["r"])):#不超过范围
        # 对于[A->α·Bβ，a]，有B->·￥，将FIRST（βa)中的每个每个终结符b，如果[B->·￥,b]不在closure（I）中，把他加进去
        #curr就是b，a是自带的本来的符号，最开始的b为空，后面正常的话为￥，然后再加上a，它们的共同FIRST为要求的
        curr=item["r"][item["point"]]#点之后的数字
        b=""
        a=item["forward"]#展望符
        curr_fir=set()#经过扩展之后的展望符号，set是为了避免重复
        if(item["point"]+1<len(item["r"])):#在合理范围内
            b=item["r"][(item["point"]+1):]#点之后两个的字母
            b += [a]#求FIRST（b）
            for sym in b:
                curr_fir |= firstSet[sym]
                if sym not in empty_first:
                    break
        else:
            curr_fir=set(a)#￥为空，所以直接set（a）即可
        if curr in First_start:#点之后的元素若为非终结符，我们需要将它的point=0的式子加进去
            for j in First_start[curr]:
                if j not in CLOSURE[y] and accept_grammar_point[j]["forward"] in curr_fir:
                    #未被加进去且它的展望符号是可以被生成的
                    CLOSURE[x].add(j)
                    CLOSURE[y].add(j)
                    CLOSURE[x] |= GET_CLOSURE(j,y)
    else:
        CLOSURE[x].add(x)
        return {x}

    return CLOSURE[x]

def PER_CLOSURE():#计算每个项目的闭包
    global CLOSURE,CLOSURESET,accept_grammar_point,Start_symbol
    #print(Start_symbol)
    for i,item in zip(range(len(accept_grammar_point)),accept_grammar_point):
        #print(item)
        CLOSURE[i].add(i)#从自己本身出发去扩展
        CLOSURE[i]=GET_CLOSURE(i,i)
        if item["forward"]=='#' and item["point"]==0 and item["l"]==Start_symbol:#0号项目集
            CLOSURESET.append(CLOSURE[i])
            #print("1")
    #print(CLOSURESET[0])

#计算GOTO表
def GET_GOTO(i):
    global All_symbol,CLOSURE,CLOSURESET,accept_grammar_point
    for j in CLOSURESET[i]:#对项目集i中的每一个元素
        item=accept_grammar_point[j]#元素对应的包含点以及展望符的式子
        if(item["point"]<len(item["r"])):#范围内
            curr=item["r"][item["point"]]#点之后的符号
            if curr in ACTION_GOTO[i]:#遇到它应该做什么
                ACTION_GOTO[i][curr].append(j+len(Terminal_symbol))
                #为什么要加上len(terminal_symbol)，这是因为我们的包含展望符号的式子中，我们是每一个式子都会包含所有的终结符，所以它的下一步的CLOSURE闭包和他相差这么多
            else:
                ACTION_GOTO[i][curr]=[j+len(Terminal_symbol)]
    for j in All_symbol:#ACTION_GOTO表的横坐标是所有变量
        if j in ACTION_GOTO[i]:#状态i碰到符号j
            new=set()
            for k in ACTION_GOTO[i][j]:#再上一步我们得到的是这个状态在输入j后可以得到的所有CLOUSURE闭包的集合，但肯定存在很多重复，set()就是为了避免重复
                new |= CLOSURE[k]
            if new in CLOSURESET:#已经存在直接找下标即可，从项目组Ij->I index(new)
                ACTION_GOTO[i][j]=CLOSURESET.index(new)
            else:#不存在需要重新构建项目族群
                CLOSURESET.append(new)
                ACTION_GOTO.append({})
                ACTION_GOTO[i][j]=len(CLOSURESET)-1

def GET_ACTION_GOTO(_first,_grammar,keywordList):
    global  Start_symbol,nonTerminal_symbol,Terminal_symbol,All_symbol,firstSet,grammar_point,CLOSURE,CLOSURESET,First_start,accept_grammar_point,ACTION_GOTO,empty_first
    firstSet=_first
    grammar=_grammar
    lista=list(grammar.keys())#下面是获取一些必要信息的步骤
    #print(lista)
    Start_symbol=lista[0]
    #print(Start_symbol)
    for i in lista:
        nonTerminal_symbol.add(i)
    #print(nonTerminal_symbol)
    for i in keywordList:
        Terminal_symbol.add(i)
    Terminal_symbol.add('#')#还有#
    #print(Terminal_symbol)
    All_symbol=Terminal_symbol | nonTerminal_symbol
    #print(All_symbol)
    for i in lista:
        x='ε' in lista
        if x:
            empty_first.append(i)

    for item in Terminal_symbol:#在first集合中增加非终结符
        firstSet[item]={item}
    #print(firstSet)

    #生成带点的所有情况
    for nonter in nonTerminal_symbol:#所有加上“点”的结果
        for i in range(len(grammar[nonter])):
            for j in range(len(grammar[nonter][i])+1):
                grammar_point.append({"l":nonter,"r":grammar[nonter][i],"point":j,"finish":(j==len(grammar[nonter][i]))})
    #print("grammar_point",grammar_point)
    #生成带展望符的所有情况
    for item in grammar_point:
        for ter_sym in Terminal_symbol:
            CLOSURE.append(set())#先初始化
            #accept_grammar_point.append(copy.deepcopy(item))
            accept_grammar_point.append({"l":item["l"],"r":item["r"],"point":item["point"],"finish":item["finish"],"forward":ter_sym})

    #将所有展望符项目输出，方便debug
    acceptFile=open("accept.txt",'w')
    for i,item in zip(range(len(accept_grammar_point)),accept_grammar_point):
        print(i,"   ",item,file=acceptFile)
    #print("accept_grammar_point",accept_grammar_point)

    #生成point=0的所有项目的集合
    for i,item in zip(range(len(accept_grammar_point)),accept_grammar_point):
        if item["point"]==0:
            if item["l"] in First_start:
                First_start[item["l"]].add(i)
            else:
                First_start[item["l"]]={i}
    #print("First_start",First_start)

    PER_CLOSURE()
    ACTION_GOTO.append({})
    num=0
    while(num<len(CLOSURESET)):
        GET_GOTO(num)
        num=num+1
    #输出构建的项目族群
    CLOSURESETFile=open("CLOSURESET.txt",'w')
    for i in range(len(CLOSURESET)):
        print(i,file=CLOSURESETFile)
        for k in CLOSURESET[i]:
            print(accept_grammar_point[k],file=CLOSURESETFile)


    lrFile=open("ACTION_GOTO.txt",'w')
    ts=sorted(list(Terminal_symbol-{Start_symbol}))
    nts=sorted(list(nonTerminal_symbol-{Start_symbol}))
    print("   ", '  '.join(map(lambda x: (x + "  ")[:8], ts)), "", '  '.join(map(lambda x: (x + "  ")[:8], nts)),file=lrFile)
    for i in range(len(CLOSURESET)):
        print("%-8d" % i, end=" ",file=lrFile)
        for k in CLOSURESET[i]:
            item=accept_grammar_point[k]
            if item["point"]==len(item["r"]):
                if item["forward"] in ACTION_GOTO[i]:
                    print("Warning!!!","%d号项目集族的\t %s \t符号与产生式"%(i,item["forward"]),accept_grammar_point[k],"冲突！")
                    exit(-1)
                else:
                    #item=['-',accept_grammar_point[k]["l"],accept_grammar_point[k]["r"]]
                    if(item["l"]==Start_symbol):#第一条产生式且已经到头了，acc
                        ACTION_GOTO[i][item["forward"]]=0
                    else:
                        ACTION_GOTO[i][item["forward"]]=-k
        #下面是ACTION_GOTO表的输出
        for j in ts:
            try:
                if ACTION_GOTO[i][j]>0:
                    print("s%-8d" % ACTION_GOTO[i][j], end=" ", file=lrFile)
                if ACTION_GOTO[i][j]<0:
                    print("r%-8d" % -ACTION_GOTO[i][j], end=" ", file=lrFile)
                if ACTION_GOTO[i][j]==0:
                    print("acc " , end=" ", file=lrFile)
            except:
                print("    ", end=" ", file=lrFile)
        for j in nts:
            try:
                print("%-9d" % ACTION_GOTO[i][j], end=" ", file=lrFile)
            except:
                print("    ", end=" ", file=lrFile)
        print(file=lrFile)

    lrFile.close()
    CLOSURESETFile.close()
    acceptFile.close()

    return ACTION_GOTO,accept_grammar_point

#GET_ACTION_GOTO()
