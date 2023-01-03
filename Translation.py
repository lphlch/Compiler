class SymbolTable:
    def __init__(self) -> None:
        self.table = {}

    def set(self, name, kind, typeOfValue, normal, value):
        self.table[name] = [kind, typeOfValue, normal, value]

    def get(self, name):
        if name not in self.table:
            return None
        return self.table[name]

    def remove(self, name):
        del self.table[name]

    def print(self):
        print(self.table)

    def checkIfExist(self, name):
        if name in self.table:
            return True
        return False

    def checkIfTypeCorrect(self, name, typeOfValue):
        if name in self.table:
            if self.table[name][1] == typeOfValue:
                return True
        return False


class TranslationProcess:
    def __init__(self) -> None:
        self.symbolTable = SymbolTable()
        self.tempNum = 0

        self.codes = []

        self.VALUEDIR = 3  # the position of values dict in the symbol stack

        # the type of production
        self.EXPRESSION = [
            "expression",
            "first_expression",
            "second_expression",
            "third_expression",
            "primary_expression",
        ]
        self.OP_EXPRESSION = ["first_operator", "second_operator"]
        self.M = ["M", "M_selection_statement", "N_iteration_statement"]
        self.N = [
            "N_selection_statement",
        ]
        self.Q=[
            "Q"
        ]
        self.IF_EXPERSSION = [
            "selection_statement",
        ]
        self.WHILE_EXPERSSION = [
            "iteration_statement",
        ]
        self.BOOL_EXPRESSION = [
            "or_bool_expression",
            "and_bool_expression",
            "single_bool_expression",
            "constant_expression",
            "Q1",
            "Q2"
        ]  # ? not sure for single_expression and constant_expression
        self.DECLARATION_ASSIGN = ["declaration_parameter_assign"]
        self.DECLARATION = ["declaration_parameter"]
        self.ASSIGN = ["assignment_expression"]

    def translate(self, parentNodeStr, childrenNode,transfomer):
        # parentNodeStr : left of production, only string
        # childrenNode : right of production, with values
        # example : translate("E", [("E",{}), ("+",{}), ("T",{values})])

        # according to parentNode and childrenNode, check which translation function should use

        parentValue = {}
        print("parentNodeStr", parentNodeStr)
        print("childrenNode", childrenNode)
        print("transfomer:",transfomer)
        temp=transfomer

        if parentNodeStr in self.M:
            parentValue = {"quad": str(len(self.codes))}

        elif parentNodeStr in self.N:
            parentValue = {"nextlist": {str(len(self.codes))}}
            code = ["j", "-", "-", "0"]
            self.codes.append(code)

        elif parentNodeStr in self.Q:
            temp=1

        elif parentNodeStr in self.EXPRESSION:  # if is arth expression, do translation
            if (
                len(childrenNode) == 1
            ):  # if only one child, assign child value to parent
                parentValue = childrenNode[0][self.VALUEDIR]
            elif parentNodeStr == "third_expression" and childrenNode[0][0] == "!":
                arg = childrenNode[1][self.VALUEDIR]
                if arg.get("falselist") == None:
                    truelist = {len(self.codes) + 1}
                    falselist = {len(self.codes)}
                    self.translate_id(arg)
                    parentValue = {"truelist": truelist, "falselist": falselist}
                else:
                    parentValue = {
                        "truelist": arg.get("falselist"),
                        "falselist": arg.get("truelist"),
                    }
            else:  # if more than one child, do translation
                op = childrenNode[1][self.VALUEDIR]
                arg1 = childrenNode[0][self.VALUEDIR]
                arg2 = childrenNode[2][self.VALUEDIR]
                newName = self.translateAddop(op, arg1, arg2)
                if newName == None:
                    parentValue = op  # this is for case of brackets like '(expression)'
                else:
                    parentValue = {"identifierName": newName}

        elif parentNodeStr in self.OP_EXPRESSION:
            parentValue = childrenNode[0][
                0
            ]  # + - * / is not an attribute, so just assign the str to parent value

        elif parentNodeStr in self.BOOL_EXPRESSION:
            if len(childrenNode) == 1:
                # if only one child, assign child value to parent
                #input()
                parentValue = childrenNode[0][self.VALUEDIR]
                #temp=0
                if parentNodeStr == "constant_expression"and transfomer==1:#要进行jnz转换
                    temp=0
                    if (childrenNode[0][self.VALUEDIR].get("truelist") == None):
                        #print(temp,parentValue,childrenNode)
                        parentValue = {"truelist": {len(self.codes)}, "falselist": {len(self.codes)+1}}
                        self.translate_id(childrenNode[0][self.VALUEDIR])
                elif parentNodeStr=="Q1" or parentNodeStr=="Q2":
                    if(childrenNode[0][self.VALUEDIR].get("truelist")==None):
                        parentValue = {"truelist": {len(self.codes)}, "falselist": {len(self.codes) + 1}}
                        self.translate_id(childrenNode[0][self.VALUEDIR])
            else:
                # if more than one child, do translation
                if "bool_operator" in childrenNode[1]:  # E->id1 relop id2
                    op = childrenNode[1][self.VALUEDIR]
                    arg1 = childrenNode[0][self.VALUEDIR]
                    arg2 = childrenNode[2][self.VALUEDIR]
                    parentValue = {
                        "truelist": {len(self.codes)},
                        "falselist": {len(self.codes) + 1},
                    }
                    self.translate_relop(op, arg1, arg2)
                elif "and_operator" in childrenNode[1]:  # and语句的翻译
                    quad = childrenNode[2][self.VALUEDIR]
                    quad = quad.get("quad")
                    arg1 = childrenNode[0][self.VALUEDIR]
                    arg2 = childrenNode[3][self.VALUEDIR]
                    if arg1.get("truelist") == None and arg2.get("truelist") == None:
                        truelist1 = {len(self.codes)}
                        falselist1 = {len(self.codes) + 1}
                        self.translate_id(arg1)
                        backlist = truelist1
                        quad = str(len(self.codes))
                    elif arg1.get("truelist") == None:
                        print("请不要输入类似a && E的形式，其中a是标识符！！！")
                        exit(0)
                    else:
                        backlist = arg1.get("truelist")  # 要回填的链表
                        falselist1 = arg1.get("falselist")
                    for item in backlist:  # 回填
                        item = int(item)
                        self.codes[item][3] = quad
                    if arg2.get("truelist") == None:
                        truelist2 = {len(self.codes)}
                        falselist2 = {len(self.codes) + 1}
                        self.translate_id(arg2)
                    else:
                        truelist2 = arg2.get("truelist")
                        falselist2 = arg2.get("falselist")
                    truelist = truelist2  # 获得实际真假链
                    falselist = falselist1 | falselist2
                    parentValue = {"truelist": truelist, "falselist": falselist}
                    quad = str(len(self.codes))
                    for item in truelist:  # 回填
                        item = int(item)
                        self.codes[item][3] = quad
                    for item in falselist:
                        item = int(item)
                        self.codes[item][3] = quad
                elif "or_operator" in childrenNode[1]:
                    quad = childrenNode[2][self.VALUEDIR]
                    quad = quad.get("quad")
                    arg1 = childrenNode[0][self.VALUEDIR]
                    arg2 = childrenNode[3][self.VALUEDIR]
                    if arg1.get("truelist") == None and arg2.get("truelist") == None:
                        truelist1 = {len(self.codes)}
                        falselist1 = {len(self.codes) + 1}
                        self.translate_id(arg1)
                        backlist = falselist1
                    elif arg1.get("truelist") == None:
                        print("请不要输入类似a || E的形式，其中a是标识符！！！")
                        exit(0)
                    else:
                        backlist = arg1.get("falselist")  # 要回填的链表
                        truelist1 = arg1.get("truelist")
                    for item in backlist:  # 回填
                        item = int(item)
                        self.codes[item][3] = quad
                    if arg2.get("truelist") == None:
                        truelist2 = {len(self.codes)}
                        falselist2 = {len(self.codes) + 1}
                        self.translate_id(arg2)
                    else:
                        truelist2 = arg2.get("truelist")
                        falselist2 = arg2.get("falselist")
                    truelist = truelist1 | truelist2
                    falselist = falselist2
                    parentValue = {"truelist": truelist, "falselist": falselist}
                    quad = str(len(self.codes))
                    for item in truelist:  # 回填
                        item = int(item)
                        self.codes[item][3] = quad
                    for item in falselist:
                        item = int(item)
                        self.codes[item][3] = quad

        elif parentNodeStr in self.DECLARATION:
            # if is declaration, need to emit a assign code & add to symbol table
            name = childrenNode[0][self.VALUEDIR]
            value = childrenNode[2][self.VALUEDIR]
            newName = self.translateAssign(name, value)
            parentValue = {"identifierName": newName}

        elif parentNodeStr in self.DECLARATION_ASSIGN:
            # if is declaration, but only after the = sign, so just assign the value to parent
            parentValue = childrenNode[1][self.VALUEDIR]

        elif parentNodeStr in self.ASSIGN:
            # if is assign, need to emit a assign code & change symbol table
            name = childrenNode[0][self.VALUEDIR]
            value = childrenNode[2][self.VALUEDIR]
            newName = self.translateAssign(name, value)
            parentValue = {"identifierName": newName}

        elif parentNodeStr == "bool_operator":
            parentValue = {"op": childrenNode[0][0]}

        elif parentNodeStr in self.IF_EXPERSSION:
            if len(childrenNode) == 7:  # 不含else
                E = childrenNode[3][self.VALUEDIR]
                S = childrenNode[6][self.VALUEDIR]
                quad = childrenNode[5][self.VALUEDIR].get("quad")
                backlist = E.get("truelist")
                for item in backlist:  # 回填
                    item = int(item)
                    self.codes[item][3] = quad
                a = S.get("nextlist")
                if S.get("nextlist") == None:
                    a = set()
                parentValue = {"nextlist": E.get("falselist") | a}
                quad = str(len(self.codes))
                for item in E.get("falselist") | a:
                    item = int(item)
                    self.codes[item][3] = quad

            else:  # 含else
                E = childrenNode[3][self.VALUEDIR]
                quad1 = childrenNode[5][self.VALUEDIR].get("quad")
                S1 = childrenNode[6][self.VALUEDIR]
                N = childrenNode[7][self.VALUEDIR]
                quad2 = childrenNode[9][self.VALUEDIR].get("quad")
                S2 = childrenNode[10][self.VALUEDIR]
                backlist1 = E.get("truelist")
                for item in backlist1:  # 回填1
                    item = int(item)
                    self.codes[item][3] = quad1
                backlist2 = E.get("falselist")
                for item in backlist2:  # 回填2
                    item = int(item)
                    self.codes[item][3] = quad2
                a = S1.get("nextlist")
                b = S2.get("nextlist")
                if S1.get("nextlist") == None:
                    a = set()
                if S2.get("nextlist") == None:
                    b = set()
                parentValue = {"nextlist": a | b | N.get("nextlist")}
                quad = str(len(self.codes))
                for item in a | b | N.get("nextlist"):
                    item = int(item)
                    self.codes[item][3] = quad

        elif parentNodeStr in self.WHILE_EXPERSSION:  # while
            quad1 = childrenNode[1][self.VALUEDIR].get("quad")
            E = childrenNode[4][self.VALUEDIR]
            quad2 = childrenNode[6][self.VALUEDIR].get("quad")
            S = childrenNode[7][self.VALUEDIR]
            if S.get("nextlist") != None:
                backlist1 = S.get("nextlist")
            else:
                backlist1 = set()
            for item in backlist1:
                item = int(item)
                self.codes[item][3] = quad1
            backlist2 = E.get("truelist")
            for item in backlist2:
                item = int(item)
                self.codes[item][3] = quad2
            parentValue = {"nextlist": E.get("falselist")}
            code = ["j", "-", "-", quad1]
            self.codes.append(code)
            quad = str(len(self.codes))
            for item in E.get("falselist"):
                item = int(item)
                self.codes[item][3] = quad

        # todo: add more translation function here

        print("return parentValue", parentValue)
        return parentValue,temp

    def genCode(self):
        print("--------------------")
        num = 0
        for code in self.codes:
            print(num, ":", code)
            num = num + 1

    def translate_relop(self, op, arg1, arg2):  # a>=b之类的翻译
        if arg1.get("identifierName") != None:
            arg1Val = arg1.get("identifierName")
        else:
            arg1Val = arg1.get("numberValue")

        if arg2.get("identifierName") != None:
            arg2Val = arg2.get("identifierName")
        else:
            arg2Val = arg2.get("numberValue")

        code = ["j" + op.get("op"), arg1Val, arg2Val, "0"]
        self.codes.append(code)
        code = ["j", "-", "-", "0"]
        self.codes.append(code)

    def translate_id(self, arg):  # a的布尔翻译（a 不是表达式）
        if arg.get("identifierName") != None:
            argVal = arg.get("identifierName")
        else:
            argVal = arg.get("numberValue")
        code = ["jnz", argVal, "-", "0"]
        self.codes.append(code)
        code = ["j", "-", "-", "0"]
        self.codes.append(code)

    # ! deprecated
    # def translateDeclareConst(self, typeOfValue, name, value):
    #     # const int a = 1;
    #     # typeOfValue = int, name = a, value = 1
    #     # target : := 1 - a

    #     # add name to symbol table
    #     self.symbolTable.set(name, "const", typeOfValue, False, value)
    #     code = [":=", value, "", name]
    #     return code

    # def translateDeclareVar(self, typeOfValue, name, value=None):
    #     # int a; int a =1;
    #     # typeOfValue = int, name = a, value = 1
    #     # target : a

    #     # add name to symbol table
    #     self.symbolTable.set(name, "var", typeOfValue, False, value)
    #     code = [":=", value, "", name]
    #     return code

    def translateAssign(self, name, value):
        # a = 1; a = b;
        # name = a, value = 1; name = a, value = b
        # target : := 1 - a; := b - a

        # get name from symbol table
        try:
            kind, typeOfValue, normal, _ = self.symbolTable.get(name["identifierName"])
        except:
            print("Notice : variable not declared")
            # add information of symbol table
            kind = "var"
            if value.get("identifierName") != None:
                typeOfValue = self.symbolTable.get(value["identifierName"])[1]
            else:
                typeOfValue = "int" if value["numberValue"].find(".") == -1 else "float"

        if value.get("identifierName") != None:
            value = value.get("identifierName")
        else:
            value = value.get("numberValue")

        name = name.get("identifierName")

        code = [":=", value, "", name]
        # add name to symbol table

        self.symbolTable.set(name, kind, typeOfValue, False, value)

        self.codes.append(code)
        return name

    def translateAddop(self, op, arg1, arg2):
        # 1 + 2;
        # op = +, left = 1, right = 2
        # target : + 1 2 newTemp

        if arg1.get("identifierName") != None:
            arg1Val = arg1.get("identifierName")
        else:
            arg1Val = arg1.get("numberValue")

        if arg2.get("identifierName") != None:
            arg2Val = arg2.get("identifierName")
        else:
            arg2Val = arg2.get("numberValue")

        if arg1Val == None and arg2Val == None:
            return None

        # make a new temp
        name = "T" + str(self.tempNum)
        self.tempNum += 1

        code = [op, arg1Val, arg2Val, name]
        self.symbolTable.set(name, "var", "int", False, None)
        self.codes.append(code)
        print("code emitted:", code)
        return name  # return name of temp


if __name__ == "__main__":
    translation = TranslationProcess()
    code = translation.translateDeclareConst("int", "a", 1)
    print(code)
    code = translation.translateDeclareVar("int", "b", 2)
    print(code)
    code = translation.translateAssign("b", 3)
    print(code)
    code, _ = translation.translateAddop("+", "a", "b")
    print(code)
    translation.symbolTable.print()
