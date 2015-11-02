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
cores_beefy = int(cfg['sys']['cores']['beefy']['cores'])
cores_wimpy = int(cfg['sys']['cores']['wimpy']['cores'])
phaseLength = int(cfg['sim']['phaseLength'])
L1DSIZE_beefy = int(cfg['sys']['caches']['l1d_beefy']['size'])/1024
L1DWAYS_beefy = int(cfg['sys']['caches']['l1d_beefy']['array']['ways'])
L1ISIZE_beefy = int(cfg['sys']['caches']['l1i_beefy']['size'])/1024
L1IWAYS_beefy = int(cfg['sys']['caches']['l1i_beefy']['array']['ways'])
L1DSIZE_wimpy = int(cfg['sys']['caches']['l1d_wimpy']['size'])/1024
L1DWAYS_wimpy = int(cfg['sys']['caches']['l1d_wimpy']['array']['ways'])
L1ISIZE_wimpy = int(cfg['sys']['caches']['l1i_wimpy']['size'])/1024
L1IWAYS_wimpy = int(cfg['sys']['caches']['l1i_wimpy']['array']['ways'])
L2SIZE = int(cfg['sys']['caches']['l2_beefy']['size'])/1024
L2WAYS = int(cfg['sys']['caches']['l2_beefy']['array']['ways'])
L3SIZE = int(cfg['sys']['caches']['l3']['size'])/1024
L3WAYS = int(cfg['sys']['caches']['l3']['size'])
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

# Core Voltage
CORE_VOLTAGE_B = (frequency/1000) * .30914 + .552688
CORE_VOLTAGE_W = (frequency/1000) * .21967 + .66066 

# Total number of instructions executed, counted by adding per-core counts
instrs1 = np.sum(dset[-1]['beefy']['instrs']) 
instrs2 = np.sum(dset[-1]['wimpy']['instrs'])
instructions = instrs1 + instrs2;

# Calculate core energy
I_leak_beefy=1.3136495
I_leak_wimpy=0.45455
CORE_DYN_ENERGY_B= 2.22/1000000000*instrs1*(CORE_VOLTAGE_B/1.35)*(CORE_VOLTAGE_B/1.35)
CORE_STA_ENERGY_B= I_leak_beefy*CORE_VOLTAGE_B*TIME*cores_beefy
CORE_DYN_ENERGY_W= .78/1000000000*instrs2*(CORE_VOLTAGE_W/1.16)*(CORE_VOLTAGE_W/1.16)
CORE_STA_ENERGY_W= I_leak_wimpy*CORE_VOLTAGE_W*TIME*cores_wimpy
CORE_DYN_ENERGY=CORE_DYN_ENERGY_B+CORE_DYN_ENERGY_W
CORE_STA_ENERGY=CORE_STA_ENERGY_B+CORE_STA_ENERGY_W

f = open('args.txt', 'w')
f.write(str(TIME) + ' ' + str(frequency) + ' ' + str(cores_beefy) + ' ' + str(cores_wimpy) + ' ' + str(L1ISIZE_beefy) + ' ' + str(L1IWAYS_beefy) + ' ' + str(L1ISIZE_wimpy) + ' ' + str(L1IWAYS_wimpy) + ' ' + str(L2SIZE) + ' ' + str(L2WAYS) + ' ' + str(L3SIZE) + ' ' + str(L3WAYS) + ' ' + str(MEM_TECH) + ' ' + str(CORE_DYN_ENERGY) + ' ' + str(CORE_STA_ENERGY))
