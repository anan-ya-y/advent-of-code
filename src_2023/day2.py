import utils
import re
  
# returns id, [red_values], [green_values], [blue_values]
def get_game_info(line):
    id = int(re.findall(r"Game (\d+):", line)[0])
    gamestr = line.split(":")[-1].split(";")

    red_values = []
    green_values = []
    blue_values = []
    for round in gamestr:
        r = re.findall(r"(\d+) red", round)
        g = re.findall(r"(\d+) green", round)
        b = re.findall(r"(\d+) blue", round)

        r = int(r[0]) if r != [] else 0
        g = int(g[0]) if g != [] else 0
        b = int(b[0]) if b != [] else 0

        red_values.append(r)
        green_values.append(g)
        blue_values.append(b)
    return id, red_values, green_values, blue_values

    

def p1(input):
    input = utils.split_and_strip(input)
    sum = 0
    for line in input:
        id, reds, greens, blues = get_game_info(line)
        if max(reds) <= 12 and \
            max(greens) <= 13 and \
            max(blues) <= 14:
            sum += id
    
    return sum

def p2(input):
    input = utils.split_and_strip(input)
    sum = 0
    for line in input:
        id, reds, greens, blues = get_game_info(line)
        this_game_value = max(reds) * max(greens) * max(blues)
        sum += this_game_value
    
    return sum
        
        

# part1_solution("inputs/2.real.txt")
# part2_solution("inputs/2.real.txt")