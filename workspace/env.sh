# kinit wenbo6@stanford.edu && aklog
export CONF_DIR=/afs/.ir/users/w/e/wenbo6/cs316/zsim_build/downloads/zsim/workspace/config
cd ~/cs316/zsim_build/
export INST_DIR=$PWD
cd ~/cs316/zsim_build/downloads/zsim/workspace
export PATH=~/cs316/zsim_build/:$PATH
export PARSECDIR=~/cs316/parsec-3.0

# Package versions
export PIN="pin-2.14-71313-gcc.4.4.7-linux"
export LIBCONFIG="libconfig-1.5"
export POLARSSL="polarssl-1.2.17"
export DOWNLOAD_DIR="${INST_DIR}/downloads"

export LIBCONFIG_DIR="${DOWNLOAD_DIR}/${LIBCONFIG}"
export LIBCONFIG_INST_DIR="$(readlink -vf ${INST_DIR})"

export POLARSSL_DIR="${DOWNLOAD_DIR}/${POLARSSL}"
export POLARSSL_INST_DIR="$(readlink -vf ${INST_DIR})"
export PINPATH="$(readlink -vf ${DOWNLOAD_DIR}/${PIN})"
export LIBCONFIGPATH="$(readlink -vf ${INST_DIR})"
export POLARSSLPATH="$(readlink -vf ${INST_DIR})"

