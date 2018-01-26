#!/bin/bash

EDK2_URL=https://github.com/tianocore/edk2.git
EDK2_CSET=bc54e50e0fe03c570014f363b547426913e92449
EDK2_FILE=edk2-$EDK2_CSET.tar.gz

echo "Checking edk2 (tianocore)..."
if [[ ! -e SOURCES/$EDK2_FILE ]] ; then
    echo "Cloning tianocore repo..."
    mkdir -p git-tmp
    pushd git-tmp

    git clone $EDK2_URL edk2.git || exit 1
    cd edk2.git
    echo "Creating $EDK2_FILE..."
    git archive --prefix=edk2/ -o ../../SOURCES/$EDK2_FILE $EDK2_CSET || exit 1
    popd
fi

if [[ -e git-tmp ]] ; then
    echo "Cleaning up cloned repositores"
    rm -rf git-tmp
fi

echo "All sources present."
