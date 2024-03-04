import re, utils
import operator

class Monkey:
    def __init__(self, name, yells):
        name = name.strip()
        yells = yells.strip()

        self.isint = yells.isdigit()
        self.name = name

        if not self.isint:
            x = yells.split(" ")
            self.content = [x[0], self.read_op(x[1]), x[2]]
        else:
            self.content = int(yells)

    def read_op(self, operation, part=1):
        ops = {"*": operator.mul, \
               "+": operator.add, \
               "-": operator.sub, \
               "/": operator.truediv}
        return ops[operation[0]]
    
    def yell(self, other_monkeys):
        if self.isint:
            return self.content
        else:
            op = self.content[1]
            m1 = other_monkeys[self.content[0]].yell(other_monkeys)
            m2 = other_monkeys[self.content[2]].yell(other_monkeys)
            return op(m1, m2)
    


def parse_input(input):
    input = utils.split_and_strip(input)
    monkeys = {}
    for line in input:
        x = line.split(":")
        monkeys[x[0]] = Monkey(x[0], x[1])

    return monkeys

def p1(input):
    monkeys = parse_input(input)
    return monkeys["root"].yell(monkeys)

def p2(input):
    return 1
