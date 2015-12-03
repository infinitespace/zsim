import numpy as np
import pickle
import random
import copy
import heapq
import pprint as pp

def runPEH_for_minPower(T, P, cmap, outputfile, Degradation):
    pnum = len(T) # process number
    n = len(cmap)    # total core number
    m = 4
    M = copy.deepcopy(P)
    X = np.zeros([pnum, m])
    Threshold = getBaselineThroughput(T) * Degradation
    print 'Threshold:', Threshold
    # Core types are ordered from biggest to smallest and assigned indices from 1 to m
    # Threads are mapped from biggest cores to smaller cores in descending order of 
    # throughput to achieve high throughput with best effort.

    coreinfo = getCoreInfo(cmap)
    print 'Core info:', coreinfo
    # small_to_big = range(m)
    # small_to_big.reverse()
    # for j in small_to_big: # from smallest core to largest core
    for j in range(m):
        col = []
        for i in range(len(M)):
            col.append(M[i][j])
        min_k_procs = getMinK(col, coreinfo[j]) # k = n/m
        # print "=============", j
        # print col
        # print min_k_procs
        for ele in min_k_procs:
            X[ele[1]][j] = 1
            for k in range(len(M[ele[1]])):
                M[ele[1]][k] = 9999999.9

    # swapsj := vectors of downward swaps for core type j
    swaps_all = getSwaps_all(m, X, T, P)
    
        
    print 'X:\n', X
    print "init:", "Power:", getPower(X, P), " Throughput:", getThroughput(X, T)

    big_to_small = range(1, m)
    finish = False
    swap_num = 0
    while check_avail(swaps_all) > 0:
        for j in big_to_small:
            # print j, swaps_all[j]
            if len(swaps_all[j]) > 0:
                swap = heapq.heappop(swaps_all[j])
                print 'j:', j, 'swap:', swap
                [proc_up, proc_down] = [swap[1], swap[2]]
                # print X[proc_down], X[proc_up]
                if X[proc_down][j-1] == 1 and X[proc_up][j] == 1:
                    X[proc_down][j] = 1
                    X[proc_down][j-1] = 0
                    X[proc_up][j] = 0
                    X[proc_up][j-1] = 1
                    swap_num += 1
                swaps_all = getSwaps_all(m, X, T, P)
                # print 'X:\n',X
                print "after swap:", "Power:", getPower(X, P), " Throughput:", getThroughput(X, T)
            if getThroughput(X, T) > Threshold:
                finish = True
                break
        if finish:
            break
    print "Swap Num:", swap_num
    return X

def getBaselineThroughput(T):
    avg = 0
    for row in T:
        avg += float(sum(row))/len(row)
    return avg

def getSwaps_all(m, X, T, P):
    swaps_all = [[]]*m
    small_to_big = range(1, m)
    small_to_big.reverse()
    for j in small_to_big: # from smallest core to secondlargest core
        swaps_all[j] = getSwaps(j, X, T, P)
    # print "\nSA:", swaps_all, len(swaps_all)
    return swaps_all

def getSwaps(j, X, T, P):
    swaps = []
    thread_on_j = []
    for i in range(len(X)):
        if X[i][j] == 1:
            thread_on_j.append(i)
    thread_on_jm1 = []
    for i in range(len(X)):
        if X[i][j-1] == 1:
            thread_on_jm1.append(i)
    # print "find swap, j:", j
    # print 'th on j:', thread_on_j
    # print 'th on j-1:', thread_on_jm1
    for proc1 in thread_on_j:
        for proc2 in thread_on_jm1:
            deltaP = (P[proc1][j-1] + P[proc2][j]) - (P[proc1][j] + P[proc2][j-1])

            avgTproc1 = sum(T[proc1])/4.0
            avgTproc2 = sum(T[proc2])/4.0
            DECLINE = 0.85

            deltaT = (T[proc1][j-1] + T[proc2][j]) - (T[proc1][j] + T[proc2][j-1])
            # print 'j:',j,'proc1:', proc1, 'proc2:', proc2, deltaP, deltaT
            if deltaT > 0:
            # if deltaP != 0 and T[proc1][j-1] > avgTproc1*DECLINE and T[proc2][j] > avgTproc2*DECLINE:
                priority = float(deltaT)/float(deltaP)
                # priority = 1/float(deltaP)
                heapq.heappush(swaps, [-priority, proc1, proc2])
    return swaps


def getCoreInfo(cmap):
    typenum = max(cmap) + 1
    coreinfo = np.zeros(typenum)
    for t in cmap:
        coreinfo[t] = coreinfo[t] + 1
    return coreinfo

# return top k element [[idx, val],[idx, val]]
def getMinK(data, k):
    res = []
    for i in range(len(data)):
        if len(res) < k:
            heapq.heappush(res, [-data[i], i])
        else:
            heapq.heappushpop(res, [-data[i], i])
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
