# 灵枢开发环境Dockerfile
# 基于Ubuntu的Python开发环境

FROM python:3.11-slim

# 设置环境变量
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUTF8=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /workspace

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    tree \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd -m -u 1000 developer && \
    chown -R developer:developer /workspace
USER developer

# 复制项目文件（从构建上下文）
COPY --chown=developer:developer . .

# 安装Python依赖
RUN pip install --user --no-cache-dir \
    pyyaml \
    pytest \
    black \
    flake8

# 设置PATH包含用户pip安装目录
ENV PATH="/home/developer/.local/bin:${PATH}"

# 默认命令
CMD ["bash"]