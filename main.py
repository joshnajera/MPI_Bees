#!/usr/bin/python3
import mpi4py
import collections

class Board:
    """   Holds and manages board data   """

    def __init__(self):
        self.SIZE_X = 5
        self.SIZE_Y = 10
        self.board = [[[0] for i in range(self.SIZE_X)] for i in range(self.SIZE_Y)]

    def __str__(self):
        """   Prints out the board   """
        output=''
        for column in self.board:
            for row in column:
                output = output + str(row)
            output = output + '\n'
        return output


my_board = Board()
print(my_board)

# location = collections.namedtuple('Point', ['x', 'y'])
# LocationOfItem = location(0, 0)
# print(location)