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


## インフラ構築

### NFS（ネットワークファイルシステム）構成

```
秘密鍵公開鍵を置いてsshログインできるようにする
```


## ソフトウェア構築

```
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh
bash Miniconda3-py38_4.11.0-Linux-x86_64.sh -b -p $HOME/miniconda
```

```
conda install pytorch torchvision cudatoolkit=10.2 -c pytorch
```

```
conda install -c anaconda mpi4py
```

```
pip install --upgrade wandb
```

```
git clone https://github.com/FedML-AI/FedML.git
cd FedML/fedml_experiments/distributed
pip install -r requirements.txt
```

## Setup Server(GUI)

これに従えばできるっぽい？

python3.7を対象としているので書き換える

- [CI-install.sh](https://github.com/FedML-AI/FedML/blob/master/CI-install.sh)
    - install miniconda
    - install dependencies
    - download sample data


- [CI-script-fedavg.sh](https://github.com/FedML-AI/FedML/blob/master/CI-script-fedavg.sh)
    - run [run_fedavg_standalone_pytorch.sh](https://github.com/FedML-AI/FedML/blob/master/fedml_experiments/standalone/fedavg/run_fedavg_standalone_pytorch.sh)
        - fedavg


## Setup Edge

1. install client agent and login
2. invite collaborators and group management
3. project management

https://doc.fedml.ai/user_guide/mlops/mlops_workflow_step_by_step.html


事前にアカウントを登録しaccount_idを取得します

```
https://open.fedml.ai/#/login?isRegister=true
```

dockerをインストールします

```
...
```

```
git clone https://github.com/FedML-AI/fedml_edge_deployment
cd fedml_edge_deployment

# start to pull docker image and run the FL Client Agent
./run.sh $account_id
```