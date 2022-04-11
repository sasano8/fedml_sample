set -eu

if [ ! -e `pwd`/miniconda ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh -O Miniconda3-py38_4.11.0-Linux-x86_64.sh
    # mkdir -p miniconda
    bash Miniconda3-py38_4.11.0-Linux-x86_64.sh -b -p `pwd`/miniconda
    miniconda/bin/conda init bash
fi

source miniconda/bin/activate
conda install -y pytorch=1.7.1 torchvision cudatoolkit=11.0 -c pytorch
conda install -y -c anaconda mpi4py
pip install --upgrade wandb