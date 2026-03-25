# 🐳 棱镜协议 Streamlit 应用 Docker 镜像
# 快速部署和分享 Web 应用

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
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ==================== 阶段 2: 运行阶段 ====================
FROM python:3.11-slim AS runtime

# 设置工作目录
WORKDIR /app

# 创建非 root 用户
RUN groupadd -r prism && useradd -r -g prism prism

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码
COPY --chown=prism:prism streamlit_app.py .
COPY --chown=prism:prism README.md .

# 切换到非 root 用户
USER prism

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import streamlit; print('✅ Streamlit 健康检查通过')" || exit 1

# 暴露端口
EXPOSE 8501

# 设置 Streamlit 配置
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE=dark

# 默认命令
CMD ["streamlit", "run", "streamlit_app.py"]

# ==================== 阶段 3: 开发阶段 ====================
FROM runtime AS development

# 切换回 root 安装开发工具
USER root

# 安装开发工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 切换回 prism 用户
USER prism

# 设置开发环境变量
ENV PRISM_ENV="development" \
    STREAMLIT_SERVER_HEADLESS=false

# 开发命令
CMD ["streamlit", "run", "streamlit_app.py", "--server.runOnSave=true"]

# ==================== 阶段 4: 生产阶段 ====================
FROM runtime AS production

# 生产环境变量
ENV PRISM_ENV="production" \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=10 \
    STREAMLIT_SERVER_MAX_MESSAGE_SIZE=10 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# 生产命令（添加更多安全选项）
CMD ["streamlit", "run", "streamlit_app.py", \
    "--server.fileWatcherType=none", \
    "--browser.serverAddress=0.0.0.0", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=true"]

# ==================== 标签和元数据 ====================
LABEL org.opencontainers.image.title="棱镜协议 Streamlit 应用" \
      org.opencontainers.image.description="火堆旁的对话 Web 界面" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="星尘 & 璇玑" \
      org.opencontainers.image.url="https://prism-interconnect.dev" \
      org.opencontainers.image.source="https://github.com/Ultima0369/prism-interconnect" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.created="2026-03-25T00:00:00Z"

# ==================== 构建和使用说明 ====================

# 构建镜像:
# docker build -t prism-streamlit -f examples/Dockerfile .

# 运行开发版本:
# docker run -p 8501:8501 --name prism-dev prism-streamlit:development

# 运行生产版本:
# docker run -p 8501:8501 --name prism-prod prism-streamlit:production

# 使用 Docker Compose:
# docker-compose -f examples/docker-compose.yml up

# 推送到 Docker Hub:
# docker tag prism-streamlit yourusername/prism-streamlit:1.0.0
# docker push yourusername/prism-streamlit:1.0.0