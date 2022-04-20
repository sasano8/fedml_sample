set -eu

cd ~/FedML/fedml_experiments/distributed/fedavg

source "$HOME/miniconda/etc/profile.d/conda.sh"
conda activate fedml
conda install -c main debugpy

mpirun -np 2 -hostfile ./mpi_host_file python3 -m debugpy --wait-for-client --listen 5678 \
  ./main_fedavg.py \
  --gpu_mapping_file "gpu_mapping.yaml" \
  --gpu_mapping_key "mapping_default" \
  --model resnet18_gn \
  --data_dir ./../../../data/fed_cifar100/datasets \
  --dataset fed_cifar100 \
  --partition_method hetero  \
  --client_num_in_total 1 \
  --client_num_per_round 1 \
  --comm_round 1000 \
  --batch_size 1 \
  --epochs 1 \
  --lr 0.03 \
  --client_optimizer adam \
  --ci 0
