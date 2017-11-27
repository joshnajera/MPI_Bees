#!/usr/bin/python3
"""
Parallel Hello World
"""

from mpi4py import MPI
from objects import Bee, Board
from collections import namedtuple
import random as rand
from os import system
import sys
from time import sleep

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
info = MPI.Status()
comm = MPI.COMM_WORLD

BoardDimensions = namedtuple('BoardDimensions', 'x y')
Node = namedtuple('Node', 'location parent g h weight')
Point = namedtuple('Point', 'x y')

# lower-cased   send,recv,isend,irecv correlate with generic python data objects
# uper-cased    Send,Recv,Isend,Irecv correlate with buffered like data objects


def bee_test():

    print('{}/{} starting'.format(rank, size))
    board = None
    pos = None

    if rank == 0:
        root = Root()
        # Generate a random board 
        board = comm.bcast(root.board, root=0)
        # Send other nodes their locations
        pos = comm.scatter(root.Bees, root=0)
        print("Everything initiated")

        while True:
            # Update everyone and ask them what they wants
            sleep(.25)
            print(root)
            new_board = comm.bcast(board, root=0)
            requests = comm.gather(root=0)
            for i, request in enumerate(requests): 

                # Skips if there is no request (i.e. Root makes no requests but still needs to pass something into gather?)
                if not request:
                    continue


                # Currently assuming request is a tuple of (Request Type, Argument)
                if request[0] == 'Move':
                    print('{} wants to move to {}'.format(i, request[1]))

                    # CAN REMOVE-- Check if that spot is clear
                    if not root.is_clear(request[1]):
                        comm.send(False, dest=i, tag=1)
                        continue

                    # Update the position of the bee
                    root.move_to(root.Bees[i], request[1])
                    root.Bees[i] = request[1]
                    # Respond to the node telling it the movement was successful
                    comm.send(True, dest=i, tag=1)
                    continue
                
        # While True
            # Display board
            # Broadcast board
            # Ask everyone for info
            # if a movement request:
                # check if new position is valid: 
                    # update it, and return Success/Failure
            # if other request???: process it
            # apply updates


    else:
        # Get board and positional info
        board = comm.bcast(board, root=0)
        pos = comm.scatter(pos, root=0)
        # Instantiate self with board and position
        me = Worker(board, pos)
        print("Node {}:\tReceived {}".format(rank, pos))


        while(True):
            # Get most updated board
            new_board = comm.bcast(board, root=0)
            me.board = new_board

            # TODO:Check if near food

            if me.mode == 'wandering':
                # TODO:This function currently not working... having an issue with the named tuple & MPI?
                new_pos = me.rand_pos()

                if not new_pos:
                    request = comm.gather(None, root=0)
                    continue

                request = comm.gather(('Move', new_pos), root=0)
                result = comm.recv(source=0,tag=1)
                # Update root with desired pos, get back success or fail

                if not result:
                # Couldn't move
                    continue

                # Could move
                me.pos = new_pos


            if me.mode == 'navigating':
                # me.navigate()
                pass


        # me.process_request(node=0, tag_ = 1)


class Root(Board):

    def __init__(self):
        Board.__init__(self)

        for i in range(1, size):
            self.add_bee()
    
    def is_clear(self, point):
        if self.check_point(point) == ' ':
            return True
        else:
            return False

    # make_request and process_request currently unused
    def make_request(self, desired_info, node, tag_ = 1):
        '''   Requests info from another node, and waits for a response   '''
        comm.ssend(desired_info, dest=node, tag=tag_)
        resp = comm.recv(source=node, tag = tag_)
        return resp

    def process_request(self, node=0, tag_ = 1):
        '''   Waits for and processes one request
        request: ('action', 'args')'''
        request, args = comm.recv(source=node, tag = tag_)

        if request[0] == 'move':
            if self.check_point(args) == ' ':
                comm.ssend(True, dest=node, tag = tag_)
            else:
                comm.ssend(False, dest=node, tag = tag_)
                

class Worker(Bee):

    def __init__(self, board, pos):
        Bee.__init__(self, board, pos)
        self.mode = 'wandering'    # Wandering, Gathering

    # make_request and process_request currently unused
    def make_request(self, info, node = 0, tag_ = 1):
        '''   Waits for and processes one request   '''
        comm.ssend(info, dest=node)
        return comm.recv(source=node, tag = tag_)

    def process_request(self, node=0, tag_ = 1):
        '''   Requests info from another node, and waits for a response   '''
        request = comm.recv(source=node, tag = tag_)
        if request == 'pos':
            comm.ssend(self.pos, dest=node, tag = tag_)


if __name__ == '__main__':
    bee_test()
