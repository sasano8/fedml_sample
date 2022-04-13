cd ~/FedML/data/cifar10
sh download_cifar10.sh

cd ~/FedML/fedml_experiments/distributed/fedavg


vi mpi_host_file
127.0.0.1:1

wandb_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
wandb login $wandb_token


# No module named 'joblib'
conda install -y -c anaconda joblib


rm -rf ~/FedML/.vscode
cp -r ~/scripts/.vscode ~/FedML/