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

``` shell
multipass launch 20.04 --disk 20G --name fedml
multipass shell fedml
```

``` shell
sudo useradd -m -d /home/nfs -s /bin/bash nfs
sudo useradd -m -d /home/fedml -s /bin/bash fedml  # head & nodes

ssh-keygen -t ed25519 -f ~/.ssh/key_`hostname`

sudo mkdir -p /home/nfs/.ssh; sudo chown nfs:nfs /home/nfs/.ssh
sudo mkdir -p /home/fedml/.ssh; sudo chown fedml:fedml /home/fedml/.ssh

sudo touch /home/nfs/.ssh/authorized_keys; sudo chown nfs /home/nfs/.ssh/authorized_keys
sudo touch /home/fedml/.ssh/authorized_keys; sudo chown fedml /home/fedml/.ssh/authorized_keys

cat ~/.ssh/key_`hostname`.pub | sudo tee /home/nfs/.ssh/authorized_keys
cat ~/.ssh/key_`hostname`.pub | sudo tee /home/fedml/.ssh/authorized_keys

sudo cp ~/.ssh/key_`hostname` /home/fedml/.ssh/key_fedml
sudo chown fedml /home/fedml/.ssh/key_fedml
```


``` shell
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
EOS
```

``` shell
ssh fedml-head

cat << EOS >> .ssh/config
Host fedml-nfs
  HostName localhost
  IdentityFile ~/.ssh/key_fedml
  User nfs
EOS

exit
```

## install ansible

https://docs.ansible.com/ansible/2.9_ja/installation_guide/intro_installation.html#ubuntu-ansible

```
sudo apt update
sudo apt-get install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible
```


##


```
git clone <URL> fedml_sample
cd fedml_sample/ansible
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

```
cat << EOS > hosts
[nfs]
fedml-nfs

[head]
fedml-head

[nodes]
fedml-node_1
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