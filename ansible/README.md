# クラスター構築

クラスタ構築手順を記します。

公式手順は次を参照ください。

- [Fedml installation](https://doc.fedml.ai/user_guide/open_source/installation/installation-distributed-computing.html)


## 構成要件

必要となるマシンの最低スペックは次の通りです。
データ容量が大きいためできるだけ大きめの容量を確保するのをおススメします。


- nfs:
    - Volume: 30GB ~
    - memo: モデルを共有するためファイルストレージが1台必要です

- head:
    - OS: Ubuntu20.04
    - Volume: 30GB ~
    - memo:
        - nodes（計算ノード）の管理用ホストが1台必要です
        - 機械学習に関するライブラリ一式がインストールされます。

- nodes:
    - OS: Ubuntu20.04
    - Volume: 30GB ~
    - memo:
        - 計算ノードです
        - 計算ノードは複数台構成できます
        - 機械学習に関するライブラリ一式がインストールされます。

- ansible（オプション）:
    - OS: Ubuntu20.04
    - Volume: 5GB ~
    - memo: nfs/head/nodesに対して、一括でスクリプトを配布、構成変更するためansibleという構成管理ソフトを使用します。ansibleを使用しない場合は、手動で構成する必要があります。


## 通信要件

- nfs:
    - ssh接続が許可されていること
- head:
    - ?
- nodes:
    - nfsへssh接続が可能であること
- ansible:
    - nfs, head, nodesへssh接続が可能であること


## 検証環境構築


### 事前準備

本手順では、multipassで仮想マシンを準備します。

ストレージの保存場所を変更したい場合は、powershellを管理者で起動し次のコマンドを実行してください。

``` powershell
PS> Stop-Service Multipass
PS> Set-ItemProperty -Path "HKLM:System\CurrentControlSet\Control\Session Manager\Environment" -Name MULTIPASS_STORAGE -Value "D:/vhd"
PS> Start-Service Multipass
```


### スタンドアロン

nfs, head, nodes, ansibleを１台のホスト上に構築する例を示します。


仮想マシンを用意します。
この例では、仮想マシンの準備にmultipassを使用しますが、任意のソフトウェアを使ってかまいません。

``` shell
multipass launch 20.04 --cpus 1 --mem 1G --disk 20G --name fedml
multipass shell fedml
```

```
# CPUの数
grep physical.id /proc/cpuinfo | sort -u | wc -l

# CPUごとのコア数
grep cpu.cores /proc/cpuinfo | sort -u

# メモリ（GB表示）
free -g
```

デフォルトのユーザであるubuntuをansible実行ホストとみなします。

加えて、nfs用ユーザ、head用ユーザ、nodesユーザを作成し、通信要件を満たすようにssh接続設定を行います。
ここでは、head用ユーザ、nodesユーザはfedmlというユーザで兼任することとします。

``` shell
whoami  # ubuntu

sudo useradd -m -d /home/nfs -s /bin/bash nfs
sudo useradd -m -d /home/fedml -s /bin/bash fedml  # head & nodes

# キーフレーズなしでキーペアを作成
ssh-keygen  -N "" -t ed25519 -f ~/.ssh/key_`hostname`

sudo mkdir -p /home/nfs/.ssh; sudo chown nfs:nfs /home/nfs/.ssh
sudo mkdir -p /home/fedml/.ssh; sudo chown fedml:fedml /home/fedml/.ssh

sudo touch /home/nfs/.ssh/authorized_keys; sudo chown nfs /home/nfs/.ssh/authorized_keys
sudo touch /home/fedml/.ssh/authorized_keys; sudo chown fedml /home/fedml/.ssh/authorized_keys

cat ~/.ssh/key_`hostname`.pub | sudo tee -a /home/nfs/.ssh/authorized_keys
cat ~/.ssh/key_`hostname`.pub | sudo tee -a /home/fedml/.ssh/authorized_keys

sudo cp ~/.ssh/key_`hostname` /home/fedml/.ssh/key_fedml
sudo chown fedml /home/fedml/.ssh/key_fedml
```

ansibleユーザ（ubuntu）で、`~/.ssh/config`を作成します。

``` shell
whoami  # ubuntu

cat << EOS >> .ssh/config
Host fedml-nfs
  HostName localhost
  IdentityFile ~/.ssh/key_`hostname`
  User nfs

Host fedml-head
  HostName localhost
  IdentityFile ~/.ssh/key_`hostname`
  User fedml

Host fedml-node_1
  HostName localhost
  IdentityFile ~/.ssh/key_`hostname`
  User fedml

# TODO: 手順に追加
Host fedml-iot_1
  HostName localhost
  IdentityFile ~/.ssh/key_`hostname`
  User iot
EOS
```

管理ノード

``` shell
ssh fedml-head

cat << EOS >> .ssh/config
Host fedml-node_1
  HostName localhost
  IdentityFile ~/.ssh/key_fedml
  User fedml
EOS
exit
```


計算ノードからnfsへssh接続できるようにします。

``` shell
ssh fedml-node_1

cat << EOS >> .ssh/config
Host fedml-nfs
  HostName localhost
  IdentityFile ~/.ssh/key_fedml
  User nfs

Host fedml-node_1
  HostName localhost
  IdentityFile ~/.ssh/key_fedml
  User fedml
EOS
exit
```

sshでVMのホストから繋ぎたい場合は、次の追加作業が必要です。

```
# 共通鍵をauthorized_keysに追加
cat ~/.ssh/key_`hostname`.pub | sudo tee -a /home/`whoami`/.ssh/authorized_keys

# VMホスト上にcat ~/.ssh/key_`hostname`の中身（秘密鍵）をコピーし、VMホスト上の~/.ssh/configの設定をする。
```


## clone repository

```
git clone <URL> fedml_sample
cd fedml_sample/ansible
```



## install ansible

https://docs.ansible.com/ansible/2.9_ja/installation_guide/intro_installation.html#ubuntu-ansible

```
sudo apt update
sudo apt-get install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible
```

## config定義

必要に応じてansible.cfgを定義します。

```
cat << EOS > ansible.cfg
[defaults]
log_path=/var/tmp/ansible.log
EOS
```


## hosts定義

環境構築対象となるホスト群を`hosts`（iniファイル形式）に定義します。
standaloneの場合、headとndoesは同一ユーザを想定しています。

standaloneの場合、headとnodesを定義すると、インストール処理が衝突し失敗するため、明示的にstandaloneと伝える必要があります。

```
cat << EOS > hosts
[nfs]
fedml-nfs

# [head]
# fedml-head

# [nodes]
# fedml-node_1

[standalone]
fedml-head
EOS
```


次のコマンドを実行し疎通確認します。

```
ansible all -i hosts -m ping
```

次のコマンドで環境構築に必要なスクリプトを配布します。

```
ansible-playbook -i hosts playbooks/delivery.yml
```

次のコマンドで配布されたスクリプトを実行し環境を構築を行います。

```
ansible-playbook -i hosts playbooks/install.yml
```

管理ノードで次のコマンドを実行

```
ssh fedml-head
```

```
export WANDB_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxx
```

次のコマンドを実行します。エラーになる実験はコメントアウトしてください。

```
cd FedML-Server/FedML
bash CI-script-fedavg.sh
```


```
sh run_fedavg_standalone_pytorch.sh 0 2 2 4 mnist ./../../../data/mnist lr hetero 1 1 0.03 sgd 1

INFO:root:load_data. dataset_name = mnist
Traceback (most recent call last):
  File "./main_fedavg.py", line 305, in <module>
    dataset = load_data(args, args.dataset)
  File "./main_fedavg.py", line 110, in load_data
    class_num = load_partition_data_mnist(args.batch_size)
  File "/home/fedml/FedML/fedml_api/data_preprocessing/MNIST/data_loader.py", line 90, in load_partition_data_mnist
    users, groups, train_data, test_data = read_data(train_path, test_path)
  File "/home/fedml/FedML/fedml_api/data_preprocessing/MNIST/data_loader.py", line 28, in read_data
    train_files = os.listdir(train_data_dir)
FileNotFoundError: [Errno 2] No such file or directory: './../../../data/MNIST/train'
```

```
ssh fedml-head
cd ~/FedML-Server/FedML/fedml_experiments/distributed/fedavg

cat << EOS > mpi_host_file
localhost:1
EOS
```

```
source "$HOME/miniconda/etc/profile.d/conda.sh"
conda activate fedml
```


```
sh ./../../../data/fed_cifar100/download_fedcifar100.sh

mpirun -np 2 -hostfile ./mpi_host_file python3 ./main_fedavg.py \
  --gpu_mapping_file "gpu_mapping.yaml" \
  --gpu_mapping_key "mapping_default" \
  --model resnet18_gn \
  --data_dir ./../../../data/fed_cifar100/datasets \
  --dataset fed_cifar100 \
  --partition_method hetero  \
  --client_num_in_total 1 \
  --client_num_per_round 1 \
  --comm_round 10 \
  --batch_size 512 \
  --epochs 1 \
  --lr 0.03 \
  --client_optimizer adam \
  --ci 0
```


# MPIのデバッグ

本当にできるかは試していない。

```
mpirun -np 2 -hostfile ./mpi_host_file python3 -m debugpy --wait-for-client --listen 5678 ./main_fedavg.py \
  --gpu_mapping_file "gpu_mapping.yaml" \
  --gpu_mapping_key "mapping_default" \
  --model resnet18_gn \
  --data_dir ./../../../data/fed_cifar100/datasets \
  --dataset fed_cifar100 \
  --partition_method hetero  \
  --client_num_in_total 1 \
  --client_num_per_round 1 \
  --comm_round 10 \
  --batch_size 512 \
  --epochs 1 \
  --lr 0.03 \
  --client_optimizer adam \
  --ci 0

```


### 複数構成

``` shell
multipass launch 20.04 --disk 20G --name ansible
multipass launch 20.04 --disk 20G --name nfs
multipass launch 20.04 --disk 20G --name head
multipass launch 20.04 --disk 20G --name node-1
```


# デバッグ

vscodeのデバッガを利用するには、次のような設定が必要。

``` json
{
  "name": "Python: debug attach fedavg",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  },
  // "cwd": "${workspaceFolder}/fedml_experiments/distributed/fedavg",
  // "program": "main_fedavg.py",
  "justMyCode": false
}
```

デバッグしたいコードに仕込む。
並列実行時は、process_idで別ポートを監視する。

```
comm, process_id, worker_number = FedML_init()

import debugpy

debugpy.listen(5678 + process_id)  # 5678, 5679...
debugpy.wait_for_client()
```

## client server grpc 実行

### cross cilo

https://github.com/FedML-AI/FedML/blob/b0fd3776bd01328f06d92ea92298221afca61b68/fedml_experiments/distributed/fedavg/README_RPC.md

データローダのファイル解凍に失敗してしまう！



概要

- 管理ノード１つ
- ノードを２つ
- ソースコードを同期
- 全てのクライアントでスクリプトを実行しておく
- その後、サーバを実行する
- サーバーはアクティブなクライアントに従って接続を構築する必要があり、この手順が必要。
- ハンドシェイクを実装することで、この制約が解決されるかもしれない

管理ノードで計算ノード分の同期スクリプトをそれぞれ実行する。


```
# rsync_fedml-node_1.sh
# 管理ノードのソースを計算ノードと同期する

#!/bin/bash
LOCAL_PATH=/home/fedml/FedML-Server

DEV_NODE=fedml-node_1
REMOTE_PATH=/home/fedml

alias ws-sync='rsync -avP -e ssh --exclude '.idea' $LOCAL_PATH $DEV_NODE:$REMOTE_PATH --progress --append'
ws-sync; fswatch -o $LOCAL_PATH | while read f; do ws-sync; done
```

```
sh rsync_fedml-node_1.sh
```

計算ノードで学習スクリプトを実行する。

```
FedML_WORKSPACE=/home/fedml/FedML-Server/FedML

# run the client first

cd $FedML_WORKSPACE/fedml_experiments/distributed/fedavg
sh run_fedavg_cross_zone.sh 1
sh run_fedavg_cross_zone.sh 2

# after all clients are up, run the server 
# this order is important because server needs to build connection according to active clients.
# we will solve this contraints by developing a shaking hand protocol.

cd $FedML_WORKSPACE/fedml_experiments/distributed/fedavg
sh run_fedavg_cross_zone.sh 0


# kill processes
kill $(ps aux | grep "main_fedavg.py" | grep -v grep | awk '{print $2}')

```

上は、無効化になっているのでドキュメントが古い。

https://github.com/FedML-AI/FedML/blob/master/fedml_experiments/distributed/fedavg/run_fedavg_grpc.sh


## スタンドアロンで検証

```
cat grpc_ipconfig.csv

receiver_id,ip
0,127.0.0.1
```

```
sh run_fedavg_distributed_pytorch.sh 10 mobilenet homo 100 20 64 0.001 cinic10 "./../../../data/cinic10" adam 0
```


## クライアント・サーバ構成（同一ホストの疑似CS構成）で検証

GRPCで動かすとき、`FedML/fedml_core/distributed/communication/gRPC/grpc_comm_manager.py`
マネージャはPORTを50000番 + 連番を払い出していく（サーバは0で50000番となる）が、
メッセージ送信時なぜか`PORT_BASE = 8888`となっているので50000に書き換える。

```
def send_message(self, msg: Message):
        payload = msg.to_json()

        receiver_id = msg.get_receiver_id()
        PORT_BASE = 8888
```

サーバ・クライアント軍を指定。
ipはhost名でもよい。

```
receiver_id,ip
0,127.0.0.1
1,127.0.0.1
```

`gpu_mapping.yaml`を編集する。

次は、

- サーバ: CPU : 1
- クライアント: CPU : 1

の例で、必要に応じてノードやCPUを数を編集する。

``` yaml
mapping_FedML_gRPC:
    hostname_node_server: [1]
    hostname_node_1: [1]
```

`main_fedavg_rpc.py`がパスの設定がイマイチで動かないので、`main_fedavg.py`からパス設定をコピーする。

```
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "./../../../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "./../../../")))

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "")))
```

VSCODEのlaunch.jsonにデバッガを用意したので、
- クライアントを起動
- サーバを起動

の順でスクリプトを実行する（その順序のプロトコルしか実装されていない）。

なお、`fl_worker_index`は0がサーバ、それ以外はクライアントとなる（重複しないようにインクリメントする）。

```
# 参考
python ./main_fedavg_rpc.py \
    --gpu_mapping_file gpu_mapping.yaml \
    --gpu_mapping_key mapping_FedML_gRPC \
    --model lr \
    --dataset mnist \
    --data_dir ./../../../data/MNIST \
    --partition_method hetero \
    --client_num_in_total 1 \
    --client_num_per_round 1 \
    --comm_round 50 \
    --epochs 2 \
    --client_optimizer adam \
    --batch_size 32 \
    --lr 0.01 \
    --ci 0 \
    --backend GRPC \
    --grpc_ipconfig_path grpc_ipconfig.csv \
    --fl_worker_index 0
```


## クロスデバイス構成

```
vi ~/FedML-Server/executor/grpc_ipconfig.csv

receiver_id,ip
0,127.0.0.1
1,127.0.0.1
```

app.pyのパスがイマイチなのでとりあえず下記を追加する

```
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "../FedML/")))
```

sudo useradd -m -d /home/iot -s /bin/bash iot
sudo mkdir -p /home/iot/.ssh; sudo chown iot:iot /home/iot/.ssh

sudo touch /home/iot/.ssh/authorized_keys; sudo chown iot /home/iot/.ssh/authorized_keys

cat ~/.ssh/key_`hostname`.pub | sudo tee -a /home/iot/.ssh/authorized_keys


https://github.com/FedML-AI/FedML-IoT

```
whoami # iot
mkdir sourcecode

git clone https://github.com/FedML-AI/FedML-IoT.git
cd FedML-Iot
cd FedML
git submodule init
git submodule update
```

ln -s ../FedML-Server/FedML FedML
cd ./raspberry_pi/fedavg
