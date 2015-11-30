#!/bin/bash
cd run2

declare -a app=("blackscholes" "streamcluster" "freqmine" "fluidanimate" "canneal")

#for j in "${app[@]}"

#for i in 0 1 2 3
#do
#    mv ../config/map_type_$i.dat ../config/map.dat
#    ../../../../zsim ../config/simple.cfg    
#
#    mv ../config/map.dat ../config/map_type_$i.dat    
#    mv zsim-ev.h5 zsim-ev-$i.h5
#done
#cd ..
for j in 0 1 2 3
do

  mv ../config/map_type_$j.dat ../config/map.dat

  for i in 0 1 2 3 4
  do
      echo "====================================================================="
      echo "i = "
      echo $i
      echo "j = "
      echo $j
      echo "====================================================================="

      ../../../../zsim ../config/${app[i]}.cfg    
  
      mv zsim-ev.h5 zsim-ev-big-$i-$j.h5
      mv zsim.out zsim-big-$i-$j.out
  done

  mv ../config/map.dat ../config/map_type_$j.dat    

done
cd ..
