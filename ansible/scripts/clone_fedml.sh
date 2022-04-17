#!/usr/bin/env bash
set -eu

cd ~

if [ ! -e FedML ]; then
        git clone https://github.com/FedML-AI/FedML.git FedML
fi
