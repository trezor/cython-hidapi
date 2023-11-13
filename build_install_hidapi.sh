#!/bin/bash

set -e
set +x

rm -rf hidapi_build
mkdir -p hidapi_build
pushd hidapi_build
cmake -GNinja -B . -S ../hidapi
ninja
sudo ninja install
popd
