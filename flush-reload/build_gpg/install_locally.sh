#!/bin/bash
# Use this script if you are using Linux or if OS X Homebrew is not installed.

set -o errexit
set -o nounset
set -o xtrace

GPG_PREFIX=gnupg-1.4.13
GPG_ARCHIVE=${GPG_PREFIX}.tar.bz2
export CC=gcc   # If building on OS X, you will need apple-gcc42
export CFLAGS="-g -O2"

curl -O https://gnupg.org/ftp/gcrypt/gnupg/${GPG_ARCHIVE}
tar xf ${GPG_ARCHIVE}
rm ${GPG_ARCHIVE}

cd ${GPG_PREFIX}
./configure --disable-dependency-tracking --disable-asm --prefix="${PWD}"
make && make check && make install
