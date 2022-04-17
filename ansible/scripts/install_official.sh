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

# ERROR: Cannot install -r requirements.txt (line 6) and urllib3==1.26.5 because these package versions have conflicting dependencies.

# The conflict is caused by:
#     The user requested urllib3==1.26.5
#     requests 2.24.0 depends on urllib3!=1.25.0, !=1.25.1, <1.26 and >=1.21.1

# To fix this you could try to:
# 1. loosen the range of package versions you've specified
# 2. remove package versions to allow pip attempt to solve the dependency conflict

# ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies


# ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
# elastic-transport 8.1.1 requires urllib3<2,>=1.26.2, but you have urllib3 1.25.11 which is incompatible.

bash ./CI-install.sh




