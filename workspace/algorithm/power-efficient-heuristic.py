import numpy as np
import pickle
import sys
import argparse
import random
import copy
import heapq
import pprint as pp

def loadMap(mapdir):
    newmap = [[]]
    try:
        newmap = pickle.load(open(mapdir, 'r'))
    except:
        print "!!!ERROR!!!: can not open and load input file from: ", mapdir
    return newmap

def runPEH(tmapdir, pmapdir, cmapdir, outputfile):
    # tmap = loadMap(tmapdir)
    # pmap = loadMap(pmapdir)
    T = getRandomMap(8, 4)
    P = getRandomMap(8, 4)
    cmap = [0,0,1,1,2,2,3,3]
    pnum = len(T) # process number
    n = len(cmap)    # total core number
    m = 4
    M = copy.deepcopy(T)
    X = np.zeros([pnum, m])
    # print tmap
    pp.pprint(M)
    # print X

    m_to_one = range(0, m)
    m_to_one.reverse()
    
    # Core types are ordered from smallest to biggest and assigned indices from 1 to m
    # Threads are mapped from biggest cores to smaller cores in descending order of 
    # throughput to achieve high throughput with best effort.
    for j in m_to_one:
        col = []
        for i in range(len(M)):
            print i, j, M[i][j]
            col.append(M[i][j])
        max_k_procs = getMaxK(col, n/m) # k = n/m
        for ele in max_k_procs:
            X[ele[0]][j] = 1
            M[ele[0]][:] = np.zeros(m)

    # swapsj := vectors of downward swaps for core type j
    m_to_two = range(1, m)
    m_to_two.reverse()
    for j from m_to_two:
        swaps = []
        thread_on_j = []
        for i in range(len(X)):
            if X[i][j] == 1:
                thread_on_j.append(i)
        thread_on_jm1 = []
        for i in range(len(X)):
            if X[i][j-1] == 1:
                thread_on_jm1.append(i)
        for proc1 in range(len(thread_on_j)):
            for proc2 in range(len(thread_on_jm1)):
                deltaP = (P[proc1, j-1] + P[proc2, j]) - (P[proc1, j] + P[proc2, j-1])
                deltaT = (T[proc1, j-1] + T[proc2, j]) - (T[proc1, j] + T[proc2, j-1])
                if deltaP < 0:
                    priority = float(deltaP)/float(deltaT)
                    swaps.append([priority, proc1, proc2])
        
'''
return top k element [[val, idx],[val, idx]]
'''
def getMaxK(data, k):
    res = []
    for i in range(len(data)):
        if len(res) < k:
            heapq.heappush(res, [i, data[i]])
        else:
            if res[0][0] < data[i]:
                heapq.heappushpop(res, [i, data[i]])
    return res

def getRandomMap(height, width):
    m = []
    for i in range(height):
        row = []
        for i in range(width):
            row.append(random.random() * 10)
        m.append(row)
    return m


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Run power-efficient-heuristic algorithm to generate a map.dat")
    parser.add_argument('-t', help = 'throughput map dir', required = False)
    parser.add_argument('-p', help = 'power map dir', required = False)
    parser.add_argument('-c', help = 'core map dir', required = False)
    parser.add_argument('-o', help = 'output map dir', required = False)
    args = parser.parse_args()

    tmapdir = 'tmap.pkl'
    pmapdir = 'pmap.pkl'
    cmapdir = 'cmap.pkl'
    outputfile = 'map.dat'
    if args.t:
        tmapdir = args.t
    if args.p:
        pmapdir = args.p
    if args.c:
        pmapdir = args.c
    if args.o:
        outputfile = args.o

    runPEH(tmapdir, pmapdir, cmapdir, outputfile)