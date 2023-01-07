from GrammarInputProcess import getInput, getFirstSet, transformInput
from SentenceFormaler import getSentenceInput, callLex, processLexResult
from ActiongotoProcess import GET_ACTION_GOTO
from AnalysisProcess import Analysis
import webbrowser

errorFile = open(r"output\error.txt", "w")
errorFile.close()
webFile = open(r"output\语法树.html", "w")
webFile.close()
inputs, keywordsList = getInput(1)  # input grammar
grammar = transformInput(inputs)  # transform grammar to a list of productions
firstSet = getFirstSet(grammar, keywordsList)  # get first set

# print('keywordsList',keywordsList)
# print("grammar",grammar)
# print("firstSet",firstSet)

ACTION_GOTO, point_grammar = GET_ACTION_GOTO(
    grammar, keywordsList
)  # get action_goto table&point_grammar is used to analyze

getSentenceInput(1)  # input sentence, save to file sentence.txt
lexResultList = callLex("./input/input1.c")  # call Lex.exe to analyze input

# print(lexResultList)  # print result of Lex.exe, for debug

formalList = processLexResult(lexResultList)  # get formal sentence

analysis = Analysis(ACTION_GOTO, point_grammar)

# add code to html
codeFile = open(r"output\code.txt", "r")
errorFile = open(r"output\error.txt", "r")
webFile = open(r"output\语法树.html", "r")
content = webFile.readlines()
for i in range(len(content)):
    if content[i].find("/body") != -1:
        codeList = codeFile.readlines()
        errorList = errorFile.readlines()
        for j in range(len(errorList)):
            content.insert(i + j, errorList[j] + "<br>")
        for j in range(len(codeList)):
            content.insert(i + j + len(errorList), codeList[j] + "<br>")

        break

webFile = open(r"output\语法树.html", "w")
webFile.writelines(content)
webFile.close()
codeFile.close()

print("！！！注意，控制台信息仅供 debug 使用，实际生成语法树结果、四元式结果及语义检查错误，请查看打开的 html 文件！！！")

webbrowser.open_new_tab(r"output\语法树.html")
