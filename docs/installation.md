# Installation

## 構成要件

https://doc.fedml.ai/user_guide/open_source/installation.html


- ヘッドノード（ログイン・テスト用）が必要
- N個のcomupute node（multi-GPU server: e.g., 8 x NVIDIA V100）が必要
- NFSなどの一元化されたフォールトトレラントファイルサーバー必要（計算ノード間で大規模なデータセットを共有）中央集権型の分散アルゴリズムを使わないのなら必要ではない？？


### Software

- Python >= 3.7.4
- MPI4Py >= 3.0.3: Message Passing Interface (MPI) 規格の Python バインディング
- PyTorch >= 1.4.0: PyTorchが提供する分散コンピューティング機械学習はMPIを使っている

- https://mpi4py.readthedocs.io/en/stable/


### 疑問

連合学習ではデータ共有が不要なのになぜNFSが必要か？


## 環境構築

### NFS（ネットワークファイルシステム）構成

```
秘密鍵公開鍵を置いてsshログインできるようにする
```



## バッチ実行

```
GPU=$1

DATASET=$2

# homo; hetero
DISTRIBUTION=$3

ROUND=$4

EPOCH_CLIENT=$5

EPOCH_SERVER=$6

OPTM=$7

LR=$8

TRAIN_OR_NOT=$9

DISTILL_ON_SERVER=$10

CLIENT_MODEL=$11

NAME=$12

DATA_DIR=$13

BATCH_SIZE=$14

hostname > mpi_host_file

mpirun -np 9 -hostfile ./mpi_host_file python3 ./main_fedgkt.py \
--gpu $GPU \
--dataset $DATASET \
--data_dir $DATA_DIR \
--partition_method $DISTRIBUTION  \
--client_number 8 \
--client_model $CLIENT_MODEL \
--comm_round $ROUND \
--epochs_client $EPOCH_CLIENT \
--epochs_server $EPOCH_SERVER \
--batch_size $BATCH_SIZE \
--optimizer $OPTM \
--lr $LR \
--weight_init_model resnet32 \
--whether_training_on_client $TRAIN_OR_NOT \
--whether_distill_on_the_server $DISTILL_ON_SERVER \
--running_name $NAME \
--multi_gpu_server

```