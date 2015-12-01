import pickle
import sys
import argparse
import random
import copy
import heapq
import pprint as pp
import powerEfficientHeuristic as peh
import numpy as np

def writeMap(X, corenum, outputfile):
    output = open(outputfile, 'w')
    for row in X:
        for i in range(len(row)):
            if row[i] == 1:
                output.write(str(i) + ','+str(corenum)+'\n')
    output.close()

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

def checkInput(T, P, cmap):
    procnum = len(T)
    coretype = len(T[0])
    if len(P) != procnum:
        print "Error: invalid input files: process number not match!"
        return False
    if len(P[0]) != coretype or max(cmap) > coretype - 1:
        print "Error: invalid input files: core type number not match!"
        return False
    return True

def enlargeMap(target, base, ctype, T, P):
    newT = np.zeros([target, ctype])
    newP = np.zeros([target, ctype])
    for i in range(target):
        for j in range(ctype):
            newT[i][j] = T[i%base][j]
            newP[i][j] = P[i%base][j]
    return newT, newP

def generateCmap(cnum, ctype):
    cmap = np.zeros(cnum)
    per = len(cmap)/ctype
    for i in range(len(cmap)):
        cmap[i] = i/per
    print cmap
    return cmap

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
        cmapdir = args.c
    if args.o:
        outputfile = args.o

    T = loadMap(tmapdir)
    P = loadMap(pmapdir)
    # cmap = loadMap(cmapdir)
    #T = getRandomMap(8, 4)
    #P = getRandomMap(8, 4)
    #cmap = [0,0,1,1,2,2,3,3]
    # T = pickle.load(open("tmap_test.pkl", "r"))
    # P = pickle.load(open("pmap_test.pkl", "r"))
    # cmap = pickle.load(open("cmap_test.pkl", "r"))    
    
    print 'input T:'
    print T
    print 'input P:'
    print P
    cmap = generateCmap(16, 4)
    T16, P16 = enlargeMap(16, 4, 4, T, P)

    if checkInput(T16, P16, cmap):
        X = peh.runPEH(T16, P16, cmap, outputfile)
        writeMap(X, 256, outputfile)
