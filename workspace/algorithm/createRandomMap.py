'''
usage:
@ parameters: proc number, core number for each proc, core type number
python createRandomMap.py 16 256 4

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

def writeMap(X, corenum, outputfile):
    output = open(outputfile, 'w')
    for row in X:
        for i in range(len(row)):
            if row[i] == 1:
                output.write(str(i) + ','+str(corenum)+'\n')
    output.close()

def getRandomMap(procnum, coretype):
    X = np.zeros([procnum, coretype])
    for i in range(procnum):
        X[i][random.randint(0, coretype - 1)] = 1
    return X

if __name__ == '__main__':
    procnum = int(sys.argv[1])
    corenum = int(sys.argv[2])
    coretype = int(sys.argv[3])
    outputfile = 'map.dat-random'
    X = getRandomMap(procnum, coretype)
    writeMap(X, corenum, outputfile)