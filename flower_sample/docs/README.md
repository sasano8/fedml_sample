- flower
- pysyft

# 比較

|  FW  |  通信  |
| ---- | ---- |
|  flower  |  GRPC  |
|  pysyft  |  WEBSOCKET  |



# flower

- 第一印象はfedmlより、apiやドキュメントが体系化されており、ガイドが親切と感じる
- 人気のある戦略（FedAvgなど）が提供され、カスタマイズできるように設計されている
- サーバを起動し、クライアントを起動すると自動的に学習プロセスが開始する（クライアント駆動可能）
- サーバは戦略（FedAvgなど）毎に起動し、予定した学習を終えるとサーバが終了する。ポートはサーバ（戦略）毎に必要となる。
- モデル評価アプローチは、Centralized(server側で評価)/federate（client側で評価）がある
- モデルをサーバ側に自動保存する仕組みは提供されていないが、カスタマイズすることができる。将来的に、デフォルトの自動保存の仕組みを提供する予定。
- サポートしているFWやサンプルは次の通り
    - TensorFlow
    - PyTorch(Lightning)
    - scikit-learn
    - MXNet
    - Hugging Face
