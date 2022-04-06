# 連合学習とは

データを取集せずに学習モデルを合成し、学習モデルを改善していく手法。
データを収集し学習する従来の手法だとプライバシーの問題があるため、近年、異なるドメイン間でデータを送信せず学習させる手法として注目を集める。


# 参考

- https://github.com/FedML-AI/FedMー
- https://github.com/chaoyanghe/Awesome-Federated-Learning
- [進歩と未解決の問題](https://arxiv.org/pdf/1912.04977.pdf)
- [ライブデモ](http://open.fedml.ai)
- [ライブデモ説明](https://doc.fedml.ai/user_guide/mlops/mlops_live_demo.html)


# メリット

- プライバシーの問題を回避できます


# デメリット

- 従来のデータセンターでの学習は、学習データの偏りをコントロールできますが、連合学習の場合、データが散らばっているため偏りをコントロールすることができません。


# アーキテクチャ

- fedml_core: 分散コンピューティングに関連する通信機能
- fedml_api: 連合学習アルゴリズムを提供
- fedml_experiments: fedmlのアルゴリズムのテスト機能を提供
- fedml_mobile: スマートフォンを使用したデバイス上のトレーニングをサポート
- fedml_IoT: IoTデバイスを使用したデバイス上のトレーニングをサポート


# 機能

## 管理機能

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
    - エッジのCPU/Memory/Swapなどを確認することができる
    - client modelとaggregated modelを確認することができる
    - client modelとaggregated modelはrunidに紐づいている
    - FLServer - ユーザー - Edge Deviceの繋がりが見える


