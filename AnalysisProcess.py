import json
import sys
from pyecharts import options as opts
from pyecharts.charts import Tree

class SynAnalyze(object):
    "语法分析类"
    def __init__(self):
        self.firstSet = dict()              # 终结符和非终结符的first集
        self.productions = list()           # 产生式列表
        self.terminators = list()           # 终结符集合
        self.nonTerminators = list()        # 非终结符集合
        self.productionsDict = dict()       # 将产生式集合按照左侧的非终结符归类
        self.LRTable = dict()               # LR(1)分析表
    def runOnLRTable(self, tokens,SynAnalyzeProcess_path):
        "进行移进规约分析"
        status_stack = [0]  # 状态栈
        symbol_stack = [('#', -1, 1)]  # 符号栈
        tree_layer = list()
        tree_layer_num = list()
        tree_line = list()
        tokens.reverse()
        isSuccess = False
        step = 0
        fp=open(SynAnalyzeProcess_path,'w')#分析过程存在这里
        message=''#报错信息/成功信息
        while True:
            step += 1
            top_status = status_stack[-1]
            now_line_num, now_token,_ = tokens[-1]
            if step != 1:
                fp.write('\ntoken:%s'%now_token)
            else:
                fp.write('token:%s'%now_token)
            fp.write('\nsymbol stack:\n')
            fp.write(str(symbol_stack))
            fp.write('\nstatus stack:\n')
            fp.write(str(status_stack))
            fp.write('\n')

            #if now_token in self.LRTable[top_status].keys():  # 进行状态转移
            if now_token in self.LRTable[top_status] or 'E' in self.LRTable[top_status]:  # 进行状态转移
                if now_token not in self.LRTable[top_status]:
                    action = self.LRTable[top_status]['E']
                else:
                    action = self.LRTable[top_status][now_token]
                    
                #print(action)
                #if action[0] == 'acc':
                if action==0:#成功
                    isSuccess = True
                    break
                #elif action[0] == 'S':
                elif action>0:#移进
                    if len(tree_layer_num) == 0:
                        tree_layer_num.append(0)
                    else:
                        tree_layer_num[0] += 1
                    #status_stack.append(action[1])
                    status_stack.append(action)
                    symbol_stack.append((now_token, 0, tree_layer_num[0]))
                    tree_layer.append((now_token, 0, tree_layer_num[0]))
                    tokens = tokens[:-1]
                #elif action[0] == 'r':
                elif action<0:#规约
                    #production = self.productions[action[1]]

                    production = self.productions[-action]#获取产生式（包含点等信息
                    #left = list(production.keys())[0]
                    left=production["l"]#产生式左部分
                    next_line = 0
                    #if production[left] != ['$']:  # 不需修改两个栈
                    if production["r"] != ['ε']:#不为空要做改变，否则不改变
                        right_length = len(production["r"])
                        status_stack = status_stack[:-right_length]
                        #symbol_stack = symbol_stack[:-right_length]
                        for i in range(len(symbol_stack) - 1, len(symbol_stack) - right_length - 1, -1):
                            next_line = max(next_line, symbol_stack[i][1])
                            tree_line.append(
                                [symbol_stack[i][1], symbol_stack[i][2], 0, 0])
                            symbol_stack.pop(i)
                        next_line += 1
                    else:
                        next_line = 1
                        right_length = 1
                        if len(tree_layer_num) == 0:
                            tree_layer_num.append(0)
                        else:
                            tree_layer_num[0] += 1
                        tree_layer.append(('$', 0, tree_layer_num[0]))
                        tree_line.append([0, tree_layer_num[0], 0, 0])
                    go = self.LRTable[status_stack[-1]][left]  # 归约时判断接下来的状态 ?????
                    if next_line == len(tree_layer_num):
                        tree_layer_num.append(0)
                    else:
                        tree_layer_num[next_line] += 1
                    for i in tree_line[-right_length:]:
                        i[2], i[3] = next_line, tree_layer_num[next_line]
                    #status_stack.append(go[1])
                    status_stack.append(go)
                    symbol_stack.append(
                        (left, next_line, tree_layer_num[next_line]))
                    tree_layer.append(
                        (left, next_line, tree_layer_num[next_line]))
            else:  # 无法进行状态转移，报错
                #print('line %s' % now_line_num)
                #print('found: %s' % now_token)Syntax Error!
                #print('expecting:')
            
                message+='\nline %s\n' % now_line_num+'found: %s\n' % now_token+'expecting:\n'
                #for exp in self.LRTable[top_status].keys():
                for exp in self.LRTable[top_status]:
                    #print(exp)
                    message+=exp+'\n'
                break
        if isSuccess==True:
            message+= '\nSyntax Analyze Successfully!\n'
        else:
            message+= '\nSyntax Error!\n'
        fp.write(message)
        fp.close()
        print(message)
        return isSuccess, tree_layer, tree_line,message

    def get_tree(self, tree_layer, tree_line):
        "获取画语法树所需信息"
        pre_data = dict()
        for i in tree_layer:
            if i[1] not in pre_data:
                pre_data[i[1]] = list()
            pre_data[i[1]].append({'name': i[0]})
        for i in tree_line:
            if 'children' not in pre_data[i[2]][i[3]]:
                pre_data[i[2]][i[3]]['children'] = list()
            pre_data[i[2]][i[3]]['children'].insert(
                0, pre_data[i[0]][i[1]])
        data = pre_data[max(pre_data.keys())]
        #print(json.dumps(data))
        file = open('./output/SynTree.txt', 'w')
        file.write(json.dumps(data))
        c = (
            Tree().add(
                "",
                data,
                orient="TB",
                initial_tree_depth=-1,
                # collapse_interval=10,
                symbol_size=3,
                is_roam=True,
                edge_shape="polyline",
                # is_expand_and_collapse=False,
                label_opts=opts.LabelOpts(
                    position="top",
                    horizontal_align="right",
                    vertical_align="middle",
                    # rotate='15',
                    font_size=15)).set_global_opts(title_opts=opts.TitleOpts(title="语法树")).render("./output/语法树.html"))
        # for i in range(len(data)):
        #     s = str(data[i]).replace('{', '').replace('}', '').replace("'", '').replace(':', ',') + '\n'
        #     file.write(s)

        #json.load(open('2.txt','w'),data)
        # Syn_tree = Tree().add("", data, orient="TB").set_global_opts(
        #     title_opts=opts.TitleOpts(title="Syn_Tree"))
        # Syn_tree.render(path=tree_path)

    def analyze(self, token_table_path,SynAnalyzeProcess_path):
        "语法分析，顶层函数"
        token_table = open(token_table_path, 'r')#读token表并处理
        tokens = list()
        for line in token_table:
            line = line[:-1]
            
            # next_token_type = line.split(' ')[1]
            # if next_token_type == 'identifier' or next_token_type == 'number':
            #     tokens.append((line.split(' ')[0], next_token_type))
            # else:
            #     next_token = line.split(' ')[1]
            #     tokens.append((line.split(' ')[0], next_token))
            
            # 将词法分析结果进行处理
            # tokens.append((line.split(' ')[0], line.split(' ')[1],line.split(' ')[2]))
            lineNum,type,value=line.split(' ')
            if type in ("int", "void", "if", "else", "while", "return", "for", "do", "break", "continue", "float", "double"):
                type=type.upper()   # 转为大写以符合文法规则
                if type == 'FLOAT':
                    type = 'DOUBLE' # 将float转为double
            if type in (">=", "<=","<",">","==","!="):
                type='RELOP'
            if type in ("+","-"):
                type='ADDOP'
            if type in ("*","/"):
                type='MULOP'
                
            tokens.append((lineNum,type,value))

        tokens.append((str(0), '#'))
        
        print('tokens',tokens)
        
        token_table.close()
        isSuccess, tree_layer, tree_line,message = self.runOnLRTable(tokens,SynAnalyzeProcess_path)#分析

        if isSuccess:#成功
            self.get_tree(tree_layer, tree_line)
            return True,message
        else:
            return False,message

def Analysis(ACTION_GOTO,grammar):
    #SynGrammar_path = './SynGra.txt'  # 语法规则文件相对路径
    TokenTable_path = './output/lexical_analysis.txt'  # 存储TOKEN表的相对路径
    #LRTable_path = './ActionGoto.csv'  # 存储LR表的相对路径
    #print(ACTION_GOTO)
    SA = SynAnalyze()
    SA.LRTable=ACTION_GOTO
    SA.productions=grammar
    SA.analyze(TokenTable_path,SynAnalyzeProcess_path="./output/StackInfo.txt")

