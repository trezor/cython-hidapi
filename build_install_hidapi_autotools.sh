#!/usr/bin/env bash

set -e
set +x

pushd hidapi
./bootstrap
./configure
make
sudo make install
popd
