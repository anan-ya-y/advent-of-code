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

def getHeight(tetris):
    if len(tetris) == 0:
        return 0
    return int(max([t.imag for t in tetris]))

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
    for i in range(length):
        piece = PIECES[i % len(PIECES)]
        # shift piece into correct position
        piece = set([p + C(3, getHeight(tetris)+4) for p in piece])
        # printTetris(tetris, piece)

        stuck = False
        while not stuck:
            dir = input[inputindex % len(input)]
            inputindex += 1
            piece = movePiece(piece, dir, tetris)
            down_piece = movePiece(piece, "v", tetris)
            if down_piece == piece:
                stuck = True
                tetris = tetris.union(piece)
                # printTetris(tetris, set())
            piece = down_piece

    return getHeight(tetris)

def p1(input):
    return simulate(input, 2022)

def p2(input):
    return simulate(input, 1000000000000)


