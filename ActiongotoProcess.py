import copy
import json

START_SYMBOL=""#初始符号
All_symbol=set()#所有符号的集合
Terminal_symbol=set()#终结符
nonTerminal_symbol=set()#非终结符

firstSet={}#从main中复制过来的，会进行更改
empty_first=[]#first集中含有空的非终结符

grammar =[]#产生式项目，key为‘l’对应左端，‘r’对应右端，‘order’对应产生式编号
grammar_point=[]#包含point的项目，key为‘l’对应左端，‘r’对应右端，‘point’对应点的位置,'finish':点的位置是否在最后
accept_grammar_point=[]#含终结符的项目，在grammer_point的基础上增加了‘forward’，展望符号
First_point={}#对应accept_grammer_point中point=0的项目编号
CLOSURE=[]#每个项目的闭包
CLOSURESET=[]#LR（1）项目族群
ACTION_GOTO=[]#ACTION_GOTO表，ACTION_GO[状态i][符号j]，0为acc，x为移进，-x为用产生式x规约（这个产生式下标为accept_grammar_point的下标号


def preprocess(_grammar,keywordList):
#_grammar是拆分后的产生式，keywordList是终结符
    global  grammar,nonTerminal_symbol,Terminal_symbol,All_symbol,START_SYMBOL,firstSet,empty_first
    lista = list(_grammar.keys())  # 下面是获取一些必要信息的步骤
    print("lista",lista)
    num=1#产生式个数
    for i in lista:
        for j in _grammar[i]:
            ######attention!!!!
            right=j
            if(j==['$']):#空的符号
                right=[]
            grammar.append({"l":i,"r":right,"order":num})
            num=num+1
    print("grammar",grammar)
    START_SYMBOL = lista[0]#所有符号
    print("START_SYMBOL",START_SYMBOL)
    for i in lista:#非终结符
        nonTerminal_symbol.add(i)
    print("nonTerminal_symbol",nonTerminal_symbol)
    for i in keywordList:#终结符
        Terminal_symbol.add(i)
    Terminal_symbol.add('#')  #终结符还包括#
    print("Terminal_symbol",Terminal_symbol)
    All_symbol = Terminal_symbol | nonTerminal_symbol
    print("All_symbol",All_symbol)

    for a in nonTerminal_symbol:
        firstSet[a]=set()
    for a in Terminal_symbol:
        firstSet[a]={a}

    help=[]#辅助变量
    for item in grammar:
        try:
            a=item["r"][0]
            if a in Terminal_symbol:
                firstSet[item["l"]].add(a)#终结符的first是他自己
        except:
            empty_first.append(item["l"])#包含有空的非终结符
            help.append(item["l"])

    grammar_copy=copy.deepcopy(grammar)#产生式
    while len(help)>0:
        a=help.pop(-1)
        for i,item in zip(range(len(grammar_copy)),grammar_copy):
            if item["l"]==a:
                grammar_copy[i]["r"]=[]
            elif a in item["r"]:
                grammar_copy[i]["r"].remove(a)
                if len(grammar_copy[i]["r"])==0 and item["l"] not in empty_first:
                    empty_first.append(item["l"])
                    help.append(a)
    print("empty_first",empty_first)
    #防止A->Bc,B->empty的情况
    judge=1
    while(judge):
        judge=0
        for item in grammar:
            for a in item["r"]:
                if not firstSet[item["l"]].issuperset(firstSet[a]):
                    judge=1
                    firstSet[item["l"]]|=firstSet[a]
                if a not in empty_first:
                    break
    print("firstset",firstSet)

def pre_stage_of_ACTION_GOTO():
    #从grammar到grammar_point
    global grammar,grammar_point,Terminal_symbol,CLOSURE,accept_grammar_point,First_point
    for order,item in zip(range(len(grammar)),grammar):
        for j in range(len(item["r"])+1):
            grammar_point.append({"l":item["l"],"r":item["r"],"order":item["order"],"point":j,"origin":order,"finish":(j==len(item["r"]))})
    #从grammar_point到accept_grammar_point
    for item in grammar_point:
        for a in Terminal_symbol:
            accept_grammar_point.append(copy.deepcopy(item))
            accept_grammar_point[-1]["forward"]=a
            CLOSURE.append(set())
    #记录首项，point=0
    for i,item in zip(range(len(accept_grammar_point)),accept_grammar_point):
        if item["point"]==0:
            if item["l"] in First_point:
                First_point[item["l"]].add(i)
            else:
                First_point[item["l"]]={i}

def GET_CLOSURE(x,y):##求项目x的CLOSURE,y是最初的项目来源
    global CLOSURE,accept_grammar_point,firstSet
    item=accept_grammar_point[x]#以其为中心扩展得到
    try:
        # 对于[A->α·Bβ，a]，有B->·￥，将FIRST（βa)中的每个每个终结符b，如果[B->·￥,b]不在closure（I）中，把他加进去
        # curr就是b，a是自带的本来的符号，最开始的b为空，后面正常的话为￥，然后再加上a，它们的共同FIRST为要求的
        curr=item["r"][item["point"]]#点之后的符号
        b=""
        a=item["forward"]#展望符
        curr_fir = set()  # 经过扩展之后的展望符号，set是为了避免重复
        try:
            b=item["r"][(item["point"]+1):]#点之后符号的之后的所有符号
            b+=[a]
            for sym in b:
                curr_fir |= firstSet[sym]
                if sym not in empty_first:
                    break
        except:
            curr_fir=set(a)
        if curr in First_point:
            for item in First_point[curr]:
                if item not in CLOSURE[y] and accept_grammar_point[item]["forward"] in curr_fir:
                    CLOSURE[x].add(item)
                    CLOSURE[y].add(item)
                    CLOSURE[x] |= GET_CLOSURE(item,y)
    except:
        CLOSURE[x].add(x)
        return {x}

    return CLOSURE[x]

def GET_PER_CLOSURE():
    #求每个项目的闭包
    global  accept_grammar_point,CLOSURE,CLOSURESET
    for i,item in zip(range(len(accept_grammar_point)),accept_grammar_point):
        CLOSURE[i].add(i)#从自己本身出发去扩展
        CLOSURE[i]=GET_CLOSURE(i,i)
        if item["origin"]==0 and item["forward"]=="#" and item["point"]==0:#0号项目集
            CLOSURESET.append(CLOSURE[i])

def GET_GOTO(x):
    global All_symbol,CLOSURE,CLOSURESET,ACTION_GOTO,Terminal_symbol
    for j in CLOSURESET[x]:
        item=accept_grammar_point[j]
        try:
            curr=item["r"][item["point"]]
            if curr in ACTION_GOTO[x]:
                ACTION_GOTO[x][curr].append(j+len(Terminal_symbol))
            else:
                ACTION_GOTO[x][curr]=[j+len(Terminal_symbol)]
        except:
            pass
    for j in All_symbol:
        if j in ACTION_GOTO[x]:
            new=set()
            for item in ACTION_GOTO[x][j]:
                new |= CLOSURE[item]
            if new in CLOSURESET:
                ACTION_GOTO[x][j]=CLOSURESET.index(new)
            else:
                CLOSURESET.append(new)
                ACTION_GOTO.append({})
                ACTION_GOTO[x][j]=len(CLOSURESET)-1

def GET_ACTION_GOTO(_grammar,keywordsList):
    global ACTION_GOTO,CLOSURESET
    preprocess(_grammar,keywordsList)
    pre_stage_of_ACTION_GOTO()
    GET_PER_CLOSURE()
    ACTION_GOTO.append({})
    num=0
    while num<len(CLOSURESET):
        GET_GOTO(num)
        num=num+1
    #输出构建的项目族群
    CLOSURESETFile=open("./intermediate/CLOSURESET.txt",'w')
    for i in range(len(CLOSURESET)):
        print(i,file=CLOSURESETFile)
        for k in CLOSURESET[i]:
            print(accept_grammar_point[k],file=CLOSURESETFile)

    ACTIONGOTOFile = open("./intermediate/ACTION_GOTO.txt", 'w')
    ts=sorted(list(Terminal_symbol-{START_SYMBOL}))
    nts=sorted(list(nonTerminal_symbol-{START_SYMBOL}))
    print("   ", '  '.join(map(lambda x: (x + "  ")[:8], ts)), "", '  '.join(map(lambda x: (x + "  ")[:8], nts)),file=ACTIONGOTOFile)
    for i in range(len(CLOSURESET)):
        print("%-3d"%i,end=" ",file=ACTIONGOTOFile)
        for k in CLOSURESET[i]:
            item=accept_grammar_point[k]
            if item["finish"]==True:
                if item["forward"] in ACTION_GOTO[i]:
                    print("Warning:,%d号项目集族的\t %s \t符号与产生式"%(i,item["forward"]),accept_grammar_point[k],"冲突！")
                    print("项目集族见下：")
                    for a in CLOSURESET[i]:
                        print(a,accept_grammar_point[a])
                else:
                    ACTION_GOTO[i][item["forward"]]=-item["origin"]

        for j in ts:
            try:
                if ACTION_GOTO[i][j] > 0:
                    print("s%-3d" % ACTION_GOTO[i][j], end=" ", file=ACTIONGOTOFile)
                if ACTION_GOTO[i][j] < 0:
                    print("r%-3d" % -ACTION_GOTO[i][j], end=" ", file=ACTIONGOTOFile)
                if ACTION_GOTO[i][j] == 0:
                    print("acc ", end=" ", file=ACTIONGOTOFile)
            except:
                print("    ", end=" ", file=ACTIONGOTOFile)
        for j in nts:
            try:
                print("%-4d"%ACTION_GOTO[i][j],end=" ",file=ACTIONGOTOFile)
            except:
                print("    ",end=" ",file=ACTIONGOTOFile)
        print(file=ACTIONGOTOFile)

    return ACTION_GOTO,grammar
'''
keywordsList=['ID', 'INT', 'VOID', 'DOUBLE', '(', ')', ';', '=', ',', '{', '}', 'IF', 'ELSE', 'WHILE', 'RETURN', 'RELOP', 'ADDOP', 'MULOP', 'NUM']
_grammar={'program': [['declaration_list']], 'declaration_list': [['declaration_list', 'declaration'], ['declaration']], 'declaration': [['var_declaration'], ['fun_declaration']], 'var_declaration': [['type_specifier', 'ID'], ['type_specifier', 'ID', '=', 'NUM', ';']], 'type_specifier': [['INT'], ['VOID'], ['DOUBLE']], 'fun_declaration': [['type_specifier', 'ID', '(', 'params', ')', 'compound_stmt']], 'params': [['param_list'], ['VOID']], 'param_list': [['param_list', ',', 'param'], ['param']], 'param': [['type_specifier', 'ID']], 'compound_stmt': [['{', 'local_declarations', 'statement_list', '}']], 'local_declarations': [['var_declaration', 'local_declarations'], ['empty']], 'statement_list': [['statement', 'statement_list'], ['empty']], 'statement': [['expression_stmt'], ['compound_stmt'], ['selection_stmt'], ['iteration_stmt'], ['return_stmt']], 'expression_stmt': [['expression', ';'], [';']], 'selection_stmt': [['IF', '(', 'expression', ')', 'statement'], ['IF', '(', 'expression', ')', 'statement', 'ELSE', 'statement']], 'iteration_stmt': [['WHILE', '(', 'expression', ')', 'statement']], 'return_stmt': [['RETURN', ';'], ['RETURN', 'expression', ';']], 'expression': [['var', '=', 'expression'], ['simple_expression']], 'var': [['ID']], 'simple_expression': [['additive_expression'], ['simple_expression', 'RELOP', 'additive_expression']], 'additive_expression': [['term'], ['additive_expression', 'ADDOP', 'term']], 'term': [['factor'], ['term', 'MULOP', 'factor']], 'factor': [['(', 'expression', ')'], ['var'], ['call'], ['NUM']], 'call': [['ID', '(', 'args', ')']], 'args': [['arg_list'], ['empty']], 'arg_list': [['arg_list', ',', 'expression'], ['expression']]}
preprocess(_grammar,keywordsList)'''
