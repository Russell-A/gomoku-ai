# import numpy
# from numpy import random
# from numpy import int64
import random

def create_hashboard(hashtable, board, width, height):
    a = 0
    for i in range(width):
        for j in range(height):
            b = board[i][j]
            if b != 0:
                a = a ^ hashtable.table()[b-1][i][j]
    return a

class hash():
    def __init__(self, Width, Height):
        self.Zobrist1 = [[random.randint(0,9223372036854775807) for _ in range(20)] for _ in range(20)]
        self.Zobrist2 = [[random.randint(0,9223372036854775807) for _ in range(20)] for _ in range(20)]


    def table(self):
        return [self.Zobrist1, self.Zobrist2]


if __name__ == '__main__':
    print(hash(3,3).table())