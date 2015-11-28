#!/usr/bin/bash

echo "PID       Core_type    Throughput         Total Power(W)" >> profile.txt
find . -name 'zsim-ev-[0-9]-[0-9].h5' | while read line; do
     sh energy_profile.sh $line $1
done
