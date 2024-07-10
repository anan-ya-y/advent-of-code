import utils
import numpy as np

class Board:
    def __init__(self, boardstr):
        rows = boardstr.split("\n")
        rows = [list(map(int, row.split())) for row in rows]
        self.board = np.array(rows)
        self.board_seen = np.zeros(self.board.shape).astype(np.bool_)
        self.boardnums = set(self.board.reshape(-1))

    def perform(self, number):
        if self.winning():
            return
        if number not in self.boardnums:
            return
        self.board_seen[np.where(self.board == number)] = True

    def winning(self):
        # rows
        for row in self.board_seen:
            if all(row):
                return True
        # columns
        for col in self.board_seen.T:
            if all(col):
                return True
        
        return False
    
    def score(self):
        n = np.logical_not(self.board_seen)
        return np.sum(self.board[n].reshape(-1))

def main(input):
    input = utils.split_and_strip(input, "\n\n")

    numbers = list(map(int, input[0].split(",")))
    boards = [Board(board) for board in input[1:]]
    nboards_winning = 0


    p1, p2 = 0, 0
    for number in numbers:
        if p1 and p2:
            break
        for board in boards:
            board.perform(number)
            if not p1 and board.winning():
                p1 = number * board.score()
            nboards_winning = sum([board.winning() for board in boards])
            if nboards_winning == len(boards) and not p2:
                p2 = number * board.score()            

    return p1, p2
            