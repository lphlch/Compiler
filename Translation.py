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

        self.VALUEDIR = 3   # the position of values dict in the symbol stack
        
        # the type of production
        self.EXPRESSION = [
            "expression",
            "first_expression",
            "second_expression",
            "third_expression",
            "primary_expression",
        ]
        self.OP_EXPRESSION = ["first_operator", "second_operator"]
        self.BOOL_EXPRESSION = [
            "or_bool_expression",
            "and_bool_expression",
            "single_bool_expression",
            "constant_expression",
        ]  # ? not sure for single_expression and constant_expression
        self.DECLARATION_ASSIGN = ["declaration_parameter_assign"]
        self.DECLARATION = ["declaration_parameter"]
        self.ASSIGN = ["assignment_expression"]

    def translate(self, parentNodeStr, childrenNode):
        # parentNodeStr : left of production, only string
        # childrenNode : right of production, with values
        # example : translate("E", [("E",{}), ("+",{}), ("T",{values})])

        # according to parentNode and childrenNode, check which translation function should use

        parentValue = {}
        print("parentNodeStr", parentNodeStr)
        print("childrenNode", childrenNode)

        if parentNodeStr in self.EXPRESSION:  # if is arth expression, do translation

            if (
                len(childrenNode) == 1
            ):  # if only one child, assign child value to parent
                parentValue = childrenNode[0][self.VALUEDIR]
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
                parentValue = childrenNode[0][self.VALUEDIR]
            else:
                # if more than one child, do translation
                ...
                # todo: bool expression translation

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

        # todo: add more translation function here

        print("return parentValue", parentValue)
        return parentValue

    def genCode(self):
        print("--------------------")
        for code in self.codes:
            print(code)

    #! deprecated
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
