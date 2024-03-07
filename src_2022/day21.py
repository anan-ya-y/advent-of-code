import re, utils
import operator

class Monkey:
    def __init__(self, name, yells):
        self.isint = yells is None or yells.isdigit()
        self.name = name
        self.children = []

        if yells is None:
            self.content = None
        elif not self.isint:
            x = yells.split(" ")
            self.content = [x[0], self.read_op(x[1]), x[2]]
            self.children = [x[0], x[2]]
        else:
            self.content = int(yells)

        self.in_human_chain = False

    def read_op(self, operation, part=1):
        ops = {"*": operator.mul, \
               "+": operator.add, \
               "-": operator.sub, \
               "/": operator.truediv, \
               "=": operator.eq}
        return ops[operation[0]]
    
    def flip_operator(self):
        if self.isint:
            return
        op = self.content[1]
        if op == operator.add:
            return operator.sub
        elif op == operator.sub:
            return operator.add
        elif op == operator.mul:
            return operator.truediv
        elif op == operator.truediv:
            return operator.mul
    
    def yell(self, other_monkeys):
        if self.isint:
            return self.content
        else:
            op = self.content[1]
            m1 = other_monkeys[self.content[0]].yell(other_monkeys)
            m2 = other_monkeys[self.content[2]].yell(other_monkeys)
            if m1 is None or m2 is None:
                self.in_human_chain = True
                return None
            return op(m1, m2)
        
    # returns what humn should yell if self has to return `target`
    def reverse_yell(self, target, other_monkeys):
        # print(self.name, "needs to yell", target)
        if self.name == "humn":
            return target
        if self.isint:
            return self.content
        
        
        child1, op, child2 = self.content
        invop = self.flip_operator()

        yell_left = other_monkeys[child1].yell(other_monkeys)
        yell_right = other_monkeys[child2].yell(other_monkeys)

        if yell_left is not None and yell_right is not None:
            return op(yell_left, yell_right)
        
        if yell_left is None:
            return other_monkeys[child1].reverse_yell(invop(target, yell_right), other_monkeys)
        
        # child2 is None
        if self.content[1] in [operator.add, operator.mul]:
            return other_monkeys[child2].reverse_yell(invop(target, yell_left), other_monkeys)
        return other_monkeys[child2].reverse_yell(op(yell_left, target), other_monkeys)



        
    
def p1(input):
    input = utils.split_and_strip(input)
    monkeys = {}
    for line in input:
        x = utils.split_and_strip(line, ":")
        monkeys[x[0]] = Monkey(x[0], x[1])
    return monkeys["root"].yell(monkeys)

def p2(input):
    input = utils.split_and_strip(input)
    monkeys = {}

    for line in input:
        x = utils.split_and_strip(line, ":")
        if x[0] == "humn":
            x[1] = None
        if x[0] == "root":
            x[1] = x[1].replace("+", "-")
        monkeys[x[0]] = Monkey(x[0], x[1])

    return monkeys["root"].reverse_yell(0, monkeys)


    # xleft = monkeys[monkeys["root"].children[0]].yell(monkeys)
    # xright = monkeys[monkeys["root"].children[1]].yell(monkeys)
    # children = [xleft, xright]
    # monkeys["root"].in_human_chain = True

    # children.remove(None)
    # target = children[0]

    # return monkeys["root"].reverse_yell(target, monkeys)







