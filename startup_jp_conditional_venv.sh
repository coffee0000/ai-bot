#!/usr/bin/env bash
# Azure App Service (Linux) startup.sh
# 前提:
# - WSL 上で Python 3.12 を使用して依存関係を wheel として事前ダウンロードし、packages/ に配置済み
# - App Service の Python バージョン = 3.12
# - 起動時にインターネット接続は不可

APP_DIR="/home/site/wwwroot"
VENV_DIR="${APP_DIR}/.venv"
WHEEL_DIR="${APP_DIR}/packages"

echo "[START] PWD=$(pwd)"
echo "[START] System Python=$(python --version 2>&1 || true)"
echo "[START] PORT=${PORT:-not set}"

cd "$APP_DIR" || exit 1

# 1) venv が存在しない場合のみ作成する（再起動時は再作成しない）
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] venv does not exist. Creating venv..."
  python -m venv "$VENV_DIR" || exit 1
else
  echo "[INFO] venv already exists. Skipping venv creation."
fi

# 2) pip の外部アクセスを完全に無効化
export PIP_NO_INDEX=1
export PIP_FIND_LINKS="$WHEEL_DIR"
unset PIP_INDEX_URL PIP_EXTRA_INDEX_URL

# 3) ローカル packages のみから依存関係をインストール
"$VENV_DIR/bin/python" -m pip install   --no-index   --find-links="$WHEEL_DIR"   -r requirements.txt || exit 1

# 4) アプリケーション起動（app.py に app オブジェクトが存在する前提）
exec "$VENV_DIR/bin/gunicorn" app:app --bind "0.0.0.0:${PORT}"
