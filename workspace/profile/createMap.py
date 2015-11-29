#!/usr/bin/python

import pickle
import sys

if __name__ == "__main__":
	files = open(sys.argv[1], "r")
	processNums = int(sys.argv[2])
	coreTypeNums = int(sys.argv[3])	
	files.readline()
	tmap = [[0 for x in range(coreTypeNums)] for x in range(processNums)]
	pmap = [[0 for x in range(coreTypeNums)] for x in range(processNums)]
	cmap = [0]*256 + [1]*256 + [2]*256 + [3]*256
	IPCmap = [[0 for x in range(coreTypeNums)] for x in range(processNums)]
	for line in files:
		my_list = line.split()
		row = int(my_list[0])
		colomn = int(my_list[1])
		tmap[row][colomn] = float(my_list[2])
		pmap[row][colomn] = float(my_list[3])
		IPCmap[row][colomn] = float(my_list[4])

	files.close()

	pickle.dump(tmap, open("tmap_time.pkl", "wb"))
	pickle.dump(pmap, open("pmap.pkl", "wb"))
	pickle.dump(cmap, open("cmap.pkl", "wb"))
	pickle.dump(IPCmap, open("tmap_ipc.pkl", "wb"))
