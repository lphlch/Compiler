class SymbolTable:
    def __init__(self) -> None:
        self.table = {}

    def set(self, name, kind, type, normal, value):
        self.table[name] = [kind, type, normal, value]

    def get(self, name):
        if name not in self.table:
            return None
        return self.table[name]

    def remove(self, name):
        del self.table[name]

    def print(self):
        print(self.table)


class Translation:
    def __init__(self) -> None:
        self.symbolTable = SymbolTable()
        self.tempNum = 0

    def translateDeclareConst(self, type, name, value):
        # const int a = 1;
        # type = int, name = a, value = 1
        # target : := 1 - a

        # add name to symbol table
        self.symbolTable.set(name, "const", type, False, value)
        code = [":=", value, "", name]
        return code

    def translateDeclareVar(self, type, name, value=None):
        # int a; int a =1;
        # type = int, name = a, value = 1
        # target : a

        # add name to symbol table
        self.symbolTable.set(name, "var", type, False, value)
        code = [":=", value, "", name]
        return code

    def translateAssign(self, name, value):
        # a = 1; a = b;
        # name = a, value = 1; name = a, value = b
        # target : := 1 - a; := b - a

        # get name from symbol table
        try:
            kind, type, normal, _ = self.symbolTable.get(name)
        except:
            return None
        code = [":=", value, "", name]
        self.symbolTable.set(name, kind, type, False, value)
        return code

    def translateAddop(self, op, arg1, arg2):
        # 1 + 2;
        # op = +, left = 1, right = 2
        # target : + 1 2 newTemp

        # make a new temp
        name = "T" + str(self.tempNum)
        self.tempNum += 1

        code = [op, arg1, arg2, name]
        self.symbolTable.set(name, "var", "int", False, None)
        return code
