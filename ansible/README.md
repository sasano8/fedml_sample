# クラスター構築

クラスタ構築手順を記します。

公式手順は次を参照ください。

- [Fedml installation](https://doc.fedml.ai/user_guide/open_source/installation/installation-distributed-computing.html)


## 構成要件

次のホストに対して、必要なスクリプトの配布とテストの実施をansibleで行います

- nfs: モデルを共有するためファイルストレージが1台必要です
- head: 計算ノード管理のホストが1台必要です
- nodes: 複数台の計算ノードが必要です

上記ホストの他に、ansibleホストが必要です。
検証の場合、ansibleホストは自身のメインマシンになります。


## 構成要件

必要となるマシンの最低スペックは次の通りです。


- nfs:
    - Volume: 5GB ~
    - memo: モデルを共有するためファイルストレージが1台必要です

- head:
    - OS: Ubuntu20.04
    - Volume: 10GB ~
    - memo:
        - nodes（計算ノード）の管理用ホストが1台必要です
        - 機械学習に関するライブラリ一式がインストールされます。

- nodes:
    - OS: Ubuntu20.04
    - Volume: 10GB ~
    - memo:
        - 計算ノードです
        - 計算ノードは複数台構成できます
        - 機械学習に関するライブラリ一式がインストールされます。

- ansible（オプション）:
    - OS: Ubuntu20.04
    - Volume: 5GB ~
    - memo: nfs/head/nodesに対して、一括でスクリプトを配布、構成変更するための構成管理サーバが１台必要です


また、透過的に次の方向でssh接続できる必要があります。

- head  ???  nodes
- nodes <- -> nfs
- head ??? nfs
- ansible --> nfs, head, nodes


## 検証環境構築


### スタンドアロン

```
multipass launch 20.04 --name ansible  # 環境構築用のマシン 兼 nfs 兼 head
multipass launch 20.04 --name fedml  # ノードはn個に増やしてかまいません
```

```
sudo useradd -m -d /home/ansible -s /bin/bash -g ubuntu ansible
sudo useradd -m -d /home/nfs -s /bin/bash -g ubuntu nfs

# head & nodes
sudo useradd -m -d /home/fedml -s /bin/bash -g ubuntu fedml

echo ansible:ubuntu | sudo chpasswd
echo nfs:ubuntu | sudo chpasswd
echo fedml:ubuntu | sudo chpasswd

ssh-keygetn -t ed25519 -f ~/.ssh/key_`hostname`

cat ~/.ssh/key_`hostname`.pub | sudo tee /home/ansible/.ssh/authorized_keys
cat ~/.ssh/key_`hostname`.pub | sudo tee /home/nfs/.ssh/authorized_keys
cat ~/.ssh/key_`hostname`.pub | sudo tee /home/fedml/.ssh/authorized_keys

sudo cp ~/.ssh/key_`hostname` /home/ansible/.ssh/key_ansible
sudo cp ~/.ssh/key_`hostname` /home/fedml/.ssh/key_fedml
sudo chown ansible /home/ansible/.ssh/key_ansible
sudo chown fedml /home/fedml/.ssh/key_fedml
```


```
su ansible

cat << EOS >> .ssh/config
Host fedml-nfs
  HostName localhost
  IdentityFile ~/.ssh/key_ansible
  User nfs

Host fedml-head
  HostName localhost
  IdentityFile ~/.ssh/key_ansible
  User fedml

Host fedml-node_1
  HostName localhost
  IdentityFile ~/.ssh/key_ansible
  User fedml
EOS
```



## ssh接続確認

必要なマシンを用意しssh接続ができるようにします。

本手順では、`~/.ssh/config`に次の設定がされていることを前提に進めます。

```
Host fedml
  HostName yourhost
  IdentityFile ~/.ssh/yourkey.pem
  User ubuntu
```

`~/.ssh/config`に設定したホスト群に接続できることを確認してください。

```
ssh fedml
```

次にssh鍵の生成例を記します。

ansibleホストの共通鍵を構築対象ホストに配布します。

```
# ansibleホスト側
ssh ssh-keygen -t ed25519 -f ~/.ssh/key_`hostname`
cat ~/.ssh/key_`hostname`.pub

# 構築されるサーバ側
echo [ansibleホストの公開鍵] >> .ssh/authorized_keys
```



```
# nfs兼head or nodes の場合は自身にsshできるようにする
ssh ssh-keygen -t ed25519 -f ~/.ssh/key_`hostname`
cat ~/.ssh/key_`hostname`.pub >> ~/.ssh/authorized_keys
```



## config定義

必要に応じてansible.cfgを定義します。

```
cd ansible

cat << EOS > ansible.cfg
[defaults]
log_path=/var/tmp/ansible.log
EOS
```


## hosts定義

環境構築対象となるホスト群を`hosts`（iniファイル形式）に定義します。

```
cd ansible

cat << EOS > hosts
[nfs]
fedml

[head]
fedml

[nodes]
fedml
EOS
```

次のコマンドを実行し疎通確認します。

```
ansible all -i hosts -m ping
```

次のコマンドで環境構築に必要なスクリプトを配布&インストールします。

```
ansible-playbook -i hosts playbooks/delivery.yml
```
