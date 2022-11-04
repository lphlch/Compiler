# Compiler

## Setup

1. Download *Flex* from [here](https://www.technorange.com/wp-content/uploads/Flex%20Windows%20%5BLex%20and%20Yacc%5D.exe) and install
2. Add the path of *flex.exe* and *gcc.exe* to the system environment
3. Clone the repository
4. Run the *run.bat*

## To Do

- [x] Rename the keywords
- [x] Rewrite the print function
- [x] Add more supporting symbols
- [ ] Add a function of pre-processing function, to read a whole sentence at once, delete comments and print the source codes

## Requirement

### Input & Output

输入 **已知文法、单词串**

输出 **分析过程和语法树**

#### Data Flow

![](dataflow.png)

输入处理，变成内部的数据结构

```python
input="S->F | T"
Grammar={
    # 'name':[symbol1,symbol2,...]
    'S':[F,T],
    'F':[...]
}
```

求FIRST集

```python
FIRST={
    #'name':[first_set]
    'S':[F,T],
    'F':[...]
}
```

构造CLOSURE

```python
CLOSURE= [
    # [state1_closure,state2_closure]
    [# state 0
        #'name':[closure]
        'S':[
            	#[sentence,point_position]
                [ [F,T], 1 ],
                [...]
        ]
        'T':[...]
    ],
	[ #state 1
        ...
    ]
]
```

求ACTION表和GOTO表

```python
ACTION_GOTO=[
    # [state0_ac/goto,state1_ac/goto]
    [	# state 0 {ac:operation,goto:operation}
        'action':{
            #'name':[action,push_number]
            'S':[PUSH,3],
            'T':[POP,4]
        }
        'goto':{
            'S':[PUSH,3],
            'T':[POP,4]
        } 
    ]
    [
        # state 1...
    ]
]
```

从输入的单词串转为形式化句子

```python
input=String() # int a=5;
FORMAL_SENTENSE=[
    START,INT,VAR,EQU,NUM,END	# defined in lex
]
```

移进/归约分析

输出 **分析过程 ** 和 **语法树**

