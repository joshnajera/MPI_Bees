#!/usr/bin/python3

from collections import namedtuple
from time import sleep
from os import system
from copy import deepcopy
import random as rand
import mpi4py
import math


rand.seed()

BoardDimensions = namedtuple('BoardDimensions', 'x y')
Node = namedtuple('Node', 'location parent g h weight')
Point = namedtuple('Point', 'x y')

class Board(object):
    """
    Holds and manages board data

    Legend:
        #   -   Wall
        %   -   Bee
        &   -   Hive
        *   -   Food
    """

    Bees = [None]

    def __init__(self):
        """   Sets up a board with dimensions: SIZE_X x SIZE_Y   """

        # Instantiate board with given dimensions
        self.dimension = BoardDimensions(x=60, y=30)
        self.board = self.blank_map(self.dimension)

        # Generate walls  -- TODO Validation of map after generation
        for _ in range(rand.randint(9, 12)):
            self.generate_wall()

        # Generate 'hive'
        goal_pnt = self.new_point()
        self.board[goal_pnt.y][goal_pnt.x] = '&'


    def add_bee(self):
        pos = self.new_point()
        Board.Bees.append(pos)
        self.board[pos.y][pos.x] = '%'
        return pos


    def __str__(self):
        """   Prints out the board   """

        output = ''
        for column in self.board:
            for row in column:
                output = output + str(row)
            output = output + '\n'
        return output


    def move_to(self, old_pos, new_pos):
        """   Moves a bee to a new location   """

        self.board[old_pos.y][old_pos.x] = ' '
        self.board[new_pos.y][new_pos.x] = '%'


    def check_point(self, pnt):
        """   Gets what is currently at a given position   """

        return self.board[pnt.y][pnt.x]


    def get_point(self):
        """   Generates a new random point within the boundary   """

        x = rand.randrange(1, self.dimension.x - 2)
        y = rand.randrange(1, self.dimension.y - 2)
        return Point(x, y)


    def new_point(self):
        """   Generates a random empty point within the boundary   """

        while True:
            x = rand.randrange(1, self.dimension.x - 2)
            y = rand.randrange(1, self.dimension.y - 2)
            if self.board[y][x] == ' ':
                return Point(x, y)


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


    def blank_map(self, size=BoardDimensions(0, 0)):
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

    def __init__(self, board, point):
        self.board = board
        self.pos = point


    def rand_pos(self):
        """   Randomly select open neighboring space   """

        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        while True:
            choice = rand.choice(directions)
            dx, dy = choice
            next_x = self.pos.x + dx
            next_y = self.pos.y + dy

            result = self.check_point(Point(next_x, next_y))
            if result == ' ':
                return Point(next_x, next_y)
            else: 
                directions.remove(choice)
                if not directions:
                    return False


    def wander(self):
        """   Wander around aimlessly   """

        while True:
            system('cls')
            new_pos = self.rand_pos()
            self.board.move_to(self.pos, new_pos)
            self.pos = new_pos
            print(self.board)
            sleep(.1)


    def navigate(self, goal_pnt):
        """   Navigates Bee to desired point   """

        nav = Navigator(self.board.board, self.pos, goal_pnt)
        result = nav.astar()
        for item in result:
            system('cls')
            new_pos = item
            self.board.move_to(self.pos, new_pos)
            self.pos=new_pos
            print(self.board)
            sleep(.03)
        print("Done")

    def check_point(self, pnt):
        """   Gets what is currently at a given position   """

        return self.board[pnt.y][pnt.x]


class Navigator(object):
    """   Manages A* navigation   """

    # heuristic = namedtuple('Heuristics', 'g h sum')
    # G     = Distance from current position
    # H     = Distance to destination
    # SUM   = H + G


    @staticmethod
    def get_key(node):
        """   Gets key value to 'sort' the nodes by weight   """

        return node.weight


    @staticmethod
    def distance(start=Point(0, 0), dest=Point(0, 0)):
        """   Returns a rounded, and weighted distance beteen two points   """

        result = math.sqrt(math.pow(start.x - dest.x, 2) + math.pow(start.y - dest.y, 2))
        return int(result*10)


    def __init__(self, board_array, start, dest):
        """   Initializes with a copy of the board   """

        # Deep copy so we don't touch Board's
        self.board = deepcopy(board_array)
        self.start = start
        self.dest = dest
        self.closed = []
        self.path = {}
        self.open = []

        # Initiate algorithm with start point
        self.origin = self.make_node(start, start)
        self.open.append(self.origin)


    def make_node(self, point, parent):
        """   Makes a node out of given data   """

        # G Heuristic = distance from start to point
        g_heur = Navigator.distance(point, parent)
        # H Heuristic = distance from point to destination
        h_heur = Navigator.distance(point, self.dest)

        return Node(point, parent, g_heur, h_heur, g_heur+h_heur)


    def calculate_path(self):
        """   Reverses the path and calculates shortest path   """
        prior_point = self.path[self.dest]
        full_path = [self.dest]

        while prior_point != self.start:
            full_path.insert(0, prior_point)
            prior_point = self.path[prior_point]
        self.path = full_path


    def astar(self):
        """   Performs a-star navigation   """

        try:
            next_node = self.open.pop(0)
        except IndexError:
            print("No path found!")
            exit()

        if next_node.location != self.start:
            self.closed.append(next_node)
            self.path[next_node.location] = next_node.parent

        self.board[next_node.location.y][next_node.location.x] = 'X'
        if next_node.location.x == self.dest.x and next_node.location.y == self.dest.y:
            print("FOUND")
            self.calculate_path()
            return self.path
        self.expand(next_node.location)

        return self.astar()


    def expand(self, pnt):
        """   Expands / updates neighbors   """

        # Check all neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):

                x = pnt.x + j
                y = pnt.y + i

                point = self.board[y][x]
                if point in {'#', '%', 'X'}:
                    continue
                new_node = self.make_node(Point(x, y), pnt)
                if point == 'O':
                    for node in self.open:
                        if node.location.x == x and node.location.y == y:
                            if new_node.weight < node.weight:
                                self.open.remove(node)
                                self.open.append(new_node)
                    continue
                self.board[y][x] = 'O'


                self.open.append(new_node)
        self.open.sort(key=Navigator.get_key)