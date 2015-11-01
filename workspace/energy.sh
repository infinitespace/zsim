#!/bin/bash

set -e

debug() { echo "D> $*" 1>&2; }

MAIN_PATH=/afs/ir/users/s/i/sihua/cs316/zsim/zsim_build

## default
CORES=4
FREQUENCY=1700
L1SIZEb=32
L1WAYSb=4
L1SIZEw=8
L1WAYSw=4
L2SIZE=256
L2WAYS=8
L3SIZE=8192
L3WAYS=16
L3REPL="LRU"
MEMRANKS=2
MEMTECH="DDR3-1066-CL8"

## Run CACTI 6.5 to get cache parameters
L1_CACTI_beefy=`$MAIN_PATH/bin/gen_cacti.sh -s $L1SIZEb -w $L1WAYSb`
L1_CACTI_wimpy=`$MAIN_PATH/bin/gen_cacti.sh -s $L1SIZEw -w $L1WAYSw`
L2_CACTI=`$MAIN_PATH/bin/gen_cacti.sh -s $L2SIZE -w $L2WAYS`
L3_CACTI=`$MAIN_PATH/bin/gen_cacti.sh -s $L3SIZE -w $L3WAYS`
# <size> <way> <type> <cycle time> <access time> <energy> <power> <area>
echo $L1_CACTI_beefy > cacti_L1_beefy.txt
echo $L1_CACTI_wimpy > cacti_L1_wimpy.txt
echo $L2_CACTI > cacti_L2.txt
echo $L3_CACTI > cacti_L3.txt




