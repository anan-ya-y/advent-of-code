import utils, re
def p1(input):
    return 213

def p2(input):
    all_sues = {}
    for line in utils.split_and_strip(input):
        suenum = re.findall(r"Sue (\d+): ", line)[0]
        def getstat(stat):
            children = re.findall(f"{stat}: (\d+)", line)
            if children != []:
                return int(children[0])
            return -1
        all_sues[suenum] = {
            "children": getstat("children"),
            "cats": getstat("cats"),
            "samoyeds": getstat("samoyeds"),
            "pomeranians": getstat("pomeranians"),
            "akitas": getstat("akitas"),
            "vizslas": getstat("vizslas"),
            "goldfish": getstat("goldfish"),
            "trees": getstat("trees"),
            "cars": getstat("cars"),
            "perfumes": getstat("perfumes")
        }

    for suenum in all_sues:
        c = all_sues[suenum]
        if c["children"] in [-1, 3] and \
            c["samoyeds"] in [-1, 2] and \
            c["akitas"] in [-1, 0] and \
            c["vizslas"] in [-1, 0] and \
            c["cars"] in [-1, 2] and \
            c["perfumes"] in [-1, 1] and \
            (c["cats"] == -1 or c["cats"] >= 7) and \
            (c["goldfish"] == -1 or c["goldfish"] <= 5) and \
            (c["trees"] == -1 or c["trees"] >= 3) and \
            (c["pomeranians"] == -1 or c["pomeranians"] <= 3):
            print(suenum, c)
            


