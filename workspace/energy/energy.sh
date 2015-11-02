#!/bin/bash

set -e

MAIN_PATH=~/cs316/zsim_build/downloads/zsim/workspace/energy/src

## configuration parameters
TIME=`cut -f1 -d " " args.txt`
FREQUENCY=`cut -f2 -d " " args.txt`
CORES_b=`cut -f3 -d " " args.txt`
CORES_w=`cut -f4 -d " " args.txt`
L1SIZEb=`cut -f5 -d " " args.txt`
L1WAYSb=`cut -f6 -d " " args.txt`
L1SIZEw=`cut -f7 -d " " args.txt`
L1WAYSw=`cut -f8 -d " " args.txt`
L2SIZE=`cut -f9 -d " " args.txt`
L2WAYS=`cut -f10 -d " " args.txt`
L3SIZE=`cut -f11 -d " " args.txt`
L3WAYS=`cut -f12 -d " " args.txt`
DRAM_TECH=`cut -f13 -d " " args.txt`
CORE_DYN_ENERGY=`cut -f14 -d " " args.txt`
CORE_STA_ENERGY=`cut -f15 -d " " args.txt`

CORES=`echo $CORES_b+$CORES_w | bc -l`

## Run CACTI 6.5 to get cache parameters
L1_CACTI_beefy=`$MAIN_PATH/gen_cacti.sh -s $L1SIZEb -w $L1WAYSb`
L1_CACTI_wimpy=`$MAIN_PATH/gen_cacti.sh -s $L1SIZEw -w $L1WAYSw`
L2_CACTI=`$MAIN_PATH/gen_cacti.sh -s $L2SIZE -w $L2WAYS`
L3_CACTI=`$MAIN_PATH/gen_cacti.sh -s $L3SIZE -w $L3WAYS`

#echo $L1_CACTI_beefy > cacti_L1_beefy.txt
#echo $L1_CACTI_wimpy > cacti_L1_wimpy.txt
#echo $L2_CACTI > cacti_L2.txt
#echo $L3_CACTI > cacti_L3.txt

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

# Beefy L1 cache energy
L1_hGETS=`grep hGETS zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`
L1_hGETX=`grep hGETX zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`
L1_mGETS=`grep mGETS zsim.out | head -$[2*CORES_b] | awk '{sum += $2} END {print sum}'`

L1_DYN_ENERGY=`echo "($L1_hGETS+$L1_hGETX+$L1_mGETS)*$L1_ENERGY_b/1000000000" | bc -l`
L1_STA_ENERGY=`echo "$CORES_b*$L1_POWER/1000*$TIME" | bc -l`

tmp_L2_hGETS=`grep hGETS zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_hGETS=$[tmp_L2_hGETS - L1_hGETS]
tmp_L2_hGETX=`grep hGETX zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_hGETX=$[tmp_L2_hGETX - L1_hGETX]
tmp_L2_mGETS=`grep mGETS zsim.out | head -$[3*CORES_b] | awk '{sum += $2} END {print sum}'`
L2_mGETS=$[tmp_L2_mGETS - L1_mGETS]

L2_DYN_ENERGY=`echo "($L2_hGETS+$L2_hGETX+$L2_mGETS)*$L2_ENERGY/1000000000" | bc -l`
L2_STA_ENERGY=`echo "$CORES_b*$L2_POWER/1000*$TIME" | bc -l`

L3_hGETS=`grep hGETS zsim.out | tail -1 | awk '{print $2}'`
L3_hGETX=`grep hGETX zsim.out | tail -1 | awk '{print $2}'`
L3_mGETS=`grep mGETS zsim.out | tail -1 | awk '{print $2}'`

L3_DYN_ENERGY=`echo "($L3_hGETS+$L3_hGETX+$L3_mGETS)*$L3_ENERGY/1000000000" | bc -l`
L3_STA_ENERGY=`echo "$L3_POWER/1000*$TIME" | bc -l`

MEM_RD=`grep -w rd zsim.out | awk '{print $2}' | paste -sd+ | bc`
MEM_WR=`grep -w wr zsim.out | awk '{print $2}' | paste -sd+ | bc`

#echo "python /afs/ir/class/ee282/pa2/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME"
MEM_DYN_ENERGY=`python /afs/ir/class/ee282/pa1/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME false`
MEM_STA_ENERGY=`python /afs/ir/class/ee282/pa1/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME true`

TOTAL_ENERGY=`echo $CORE_DYN_ENERGY+$CORE_STA_ENERGY+$L1_DYN_ENERGY+$L1_STA_ENERGY+$L2_DYN_ENERGY+$L2_STA_ENERGY+$L3_DYN_ENERGY+$L3_STA_ENERGY+$MEM_DYN_ENERGY+$MEM_STA_ENERGY | bc -l`
EDP=`echo $TOTAL_ENERGY*$TIME | bc -l`

echo "Execution    time (s)  : $TIME"
echo "L1 dynamic energy (J)  : $L1_DYN_ENERGY"
echo "L1 static energy (J)   : $L1_STA_ENERGY"
echo "L2 dynamic energy (J)  : $L2_DYN_ENERGY"
echo "L2 static energy (J)   : $L2_STA_ENERGY"
echo "L3 dynamic energy (J)  : $L3_DYN_ENERGY"
echo "L3 static energy (J)   : $L3_STA_ENERGY"
echo "Mem dynamic energy (J) : $MEM_DYN_ENERGY"
echo "Mem static energy (J)  : $MEM_STA_ENERGY"

echo "$L1_ENERGY_b"
echo "$L1_POWER_b"
echo "$L2_ENERGY"
echo "$L2_POWER"
echo "$L2_AREA"
echo "$L3_ENERGY"
echo "$L3_POWER"
echo "$L3_AREA"

