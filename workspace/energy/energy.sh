#!/bin/bash

set -e

debug() { echo "D> $*" 1>&2; }

MAIN_PATH=~/cs316/zsim_build/downloads/zsim/workspace/energy/src

## default
CORES_b=6
CORES_w=10
CORES=16
FREQUENCY=2400
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
L1_CACTI_beefy=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZEb -w $L1WAYSb`
L1_CACTI_wimpy=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZEw -w $L1WAYSw`
L2_CACTI=`sh $MAIN_PATH/gen_cacti.sh -s $L2SIZE -w $L2WAYS`
L3_CACTI=`sh $MAIN_PATH/gen_cacti.sh -s $L3SIZE -w $L3WAYS`
# <size> <way> <type> <cycle time> <access time> <energy> <power> <area>
echo $L1_CACTI_beefy > cacti_L1_beefy.txt
echo $L1_CACTI_wimpy > cacti_L1_wimpy.txt
echo $L2_CACTI > cacti_L2.txt
echo $L3_CACTI > cacti_L3.txt

L1_ENERGY_b=`cut -f6 -d " " cacti_L1_beefy.txt`
L1_POWER_b=`cut -f7 -d " " cacti_L1_beefy.txt`
L1_ENERGY_w=`cut -f6 -d " " cacti_L1_wimpy.txt`
L1_POWER_w=`cut -f7 -d " " cacti_L1_wimpy.txt`
L2_ENERGY=`cut -f6 -d " " cacti_L2.txt`
L2_POWER=`cut -f7 -d " " cacti_L2.txt`
L2_AREA=`cut -f8 -d " " cacti_L2.txt`
L3_ENERGY=`cut -f6 -d " " cacti_L3.txt`
L3_POWER=`cut -f7 -d " " cacti_L3.txt`
L3_AREA=`cut -f8 -d " " cacti_L3.txt`

#TIME=`python /afs/ir/users/s/i/sihua/cs316/zsim_backup/zsim_build/extract.py`

L1_hGETS=`grep hGETS zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`
L1_hGETX=`grep hGETX zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`
L1_mGETS=`grep mGETS zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`

L1_DYN_ENERGY=`echo "($L1_hGETS+$L1_hGETX+$L1_mGETS)*$L1_ENERGY/1000000000" | bc -l`
#L1_STA_ENERGY=`echo "$CORES_b*$L1_POWER/1000*$TIME" | bc -l`

tmp_L2_hGETS=`grep hGETS zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_hGETS=$[tmp_L2_hGETS - L1_hGETS]
tmp_L2_hGETX=`grep hGETX zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_hGETX=$[tmp_L2_hGETX - L1_hGETX]
tmp_L2_mGETS=`grep mGETS zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_mGETS=$[tmp_L2_mGETS - L1_mGETS]

L2_DYN_ENERGY=`echo "($L2_hGETS+$L2_hGETX+$L2_mGETS)*$L2_ENERGY/1000000000" | bc -l`
#L2_STA_ENERGY=`echo "$CORES_B*$L2_POWER/1000*$TIME" | bc -l`

L3_hGETS=`grep hGETS zsim.out | tail -1 | awk '{print $2}'`
L3_hGETX=`grep hGETX zsim.out | tail -1 | awk '{print $2}'`

echo "L1 dynamic energy (J)  : $L1_DYN_ENERGY"
echo "L1 static energy (J)   : $L1_STA_ENERGY"
echo "L2 dynamic energy (J)  : $L2_DYN_ENERGY"
echo "L2 static energy (J)   : $L2_STA_ENERGY"
echo "L3 dynamic energy (J)  : $L3_DYN_ENERGY"
echo "L3 static energy (J)   : $L3_STA_ENERGY"
echo "$L1_hGETS"


