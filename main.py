from GrammarInputProcess import getInput,getFirstSet,transformInput
from SentenceFormaler import getSentenceInput,callLex,processLexResult

inputs, keywordsList = getInput(1)  # input grammar
grammar = transformInput(inputs)  # transform grammar to a list of productions
firstSet = getFirstSet(grammar, keywordsList)  # get first set

ACTION_GOTO,point_grammar=GET_ACTION_GOTO(firstSet,grammar,keywordsList) #get action_goto table&point_grammar is used to analyze

getSentenceInput(1)  # input sentence, save to file sentence.txt
lexResultList = callLex("sentence.txt")  # call Lex.exe to analyze input
formalList = processLexResult(lexResultList)  # get formal sentence
