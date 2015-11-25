#!/bin/bash

#declare -a num=("1" "2" "3" "4" "5" "6" "7" "8" "9" "d")
cd run

for i in 0 1 2 3
do
    mv ../config/map_type_$i.dat ../config/map.dat
    ../../../../zsim ../config/simple.cfg    

    mv ../config/map.dat ../config/map_type_$i.dat    
    mv zsim-ev.h5 zsim-ev-$i.h5
    
done
cd ..
