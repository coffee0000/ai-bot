#!/bin/bash

# 使用 Gunicorn 启动 Uvicorn 作为 worker，app.py 作为应用入口
# app:app 表示 app.py 中定义的 FastAPI 实例 app
gunicorn app:APP --bind 0.0.0.0:3978 --worker-class aiohttp.GunicornWebWorker --workers 4
