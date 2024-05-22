import utils, re
from functools import reduce
from operator import add, mul

def read_input(input):
    input = utils.split_and_strip(input)
    reindeer = []
    for line in input:
        r = re.findall(r"\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)[0]
        reindeer.append(list(map(int, r)))

    return reindeer

def get_speed(reindeer, timestamp):
    fly, flytime, resttime = reindeer
    if timestamp % (flytime+resttime) < flytime:
        return fly
    return 0

def speeds(reindeer, total_time):
    return map(lambda x: get_speed(reindeer, x), range(total_time))

def position_over_time(reindeer, total_time):
    sum = 0
    s = speeds(reindeer, total_time)
    for i in s:
        sum += i
        yield sum

def position_at(reindeer, total_time):
    return reduce(add, speeds(reindeer, total_time))
    
max_time = 2503
def p1(input):
    input = read_input(input)
    return max(map(lambda r: position_at(r, max_time), input))

def p2(input):
    input = read_input(input)
    
    reindeer_per_ts = list(map(lambda x: list(position_over_time(x, max_time)), input))
    winning_positions = list(reduce(lambda x, y: map(max, x, y), reindeer_per_ts))
    reindeer_scores = map(lambda x: map(lambda a, b: a==b, x, winning_positions), reindeer_per_ts)
    total_scores = map(sum, reindeer_scores)
    return max(total_scores)