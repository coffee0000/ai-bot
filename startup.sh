#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/site/wwwroot"
VENV_DIR="${APP_DIR}/.venv"
WHEEL_DIR="${APP_DIR}/packages"

echo "[起動] 現在のディレクトリ: $(pwd)"
echo "[起動] Python バージョン: $(python --version 2>&1 || true)"
echo "[起動] 使用ポート: ${PORT:-未設定}"

cd "$APP_DIR"

# ① 仮想環境を作成（初回のみ）
if [ ! -d "$VENV_DIR" ]; then
  echo "[起動] 仮想環境を作成します: $VENV_DIR"
  python -m venv "$VENV_DIR"
fi

# ② ローカルの wheel（オフライン依存）から依存関係をインストール
echo "[起動] ローカル依存パッケージからインストールします: $WHEEL_DIR"
"$VENV_DIR/bin/python" -m pip install -U pip
"$VENV_DIR/bin/pip" install --no-index --find-links="$WHEEL_DIR" -r requirements.txt

# ③ gunicorn でアプリケーションを起動
echo "[起動] gunicorn を起動します..."
exec "$VENV_DIR/bin/gunicorn" app:app --bind "0.0.0.0:${PORT}"
