#!/usr/bin/python

import h5py
import pprint
import numpy as np
import parse_cfg as ps

CFG_PATH = '../config/het.cfg'
ZSIMH5_PATH = '../run/zsim-ev.h5'

cfg = ps.parse(CFG_PATH)

#pprint.pprint(cfg)

frequency = float(cfg['sys']['frequency'])
phaseLength = int(cfg['sim']['phaseLength'])
# core numbers
cores_big = int(cfg['sys']['cores']['big']['cores'])
cores_little = int(cfg['sys']['cores']['little']['cores'])
cores_mid1 = int(cfg['sys']['cores']['mid1']['cores'])
cores_mid2 = int(cfg['sys']['cores']['mid2']['cores'])

# L1 
L1SIZE_big = int(cfg['sys']['caches']['l1d_big']['size'])/1024
L1WAYS_big = int(cfg['sys']['caches']['l1d_big']['array']['ways'])
L1SIZE_mid1 = int(cfg['sys']['caches']['l1d_mid1']['size'])/1024
L1WAYS_mid1 = int(cfg['sys']['caches']['l1d_mid1']['array']['ways'])
L1SIZE_mid2 = int(cfg['sys']['caches']['l1d_mid2']['size'])/1024
L1WAYS_mid2 = int(cfg['sys']['caches']['l1d_mid2']['array']['ways'])
L1SIZE_little = int(cfg['sys']['caches']['l1d_little']['size'])/1024
L1WAYS_little = int(cfg['sys']['caches']['l1d_little']['array']['ways'])

# L2
L2SIZE_big = int(cfg['sys']['caches']['l2_big']['size'])/1024
L2WAYS_big = int(cfg['sys']['caches']['l2_big']['array']['ways'])
L2SIZE_mid1 = int(cfg['sys']['caches']['l2_mid1']['size'])/1024
L2WAYS_mid1 = int(cfg['sys']['caches']['l2_mid1']['array']['ways'])

# L3
L3SIZE = int(cfg['sys']['caches']['l3']['size'])/1024
L3WAYS = int(cfg['sys']['caches']['l3']['array']['ways'])
MEM_TECH = cfg['sys']['mem']['tech']

#print frequency, cores_beefy, cores_wimpy, phaseLength, L1DSIZE_beefy, L1DWAYS_beefy, L2SIZE, L2WAYS, MEM_TECH 

# Open stats file
f = h5py.File(ZSIMH5_PATH, 'r')

# Get the single dataset in the file
dset = f["stats"]["root"]
#print dset.shape
#print dset.dtype

# Phase count at end of simulation
endPhase = dset[-1]['phase']
ccycles = endPhase * phaseLength
TIME = float(ccycles / frequency) * 0.000001

# Cache hits and misses
l1_1 = np.sum(dset[-1]['l1i_big']['hGETS']+dset[-1]['l1d_big']['hGETS']+dset[-1]['l1i_big']['hGETX']+dset[-1]['l1d_big']['hGETX']+dset[-1]['l1i_big']['mGETS']+dset[-1]['l1d_big']['mGETS'])
l1_2 = np.sum(dset[-1]['l1i_mid1']['hGETS'])+np.sum(dset[-1]['l1d_mid1']['hGETS'])+np.sum(dset[-1]['l1i_mid1']['hGETX'])+np.sum(dset[-1]['l1d_mid1']['hGETX'])+np.sum(dset[-1]['l1i_mid1']['mGETS'])+np.sum(dset[-1]['l1d_mid1']['mGETS'])
l1_3 = np.sum(dset[-1]['l1i_mid2']['hGETS'])+np.sum(dset[-1]['l1d_mid2']['hGETS'])+np.sum(dset[-1]['l1i_mid2']['hGETX'])+np.sum(dset[-1]['l1d_mid2']['hGETX'])+np.sum(dset[-1]['l1i_mid2']['mGETS'])+np.sum(dset[-1]['l1d_mid2']['mGETS'])
l1_4 = np.sum(dset[-1]['l1i_little']['hGETS'])+np.sum(dset[-1]['l1d_little']['hGETS'])+np.sum(dset[-1]['l1i_little']['hGETX'])+np.sum(dset[-1]['l1d_little']['hGETX'])+np.sum(dset[-1]['l1i_little']['mGETS'])+np.sum(dset[-1]['l1d_little']['mGETS'])

l2_1 = np.sum(dset[-1]['l2_big']['hGETS'] + dset[-1]['l2_big']['hGETX'] + dset[-1]['l2_big']['mGETS'])
l2_2 = np.sum(dset[-1]['l2_mid1']['hGETS'] + dset[-1]['l2_mid1']['hGETX'] + dset[-1]['l2_mid1']['mGETS'])

l3 = np.sum(dset[-1]['l3']['hGETS'] + dset[-1]['l3']['hGETX'] + dset[-1]['l3']['mGETS'])


# Core Voltage depends on core type. w indicate type OOO, n idicate Simple
CORE_VOLTAGE_w = (frequency/1000) * .30914 + .552688
CORE_VOLTAGE_n = (frequency/1000) * .21967 + .66066 

# Total number of instructions executed, counted by adding per-core counts
instrs1 = np.sum(dset[-1]['big']['instrs']) 
instrs2 = np.sum(dset[-1]['mid1']['instrs']) 
instrs3 = np.sum(dset[-1]['mid2']['instrs']) 
instrs4 = np.sum(dset[-1]['littl2']['instrs'])

# Core Energy Model
I_leak_w=1.3136495
I_leak_n=0.45455
CORE_DYN_ENERGY_w= 2.22/1000000000*(instrs1+instrs1)*(CORE_VOLTAGE_w/1.35)*(CORE_VOLTAGE_w/1.35)
CORE_STA_ENERGY_w= I_leak_w*CORE_VOLTAGE_w*TIME*(cores_big+cores_mid1)
CORE_DYN_ENERGY_n= .78/1000000000*(instrs3+instrs4)*(CORE_VOLTAGE_n/1.16)*(CORE_VOLTAGE_n/1.16)
CORE_STA_ENERGY_n= I_leak_n*CORE_VOLTAGE_n*TIME*(cores_mid2+cores_little)
CORE_DYN_ENERGY=CORE_DYN_ENERGY_w+CORE_DYN_ENERGY_n
CORE_STA_ENERGY=CORE_STA_ENERGY_w+CORE_STA_ENERGY_n

f = open('args.txt', 'w')
f.write(str(TIME) + ' ' + str(frequency) + ' ' + str(cores_big) + ' ' + str(cores_mid1) + ' ' + str(cores_mid2) + ' ' + str(cores_little) + ' ' + str(L1ISIZE_big) + ' ' + str(L1IWAYS_big) + ' ' + str(L1ISIZE_mid1) + ' ' + str(L1IWAYS_mid1) + ' ' + str(L1ISIZE_mid2) + ' ' + str(L1IWAYS_mid2) + ' ' + str(L1ISIZE_little) + ' ' + str(L1IWAYS_little) + ' ' + str(L2SIZE_big) + ' ' + str(L2WAYS_big) + ' ' + str(L2SIZE_mid1) + ' ' + str(L2WAYS_mid1) + ' ' + str(L3SIZE) + ' ' + str(L3WAYS) + ' ' + str(MEM_TECH) + ' ' + str(CORE_DYN_ENERGY) + ' ' + str(CORE_STA_ENERGY) + ' ' + str(l1_1) + ' ' + str(l1_2) + ' ' + str(l1_3) + ' ' + str(l1_4) + ' ' + str(l2_1) + ' ' + str(l2_2) + ' ' + str(l3))



