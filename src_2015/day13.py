import utils, itertools

def parse_input(input):
    happiness_dict = {}
    input = utils.split_and_strip(input)
    for line in input:
        line = line.split()
        person1 = line[0]
        person2 = line[-1][:-1]
        units = int(line[3]) if line[2] == "gain" else -int(line[3])
        
        if person1 not in happiness_dict:
            happiness_dict[person1] = {}
        happiness_dict[person1][person2] = units
        
    return happiness_dict

def get_best_happiness(happiness_dict):
    def get_happiness(seating):
        total = 0
        for i in range(len(seating)):
            total += happiness_dict[seating[i]][seating[i-1]] + \
                     happiness_dict[seating[i]][seating[(i+1)%len(seating)]]
        return total
    
    people = list(happiness_dict.keys())
    max_happiness = 0
    for p in itertools.permutations(people):
        max_happiness = max(max_happiness, get_happiness(p))
    return max_happiness

def p1(input):
    happiness = parse_input(input)
    return get_best_happiness(happiness)


def p2(input):
    happiness = parse_input(input)
    for person in happiness:
        happiness[person]["me"] = 0
    happiness["me"] = {person: 0 for person in happiness}

    return get_best_happiness(happiness)