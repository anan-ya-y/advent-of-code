import re, utils
from functools import reduce
from operator import mul, add

# gonna map reduce this one

def read_input(input):
    input = utils.split_and_strip(input)
    all = []
    for line in input:
        r = re.findall(r"(\w+): capacity (-?[0-9]+), durability (-?[0-9]+), flavor (-?[0-9]+), texture (-?[0-9]+), calories (-?[0-9]+)", line)[0]
        r = list(r)
        nums = list(map(int, r[1:]))
        all.append([r[0]] + nums)

    return all

def generate_allocs(max_num, ningredients):
    if ningredients == 1:
        yield [max_num]
        return
    
    for i in range(0, max_num+1):
        for j in generate_allocs(max_num-i, ningredients-1):
            yield [i] + j  

def get_score(recipes, vals, part=1):
    qtys = [list(map(lambda x: x*val, recipe)) for recipe, val in zip(recipes, vals)]
    total_qtys = reduce(lambda x, y: map(add, x, y), qtys)
    total_qtys = list(map(lambda x: max(0, x), total_qtys))
    if part == 2 and total_qtys[-1] != 500:
        return 0
    return reduce(mul, total_qtys[:-1])

def p1(input):
    input = read_input(input)
    recipes_only = [x[1:] for x in input]
    
    return max(map(lambda qtys: get_score(recipes_only, qtys), 
                   generate_allocs(100, len(input)))
                   )
    
def p2(input):
    input = read_input(input)
    recipes_only = [x[1:] for x in input]
    return max(map(lambda qtys: get_score(recipes_only, qtys, part=2), 
                   generate_allocs(100, len(input)))
                   )
    