输入 **已知文法**

S->F | T

输入处理，变成内部的数据结构

```python
Grammar={
    # 'name':[symbol1,symbol2,...]
    'S':[F,T],
    'F':[...]
}
```

FIRST集

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

ACTION表和GOTO表

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
移进/归约分析

直接输出

输出 **分析过程 **和 **语法树**

