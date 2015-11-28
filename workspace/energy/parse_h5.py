#!/usr/bin/python

import h5py
import pprint
import numpy as np
import parse_cfg as ps
import sys

if __name__ == "__main__":
	CFG_PATH = sys.argv[1]  
	ZSIMH5_PATH = sys.argv[2] 

	my_list = []
	for i in ZSIMH5_PATH:
		if i.isdigit():
			my_list.append(i)
	 
	if len(my_list) == 6:
		PID = my_list[3]
		COREID = my_list[4]
	else:
		PID = "default"
		COREID = "default"
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
	instrs4 = np.sum(dset[-1]['little']['instrs'])
 
	instructions = instrs1 + instrs2 + instrs3 + instrs4
	T = 1.0 / TIME

	# Core Energy Model
	I_leak_w=1.3136495
	I_leak_n=0.45455
	if  len(my_list) == 4:
		cores_w = cores_big+cores_mid1
		cores_n = cores_mid2+cores_little
	else:
		if COREID == 0 or COREID == 1:
			cores_w = 1
			cores_n = 0
		else:
			cores_w = 0
			cores_n = 0 

	CORE_DYN_ENERGY_w= 2.22/1000000000*(instrs1+instrs2)*(CORE_VOLTAGE_w/1.35)*(CORE_VOLTAGE_w/1.35)
	CORE_STA_ENERGY_w= I_leak_w*CORE_VOLTAGE_w*TIME*cores_w
	CORE_DYN_ENERGY_n= .78/1000000000*(instrs3+instrs4)*(CORE_VOLTAGE_n/1.16)*(CORE_VOLTAGE_n/1.16)
	CORE_STA_ENERGY_n= I_leak_n*CORE_VOLTAGE_n*TIME*cores_n

	CORE_DYN_ENERGY=CORE_DYN_ENERGY_w+CORE_DYN_ENERGY_n
	CORE_STA_ENERGY=CORE_STA_ENERGY_w+CORE_STA_ENERGY_n

	f = open('args.txt', 'w')
	line = str(TIME) + ' ' + str(frequency) + ' ' + str(cores_big) + ' ' + str(cores_mid1) + ' ' + str(cores_mid2) + ' ' + str(cores_little)
	line += ' ' + str(L1SIZE_big) + ' ' + str(L1WAYS_big) + ' ' + str(L1SIZE_mid1) + ' ' + str(L1WAYS_mid1) + ' ' + str(L1SIZE_mid2) + ' '
	line += str(L1WAYS_mid2) + ' ' + str(L1SIZE_little) + ' ' + str(L1WAYS_little) + ' ' + str(L2SIZE_big) + ' ' + str(L2WAYS_big) + ' '
	line += str(L2SIZE_mid1) + ' ' + str(L2WAYS_mid1) + ' ' + str(L3SIZE) + ' ' + str(L3WAYS) + ' ' + str(MEM_TECH) + ' ' 
	line += str(CORE_DYN_ENERGY) + ' ' + str(CORE_STA_ENERGY) + ' ' + str(l1_1) + ' ' + str(l1_2) + ' ' + str(l1_3) + ' '
	line += str(l1_4) + ' ' + str(l2_1) + ' ' + str(l2_2) + ' ' + str(l3) + ' ' + str(T) + ' ' + str(PID) + ' ' + str(COREID)

	f.write(line)
