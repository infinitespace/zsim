#!/usr/bin/bash
# sh ProfileApplication.sh het.cfg


find . -name 'zsim-ev-[0-9]-[0-9].h5' | while read line; do
     sh energy_profile.sh $line $1
done
