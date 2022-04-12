#!/usr/bin/env bash
set -eu

cd ~

if [ ! -e FedML ]; then
        git clone https://github.com/FedML-AI/FedML.git FedML
fi


source miniconda/bin/activate

pip3 install --upgrade wandb
# 何のためのID?
# wandb login ee0b5f53d949c84cee7decbe7a629e63fb2f8408

cd FedML
# cd fedml/fedml_experiments/distributed
pip3 install -r requirements.txt




