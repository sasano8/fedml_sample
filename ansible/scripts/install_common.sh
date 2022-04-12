#!/usr/bin/env bash
set -eu

cd ~

# sudo apt-get install -y python3-pip
pip3 --version

if [ ! -e `pwd`/miniconda ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh -O Miniconda3-py38_4.11.0-Linux-x86_64.sh
    # mkdir -p miniconda
    bash Miniconda3-py38_4.11.0-Linux-x86_64.sh -b -p `pwd`/miniconda
    miniconda/bin/conda init bash
fi

source miniconda/bin/activate

conda install -y pytorch=1.7.1 torchvision cudatoolkit=11.0 -c pytorch
conda install -y -c anaconda mpi4py h5py
# mpi4py:  mpi通信に必要
# h5py: HDF5（階層的データ形式フォーマットファイル）を取り扱うライブラリ

# 学習＆結果のモニタリング
pip3 install --upgrade wandb
# 何のためのID?
# wandb login ee0b5f53d949c84cee7decbe7a629e63fb2f8408