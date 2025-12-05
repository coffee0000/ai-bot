# 使用 Python 3.13 官方轻量级镜像
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装证书（必要）
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝源代码
COPY . .

EXPOSE 3978

CMD ["gunicorn", "app:APP", "--bind", "0.0.0.0:3978", "--worker-class", "aiohttp.GunicornWebWorker", "--workers", "4"]

