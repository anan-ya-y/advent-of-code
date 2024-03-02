import utils
C = complex

# Okay, this is tetris. 
PIECES = [
    set([C(0, 0), C(1, 0), C(2, 0), C(3, 0)]),
    set([C(1, 0), C(0, 1), C(1, 1), C(2, 1), C(1, 2)]),
    set([C(0, 0), C(1, 0), C(2, 0), C(2, 1), C(2, 2)]),
    set([C(0, 0), C(0, 1), C(0, 2), C(0, 3)]),
    set([C(0, 0), C(0, 1), C(1, 0), C(1, 1)])
]

def movePiece(piece, direction, tetris):
    if direction == ">":
        dir = C(1, 0)
    elif direction == "<":
        dir = C(-1, 0)
    elif direction == "v":
        dir = C(0, -1)
    else:
        return piece # invalid instruction.

    new_piece = set([p + dir for p in piece])
    if len(new_piece.intersection(tetris)) > 0:
        return piece # piece can't be moved. 
    if any(p.real <= 0 or p.real >= 8 for p in new_piece):
        return piece # piece is out of bounds.
    if any(p.imag <= 0 for p in new_piece):
        return piece # piece is out of bounds.
    return new_piece

def printTetris(tetris, piece):
    # top to bottom
    height = int(max([t.imag for t in tetris.union(piece)]))
    for y in range(height, 0, -1):
        line = "|"
        for x in range(1, 8):
            if C(x, y) in tetris:
                line += "#"
            elif C(x, y) in piece:
                line += "@"
            else:
                line += "."
        print(line+"|")
    print("+" + "-" * 8 + "+")


def simulate(input, length):
    inputindex = 0
    tetris = set()
    height = 0
    historical_height = []
    cycle_start = None
    for i in range(length):
        historical_height.append(height)
        piece = PIECES[i % len(PIECES)]
        # shift piece into correct position
        piece = set([p + C(3, height+4) for p in piece])

        stuck = False
        while not stuck:
            dir = input[inputindex % len(input)]
            inputindex += 1
            piece = movePiece(piece, dir, tetris)
            down_piece = movePiece(piece, "v", tetris)
            if down_piece == piece:
                stuck = True
                tetris = tetris.union(piece)
            piece = down_piece
            
        height = max(height, max([p.imag for p in tetris]))
        # printTetris(tetris, piece)

        # UPDATE HEIGHT
        height = max(height, max([p.imag for p in tetris]))
        
        # print top row
        toprow = [p for p in tetris if p.imag == height]
        if len(toprow) == 7: # we have found a cycle! 
            # print(toprow)
            if cycle_start is None:
                cycle_start = i
            elif (cycle_start % len(PIECES)) == (i % len(PIECES)):
                cycle_length = i - cycle_start
                cycle_height = height - historical_height[cycle_start]
                ncycles = (length - cycle_start) // cycle_length 
                height = (cycle_height * ncycles) + \
                    historical_height[length - (ncycles * cycle_length)]
                return height


    return height

def p1(input):
    return simulate(input, 2022)

def p2(input):
    return simulate(input, 1000000000000)
    return 1


