source ./env.sh
cd ~/cs316/parsec-3.0/
source ./env.sh
echo $PARSECDIR
parsecmgmt -a build -p blackscholes
parsecmgmt -a build -p bodytrack
parsecmgmt -a build -p facesim
parsecmgmt -a build -p ferret
parsecmgmt -a build -p fluidanimate
parsecmgmt -a build -p freqmine
parsecmgmt -a build -p raytrace
parsecmgmt -a build -p swaptions
parsecmgmt -a build -p vips
parsecmgmt -a build -p x264
cd ~/cs316/zsim_build/downloads/zsim/workspace/
