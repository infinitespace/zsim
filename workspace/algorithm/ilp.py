'''
To install pulp:

In windows (please make sure pip is on your path):
c:\Python26\Scripts\> pip install pulp

In Linux:
$ sudo pip install pulp
$ sudo pulptest             #needed to get the default solver to work
'''
import pickle
import sys
import argparse
import random
import copy
import heapq
import pprint as pp
import powerEfficientHeuristic as peh
import powerEfficientHeuristic_minP as pehmp 
import numpy as np
from pulp import *

def ilpSolver(T, P ,C, Degradation):
    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("Min_power",LpMinimize)

    procnum = len(T)
    coretype = len(T[0])
    corenum = len(C)

    Threshold = pehmp.getBaselineThroughput(T) * Degradation
    # The procnum variables are created with a lower limit of zero, hiher limit of coretype - 1
    x = [LpVariable("Proc " + str(i) + " Core " + str(j), 0, 1, LpInteger) for i in range(procnum) for j in range(coretype)]
    # The objective function is added to 'prob' first
    # print x

    prob += lpSum([P[i][j]*x[i*coretype + j] for i in range(procnum) for j in range(coretype)]), "Total Power"

    # The five constraints are entered
    prob += lpSum([T[i][j]*x[i*coretype + j] for i in range(procnum) for j in range(coretype)]) > Threshold, 'throughput Threshold'
    prob += lpSum([x[i] for i in [j*4 for j in range(procnum)]]) == corenum/coretype, "max proc on one type of core 0"
    prob += lpSum([x[i] for i in [j*4 + 1 for j in range(procnum)]]) == corenum/coretype, "max proc on one type of core 1"
    prob += lpSum([x[i] for i in [j*4 + 2 for j in range(procnum)]]) == corenum/coretype, "max proc on one type of core 2"
    prob += lpSum([x[i] for i in [j*4 + 3 for j in range(procnum)]]) == corenum/coretype, "max proc on one type of core 3"
    for i in range(procnum):
        prob += lpSum([x[j] for j in range(i * coretype, i * coretype + coretype)]) == 1, "max core on one type of proc" + str(i)

    # The problem data is written to an .lp file
    prob.writeLP("Min_power.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    X = np.zeros([procnum, coretype])
    row = []
    for v in prob.variables():
        print(v.name, "=", v.varValue)
        idx = [ int(s) for s in v.name.split('_') if s.isdigit()]
        X[idx[0]][idx[1]] = v.varValue

    # The optimised objective function value is printed to the screen
    print("Total Power = ", value(prob.objective))
    print " Throughput:", pehmp.getThroughput(X, T)
    return X

