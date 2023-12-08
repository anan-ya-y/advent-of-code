import utils
import re
import operator
import math

class Monkey:
    def __init__(self, num, items, operation, test, monkey_true, monkey_false, part=1):
        self.num = num
        self.op = self.read_op(operation, part=part)
        self.test = lambda x : x % test == 0
        self.div = test
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.items = items
        self.nitems_inspected = 0
    
    def read_op(self, operation, part=1):
        ops = {"*": operator.mul, "+": operator.add}
        if operation[1] == "old":
            return lambda x: ops[operation[0]](x, x)
        return lambda x: ops[operation[0]](x, int(operation[1]))

            
    def one_item_iteration(self, item, part=1):
        new_value = self.op(item)
        if part == 1:
            new_value //= 3
        full_operation = self.test(new_value)
        self.nitems_inspected += 1
        # print(self.num, item, new_value)
        return new_value, (self.monkey_true if full_operation else self.monkey_false)
    def one_iteration(self, part=1):
        new_items = []
        new_locs = []
        for i in self.items:
            new_value, new_loc = self.one_item_iteration(i, part)
            new_items.append(new_value)
            new_locs.append(new_loc)
        self.items = []
        return new_items, new_locs


def process_input(input, part=1):
    monkey_text = input.split("\n\n")
    monkeys = {}
    for ls in monkey_text:
        l = ls.split("\n")
        num = int(re.findall(r"Monkey (\d+):", l[0])[0])
        holding = re.findall(r"(\d+)", l[1])
        op = re.findall(r"new = old (\*|\+) (\d+|old)", l[2])[0]
        test = int(re.findall(r"(\d+)", l[3])[0])
        monkey_true = int(re.findall(r"(\d+)", l[4])[0])
        monkey_false = int(re.findall(r"(\d+)", l[5])[0])

        holding = [int(h) for h in holding]
        
        monkeys[num] = Monkey(num, holding, op, test ,monkey_true, monkey_false, part)
    return monkeys


def p1(input):
    monkeys = process_input(input, part=1)
    niterations = 20
    for _ in range(niterations):
        for i in range(len(monkeys.keys())):
            new_items, new_locs = monkeys[i].one_iteration()
            for item, loc in zip(new_items, new_locs):
                monkeys[loc].items.append(item)
        # print([m.items for m in monkeys.values()])
        # print("---")
    
    monkey_inspections = [m.nitems_inspected for m in monkeys.values()]
    max_monkeys = max(monkey_inspections)
    monkey_inspections.remove(max_monkeys)
    return max_monkeys * max(monkey_inspections)

def p2(input):
    monkeys = process_input(input, part=2)
    monkey_divisibility = 1
    for m in monkeys:
        monkey_divisibility *= monkeys[m].div
    print(monkey_divisibility)

    niterations = int(1e4)
    for n in range(niterations):
        for i in range(len(monkeys.keys())):
            new_items, new_locs = monkeys[i].one_iteration(part=2)
            for item, loc in zip(new_items, new_locs):
                item %= monkey_divisibility
                monkeys[loc].items.append(item)
        # print([m.items for m in monkeys.values()])
        # print("---")
        if n+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]:
            print(n+1, [m.nitems_inspected for m in monkeys.values()])
    
    monkey_inspections = [m.nitems_inspected for m in monkeys.values()]
    max_monkeys = max(monkey_inspections)
    monkey_inspections.remove(max_monkeys)
    return max_monkeys * max(monkey_inspections)