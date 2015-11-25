run zsim under run director

0. directory explaination:
	config: zsim.cfg files, and CPU map config files
	energy: energy model files for zsim output
	input: python scripts to add process to zsim cfg files
	map: python scripts to generate CPU map files

1. build application
parsecmgmt -a build -p blackscholes

2. run zsim
cd workspace
. env.sh
cd run
zsim ../config/het.sfg

3. rebuild zsim
cd workspace
sh zsim_rebuild.sh


