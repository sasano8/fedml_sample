# クラスター構築

クラスタ構築手順を記します。

公式手順は次を参照ください。

- [Fedml installation](https://doc.fedml.ai/user_guide/open_source/installation/installation-distributed-computing.html)


## 構成要件

次のホストに対して、必要なスクリプトの配布とテストの実施を行います

- nfs: モデルを共有するためファイルストレージが1台必要です
- head: 計算ノード管理のホストが1台必要です
- nodes: 複数台の計算ノードが必要です

## マシンを用意

必要となるマシンの最低スペックは次の通りです。

- OS: Ubuntu20.04
- Volume: 16GB


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
