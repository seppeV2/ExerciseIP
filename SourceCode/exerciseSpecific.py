import pathlib
import numpy as np
from SourceCode.ownFunctions import getODGraph
from dyntapy.assignments import StaticAssignment
from SourceCode.greenTimes import get_green_times
from SourceCode.ownFunctions import getODGraph
from SourceCode.main import main

def load_demand(method: str, demands: list):
    if method == 'y-network':
        [d_L0, d_L1] = demands
        matrix = np.zeros([4,4])
        matrix[0,3] = d_L0
        matrix[1,3] = d_L1
        ODMatrix_location = str(pathlib.Path(__file__).parent)+'/data/Y-network-demand.csv'
        np.savetxt(ODMatrix_location, matrix, delimiter=",")


def assign(method: str, g, centroids):
    initial_greens = {0: 0.5, 1: 0.5 , 2: 0}
    odGraph = getODGraph(str(pathlib.Path(__file__).parent)+'/data/Y-network-demand.csv', centroids)
    assignment = StaticAssignment(g, odGraph)
    result = assignment.run('msa')
    ff_tt = assignment.internal_network.links.length / assignment.internal_network.links.free_speed
    greens,_, _ = get_green_times(assignment.internal_network.links.capacity,result.flows,assignment, method, initial_greens, g, ff_tt)
    return result.flows, greens

def assign_simple(demand, methodGreen, methodCost = 'bpr'):
    _,flows = main(demand, methodCost, methodGreen)
    return flows
