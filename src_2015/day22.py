SHIELD = "shield"
POISON = "poison"
RECHARGE = "recharge"
MAGIC_MISSILE = "magic_missile"
DRAIN = "drain"

class Fight:
    def __init__(self, player_hp, player_mana, boss_hp, boss_damage, actions):
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.actions = actions
        self.effects = []
        self.player_armor = 0

    def play_match(self):


# # data = (player_hp, player_mana, boss_hp, boss_damage, [(effect_type, effect_timer)]
# def play_turn(player_turnchoice, data):
    # deal with effects
#     player_hp, player_mana, boss_hp, boss_damage, effects = data
#     player_armor = 0 # can only get armor thru effects
#     new_effects = []
#     if effects != []:
#         effect_type, effect_timer = effects[0]
#         if effect_timer > 0:
#             if effect_type == SHIELD:
#                 player_armor += 7
#             elif effect_type == RECHARGE:
#                 player_mana += 101
#             elif effect_timer > 0 and effect_type == POISON:
#                 boss_hp -= 3
#                 effect_timer -= 1

#             effect_timer -= 1
#             new_effects.append((effect_type, effect_timer))
    
#     # play the player 
#     if player_turnchoice == MAGIC_MISSILE:
#         player_mana -= 53
#         boss_damage -= 4
#     if player_turnchoice == DRAIN:
#         player_mana -= 73
#         boss_damage -= 2
#         player_hp += 4
#     if player_turnchoice == SHIELD:
#         player_mana -= 113
#         new_effects.append((SHIELD, 6))
#         player_armor += 7
#     if player_turnchoice == POISON:
#         player_mana -= 173
#         new_effects.append((POISON, 6))
#         boss_hp -= 3
#     if player_turnchoice == RECHARGE:
#         player_mana -= 229
#         new_effects.append((RECHARGE, 5))
#         player_mana += 101

#     if boss_hp <= 0:
#         return True
#     if player_mana <= 0:
#         return False

#     # play the boss
#     player_hp -= max(1, boss_damage - player_armor)
#     if player_hp <= 0:
#         return False
#     return (player_hp, player_mana, boss_hp, boss_damage, new_effects)

# def p1(input):
#     boss_hp, boss_damage = [int(x.split(": ")[1]) for x in input]
#     player_hp = 50
#     player_mana = 500
#     effects = []

#     # Some kind of BFS/dijkstra but I don't care enough to try to fit the utils template to it
#     queue = [(player_hp, player_mana, boss_hp, boss_damage, effects), 0]

