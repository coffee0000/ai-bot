#!/usr/bin/env bash
# Azure App Service (Linux) startup.sh
# 前提：
# - 你已经在 WSL 用 Python 3.12 把所有依赖下载成 wheel，放在 packages/
# - App Service 的 Python 版本 = 3.12
# - 不允许联网安装依赖

APP_DIR="/home/site/wwwroot"
VENV_DIR="${APP_DIR}/.venv"
WHEEL_DIR="${APP_DIR}/packages"

echo "[START] PWD=$(pwd)"
echo "[START] System Python=$(python --version 2>&1 || true)"
echo "[START] PORT=${PORT:-not set}"

cd "$APP_DIR" || exit 1

# 1) 每次启动都重新创建 venv（避免 Python 版本/路径残留问题）
rm -rf "$VENV_DIR"
python -m venv "$VENV_DIR" || exit 1

# 2) 彻底禁止 pip 访问外网
export PIP_NO_INDEX=1
export PIP_FIND_LINKS="$WHEEL_DIR"
unset PIP_INDEX_URL PIP_EXTRA_INDEX_URL

# 3) 只从本地 packages 安装依赖
"$VENV_DIR/bin/python" -m pip install   --no-index   --find-links="$WHEEL_DIR"   -r requirements.txt || exit 1

# 4) 启动应用（假设 app.py 里有 app 对象）
exec "$VENV_DIR/bin/gunicorn" app:app --bind "0.0.0.0:${PORT}"
