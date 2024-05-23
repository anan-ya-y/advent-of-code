import re, utils

def read_input(input):
    input = utils.split_and_strip(input)
    distances = {}
    for line in input:
        r = re.findall(r'(\w+) to (\w+) = (\d+)', line)[0]
        distances[(r[0], r[1])] = int(r[2])
        distances[(r[1], r[0])] = int(r[2])

    return distances

# shortest distance to visit all cities, given the first city we visited
def calculate_distances(cities_to_visit, first_city, distances, part=1):
    assert first_city not in cities_to_visit
    if len(cities_to_visit) == 1:
        return distances[first_city, list(cities_to_visit)[0]]
    
    dist = float('inf') if part == 1 else 0
    for city in cities_to_visit:
        remaining_cities = cities_to_visit - {city}
        remaining_distances = calculate_distances(remaining_cities, city, distances, part=part)
        current_dist = distances[(first_city, city)] + remaining_distances
        if part == 1:
            dist = min(dist, current_dist)
        else:
            dist = max(dist, current_dist)

    return dist


def p1(input):
    distances = read_input(input)
    cities = set([city for city, _ in distances.keys()])

    return min(map(lambda x: calculate_distances(cities - {x}, x, distances, part=1), cities))

def p2(input):
    distances = read_input(input)
    cities = set([city for city, _ in distances.keys()])

    return max(map(lambda x: calculate_distances(cities - {x}, x, distances, part=2), cities))

