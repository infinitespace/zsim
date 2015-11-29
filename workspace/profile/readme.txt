## this file explains how to profile processes
all steps running under workspace/run/ directory


1.Command: sh ProfileApplication.sh het.cfg
This step search all files with format zsim-ev-[0-9]-[0-9].h5, each file is the simulation
result of each process running on each core type. 
(I copy all zsim-ev-[0-9][0-9].h5 files to /run directory because it needs other h5 file and
zsim.out to parse zsim results correctly)


2. generate profile.txt
Inside shell script, run energy_profile.sh to get the power and throughput characteristics
of each application running on each core type. Write the result into profile.txt.
format:        PID CORE_TYPE_ID THROUGHPUT POWER


3.Command: python createMap.py profile.txt ProcessNums CoreTypeNums
e.g. python createMap.py profile.txt 6 4

ProcessNums is the number of processes, CoreTypesNums is the number of core types.
build three maps.

