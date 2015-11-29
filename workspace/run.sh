#!/bin/bash
cd run

declare -a app=("blackscholes" "streamcluster" "ferret" "freqmine"
"fluidanimate" "canneal")

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

  for i in 2 3 4 5
  do
      echo "====================================================================="
      echo "i = "
      echo $i
      echo "j = "
      echo $j
      echo "====================================================================="

      ../../../../zsim ../config/${app[i]}.cfg    
  
      mv zsim-ev.h5 zsim-ev-$i-$j.h5
  done

  mv ../config/map.dat ../config/map_type_$j.dat    

done
cd ..
