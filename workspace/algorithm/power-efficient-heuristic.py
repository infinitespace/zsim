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
    tmap = getRandomMap(8, 4)
    pmap = getRandomMap(8, 4)
    cmap = [0,0,1,1,2,2,3,3]
    pnum = len(tmap) # process number
    n = len(cmap)    # total core number
    m = 4
    M = copy.deepcopy(tmap)
    X = np.zeros([pnum, n])
    # print tmap
    pp.pprint(M)
    # print X

    m_to_one = range(0, m)
    m_to_one.reverse()
    
    # Core types are ordered from smallest to biggest and assigned indices from 1 to m
    for j in m_to_one:
        col = []
        for i in range(len(M)):
            print i, j, M[i][j]
            col.append(M[i][j])
        i_idx = getMaxK(col, n/m)
        print i_idx

def getMaxK(data, k):
    res = []
    for i in range(len(data)):
        if len(res) < k:
            heapq.heappush(res, [data[i], i])
        else:
            if res[0][0] < data[i]:
                heapq.heappushpop(res, [data[i], i])
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