# Installation

## 構成要件

https://doc.fedml.ai/user_guide/open_source/installation.html


- ヘッドノード（ログイン・テスト用）が必要
- N個のcomupute node（multi-GPU server: e.g., 8 x NVIDIA V100）が必要
- NFSなどの一元化されたフォールトトレラントファイルサーバー必要（計算ノード間で大規模なデータセットを共有）


- エージェント

### Software

- Python >= 3.7.4
- MPI4Py >= 3.0.3: Message Passing Interface (MPI) 規格の Python バインディング
- PyTorch >= 1.4.0: PyTorchが提供する分散コンピューティング機械学習はMPIを使っている

- https://mpi4py.readthedocs.io/en/stable/



## 環境構築

### NFS（ネットワークファイルシステム）構成

```
秘密鍵公開鍵を置いてsshログインできるようにする
```

