import utils
from queue import PriorityQueue

SHIELD = "shield"
POISON = "poison"
RECHARGE = "recharge"
MAGIC_MISSILE = "magic_missile"
DRAIN = "drain"

actionchoices = {
    MAGIC_MISSILE: {
        "cost": 53, "damage": 4, "heal": 0, "effect_time": 0, 
        "effect_armor": 0, "effect_damage": 0, "effect_mana": 0
        }, 
    DRAIN: {
        "cost": 73, "damage": 2, "heal": 2, "effect_time": 0, 
        "effect_armor": 0, "effect_damage": 0, "effect_mana": 0
        }, 
    SHIELD: {
        "cost": 113, "damage": 0, "heal": 0, "effect_time": 6, 
        "effect_armor": 7, "effect_damage": 0, "effect_mana": 0
        }, 
    POISON: {
        "cost": 173, "damage": 0, "heal": 0, "effect_time": 6, 
        "effect_armor": 0, "effect_damage": 3, "effect_mana": 0
        }, 
    RECHARGE: {
        "cost": 229, "damage": 0, "heal": 0, "effect_time": 5, 
        "effect_armor": 0, "effect_damage": 0, "effect_mana": 101
        }, 
}

# I DON'T CARE ABOUT RUNTIME
cached_fights = {}

class Fight:
    # player_hp = starting player hp
    # player_mana = start player mana
    # boss_hp = 
    def __init__(self, player_hp, player_mana, boss_hp, boss_damage, actions, hardmode, debug=False):
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.actions = actions
        self.effects = []
        self.player_armor = 0
        self.debug = debug
        self.hardmode = hardmode
    
    def fight(self):
        c = self.retrieve_cached_fight()
        if not c:
            self.win = self.play_match()
            self.cache_fight()
        else:
            print("found cached win")

        return self.win


    def cache_fight(self):
        actioninput = tuple(self.actions+[self.hardmode])
        if self.win != 0:
            cached_fights[actioninput] = self.win
            return

        cached_fights[actioninput] = (self.player_hp, self.player_mana, self.player_armor,\
                                       self.boss_hp, self.boss_damage, self.effects)

    # returns true if fight win found, false if more needs to be done
    def retrieve_cached_fight(self):
        for i in range(len(self.actions)-1, -1, -1):
            actioninput = tuple(self.actions[:i+1]+[self.hardmode])
            if actioninput in cached_fights:
                if type(cached_fights[actioninput]) is int:
                    self.win = cached_fights[actioninput]
                    return True
                self.player_hp, self.player_mana, self.player_armor, \
                    self.boss_hp, self.boss_damage, self.effects = cached_fights[actioninput]
                self.actionable_actions = self.actions[i+1:]
                return False
            
        # nothing found. 
        self.actionable_actions = self.actions
        return False

    def prune_effects(self):
        return [(e, t) for (e, t) in self.effects if t > 0]
    
    # returns 0 if nobody wins. 1 if player wins, 2 if boss wins. 
    # I DON'T CARE ABOUT RUNTIME. run thru the whole game, no smartness
    def play_match(self):
        for action in self.actionable_actions:
            if self.debug:
                print("--Player turn--")
                self.print_status()

            self.apply_effects()
            # play the player

            if self.debug:
                print("Player plays", action)

            # no effect stacking:
            if action in [e for (e, t) in self.effects]:
                return -1 # technically, since it's an invalid sequence, player loses. 

            self.player_mana -= actionchoices[action]["cost"]
            self.player_hp += actionchoices[action]["heal"]
            self.boss_hp -= actionchoices[action]["damage"]
            self.effects.append((action, actionchoices[action]["effect_time"]))
            # self.player_armor += actions[action]["effect_armor"]
            # self.boss_hp -= actions[action]["effect_damage"]
            if self.hardmode:
                self.player_hp -= 1

            if self.boss_hp <= 0:
                if self.debug:
                    print("Player wins")
                    self.print_status()
                return 1
            if self.player_mana <= 0:
                if self.debug:
                    print("out of money")
                return -1
            
            if self.debug:
                print("--Boss turn--")
                self.print_status()


            # play the boss 
            self.apply_effects()
            if self.boss_hp <= 0:
                if self.debug:
                    print("Player wins")
                    self.print_status()
                return 1
            
            self.player_hp -= max(1, self.boss_damage - self.player_armor)

            if self.player_hp <= 0 or self.player_mana <= 0:
                if self.debug:
                    print("Boss wins")
                    self.print_status()
                return -1
            
            if self.debug:
                print("")

        if self.debug:
            print("--end fight--")
        return 0
    
    def apply_effects(self):
        new_effects = []
        for effect in self.effects:
            effect_type, effect_timer = effect
            if effect_timer <= 0:
                continue
            if effect_type == SHIELD and effect_timer == actionchoices[SHIELD]["effect_time"]:
                self.player_armor += 7
            elif effect_type == SHIELD and effect_timer == 1:
                self.player_armor -= 7
            elif effect_type in [RECHARGE, POISON]:
                self.player_mana += actionchoices[effect_type]["effect_mana"]
                self.boss_hp -= actionchoices[effect_type]["effect_damage"]
            effect_timer -= 1
            if effect_timer > 0:
                new_effects.append((effect_type, effect_timer))
        self.effects = new_effects
        self.prune_effects()

    def print_status(self):
        print(f"Player HP: {self.player_hp}, Player Mana: {self.player_mana}, Player Armor: {self.player_armor}, \nBoss HP: {self.boss_hp}, Boss Damage: {self.boss_damage}")
        print("Effects:", self.effects)

    def need_to_fight(self):
        if tuple(self.actions) in cached_fights:
            print("seen!", self.actions)
        return not tuple(self.actions) in cached_fights

def get_next_action_sequences(remaining_mana, action_seq):    
    next_action_sequences = []
    for action in actionchoices:
        if actionchoices[action]["cost"] <= remaining_mana :
            next_action_sequences.append(action_seq + [action])

    return next_action_sequences
   
def get_actionseq_cost(action_seq):
    return sum([actionchoices[action]["cost"] for action in action_seq])

def get_best_cost(player_hp, player_mana, boss_hp, boss_damage, hardmode=False):
    best_winning_cost = float('inf')

    actionseq_queue = [[x] for x in actionchoices.keys()][::-1]
    while actionseq_queue:
        a = actionseq_queue.pop()
        cost = get_actionseq_cost(a)
        if cost >= best_winning_cost:
            continue # don't bother executing this fight

        fight = Fight(player_hp, player_mana, boss_hp, boss_damage, a, hardmode)
        if fight.need_to_fight():   
            fight.fight()
        else:
            continue
        if fight.win == 0:
            next_actions = get_next_action_sequences(fight.player_mana, a)
            actionseq_queue += next_actions

        elif fight.win == 1:
            best_winning_cost = min(best_winning_cost, cost)

        elif fight.win == -1:
            continue

        else:
            print("ERROR WITH FIGHT EXECUTION")
            return -1
    return best_winning_cost


def p1(input):
    input = utils.split_and_strip(input)
    boss_hp, boss_damage = [int(x.split(": ")[1]) for x in input]
    player_hp = 50
    player_mana = 500

    return get_best_cost(player_hp, player_mana, boss_hp, boss_damage)

def p2(input):
    input = utils.split_and_strip(input)
    boss_hp, boss_damage = [int(x.split(": ")[1]) for x in input]
    player_hp = 50
    player_mana = 500

    return get_best_cost(player_hp, player_mana, boss_hp, boss_damage, hardmode=True)