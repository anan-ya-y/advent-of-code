import utils
import re

def getmaps(lines):
    seeds = []
    seed_soil = []
    soil_fertilizer = []
    fertilizer_water = []
    water_light = []
    light_temp = []
    temp_humid = []
    humid_loc = []

    def get_lines(lines, start):
        i = start
        while i < len(lines) and lines[i] != "":
            i += 1
        l = lines[start:i] # the actual content

        # string cleanup
        l = [x.split(" ") for x in l]
        l = [[int(k) for k in x] for x in l]
        return l

    for i in range(len(lines)): # chatgpt wrote the next few lines. 
        line = lines[i]
        if line.__contains__("seeds"):
            seeds = re.findall(r"(\d+)", line)
            seeds = [int(s) for s in seeds]

        if line.__contains__("seed-to-soil map:"):
            i += 1
            seed_soil = get_lines(lines, i)
        
        if line.__contains__("soil-to-fertilizer map:"):
            i += 1
            soil_fertilizer = get_lines(lines, i)
        
        if line.__contains__("fertilizer-to-water map:"):
            i += 1
            fertilizer_water = get_lines(lines, i)

        if line.__contains__("water-to-light map:"):
            i += 1
            water_light = get_lines(lines, i)
        
        if line.__contains__("light-to-temperature map:"):
            i += 1
            light_temp = get_lines(lines, i)

        if line.__contains__("temperature-to-humidity map:"):
            i += 1
            temp_humid = get_lines(lines, i)

        if line.__contains__("humidity-to-location map:"):
            i += 1
            humid_loc = get_lines(lines, i)

        i += 1
        
    return seeds, [seed_soil, soil_fertilizer, fertilizer_water, \
        water_light, light_temp, temp_humid, humid_loc]

def get_loc_from_seed(seed, maps):
    x = seed
    for i in range(7):
        x = get_dest(maps[i], x)
    return x

def get_dest(map, input):
    for i in range(len(map)):
        dest_start, src_start, range_len = map[i]
        if input < src_start or input >= src_start+range_len:
            continue
    
        return dest_start + (input-src_start)
    
    return input

def get_best_loc(seeds, maps):
    best_loc = None
    for s in seeds:
        loc = get_loc_from_seed(s, maps)
        if best_loc is None:
            best_loc = loc
        if loc < best_loc:
            best_loc = loc
    return best_loc

def get_best_loc_binsearch(seed_min, seed_max, maps):
    # base cases
    if seed_min > seed_max:
        print("oh no")
        return None
    if abs(seed_min-seed_max) <= 15:
        # brute force
        # print(seed_min, seed_max, "brute force")
        return get_best_loc(range(seed_min, seed_max+1), maps)

    # 1/n of the range at a time. 
    n = 2
    chosenseeds = list(range(seed_min, seed_max, max(1, (seed_max-seed_min)//n))) 
    chosenseeds += [seed_max]

    best_loc = None
    for i in range(len(chosenseeds)-1):
        startseed = chosenseeds[i]
        endseed = chosenseeds[i+1]
        startloc = get_loc_from_seed(startseed, maps)
        endloc = get_loc_from_seed(endseed, maps)
        if startloc-endloc != startseed-endseed:
            interval_bestloc = get_best_loc_binsearch(startseed, endseed, maps)
            best_loc = min(startloc, endloc, interval_bestloc)
        elif best_loc is None or best_loc > min(startloc, endloc): # no map boundaries
            best_loc = min(startloc, endloc)
            
    return best_loc

# p2 amswer: 99751240


def p1(input):
    lines = utils.split_and_strip(input)
    seeds, maps = getmaps(lines)
    best_loc = get_best_loc(seeds, maps)
    return (best_loc)

def p2(input):
    lines = utils.split_and_strip(input)
    seedpairs, maps = getmaps(lines)
    seedpairs = seedpairs

    best_loc = None
    for i in range(0, len(seedpairs), 2):
        start = seedpairs[i]
        length = seedpairs[i+1]
        seeds = range(start, start+length)
        # loc = get_best_loc(seeds, maps)

        loc = get_best_loc_binsearch(start, start+length, maps)
        if best_loc is None or loc < best_loc:
            best_loc = loc

    return (best_loc)

    

p1("inputs/5.real.txt")
p2("inputs/5.real.txt")
