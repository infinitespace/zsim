#!/bin/bash
#
# This is a script that will install zsim to 'INST_DIR' which by default is
# the directory 'zsim' where the script is located.
#
# This script assumes that you have gcc, make, cmake, scons, libhdf5, and
# libelfg0 installed in your system, and that you are using Ubuntu 14.04.
# It also assumes that /proc/sys/kernel/shmmax is >= 1GB and that
# /proc/sys/kernel/yama/ptrace_scope is 0.
#
# If the above conditions are true, you should have no problem building and
# running zsim.


# Directory in which zsim will be built and installed
INST_DIR="./zsim_build"


#### No need to modify below ####
set -e

# Package versions
PIN="pin-2.14-71313-gcc.4.4.7-linux"
LIBCONFIG="libconfig-1.5"
POLARSSL="polarssl-1.2.17"

printf "\nThis is a zsim installation script installing to '${INST_DIR}'\n"
printf "Please ensure that your system has the following packages:\n"
printf "   - gcc/g++\n"
printf "   - make\n"
printf "   - cmake\n"
printf "   - scons\n"
printf "   - libhdf5\n"
printf "   - libelfg0\n"
printf "\nStarting in 5 seconds...\n"
sleep 5

BASE_DIR="$(readlink -f .)"

# Package download URLs
# ZSIM_URL="https://github.com/s5z/zsim"
ZSIM_URL="https://github.com/infinitespace/zsim.git"
PIN_URL="http://software.intel.com/sites/landingpage/pintool/downloads/${PIN}.tar.gz"
LIBCONFIG_URL="http://www.hyperrealm.com/libconfig/${LIBCONFIG}.tar.gz"
POLARSSL_URL="https://tls.mbed.org/download/${POLARSSL}-gpl.tgz"

#### Download the packages ####
DOWNLOAD_DIR="${INST_DIR}/downloads"
if [ -d "${DOWNLOAD_DIR}" ]; then
    echo "Error: Download directory '${DOWNLOAD_DIR}' already exists!"
    exit 1
fi
echo "Downloading packages to '${DOWNLOAD_DIR}'..."
mkdir -p "${DOWNLOAD_DIR}"
git clone "${ZSIM_URL}" "${DOWNLOAD_DIR}/zsim"
wget -P "${DOWNLOAD_DIR}" --no-use-server-timestamps "${PIN_URL}"
wget -P "${DOWNLOAD_DIR}" --no-use-server-timestamps "${LIBCONFIG_URL}"
wget -P "${DOWNLOAD_DIR}" --no-use-server-timestamps "${POLARSSL_URL}"

echo "Unpacking..."
tar -C "${DOWNLOAD_DIR}" -xzf "${DOWNLOAD_DIR}/$(basename ${PIN_URL})"
tar -C "${DOWNLOAD_DIR}" -xzf "${DOWNLOAD_DIR}/$(basename ${LIBCONFIG_URL})"
tar -C "${DOWNLOAD_DIR}" -xzf "${DOWNLOAD_DIR}/$(basename ${POLARSSL_URL})"

#### Build libconfig ####
LIBCONFIG_DIR="${DOWNLOAD_DIR}/${LIBCONFIG}"
if [ ! -d "${LIBCONFIG_DIR}" ]; then
    echo "Error: Libconfig extraction failed."
    exit 1
fi
echo "Building libconfig..."
LIBCONFIG_INST_DIR="$(readlink -f ${INST_DIR})"
cd "${LIBCONFIG_DIR}" && ./configure --prefix="${LIBCONFIG_INST_DIR}" && make -j8 && make install
cd "${BASE_DIR}"

#### Build PolarSSL ####
POLARSSL_DIR="${DOWNLOAD_DIR}/${POLARSSL}"
if [ ! -d "${POLARSSL_DIR}" ]; then
    echo "Error: PolarSSL extraction failed."
    exit 1
fi
echo "Building PolarSSL..."
POLARSSL_INST_DIR="$(readlink -f ${INST_DIR})"
sed -i 's/-Wextra/-Wextra -fPIC/' "${POLARSSL_DIR}/CMakeLists.txt"
cd "${POLARSSL_DIR}" && cmake "-DCMAKE_INSTALL_PREFIX:PATH=${POLARSSL_INST_DIR}" "-DENABLE_PROGRAMS=OFF" . && make -j8 && make install
cd "${BASE_DIR}"

#### Build zsim ####
echo "Building zsim..."
export PINPATH="$(readlink -f ${DOWNLOAD_DIR}/${PIN})"
export LIBCONFIGPATH="$(readlink -f ${INST_DIR})"
export POLARSSLPATH="$(readlink -f ${INST_DIR})"
cd "${DOWNLOAD_DIR}/zsim" && scons -j8
cd "${BASE_DIR}"
ln -s "$(readlink -f ${DOWNLOAD_DIR}/zsim/build/opt/zsim)" "${INST_DIR}/zsim"

#### Finished ####
printf "\nFinished. zsim is in '${DOWNLOAD_DIR}/zsim/build/opt' and linked to '${INST_DIR}/zsim'.\n"
