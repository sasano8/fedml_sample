set -eu

cd ~

if [ ! -e FedML ]; then
        git clone https://github.com/FedML-AI/FedML.git
fi

cd FedML
# cd fedml/fedml_experiments/distributed
pip install -r requirements.txt

# conda install nomkl
# conda install mkl=2018.0.2
conda install -y h5py  # HDF5 フォーマットファイルを取り扱うライブラリ

# 何のためのID?
wandb login ee0b5f53d949c84cee7decbe7a629e63fb2f8408
