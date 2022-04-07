# 連合学習とは

データを取集せずに学習モデルを合成し、学習モデルを改善していく手法。
データを収集し学習する従来の手法だとプライバシーの問題があるため、近年、異なるドメイン間でデータを送信せず学習させる手法として注目を集める。

## メリット・デメリット

- M: プライバシーの問題を回避できる
- D: 従来のデータセンターでの学習は、学習データの偏りをコントロールできますが、連合学習の場合、データが散らばっているため偏りをコントロールすることができない

より詳しくは次のリンクを参照

- [進歩と未解決の問題](https://arxiv.org/pdf/1912.04977.pdf)

## FedML

連合学習における有名なライブラリ

- https://github.com/FedML-AI/FedMー
- https://github.com/chaoyanghe/Awesome-Federated-Learning

複数のノードへのモデル展開など複雑なワークフローを簡略化し、連合学習の実行を支援する

## 機能

次のリンクからGUIから提供している機能を調べた

- [ライブデモ](http://open.fedml.ai)
- [ライブデモ説明](https://doc.fedml.ai/user_guide/mlops/mlops_live_demo.html)

### 管理機能

- ユーザ管理
- グループ管理
- プロジェクト管理
    - グループは１つのみアタッチすることができる
- 計算ノード（エッジ）管理
- 構成管理（モデルとハイパーパラメータなど学習に関する設定）
- 学習を開始する
    - 構成を指定する
    - デバイスを指定する
- ジョブ管理
    - 開始したジョブに名前とタグをつけることができる
    - ステータスを確認することができる
    - トレーニング結果の視覚化
    - Edgeのシステムパフォーマンスの視覚化
    - 分散ロギング
    - client modelとaggregated modelを確認することができる
    - client modelとaggregated modelはrunidに紐づいている
    - FLServer - ユーザー - Edge Deviceの繋がりが見える

### 実装されていない機能

- 任意のタイミングで自動実行するジョブスケジューラは特に見当たらない
- 1つ連合学習のサイクルを管理。関連するジョブフローなどの実行などは管理していない。

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

## アーキテクチャ

- fedml_core: 動的計画法に基づく分散コンピューティングに関する通信やスケジューラを提供
- fedml_api: 連合学習アルゴリズムを提供
- fedml_experiments: fedmlのアルゴリズムのテスト機能を提供
- fedml_mobile: スマートフォンを使用したデバイス上のトレーニングをサポート
- fedml_IoT: IoTデバイスを使用したデバイス上のトレーニングをサポート


## ソースコードの読み方


### fedml_experiments

fedmlのアルゴリズムのテストを提供し、どのようにアルゴリズムを実装するかサンプルを確認できる。

- https://github.com/FedML-AI/FedML/tree/master/fedml_experiments


|  タイプ/リンク |  概要  | 論文 |
| ---- | ---- | ---- |
|  [centralized/fedgkt](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/centralized)  |  単体プロセスでの学習  |  |
|  [standalone/decentralized](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/standalone/decentralized)  |  片側信頼ソーシャルネットワークを介した中央サーバーの自由連合学習（分散型FL）  | [リンク](https://arxiv.org/pdf/1910.04956) |
|  [distributed/fedgkt](https://github.com/FedML-AI/FedML/tree/master/fedml_experiments/distributed/fedgkt)  |  大規模エッジ群でのCNN連合学習  |  |


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


## キーワード

pytorchなどで出てくるキーワードをメモしておく

- DDP(DistributedDataParallel)
- optim（最適化）: 任意の方法で効率的にパラメータを更新する

学習率（lr）

## fedml_core

FedML-coreは、通信とモデルトレーニングを2つのコアコンポーネントに分離します。

1. 通信プロトコルコンポーネント
2. PyTorchまたはTensorFlowに基づいて構築されたデバイス上のディープラーニングコンポーネント

## Worker-Oriented Programming

FedML-coreは、FLアルゴリズムのトレーニングまたは調整に参加するときに、ワーカーの動作をプログラムするために使用できる、
ワーカー指向のプログラミングデザインパターンを提供する

- Coordinator: 中央ワーカーでトレーナの管理をする
- Trainer: 中央ワーカー以外のワーカー

## MPI

FedMLの並列処理の通信はMPIと呼ばれる通信規格を用いる（別の規格にも対応している）。

- MPI
- MQTT
- GRPC
- TRPC


MPI_Comm_rank: 自分のプロセス番号（＝ランク）を取得
MPI_Comm_size: 実行に参加しているプロセス数を取得



勾配法



##

ComManager: トポロジ（隣接するノード）に基づいて通信を行う？
モデルマネージャー







