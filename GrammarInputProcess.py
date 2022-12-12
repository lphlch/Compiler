from copy import deepcopy

def getInput(method=0):
    """get input from user
    Args:
        method (int): 0 for input from keyboard, 1 for input from file

    Returns:
        list,list: a list of input,a list of keywords
        example: ['E->T E1', 'E->+ T E1 │ e', 'T->F T1', 'T1->* F T1 │ e', 'F->( E ) │ i'],['+','*','(',')','i','e']

    """
    inputList = []
    keywordsList = []
    if method == 0:
        print("Enter the grammar in the form of productions, enter two # to stop")
        while True:
            s = input()
            if s == "##":
                break
            if s.replace(" ", "") == "":
                continue
            inputList.append(s)

        print("Enter a keyword each line, enter two # to stop")
        while True:
            s = input()
            if len(s.split()) != 1:
                print("Error: keyword should be a single word, no space allowed")
                continue
            if s == "##":
                break
            if s.replace(" ", "") == "":
                continue
            keywordsList.append(s)

    if method == 1:
        file = open("./input/grammar.txt", "r")
        mode = 0
        for line in file:
            line = line.replace("\n", "")  # delete the newline character
            if line == "##":
                mode += 1
                continue
            if line.replace(" ", "") == "":
                continue
            if mode == 0:
                inputList.append(line)
            elif mode == 1:
                keywordsList.append(line)
            else:
                break
    
    
    # print("inputList:", inputList)
    # print("keywordsList:", keywordsList)
    return inputList, keywordsList


def transformInput(inputList):
    """transform input to a list of productions

    Args:
        inputList (list): a list of input
        example:['E->T E1', 'E->+ T E1 │ e', 'T->F T1', 'T1->* F T1 │ e', 'F->( E ) │ i']

    Returns:
        grammarList: grammarList
        example:{'E': [['+', 'T', 'E1'], ['e']], 'T': [['F', 'T1']], 'T1': [['*', 'F', 'T1'], ['e']], 'F': [['(', 'E', ')'], ['i']]}
    """
    _grammar = {}
    for item in inputList:
        head, tail = item.split("->")
        subList = []
        for subItem in tail.split("|"):
            subList.append(subItem.split())
        _grammar[head] = subList
    return _grammar


def getFirstSet(grammarList, keywordsList):
    """get first set

    Args:
        grammarList (list): grammarList
        keywordsList (list): keywordsList

    Returns:
        list: firstSet
        example:{'E': {'+', 'e', 'i'}, 'T': {'*', 'e', 'i'}, 'T1': {'*', 'e'}, 'F': {'(', 'i'}}
    """
    first = {item: set() for item in grammarList}  # initialize first set

    # for each sentence, add the first non-terminal symbol to the first set
    for sentence in grammarList:
        for symbol in grammarList[sentence]:
            if symbol[0] in keywordsList:
                first[sentence].add(symbol[0])
    while True:
        lastFirst = deepcopy(first)  # lastFirst is the first set of the last iteration
        # for each sentence like A->B C D, add the first set of B to the first set of A
        for sentence in grammarList:
            for symbol in grammarList[sentence]:
                if symbol[0] in grammarList:
                    first[sentence] = first[sentence].union(first[symbol[0]])
        if lastFirst == first:
            break

    # print("firstSet:", first)
    return first

if __name__ == "__main__":
    inputList, keywordsList = getInput(1)
    grammarList = transformInput(inputList)
    firstSet = getFirstSet(grammarList, keywordsList)
    print("grammarList:", grammarList)
    print("keywordsList:", keywordsList)

