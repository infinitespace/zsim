#!/bin/bash

set -e

L1_ENERGY=`cut -f6 -d " " cacti_L1_beefy.txt`
L1_POWER=`cut -f7 -d " " cacti_L1_beefy.txt`
L2_ENERGY=`cut -f6 -d " " cacti_L2.txt`
L2_POWER=`cut -f7 -d " " cacti_L2.txt`
L2_AREA=`cut -f8 -d " " cacti_L2.txt`
L3_ENERGY=`cut -f6 -d " " cacti_L3.txt`
L3_POWER=`cut -f7 -d " " cacti_L3.txt`
L3_AREA=`cut -f8 -d " " cacti_L3.txt`

echo "L1 ENERGY (J): $L1_ENERGY"
