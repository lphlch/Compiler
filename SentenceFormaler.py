import os


def getSentenceInput(method=0):
    if method == 0:
        string = input("Please input a sentence: ")
        file = open("./input/input.c", "w")
        file.write(string + "\n")
        file.close()
        return 0
    else:
        file = open("./input/input.c", "r")
        if not file:
            print("Error: cannot open file sentence.txt")
            return -1
        file.close()
        return 0


def callLex(inputString):
    exeFile = "Lex.exe"
    os.popen(exeFile + " " + inputString).read()
    lexResultFile = open("./output/lexical_analysis.txt", "r")
    lexResultList = lexResultFile.read()
    return lexResultList

def processLexResult(lexResultList):
    # ignore first line and last line
    formalList = lexResultList.split("\n")[3:-1]
    resultList=[]
    for item in formalList:
        item = item.split()[0]
        # print(item)
        resultList.append(item)
        # print(item.split('\t')[1])
        
    # print('formalList: ', resultList)
    return resultList
    
    
    
    
# getSentenceInput(1)
# lexResultList=(callLex("./input/sentence.txt"))
# # print(lexResultList)
# print(processLexResult(lexResultList))