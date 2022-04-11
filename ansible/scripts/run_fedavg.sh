set -eu

cd FedML/data/cifar10

if [ ! -e cifar-10-python.tar.gz ]; then
    sh download_cifar10.sh
fi

cd ~/FedML/fedml_experiments/distributed/fedavg

# 実際の物理ネットワークトポロジに対応するように変更　めんどい、、
echo localhost:1 > mpi_host_file

mpirun -np $PROCESS_NUM -hostfile ./mpi_host_file python3 ./main_fedavg.py \
  --gpu_server_num $SERVER_NUM \
  --gpu_num_per_server $GPU_NUM_PER_SERVER \
  --model $MODEL \
#   --dataset $DATASET \
#   --data_dir $DATA_DIR \
#   --partition_method $DISTRIBUTION  \
  --client_num_in_total $CLIENT_NUM \
  --client_num_per_round $WORKER_NUM \
  --comm_round $ROUND \
  --epochs $EPOCH \
  --client_optimizer $CLIENT_OPTIMIZER \
  --batch_size $BATCH_SIZE \
  --lr $LR \
  --ci $CI




sh run_fedavg_distributed_pytorch.sh 10 1 8 1 resnet56 homo 100 20 64 0.001 cifar10 "./../../../data/cifar10"

    parser.add_argument('--model', type=str, default='mobilenet', metavar='N',
                        help='neural network used in training')

    # parser.add_argument('--dataset', type=str, default='cifar10', metavar='N',
    #                     help='dataset used for training')

    # parser.add_argument('--data_dir', type=str, default='./../../../data/cifar10',
    #                     help='data directory')

    # parser.add_argument('--partition_method', type=str, default='hetero', metavar='N',
    #                     help='how to partition the dataset on local workers')

    parser.add_argument('--partition_alpha', type=float, default=0.5, metavar='PA',
                        help='partition alpha (default: 0.5)')

    parser.add_argument('--client_num_in_total', type=int, default=1000, metavar='NN',
                        help='number of workers in a distributed cluster')

    parser.add_argument('--client_num_per_round', type=int, default=4, metavar='NN',
                        help='number of workers')

    parser.add_argument('--batch_size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')

    parser.add_argument('--client_optimizer', type=str, default='adam',
                        help='SGD with momentum; adam')

    parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
                        help='learning rate (default: 0.001)')

    parser.add_argument('--wd', help='weight decay parameter;', type=float, default=0.001)

    parser.add_argument('--epochs', type=int, default=5, metavar='EP',
                        help='how many epochs will be trained locally')

    parser.add_argument('--comm_round', type=int, default=10,
                        help='how many round of communications we shoud use')

    parser.add_argument('--is_mobile', type=int, default=0,
                        help='whether the program is running on the FedML-Mobile server side')

    parser.add_argument('--frequency_of_the_test', type=int, default=1,
                        help='the frequency of the algorithms')

    parser.add_argument('--gpu_server_num', type=int, default=1,
                        help='gpu_server_num')

    parser.add_argument('--gpu_num_per_server', type=int, default=4,
                        help='gpu_num_per_server')

    parser.add_argument('--ci', type=int, default=0,
                        help='CI')