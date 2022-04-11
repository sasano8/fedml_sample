# クラスター構築

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

## hosts定義

環境構築対象となるホスト群を`hosts`に定義します。

```
cd ansible

cat << EOS > hosts
[nfs]
fedml

[manager]
fedml

[nodes]
fedml
EOS
```

次のコマンドを実行し疎通確認します。

```
make ping
```

