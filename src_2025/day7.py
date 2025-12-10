import utils

def add_to_dict(d, key, value):
    if key not in d:
        d[key] = 0
    d[key] += value

def main(input):
    input = utils.split_and_strip(input)
    tachyons = {input[0].index("S"): 1}
    p1 = 0
    for line in input[1:]:
        new_tachyons = {}
        for t in tachyons:
            if line[t] == "^":
                p1 += 1
                add_to_dict(new_tachyons, t - 1, tachyons[t])
                add_to_dict(new_tachyons, t + 1, tachyons[t])
            else:
                add_to_dict(new_tachyons, t, tachyons[t])

        tachyons = new_tachyons

    return p1, sum(tachyons.values())
