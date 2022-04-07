# はじめに

本ドキュメントは、連合学習と連合学習に関する技術やライブラリについてまとめたもので、
連合学習の環境構築者向けのドキュメントとなる。

連合学習の環境構築者は、主にネットワーク・グラフに関する知識が重要となる。


# 連合学習とは

データを取集せずに学習モデルを合成し、学習モデルを改善していく手法。
データを収集し学習する従来の手法だとプライバシーの問題があるため、近年、異なるドメイン間でデータを送信せず学習させる手法として注目を集める。

## メリット・デメリット

- M: プライバシーの問題を回避できる
- D: 従来のデータセンターでの学習は、学習データの偏りをコントロールできますが、連合学習の場合、データが散らばっているため偏りをコントロールすることができない

より詳しくは次のリンクを参照

- [進歩と未解決の問題](https://arxiv.org/pdf/1912.04977.pdf)


## 連合学習フロー

モデルは次のフローで改善されていく

1. train: Edge側で学習済みモデルを生成する
2. feedback: 複数のEdgeからサーバへモデルを送信する
3. aggregate: モデルを合成する
4. transfer:  合成されたモデルをEdgeへ展開する

## 機械学習の一般的なフロー

1. データ収集
2. データ加工・クレンジング
3. データロード
4. モデル学習
5. モデル評価
6. モデルデプロイ（本番稼働）
7. モデル監視（運用）

## 並列・分散・連合処理について

並列・分散・連合処理について、次のように区別することとする。

1. 並列: １つのマシン上で複数のCPUで同一データセットで同一処理を行い結果を集約する
2. 分散: 複数のマシン上で同一データセットで同一処理を行い（並列を組み合わせてもよい）結果を集約する
3. 連合: 複数のマシン上あるいは複数のCPUを用いて、データセットを共有せず同一処理を行い結果を集約する

連合学習のユースケースとしては、

1. 企業Ａ内のデータセットAを企業Ａ内のEdge A, Edge Bを用いて並列処理でモデルAを生成
2. 企業Ｂ内のデータセットBを企業B内のEdge C, Edge Dを用いて並列処理でモデルBを生成
3. 連合学習サーバにモデルA, モデルBを集約しモデルCを生成
4. 異なる連合学習サーバで生成したモデル群を集約し、モデルDを生成（クロスサイロ）

ということができる理解。

ただし、4.のケース（複数の連合学習サーバ）を組み合わせることは未対応の模様。

https://github.com/FedML-AI/FedML/issues/59


疑問

モデルは隣接ノードの資源を使って集約されていく？
連合学習サーバで集約される？
連合転移学習とは


## 転移学習（Transfer learning）

別のタスクで学習された知識を転移する機械学習の手法


## スケーリングについて


### cross-device

データの所有者自体の数が多いが、データや計算資源は少ない。
IOT機器など。


### cross-silo（クロスサイロ）

データの所有者自体の数は多くないが、データや計算資源は比較的十分にある。
企業間での連合学習などのケース。

## データパーティションについて

### 集中型（FedAVG）

データの流れは非対称で、マネージャーがローカルモデルの情報を集計し、グローバルなパラメータをアップデートする。
セキュリティリスクが高いらしい。

### 分散型（SimFL）

通信が直接データの所有者同士で行われ、すべてのデータの所有者がグローバルなパラメータを更新するあ。


データの流れは非対称とは？？？


## 通信について

FedMLは、次の通信規格を使用可能。

- MPI
- MQTT
- GRPC
- TRPC

|  規格名 |  レイヤー  | スループット |
| ---- | ---- | ---- |
| MPI | TCP/IP | High |
| MQTT | TCP/IP | High |
| GRPC | HTTP2 | low |
| TRPC | HTTP? | low |


通信バックエンドを検討する時、レイヤーとスループットの観点で検討する。


学習にPyTorchを用い、デフォルトでMPIを通信バックエンドに利用する。

なお、BytePSというフレームワークは、MPIではなくクラウドベースの模様。


WSGIの実装であるwerkzeug
mod_wsgiへのインターフェースとしてWerkzeug


ASGIは、HTTP Trailersを処理しない。
gRPCストリームではHTTP Trailersを使用するため、ASGIは対応できない。

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Trailer

### MPI

Point-to-Pointとグループ通信がサポートされる。
MPIはOSI参照モデルの役割にあてはめると、役割としては5層（セッション層）以上に対応すると考えられるが、実際の実装ではソケットとTCP（トランスポート層）を使用している。

MPI_Comm_rank: 自分のプロセス番号（＝ランク）を取得
MPI_Comm_size: 実行に参加しているプロセス数を取得

### MQTT

主にIOTなど、低電力でコンパクトである場面でのメッセージングで主流となってきている。

### GRPC

HTTP2上に構築されるRPCプロトコル。

GPRCのサンプルは次で紹介されている。

- https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/distributed/fedavg
- https://github.com/FedML-AI/FedML/tree/master/scripts/aws

```
#!/bin/bash
DEV_NODE=fedml-grpc-server
LOCAL_PATH=/Users/hchaoyan/source/FedML/
REMOTE_PATH=/home/ec2-user/FedML_gRPC
alias ws-sync='rsync -avP -e ssh --exclude '.idea' $LOCAL_PATH $DEV_NODE:$REMOTE_PATH'
ws-sync; fswatch -o $LOCAL_PATH | while read f; do ws-sync; done

# fswatch -o 現在のバッチの変更イベントの数を含む単一のメッセージを出力します。
```

GRPCのサンプル定義ファイルは次に存在する。

- https://github.com/FedML-AI/FedML/tree/e0c58c539bf1d7ae9911e57d7f223ac19af03902/fedml_core/distributed/communication/gRPC/proto


FastAPIとGRPCの両方（１度の定義で両対応）をサポートするフレームワーク。スター数が少ないのがネック。

https://bali-framework.github.io/bali/




### TRPC

HTTP2


- [pythonバインディング](https://mpi4py.readthedocs.io/en/stable/index.html)

インストールにはMPIを実装した共有ライブラリが必要。

```
sudo apt-get install libopenmpi-dev
python3 -m pip install mpi4py
```

```
# mpi4py.MPI.Open_portでMPIプロセスのグループ間の接続を確立するために使用できるアドレスを返す

from mpi4py import MPI
MPI.Open_port()

# port_name文字列 でエンコードされたネットワークアドレス
# => '4206821377.0:3078334918'
```

## アーキテクチャ

- fedml_core: 動的計画法に基づく分散コンピューティングに関する通信やスケジューラを提供
- fedml_api: 連合学習アルゴリズムを提供
- fedml_experiments: fedmlのアルゴリズムのテスト機能を提供
- fedml_mobile: スマートフォンを使用したデバイス上のトレーニングをサポート
- fedml_IoT: IoTデバイスを使用したデバイス上のトレーニングをサポート


## ソースコードの読み方

https://doc.fedml.ai/user_guide/open_source/algorithm-reference-implementation.html

### fedml_experiments

fedmlのアルゴリズムのテストを提供し、どのようにアルゴリズムを実装するかサンプルを確認できる。

- https://github.com/FedML-AI/FedML/tree/master/fedml_experiments


|  タイプ/リンク |  概要  | 論文 |
| ---- | ---- | ---- |
|  [centralized/fedgkt](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/centralized)  |  単体プロセスでの学習  |  |
|  [standalone/decentralized](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/standalone/decentralized)  |  片側信頼ソーシャルネットワークを介した中央サーバーの自由連合学習（分散型FL）  | [リンク](./pdf/1910.04956.pdf) |
|  [distributed/fedgkt](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/distributed/fedgkt)  |  大規模エッジ群でのCNN連合学習  |  |
|  fedavg  | エッジデバイスが中央サーバのプライバシー保護を信頼していない場合に選択される学習パラダイム | [リンク](./pdf/2104.11375.pdf) |


### fedml_api

連合学習アルゴリズムを提供

- https://github.com/FedML-AI/FedML/tree/master/fedml_api


### fedml_core

動的計画法に基づく分散コンピューティングに関する通信やスケジューラを提供

- https://github.com/FedML-AI/FedML/tree/master/fedml_api



## トポロジ

分散型機械学習では、コンピュータネットワークの接続形態（トポロジ）を考慮する必要がある（どのような時、何を選ぶかについては理解していない）。

FedMLには、垂直FL、分割学習、分散型FL、階層型FLなどのさまざまなトポロジ定義がある。

- バス
- スター
- リング
- フルメッシュ
- パーシャルメッシュ
- Centralized
- Hierarchical
- Decentralized
- Vertical
- Split


- symmetry（左右対称）
- asymmetry（左右非対称・非対称トポロジ）

## fedml_core

FedML-coreは、通信とモデルトレーニングを2つのコアコンポーネントに分離します。

1. 通信プロトコルコンポーネント
2. PyTorchまたはTensorFlowに基づいて構築されたデバイス上のディープラーニングコンポーネント

## Worker-Oriented Programming

FedML-coreは、FLアルゴリズムのトレーニングまたは調整に参加するときに、ワーカーの動作をプログラムするために使用できる、
ワーカー指向のプログラミングデザインパターンを提供する

- Coordinator: 中央ワーカーでトレーナの管理をする
- Trainer: 中央ワーカー以外のワーカー






勾配法



##

ComManager: トポロジ（隣接するノード）に基づいて通信を行う？
モデルマネージャー
