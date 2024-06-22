import re

# cost, damage, armor
weapons = [   
    [8, 4, 0],
    [10, 5, 0],
    [25, 6, 0],
    [40, 7, 0],
    [74, 8, 0],
]

armor = [
    [0, 0, 0],
    [13, 0, 1],
    [31, 0, 2],
    [53, 0, 3],
    [75, 0, 4], 
    [102, 0, 5]
]

rings = [
    [0, 0, 0], 
    [25, 1, 0], 
    [50, 2, 0], 
    [100, 3, 0], 
    [20, 0, 1], 
    [40, 0, 2], 
    [80, 0, 3]
]

answers = [-1, -1]



def can_buy(goods, money):
    w, a, r1, r2 = goods
    if r1 == r2:
        return False, float('inf') # cant buy 2 of the same ring
    
    cost = weapons[w][0] + armor[a][0]
    for r in [r1, r2]:
        cost += rings[r][0]

    return cost <= money, cost

# stats are [hp, damage, armor]
# [100, 8, 0] [100 8 2]
def can_win(player_stats, boss_stats):
    boss_hp = boss_stats[0]
    player_hp = player_stats[0]

    player_hit_val = max(1, player_stats[1] - boss_stats[2]) # player damage - boss armor
    boss_hit_val = max(1, boss_stats[1] - player_stats[2]) # boss damage - player armor

    return player_hit_val >= boss_hit_val

    # TODO: make this so that it's just a math eqn and not a while loop
    while True:
        boss_hp -= player_hit_val
        if boss_hp <= 0:
            return True
        player_hp -= boss_hit_val
        if player_hp <= 0:
            return False

def read_input(input):
    return list(map(int, re.findall(r'\d+', input)))

def main(input):
    global answers 
    boss = read_input(input)
    money = 100

    lowest_cost_to_win = 100
    highest_cost_to_lose = 0

    player_hp = 100

    # weapon, armor, ring1, ring2
    for w in range(len(weapons)):
        for a in range(len(armor)):
            for r1 in range(len(rings)):
                for r2 in range(r1+1, len(rings)):
                    buyable, cost = can_buy([w, a, r1, r2], money)
                    # if not buyable:
                    #     continue
                    player_damage = weapons[w][1] + rings[r1][1] + rings[r2][1]
                    player_armor = armor[a][2] + rings[r1][2] + rings[r2][2]
                    player_stats = [player_hp, player_damage, player_armor]
                    winnable = can_win(player_stats, boss)
                    if winnable:
                        lowest_cost_to_win = min(lowest_cost_to_win, cost)
                    else:
                        highest_cost_to_lose = max(highest_cost_to_lose, cost)

    answers = (lowest_cost_to_win, highest_cost_to_lose)

def p1(input):
    main(input)
    return answers[0]

def p2(input):
    return answers[1]
