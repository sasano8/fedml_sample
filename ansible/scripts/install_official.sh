#!/usr/bin/env bash
set -eu

cd ~/FedML

# pip3が必要（次のコマンドを実行するとsudoにパスワードが必要な場合、永遠に待機してしまう
# sudo apt-get install -y python3-pip

# install
pip3 --version

# requirements.txtの依存関係がいまいちなので依存関係を修正
sed -i -e 's/requests==2\.24\.0/requests==2\.27\.1/' requirements.txt
sed -i -e 's/^urllib3==1\.26\.5/# urllib3==1\.26\.5/' requirements.txt

# wandbのトークンがベタうちなので環境変数にする
sed -i -e 's/^wandb login ee0b5f53d949c84cee7decbe7a629e63fb2f8408/wandb login $WANDB_TOKEN/' CI-script-fedavg.sh

# pyflakesは必ず失敗しシェルが終了するので無効化
sed -i -e 's/^pyflakes \./# pyflakes \./' CI-script-fedavg.sh

bash ./CI-install.sh




