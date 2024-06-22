import utils
c = complex # x, y
passcode = ""


directions = [c(0, -1), c(0, 1), c(-1, 0), c(1, 0)]

def moves_to_string(moves):
    if moves is None:
        return ""
    letters = ['U', 'D', 'L', 'R']
    str = ""
    pos = moves[0]
    for i in range(1, len(moves)):
        new_pos = moves[i]
        for d in directions:
            if pos + d == new_pos:
                str += letters[directions.index(d)]
                break
        pos = new_pos
    return str


def get_open_doors(passcode, moves):
    moves = moves_to_string(moves)
    hash = utils.get_md5(passcode+"".join(moves))[:4]

    return [c in 'bcdef' for c in hash]

def is_valid_position(c):
    x, y = c.real, c.imag
    if x < 0 or x > 3 or y < 0 or y > 3:
        return False
    return True

def neighbors_generator(state):
    p, path = state
    doors = get_open_doors(passcode, path)

    next_moves = []
    for i in range(4):
        if doors[i]:
            new_position = p + directions[i]
            if is_valid_position(new_position):
                next_moves.append(new_position)

    return next_moves

def p1(input):
    global passcode
    # states = list of positions

    passcode = input
    path = utils.bfs_return_path(neighbors_generator, c(0, 0), c(3, 3), lambda x, y: False)
    return (moves_to_string(path))


def p2(input):
    global passcode
    # states = list of positions

    passcode = input
    path = utils.longest_path_length(neighbors_generator, c(0, 0), c(3, 3), lambda x, y: False)
    return path