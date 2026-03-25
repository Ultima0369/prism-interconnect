# 🐳 棱镜协议 Python SDK Docker 镜像
# 生产就绪的企业级部署方案

# ==================== 阶段 1: 构建阶段 ====================
FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --user --no-warn-script-location \
    -r requirements.txt

# ==================== 阶段 2: 运行阶段 ====================
FROM python:3.11-slim AS runtime

# 设置工作目录
WORKDIR /app

# 创建非 root 用户
RUN groupadd -r prism && useradd -r -g prism prism

# 从构建阶段复制已安装的包
COPY --from=builder /root/.local /home/prism/.local

# 复制应用代码
COPY --chown=prism:prism prism_sdk ./prism_sdk
COPY --chown=prism:prism setup.py .
COPY --chown=prism:prism README.md .

# 切换到非 root 用户
USER prism

# 设置 PATH 以便使用用户安装的包
ENV PATH="/home/prism/.local/bin:${PATH}" \
    PYTHONPATH="/app:${PYTHONPATH}"

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import prism_sdk; print('✅ 棱镜协议 SDK 健康检查通过')" || exit 1

# 暴露端口（如果需要）
# EXPOSE 8000

# 默认命令
CMD ["python", "-c", "import prism_sdk; print(f'🧠 棱镜协议 {prism_sdk.__version__} 已启动')"]

# ==================== 阶段 3: 开发阶段 ====================
FROM python:3.11-slim AS development

WORKDIR /app

# 安装开发工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 复制所有文件
COPY . .

# 安装开发依赖
RUN pip install -e .[dev,test,benchmark,docs]

# 设置开发环境变量
ENV PYTHONPATH="/app:${PYTHONPATH}" \
    PRISM_ENV="development"

# 开发命令
CMD ["bash"]

# ==================== 阶段 4: 测试阶段 ====================
FROM development AS test

# 运行测试
RUN pytest tests/ -v --cov=prism_sdk --cov-report=term

# ==================== 阶段 5: 基准测试阶段 ====================
FROM development AS benchmark

# 安装基准测试依赖
RUN pip install psutil matplotlib numpy

# 运行基准测试
CMD ["python", "benchmarks/performance_benchmark.py"]

# ==================== 标签和元数据 ====================
LABEL org.opencontainers.image.title="棱镜协议 Python SDK" \
      org.opencontainers.image.description="数字时代的认知革命基础设施" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="星尘 & 璇玑" \
      org.opencontainers.image.url="https://prism-interconnect.dev" \
      org.opencontainers.image.source="https://github.com/Ultima0369/prism-interconnect" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.created="2026-03-25T00:00:00Z"