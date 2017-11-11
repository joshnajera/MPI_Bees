#!/usr/bin/python3

from collections import namedtuple
from time import sleep
from os import system
from copy import deepcopy
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


    def __init__(self):
        """   Sets up a board with dimensions: SIZE_X x SIZE_Y   """

        # Instantiate board with given dimensions
        self.dimension = Board.dimensions(x=40, y=30)
        self.board = self.blank_map(self.dimension)

        # Generate walls  -- TODO Validation of map after generation
        for _ in range(rand.randint(7, 10)):
            self.generate_wall()

        # Generate 'hive'
        pnt = self.new_point()
        self.board[pnt.y][pnt.x] = '&'

        # Generate 'Bee'
        pnt = self.new_point()
        self.board[pnt.y][pnt.x] = '%'
        print(pnt)
        bee1 = Bee(self, pnt)
        # bee1.wander()
        bee1.navigate()


    def __str__(self):
        """   Prints out the board   """

        output = ''
        for column in self.board:
            for row in column:
                output = output + str(row)
            output = output + '\n'
        return output


    def move_to(self, old_pos=point(0, 0), new_pos=point(0, 0)):
        """   Moves a bee to a new location   """

        self.board[old_pos.y][old_pos.x] = ' '
        self.board[new_pos.y][new_pos.x] = '%'


    def check_point(self, pnt=point(0, 0)):
        """   Gets what is currently at a given position   """

        return self.board[pnt.y][pnt.x]


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


    def blank_map(self, size=dimensions(0, 0)):
        """   Generates a blank map with boarders   """
        board = [[' ' for j in range(size.x)] for i in range(size.y)]
        # Generate boundary
        for i, column in enumerate(board):
            for j, _ in enumerate(column):
                if i == 0 or i == (size.y - 1):
                    board[i][j] = '#'
                elif j == 0 or j == (size.x - 1):
                    board[i][j] = '#'
        return board



class Bee(object):
    """   Bee   """


    location = namedtuple('Point', 'x y')

    def __init__(self, board, point=location(0, 0)):
        self.board = board
        self.pos = point

    def rand_pos(self):
        directions = ['L', 'R', 'U', 'D']
        while True:
            dir = directions[rand.randint(0, len(directions) - 1)]
            if dir == 'L':
                next_x = -1
                next_y = 0
            elif dir == 'R':
                next_x = 1
                next_y = 0
            elif dir == 'U':
                next_x = 0
                next_y = -1
            elif dir == 'D':
                next_x = 0
                next_y = 1
            next_x = next_x + self.pos.x
            next_y = next_y + self.pos.y
            result = self.board.check_point( Bee.location(next_x, next_y) )
            if result == ' ':
                print("Going %s"%(dir))
                return( Bee.location(next_x, next_y) )
            else:
                print("Failed going %s"%(dir))
                directions.remove(dir)

    def wander(self):
        while True:
            system('cls')
            new_pos = self.rand_pos()
            self.board.move_to(self.pos, new_pos)
            self.pos = new_pos
            print(self.board)
            sleep(.1)

    def navigate(self):
        nav = Navigator(self.board.board)

class Navigator(object):
    """   Manages A* navigation   """

    # G     = Distance from current position
    # H     = Distance to destination
    # SUM   = H + G
    heuristic = namedtuple('Heuristics', 'g h sum')
    location = namedtuple('Point', 'x y')
    node = namedtuple('Node', 'location heuristic')

    def __init__(self, board_array):
        """   Initializes with a copy of the board   """

        self.board = deepcopy(board_array)
        self.closed = []
        self.open = []

        # for row in self.board:
        #     for column in row:
        #         print(column, end='')
        #     print()


    def astar(self, start=location(0, 0), dest=location(0, 0)):
        """   Performs a-star navigation   """

        pass

    def expand(self, pnt=location(0, 0)):
        """   Expands / updates neighbors   """

        pass


MY_BOARD = Board()
print(MY_BOARD)
