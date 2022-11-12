# Compiler

## Setup

1. Download *Flex* from [here](https://www.technorange.com/wp-content/uploads/Flex%20Windows%20%5BLex%20and%20Yacc%5D.exe) and install
2. Add the path of *flex.exe* and *gcc.exe* to the system environment
3. Clone the repository
4. Run the *run.bat*

## To Do

### Lex part

- [x] Rename the keywords
- [x] Rewrite the print function
- [x] Add more supporting symbols
- [ ] Add a function of pre-processing function, to read a whole sentence at once, delete comments and print the source codes

### Syntax part

- [ ] Grammar input process & create FIRST set
- [ ] Sentence input process & transform into FORMAL present
- [ ] from FIRST set to CLOSURE set
- [ ] from CLOSURE set to ACTION/GOTO table
- [ ] from FORMAL present & ACTION/GOTO table to solve the syntax
- [ ] show the result in a tree

## Requirement

### Input & Output

输入 **已知文法、单词串**

输出 **分析过程和语法树**

#### Data Flow

![](resource/dataflow.png)

输入处理，变成内部的数据结构

```python
input="S->F KK | T" # use the space to spilt symbol, no space in around the ->
Grammar={
    # 'name':[symbol1List,symbol2List,...]
    'S':[[F,KK],[T]]
    'F':[...]
}
KeywordsList=['e','a',...]
```

求FIRST集

```python
FIRST={
    #'name':{first_set}
    'S':{F,T},
    'F':{...}
}
```

构造CLOSURE

```python
accept_grammar_point={
    #包括展望符号以及点的位置
    {'l':['S'],'r':['B','B'],'point':0,'forward':'a'}#0
    {...}#1
    ...
}
#输出到accept.txt
CLOSURESET={#项目集族，里面的数字对应accept_grammar_point的下标
    [0,1,3,5,7],#I0
    [2,4,6,8],#I1
    ...#In
}
#输出到CLOSURESET.txt
```

求ACTION表和GOTO表

```python
 xxxxxxxxxx ACTION_GOTO=[#ACTION_GO[状态i][符号j]，0为acc，x为移进，-x为用产生式x规约（这个产生式下标为accept_grammar_point的下标号    # [state0_ac/goto,state1_ac/goto]    [   # state 0 {ac:operation,goto:operation}       'a':#在状态0遇见a做什么       'S':#遇见S做什么    ]    [        # state 1...    ]]#输出到ACTION_GOTO.txt
```

从输入的单词串转为形式化句子

```python
input=String() # int a=5;
FORMAL_SENTENSE=[
    START,INT,VAR,EQU,NUM,END	# defined in lex
]
```

移进/归约分析

输出 **分析过程** 和 **语法树**

## Test data

```python
# ppt chapter 4 page 34
E->T E1
E->+ T E1 | e
T->F T1
T1->* F T1 | e
F->( E ) | i
#
+
*
e
i
(
)
#

# homework 4
S->a | b | ( T )
T->S T1
T1->, S T1 | e
#
(
)
a
b
,
e
#

# ppt chapter 5 page 120
S1->S
S->B B
B->a B
B->b

# declare varible
D->D_S
D_S->D_H D_B
D_H->KEYWORD_char | KEYWORD_int | KEYWORD_float | KEYWORD_double | KEYWORD_string
D_B->D_WV | D_WOV
D_WOV->id
D_WV->id assign VALUE
VALUE->integer | decimal | charConst | stringConst
#
integer
decimal
charConst
stringConst
id
assign
KEYWORD_char
KEYWORD_int
KEYWORD_float
KEYWORD_double
KEYWORD_string
#

```



