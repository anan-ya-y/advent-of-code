import utils
from itertools import permutations

def check_rule(page, rules_dict):
    for i in range(len(page)):
        entry = page[i]
        if entry not in rules_dict:
            continue
        # check that none of the pages that have to be after entry are before entry
        before_entry = set(page[:i])
        after_rules = set(rules_dict[entry])
        # print(f"Entry: {entry}, Before: {before_entry}, Allowed: {after_rules}")
        if len(before_entry.intersection(after_rules)) != 0:
            return False
    return True

def get_corrected_rule(page, rule_dict):
    for i in range(len(page)):
        entry = page[i]
        if entry not in rule_dict:
            continue
        before_entry = set(page[:i])
        after_rules = set(rule_dict[entry])
        if len(before_entry.intersection(after_rules)) > 0:
            # swap the entry. 
            other = list(before_entry.intersection(after_rules))[0]
            val = page[i]
            new_pagei_index = page.index(other)
            page[i] = other
            page[new_pagei_index] = val
            return get_corrected_rule(page, rule_dict)

    return page


def main(input):
    rules, pages = utils.split_and_strip(input, '\n\n')
    rules = utils.split_and_strip(rules)
    rules_dict = {}
    for rule in rules:
        rule = list(map(int, rule.split("|")))
        if rule[0] not in rules_dict:
            rules_dict[rule[0]] = []
        rules_dict[rule[0]].append(rule[1])
    pages = [list(map(int, line.split(","))) for line in utils.split_and_strip(pages)]

    allowed_rules = [x for x in pages if check_rule(x, rules_dict)]
    p1 = 0
    p2 = 0
    for page in pages:
        if check_rule(page, rules_dict):
            p1 += page[int(len(page)/2)]
        else:
            new_rule = get_corrected_rule(page, rules_dict)
            p2 += new_rule[int(len(new_rule)/2)]

    
    return p1, p2