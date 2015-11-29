import numpy as np
import pickle
import sys
import argparse
import random
import copy
import heapq
import pprint as pp
import powerEfficientHeuristic as peh

def getRandomMap(height, width):
    m = []
    for i in range(height):
        row = []
        for i in range(width):
            row.append(random.random() * 10)
        m.append(row)
    return m

def loadMap(mapdir):
    newmap = [[]]
    try:
        newmap = pickle.load(open(mapdir, 'r'))
    except:
        print "!!!ERROR!!!: can not open and load input file from: ", mapdir
    return newmap

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

    # T = loadMap(tmapdir)
    # P = loadMap(pmapdir)
    # cmap = loadMap(cmapdir)
    T = getRandomMap(8, 4)
    P = getRandomMap(8, 4)
    cmap = [0,0,1,1,2,2,3,3]

    peh.runPEH(T, P, cmap, outputfile)