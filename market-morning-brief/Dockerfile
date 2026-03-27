FROM python:3.12-slim

LABEL maintainer="Market Brief System"
LABEL description="三地股市智能晨报/晚报系统"

# 设置时区为 Asia/Shanghai（CST）
ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y \
    tzdata \
    curl \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# 工作目录
WORKDIR /app

# 安装 Python 依赖（先复制 requirements.txt 利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 复制源代码
COPY src/ ./src/

# 创建缓存目录
RUN mkdir -p /app/cache

# 健康检查（通过日志文件判断进程存活）
HEALTHCHECK --interval=60s --timeout=10s --retries=3 \
    CMD test -f /app/cache/market_brief.log || exit 1

# 非 root 用户运行（安全）
RUN useradd -r -s /bin/false marketbot && chown -R marketbot:marketbot /app
USER marketbot

# 入口
CMD ["python", "src/main.py"]
