#!/bin/bash
cd run

declare -a app=("final-0" "final-0" "final-0" "final-0" "final-1" "final-1" "final-1" "final-1" "final-2" "final-2" "final-2" "final-2" "final-3" "final-3" "final-4" "final-4" "final-5" "final-5" "final-5" "final-5" "final-6" "final-6" "final-6" "final-6" "final-7" "final-7" "final-7" "final-7" "final-8" "final-8" "final-8" "final-8")

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
for j in 3
do

  mv ../config/map_type_$j.dat ../config/map.dat

  for i in `seq 0 31`;
  do
      echo "====================================================================="
      echo "i = "
      echo $i
      echo "j = "
      echo $j
      echo "====================================================================="

      ../../../../zsim ../config/${app[i]}.cfg 
  
      mv zsim-ev.h5 zsim-ev-$i-$j.h5
      mv zsim.out zsim-$i-$j.out
      rm -f *.fluid
  done

  mv ../config/map.dat ../config/map_type_$j.dat    

done
cd ..
