#!/usr/bin/python3

from collections import namedtuple
import random as rand
import mpi4py

# location = collections.namedtuple('Point', ['x', 'y'])
# LocationOfItem = location(0, 0)
# print(location)

rand.seed()

class Board(object):
    """
    Holds and manages board data

    Legend:
        #   -   Wall
        %   -   Bee
        &   -   Hive
        *   -   Food
    """

    dimensions = namedtuple('BoardDimensions', 'x y')
    point = namedtuple('Point', 'x y')


    def get_point(self):
        """   Generates a new random point within the boundary   """

        x = rand.randrange(1, self.dimension.x - 2)
        y = rand.randrange(1, self.dimension.y - 2)
        return Board.point(x, y)


    def new_point(self):
        """   Generates a new random point within the boundary   """

        while True:
            x = rand.randrange(1, self.dimension.x - 2)
            y = rand.randrange(1, self.dimension.y - 2)
            if self.board[y][x] != '#':
                return Board.point(x, y)


    def generate_wall(self):
        """   Creates random walls   """

        resolution_x = rand.randint(9, 17)
        resolution_y = rand.randint(5, 11)

        start = self.get_point()

        for i in range(resolution_y):
            for j in range(resolution_x):
                if start.y + i >= self.dimension.y:
                    continue
                if start.x + j >= self.dimension.x:
                    continue
                self.board[start.y + i][start.x + j] = '#'


    def __init__(self):
        """   Sets up a board with dimensions: SIZE_X x SIZE_Y   """

        # Instantiate board with given dimensions
        self.dimension = Board.dimensions(x=80, y=30)
        self.board = [[' ' for j in range(self.dimension.x)] for i in range(self.dimension.y)]

        # Generate boundary
        for i, column in enumerate(self.board):
            for j, _ in enumerate(column):
                if i == 0 or i == (self.dimension.y - 1):
                    self.board[i][j] = '#'
                elif j == 0 or j == (self.dimension.x - 1):
                    self.board[i][j] = '#'

        # Generate walls
        for i in range(rand.randint(7, 10)):
            self.generate_wall()

        # Generate hive
        pnt = self.new_point()
        self.board[pnt.y][pnt.x] = '&'


    def __str__(self):
        """   Prints out the board   """

        output = ''
        for column in self.board:
            for row in column:
                output = output + str(row)
            output = output + '\n'
        return output

class Bee(object):
    """   Bee   """

    location = namedtuple('Point', 'x y')

    def __init__(self, x, y):
        self.pos = Bee.location(x, y)


MY_BOARD = Board()
print(MY_BOARD)
