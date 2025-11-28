#!/bin/bash

# 激活 Python 虚拟环境
source /home/site/wwwroot/antenv/bin/activate

# 运行应用
uvicorn app:APP --host 0.0.0.0 --port $PORT
