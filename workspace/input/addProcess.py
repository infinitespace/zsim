'''
Note: need to modify addProcess() function to customize your process
Usage:
    input:
        python addProcess.py ../config/het_no_proc.cfg
    output:
        ../config/het_no_proc_added.cfg
'''
import sys
import os
import pprint
import shutil

LIBRARY_PATH = os.path.abspath(os.path.realpath('../energy'))
sys.path.append(LIBRARY_PATH)

import parse_cfg as ps


def addProcess(procs):
    workload_small(procs)

def workload_small(procs):
    procs.append("parsecmgmt -a run -p blackscholes")
    #procs.append("parsecmgmt -a run -p bodytrack")
    #procs.append("parsecmgmt -a run -p streamcluster")



def workload_medium(procs):
    procs.append("parsecmgmt -a run -p bodytrack")
    procs.append("parsecmgmt -a run -p streamcluster")
    procs.append("parsecmgmt -a run -p x264")


def workload_large(procs):
    procs.append("parsecmgmt -a run -p facesim")
    procs.append("parsecmgmt -a run -p fluidanimate")


def workload_huge(procs):
    procs.append("parsecmgmt -a run -p ferret")
    procs.append("parsecmgmt -a run -p canneal")
    procs.append("parsecmgmt -a run -p freqmine")


def loadCfgFile(filename):
    config = ps.parse(filename)
    # pprint.pprint(config, depth=2)
    if(config.has_key('process0')):
        print "Error: Input .cfg file already have a process!"
    else:
        procs = []
        addProcess(procs)
        # print procs
        outputToFile(procs, filename)

def outputToFile(procs, orgfile):
    postFix = "_added.cfg"
    newfile = orgfile.split('.cfg')[0] + postFix
    print "Load cfg file from: " + orgfile
    print "Write cfg file to: " + newfile
    if os.path.isfile(newfile):
        print "Error: Output .cfg file already exist!"
    else:
        try:
            shutil.copyfile(orgfile, newfile)
            f = open(newfile, 'a')
            for i in range(len(procs)):
                f.write("process" + str(i) + " = {" + '\n')
                f.write("    command = \"")
                f.write(procs[i])
                f.write("\";\n")
                f.write("};\n")
            print "Successfully add processes to a new .cfg file"
        except:
            print "Error: failed at writting the new file"
            if os.path.isfile(newfile):
                os.remove(newfile)

if __name__ == '__main__':
    loadCfgFile(sys.argv[1])
