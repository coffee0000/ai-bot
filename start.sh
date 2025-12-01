#!/bin/bash

# 使用 Gunicorn 启动 Uvicorn 作为 worker，app.py 作为应用入口
# app:app 表示 app.py 中定义的 FastAPI 实例 app
uvicorn app:app --host 0.0.0.0 --port 3978 --workers 2
