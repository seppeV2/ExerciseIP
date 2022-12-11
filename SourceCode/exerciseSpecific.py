import pathlib
import numpy as np
from SourceCode.ownFunctions import getODGraph
from dyntapy.assignments import StaticAssignment
from SourceCode.greenTimes import get_green_times
from SourceCode.ownFunctions import getODGraph
from SourceCode.main import main
from dyntapy.settings import parameters


bpr_b = parameters.static_assignment.bpr_beta
bpr_a = parameters.static_assignment.bpr_alpha

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
    print('Link costs: link 1 = {}, link 2 = {}'.format(round(result.link_costs[0],3), round(result.link_costs[1],3)))
    print('Link flows: link 1 = {}, link 2 = {}'.format(result.flows[0], result.flows[1]))
    print('Saturations: link 0 = {},    link3 = {}\n'.format(round(result.flows[0]/(assignment.internal_network.links.capacity[0]*greens[0]),5),round(result.flows[1]/(assignment.internal_network.links.capacity[1]*greens[1]),5)))
    delays = []
    for i in range(len(ff_tt)):
        delays.append(ff_tt[i] * (np.multiply(bpr_a, pow((result.flows[i] / (np.multiply(assignment.internal_network.links.capacity[i] ,greens[i]))), bpr_b))))
    print('Delays: link 1 = {}, link 2 = {}'.format(round(delays[0],5), round(delays[1],5)))
    print('Capacities: link 1 = {}, link 2 = {}'.format(assignment.internal_network.links.capacity[0], assignment.internal_network.links.capacity[1]))
    print('Pressure: link 1 = {}, link 2 = {}'.format(round(assignment.internal_network.links.capacity[0]*delays[0],5), round(assignment.internal_network.links.capacity[1]*delays[1],5)))

    return result.flows, greens

def assign_simple(demand, methodGreen, methodCost = 'bpr'):
    _,flows = main(demand, methodCost, methodGreen)
    return flows
