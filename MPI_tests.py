
from mpi4py import MPI
from objects import Bee, Board
import random as rand
import sys

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
info = MPI.Status()
comm = MPI.COMM_WORLD

'''    MPI TESTS   '''

def hello():
    # Hello World example
    sys.stdout.write(
        "Hello, World! I am process %d of %d on %s.\n"
        % (rank, size, name))

def nonblocking():
    # Non-Blocking isend/irecv example
    if rank == 0:
        for i in range(1, size):
            num = rand.randint(0, 10)
            req = comm.isend(num, dest=i, tag=1)
            print("Node {} sending".format(rank))
            req.wait()
            print("Node {} sent: {}".format(rank, num))

    else:
        req = comm.irecv(tag=1)
        print("Node {} requesting...".format(rank))
        data = req.wait()
        print("Node {} received: {}".format(rank, data))

def blocking():
    # Blocking send/recv example
    if rank == 0:
        num = rand.randint(1,100)
        for i in range(1,size):
            req = comm.ssend(num, dest=i, tag=1) # returns a Request object, which can call Wait and Test
            print("Node {} sent: {}".format(rank, num))
    else:
        data = comm.recv(source=0, tag=1)
        print("Node {} received: {}".format(rank, data))
    
def broadcast():
    # Broadcasting example
    if rank == 0:
        data = ['this', 'is', 'a', 'test']
    else:
        data = None
    
    data = comm.bcast(data, root=0)
    print("Node {} has data: {}".format(rank, data))

def scatter():
    # Scatter example
    if rank == 0:
        data = [rand.randint(1,100) for _ in range(size)]
        print("Node 0 is scattering... {}".format(data))
    else:
        data = None

    data = comm.scatter(data, root=0)
    print("Node {} received: {}".format(rank, data))

def gather():
    # [Scatter and] Gather example
    if rank == 0:
        data = [rand.randint(1,100) for _ in range(size)]
        print("Node 0 is scattering... {}".format(data))
    else:
        data = None
    
    data = comm.scatter(data, root=0)
    print("Node {} received: {} and processing...".format(rank, data))
    new_data = data*3

    result = comm.gather(new_data, root=0)
    if rank == 0:
        print("Result: {}".format(result))
