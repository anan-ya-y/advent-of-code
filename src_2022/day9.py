import utils

C = complex
possible_directions = [C(-1, -1), C(-1, 0), C(-1, 1), 
                         C(0, -1), C(0, 0), C(0, 1),
                         C(1, -1), C(1, 0), C(1, 1)]

direction_vectors = {
    "R": C(0, 1), 
    "L": C(0, -1), 
    "U": C(-1, 0), 
    "D": C(1, 0)
}

def find_best_tail_location(head, tail):
    if abs(head-tail) <= abs(C(1, 1)):
        return tail
    best_position = None
    best_distance = None
    for d in possible_directions:
        position = tail + d
        distance = abs(head - position)
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_position = position
    return best_position

def p1(input):
    lines = utils.split_and_strip(input)
    moves = [l.split(" ") for l in lines]
    moves = [(r, int(t)) for r, t in moves]

    head = C(0, 0)
    tail = C(0, 0)
    tail_positions = []

    for move in moves:
        dir, dist = move
        # print(move)
        for _ in range(dist):
            # print(head, tail)
            head += direction_vectors[dir]
            tail = find_best_tail_location(head, tail)
            tail_positions.append(tail)
            # print(head, tail)
    return len(set(tail_positions))

def p2(input):
    lines = utils.split_and_strip(input)
    moves = [l.split(" ") for l in lines]
    moves = [(r, int(t)) for r, t in moves]

    tail_positions = []
    rope = [C(0, 0)]*10

    for move in moves:
        dir, dist = move
        # print(move)
        for _ in range(dist):
            # print(head, tail)
            rope[0] += direction_vectors[dir]
            for i in range(1, len(rope)):
                rope[i] = find_best_tail_location(rope[i-1], rope[i])
            tail_positions.append(rope[-1])
            # print(head, tail)
    return len(set(tail_positions))
