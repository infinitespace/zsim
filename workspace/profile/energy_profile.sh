#!/bin/bash

set -e

debug() { echo "D> $*" 1>&2; }

WORK_PATH=~/cs316/zsim_build/downloads/zsim/workspace
MAIN_PATH=$WORK_PATH/energy/src
PY_PATH=$WORK_PATH/energy/parse_h5.py
ZSIM_CFG_PATH=$WORK_PATH/config/$2
ZSIM_H5_PATH=$WORK_PATH/input/profile_1202/$1

python $PY_PATH $ZSIM_CFG_PATH $ZSIM_H5_PATH

## configuration parameters
TIME=`cut -f1 -d " " args.txt`
FREQUENCY=`cut -f2 -d " " args.txt`
CORES_1=`cut -f3 -d " " args.txt`
CORES_2=`cut -f4 -d " " args.txt`
CORES_3=`cut -f5 -d " " args.txt`
CORES_4=`cut -f6 -d " " args.txt`

L1SIZE_1=`cut -f7 -d " " args.txt`
L1WAYS_1=`cut -f8 -d " " args.txt`
L1SIZE_2=`cut -f9 -d " " args.txt`
L1WAYS_2=`cut -f10 -d " " args.txt`
L1SIZE_3=`cut -f11 -d " " args.txt`
L1WAYS_3=`cut -f12 -d " " args.txt`
L1SIZE_4=`cut -f13 -d " " args.txt`
L1WAYS_4=`cut -f14 -d " " args.txt`

L2SIZE_1=`cut -f15 -d " " args.txt`
L2WAYS_1=`cut -f16 -d " " args.txt`
L2SIZE_2=`cut -f17 -d " " args.txt`
L2WAYS_2=`cut -f18 -d " " args.txt`

L3SIZE=`cut -f19 -d " " args.txt`
L3WAYS=`cut -f20 -d " " args.txt`
DRAM_TECH=`cut -f21 -d " " args.txt`
CORE_DYN_ENERGY=`cut -f22 -d " " args.txt`
CORE_STA_ENERGY=`cut -f23 -d " " args.txt`

l1_1=`cut -f24 -d " " args.txt`
l1_2=`cut -f25 -d " " args.txt`
l1_3=`cut -f26 -d " " args.txt`
l1_4=`cut -f27 -d " " args.txt`
l2_1=`cut -f28 -d " " args.txt`
l2_2=`cut -f29 -d " " args.txt`
l3=`cut -f30 -d " " args.txt`

T=`cut -f31 -d " " args.txt`
PID=`cut -f32 -d " " args.txt`
COREID=`cut -f33 -d " " args.txt`

IPC=`cut -f34 -d " " args.txt`

## Run CACTI 6.5 to get cache parameters
L1_CACTI_big=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZE_1 -w $L1WAYS_1`
L1_CACTI_mid1=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZE_2 -w $L1WAYS_2`
L1_CACTI_mid2=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZE_3 -w $L1WAYS_3`
L1_CACTI_little=`sh $MAIN_PATH/gen_cacti.sh -s $L1SIZE_4 -w $L1WAYS_4`

L2_CACTI_big=`sh $MAIN_PATH/gen_cacti.sh -s $L2SIZE_1 -w $L2WAYS_1`
L2_CACTI_mid1=`sh $MAIN_PATH/gen_cacti.sh -s $L2SIZE_2 -w $L2WAYS_2`

L3_CACTI=`sh $MAIN_PATH/gen_cacti.sh -s $L3SIZE -w $L3WAYS`

echo $L1_CACTI_big > cacti_L1_big.txt
echo $L1_CACTI_mid1 > cacti_L1_mid1.txt
echo $L1_CACTI_mid2 > cacti_L1_mid2.txt
echo $L1_CACTI_little > cacti_L1_little.txt
echo $L2_CACTI_big > cacti_L2_big.txt
echo $L2_CACTI_mid1 > cacti_L2_mid1.txt
echo $L3_CACTI > cacti_L3.txt

L1_ENERGY_1=`cut -f6 -d " " cacti_L1_big.txt`
L1_POWER_1=`cut -f7 -d " " cacti_L1_big.txt`
L1_ENERGY_2=`cut -f6 -d " " cacti_L1_mid1.txt`
L1_POWER_2=`cut -f7 -d " " cacti_L1_mid1.txt`
L1_ENERGY_3=`cut -f6 -d " " cacti_L1_mid2.txt`
L1_POWER_3=`cut -f7 -d " " cacti_L1_mid2.txt`
L1_ENERGY_4=`cut -f6 -d " " cacti_L1_little.txt`
L1_POWER_4=`cut -f7 -d " " cacti_L1_little.txt`
L1_AREA_1=`cut -f8 -d " " cacti_L1_big.txt`      # L1 area
L1_AREA_2=`cut -f8 -d " " cacti_L1_mid1.txt`     #
L1_AREA_3=`cut -f8 -d " " cacti_L1_mid2.txt`     #   
L1_AREA_4=`cut -f8 -d " " cacti_L1_little.txt`   #

L2_ENERGY_1=`cut -f6 -d " " cacti_L2_big.txt`
L2_POWER_1=`cut -f7 -d " " cacti_L2_big.txt`
L2_ENERGY_2=`cut -f6 -d " " cacti_L2_mid1.txt`
L2_POWER_2=`cut -f7 -d " " cacti_L2_mid1.txt`
L2_AREA_1=`cut -f8 -d " " cacti_L2_big.txt`      # L2 area
L2_AREA_2=`cut -f8 -d " " cacti_L2_mid1.txt`     #

L3_ENERGY=`cut -f6 -d " " cacti_L3.txt`
L3_POWER=`cut -f7 -d " " cacti_L3.txt`
L3_AREA=`cut -f8 -d " " cacti_L3.txt`            # L3 area

CORES=`echo $CORES_1+$CORES_2+$CORES_3+$CORES_4 | bc -l`

# Beefy L1 cache energy
if [ "$COREID" = "0" ]
then
    L1_STA_ENERGY=`echo "$L1_POWER_1/1000*$TIME" | bc -l`
    L2_STA_ENERGY=`echo "$L2_POWER_1/1000*$TIME" | bc -l`
elif [ "$COREID" = "1" ]   
then 
    L1_STA_ENERGY=`echo "$L1_POWER_2/1000*$TIME" | bc -l`
    L2_STA_ENERGY=`echo "$L2_POWER_2/1000*$TIME" | bc -l`
elif [ "$COREID" = "2" ]
then
    L1_STA_ENERGY=`echo "$L1_POWER_3/1000*$TIME" | bc -l`
    L2_STA_ENERGY=`echo "0" | bc -l`
elif [ "$COREID" = "3" ]
then
    L1_STA_ENERGY=`echo "$L1_POWER_4/1000*$TIME" | bc -l`
    L2_STA_ENERGY=`echo "0" | bc -l`
else    
    L1_STA_ENERGY=`echo "($CORES_1*$L1_POWER_1+$CORES_2*$L1_POWER_2+$CORES_3*$L1_POWER_3+$CORES_4*$L1_POWER_4)/1000*$TIME" | bc -l`
    L2_STA_ENERGY=`echo "($CORES_1*$L2_POWER_1+$CORES_2*$L2_POWER_2)/1000*$TIME" | bc -l`
fi


L1_DYN_ENERGY=`echo "($l1_1*$L1_ENERGY_1+$l1_2*$L1_ENERGY_2+$l1_3*$L1_ENERGY_3+$l1_4*$L1_ENERGY_4)/1000000000" | bc -l`
L2_DYN_ENERGY=`echo "($l2_1*$L2_ENERGY_1+$l2_2*$L2_ENERGY_2)/1000000000" | bc -l`
L3_DYN_ENERGY=`echo "$l3*$L3_ENERGY/1000000000" | bc -l`
L3_STA_ENERGY=`echo "$L3_POWER/1000*$TIME" | bc -l`

MEM_RD=`grep -w rd zsim-$PID-$COREID.out | awk '{print $2}' | paste -sd+ | bc`
MEM_WR=`grep -w wr zsim-$PID-$COREID.out | awk '{print $2}' | paste -sd+ | bc`

#echo "python /afs/ir/class/ee282/pa2/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME"
#MEM_DYN_ENERGY=`python /afs/ir/class/ee282/pa1/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME false`
#MEM_STA_ENERGY=`python /afs/ir/class/ee282/pa1/bin/mem.py $DRAM_TECH $MEM_RD $MEM_WR $TIME true`
MEM_DYN_ENERGY=`echo "200*($MEM_RD+$MEM_WR)/1000000000" | bc -l`
MEM_STA_ENERGY=`echo "50.63/1000*$TIME" | bc -l`

TOTAL_ENERGY=`echo $CORE_DYN_ENERGY+$CORE_STA_ENERGY+$L1_DYN_ENERGY+$L1_STA_ENERGY+$L2_DYN_ENERGY+$L2_STA_ENERGY+$L3_DYN_ENERGY+$L3_STA_ENERGY+$MEM_DYN_ENERGY+$MEM_STA_ENERGY | bc -l`
EDP=`echo $TOTAL_ENERGY*$TIME | bc -l`

TOTAL_POWER=`echo $TOTAL_ENERGY/$TIME | bc -l`

ENERGY_DELAY_PRODUCT=`echo $TIME*$TOTAL_ENERGY | bc -l`

echo "$PID $COREID $T $TOTAL_POWER $IPC" >> profile.txt

