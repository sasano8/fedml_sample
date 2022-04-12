#!/usr/bin/env bash
set -eu

cd ~

if [ ! -e FedML ]; then
        git clone https://github.com/FedML-AI/FedML.git FedML
fi


source miniconda/bin/activate

cd FedML
# cd fedml/fedml_experiments/distributed
pip3 install -r requirements.txt




