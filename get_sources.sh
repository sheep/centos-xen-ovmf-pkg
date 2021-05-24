#!/bin/bash

set -e

filename=$(rpmspec -q --srpm --define "dist .el7" --queryformat '[%{SOURCE}\n]' SPECS/xen-ovmf.spec | grep '^edk2')
if [[ "$filename" =~ ^edk2-([a-f0-9]+)\.tar\.gz ]]; then
  EDK2_CSET="${BASH_REMATCH[1]}"
else
  echo >&2 "Failed to find git commit to use"
  exit 1
fi

EDK2_URL=https://github.com/tianocore/edk2.git
EDK2_FILE=edk2-$EDK2_CSET.tar.gz

archive_submodule() {
    local name=$1
    local subdir=$2

    echo "Creating $name archive..."
    git submodule update --init $subdir
    local cset="$(git submodule status $subdir | sed -r 's/^.([0-9a-f]{40}) .*/\1/')"
    local source_file="$name-$cset.tar.gz"
    pushd "$subdir"
    git archive --prefix="edk2/$subdir/" -o "$rootdir/SOURCES/$source_file" $cset || exit 1
    popd
}

echo "Checking edk2 (tianocore)..."
if [[ ! -e SOURCES/$EDK2_FILE ]] ; then
    rootdir=`pwd`
    echo "Cloning tianocore repo..."
    mkdir -p git-tmp
    mkdir -p SOURCES
    pushd git-tmp

    git clone $EDK2_URL edk2.git || exit 1
    cd edk2.git

    archive_submodule brotly-tool BaseTools/Source/C/BrotliCompress/brotli
    archive_submodule openssl CryptoPkg/Library/OpensslLib/openssl
    archive_submodule brotly-library MdeModulePkg/Library/BrotliCustomDecompressLib/brotli

    echo "Creating $EDK2_FILE..."
    git archive --prefix=edk2/ -o ../../SOURCES/$EDK2_FILE $EDK2_CSET || exit 1

    popd
fi

if [[ -e git-tmp ]] ; then
    echo "Cleaning up cloned repositores"
    rm -rf git-tmp
fi

echo "All sources present."
