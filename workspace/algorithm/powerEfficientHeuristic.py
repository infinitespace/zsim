import numpy as np
import pickle
import random
import copy
import heapq
import pprint as pp

def runPEH(T, P, cmap, outputfile):
    pnum = len(T) # process number
    n = len(cmap)    # total core number
    m = 4
    M = copy.deepcopy(T)
    X = np.zeros([pnum, m])
    
    # Core types are ordered from biggest to smallest and assigned indices from 1 to m
    # Threads are mapped from biggest cores to smaller cores in descending order of 
    # throughput to achieve high throughput with best effort.
    pp.pprint(M)
    pp.pprint(X)
    for j in range(m): # from largest core to smallest core
        col = []
        for i in range(len(M)):
            col.append(M[i][j])
        max_k_procs = getMaxK(col, n/m) # k = n/m
        # print "=============", j
        # print col
        # print max_k_procs
        for ele in max_k_procs:
            X[ele[1]][j] = 1
            for k in range(len(M[ele[1]])):
                M[ele[1]][k] = 0
    

    # swapsj := vectors of downward swaps for core type j
    swaps_all = getSwaps_all(m, X, T, P)
    
    print 'X:\n', X
    print "init:", "Power:", getPower(X, P), " Throughput:", getThroughput(X, T)

    small_to_big = range(m-1)
    small_to_big.reverse()
    while check_avail(swaps_all) > 0:
        for j in small_to_big:
            if len(swaps_all[j]) > 0:
                swap = heapq.heappop(swaps_all[j])
                print 'j:', j, 'swap:', swap
                [proc_down, proc_up] = [swap[1], swap[2]]
                if X[proc_down][j] == 1 and X[proc_up][j+1] == 1:
                    X[proc_down][j] = 0
                    X[proc_down][j+1] = 1
                    X[proc_up][j] = 1
                    X[proc_up][j+1] = 0
                swaps_all = getSwaps_all(m, X, T, P)
        print 'X:\n',X
        print "after swap:", "Power:", getPower(X, P), " Throughput:", getThroughput(X, T)
    return X

'''
return top k element [[idx, val],[idx, val]]
'''
def getMaxK(data, k):
    res = []
    for i in range(len(data)):
        if len(res) < k:
            heapq.heappush(res, [data[i], i])
        else:
            heapq.heappushpop(res, [data[i], i])
    return res

def getPower(X, P):
    p = 0.0
    for i in range(len(X)):
        coretype = -1
        for j in range(len(X[i])):
            if X[i][j] == 1:
                coretype = j
                break
        if coretype == -1:
            print "Error: no core is assigned to process ", i
        else:
            p = p + P[i][coretype]
    return p

def getThroughput(X, T):
    t = 0.0
    for i in range(len(X)):
        coretype = -1
        for j in range(len(X[i])):
            if X[i][j] == 1:
                coretype = j
                break
        if coretype == -1:
            print "Error: no core is assigned to process ", i
        else:
            t = t + T[i][coretype]
    return t

def check_avail(swaps_all):
    res = False
    for v in swaps_all:
        if len(v) != 0:
            return True
    return False

def getSwaps_all(m, X, T, P):
    swaps_all = []
    for j in range(m-1): # from largest core to second smallest core
        swaps_all.append(getSwaps(j, X, T, P))
    # print "SA:", swaps_all, len(swaps_all)
    return swaps_all

def getSwaps(j, X, T, P):
    swaps = []
    thread_on_j = []
    for i in range(len(X)):
        if X[i][j] == 1:
            thread_on_j.append(i)
    thread_on_ja1 = []
    for i in range(len(X)):
        if X[i][j+1] == 1:
            thread_on_ja1.append(i)
    # print "find swap, j:", j
    # print 'th on j:', thread_on_j
    # print 'th on j-1:', thread_on_ja1
    for proc1 in thread_on_j:
        for proc2 in thread_on_ja1:
            deltaP = (P[proc1][j+1] + P[proc2][j]) - (P[proc1][j] + P[proc2][j+1])
            deltaT = (T[proc1][j+1] + T[proc2][j]) - (T[proc1][j] + T[proc2][j+1])
            # print 'proc1:', proc1, 'proc2:', proc2, deltaP, deltaT
            if deltaP < 0:
                priority = float(deltaP)/float(deltaT)
                heapq.heappush(swaps, [-priority, proc1, proc2])
    return swaps