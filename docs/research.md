# research

## FedML

連合学習における有名なライブラリ

- [公式ドキュメント](https://doc.fedml.ai/overview.html)
- [リポジトリ](https://github.com/FedML-AI/FedML)
- [連合学習に関する論文など](https://github.com/chaoyanghe/Awesome-Federated-Learning)


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