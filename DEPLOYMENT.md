# 🚀 棱镜协议部署指南

## 📋 目录

- [1. 部署架构](#1-部署架构)
- [2. 单机部署](#2-单机部署)
- [3. 容器化部署](#3-容器化部署)
- [4. Kubernetes部署](#4-kubernetes部署)
- [5. 云原生部署](#5-云原生部署)
- [6. 监控与运维](#6-监控与运维)
- [7. 安全配置](#7-安全配置)
- [8. 性能优化](#8-性能优化)
- [9. 灾难恢复](#9-灾难恢复)
- [10. 成本优化](#10-成本优化)

---

## 1. 部署架构

### 1.1 系统组件

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端层 (Client Layer)                   │
├─────────────────────────────────────────────────────────────┤
│  Web客户端 │ 移动应用 │ CLI工具 │ SDK集成 │ 第三方服务        │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                    API网关层 (API Gateway)                   │
├─────────────────────────────────────────────────────────────┤
│ 负载均衡 │ 速率限制 │ 身份验证 │ SSL终止 │ 请求路由          │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                  业务逻辑层 (Business Logic)                 │
├─────────────────────────────────────────────────────────────┤
│ 棱镜引擎 │ 光谱生成 │ 留白计算 │ 合成处理 │ 递归管理         │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                   数据层 (Data Layer)                       │
├─────────────────────────────────────────────────────────────┤
│ 会话存储 │ 消息队列 │ 缓存系统 │ 分析数据库 │ 文件存储        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 部署模式

| 模式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **单机部署** | 开发测试、小规模使用 | 简单、成本低 | 扩展性差、单点故障 |
| **容器化部署** | 中小规模生产 | 环境一致、易于部署 | 需要容器管理 |
| **Kubernetes部署** | 大规模生产 | 高可用、自动扩展 | 复杂度高 |
| **云原生部署** | 企业级应用 | 全托管、弹性伸缩 | 成本较高 |

---

## 2. 单机部署

### 2.1 环境要求

```bash
# 系统要求
- Ubuntu 20.04+ / CentOS 8+ / macOS 11+
- Python 3.8+
- 内存: 4GB+ (推荐8GB)
- 存储: 20GB+ SSD
- 网络: 公网IP或内网访问

# 软件依赖
- Redis 6.0+ (缓存和会话)
- PostgreSQL 13+ (主数据库)
- Nginx 1.18+ (反向代理)
```

### 2.2 安装步骤

```bash
# 1. 克隆代码
git clone https://github.com/Ultima0369/prism-interconnect.git
cd prism-interconnect

# 2. 安装Python依赖
python -m venv venv
source venv/bin/activate
pip install -e "implementations/python[full]"

# 3. 配置环境变量
cp .env.example .env
# 编辑.env文件，设置数据库、Redis等配置

# 4. 初始化数据库
python -m prism_sdk.cli db init
python -m prism_sdk.cli db migrate

# 5. 启动服务
# 开发模式
python -m prism_sdk.cli server --dev

# 生产模式（使用Gunicorn）
gunicorn prism_sdk.server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### 2.3 Nginx配置

```nginx
# /etc/nginx/sites-available/prism
server {
    listen 80;
    server_name prism.yourdomain.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name prism.yourdomain.com;
    
    # SSL证书
    ssl_certificate /etc/letsencrypt/live/prism.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/prism.yourdomain.com/privkey.pem;
    
    # SSL优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # 反向代理到应用
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 静态文件
    location /static/ {
        alias /path/to/prism-interconnect/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 健康检查
    location /health {
        access_log off;
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

### 2.4 系统服务配置

```systemd
# /etc/systemd/system/prism.service
[Unit]
Description=Prism Interconnect Server
After=network.target postgresql.service redis-server.service
Requires=postgresql.service redis-server.service

[Service]
Type=simple
User=prism
Group=prism
WorkingDirectory=/opt/prism-interconnect
EnvironmentFile=/opt/prism-interconnect/.env
ExecStart=/opt/prism-interconnect/venv/bin/gunicorn prism_sdk.server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=prism

# 安全限制
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/prism-interconnect/logs /opt/prism-interconnect/data

[Install]
WantedBy=multi-user.target
```

---

## 3. 容器化部署

### 3.1 Docker配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制依赖文件
COPY implementations/python/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY implementations/python/ .

# 创建非root用户
RUN useradd -m -u 1000 prism && chown -R prism:prism /app
USER prism

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "prism_sdk.server:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]
```

### 3.2 Docker Compose配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 棱镜服务
  prism:
    build:
      context: .
      dockerfile: implementations/python/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://prism:password@postgres/prism
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG:-false}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - prism-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL数据库
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=prism
      - POSTGRES_USER=prism
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - prism-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U prism"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis缓存
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - prism-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - prism
    networks:
      - prism-network
    restart: unless-stopped

networks:
  prism-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 3.3 部署脚本

```bash
#!/bin/bash
# deploy.sh

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始部署棱镜协议...${NC}"

# 1. 检查环境
echo -e "${YELLOW}检查环境...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker未安装${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose未安装${NC}"
    exit 1
fi

# 2. 创建环境文件
echo -e "${YELLOW}配置环境...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}请编辑.env文件配置环境变量${NC}"
    exit 1
fi

# 3. 构建镜像
echo -e "${YELLOW}构建Docker镜像...${NC}"
docker-compose build

# 4. 启动服务
echo -e "${YELLOW}启动服务...${NC}"
docker-compose up -d

# 5. 等待服务就绪
echo -e "${YELLOW}等待服务就绪...${NC}"
sleep 10

# 6. 运行数据库迁移
echo -e "${YELLOW}运行数据库迁移...${NC}"
docker-compose exec prism python -m prism_sdk.cli db migrate

# 7. 检查服务状态
echo -e "${YELLOW}检查服务状态...${NC}"
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ 棱镜服务运行正常${NC}"
else
    echo -e "${RED}❌ 棱镜服务启动失败${NC}"
    docker-compose logs prism
    exit 1
fi

echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "访问地址: http://localhost:8000"
echo -e "API文档: http://localhost:8000/docs"
```

---

## 4. Kubernetes部署

### 4.1 命名空间配置

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prism
  labels:
    name: prism
    environment: production
```

### 4.2 配置映射

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prism-config
  namespace: prism
data:
  # 应用配置
  DATABASE_URL: "postgresql://prism:$(DB_PASSWORD)@postgres.prism.svc.cluster.local/prism"
  REDIS_URL: "redis://redis.prism.svc.cluster.local:6379/0"
  DEBUG: "false"
  
  # Nginx配置
  nginx.conf: |
    events {
      worker_connections 1024;
    }
    
    http {
      upstream prism {
        server prism:8000;
      }
      
      server {
        listen 80;
        
        location / {
          proxy_pass http://prism;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
        }
      }
    }
```

### 4.3 密钥配置

```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: prism-secrets
  namespace: prism
type: Opaque
data:
  # 使用base64编码的值
  SECRET_KEY: "YOUR_BASE64_ENCODED_SECRET_KEY"
  DB_PASSWORD: "YOUR_BASE64_ENCODED_DB_PASSWORD"
  REDIS_PASSWORD: "YOUR_BASE64_ENCODED_REDIS_PASSWORD"
```

### 4.4 部署配置

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism
  namespace: prism
  labels:
    app: prism
    component: server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prism
      component: server
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: prism
        component: server
    spec:
      containers:
      - name: prism
        image: your-registry/prism:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: prism-config
              key: DATABASE_URL
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: prism-secrets
              key: SECRET_KEY
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: data
          mountPath: /app/data
      volumes:
      - name: logs
        emptyDir: {}
      - name: data
        persistentVolumeClaim:
          claimName: prism-data-pvc
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
```

### 4.5 服务配置

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: prism
  namespace: prism
  labels:
    app: prism
spec:
  selector:
    app: prism
    component: server
  ports:
  - port: 80
    targetPort: 8000
    name: http
  type: ClusterIP
```

### 4.6 入口配置

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: prism-ingress
  namespace: prism
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - prism.yourdomain.com
    secretName: prism-tls
  rules:
  - host: prism.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: prism
            port:
              number: 80
```

### 4.7 水平自动扩展

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: prism-hpa
  namespace: prism
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: prism
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

### 4.8 部署脚本

```bash
#!/bin/bash
# k8s-deploy.sh

set -e

echo "🚀 开始Kubernetes部署..."

# 1. 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 2. 创建配置
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# 3. 创建持久化存储
kubectl apply -f k8s/pvc.yaml

# 4. 部署数据库
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml

# 5. 等待数据库就绪
echo "⏳ 等待数据库就绪..."
kubectl wait --for=condition=ready pod -l app=postgres -n prism --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n prism --timeout=300s

# 6. 部署应用
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 7. 等待应用就绪
echo "⏳ 等待应用就绪..."
kubectl wait --for=condition=ready pod -l app=prism -n prism --timeout=300s

# 8. 部署入口和扩展
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# 9. 检查状态
echo "📊 检查部署状态..."
kubectl get all -n prism

echo "✅ 部署完成！"
echo "🌐 访问地址: https://prism.yourdomain.com"
```

---

## 5. 云原生部署

### 5.1 AWS ECS部署

```yaml
# aws/task-definition.json
{
  "family": "prism",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/prismTaskRole",
  "cpu": "1024",
  "memory": "2048",
  "requiresCompatibilities": ["FARGATE"],
  "containerDefinitions": [
    {
      "name": "prism",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/prism:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://prism:${DB_PASSWORD}@${DB_HOST}:5432/prism"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://${REDIS_HOST}:6379/0"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prism/secret_key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/prism",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 40
      }
    }
  ]
}
```

### 5.2 Google Cloud Run部署

```yaml
# gcp/cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: prism
  namespace: default
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project/prism:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: prism-secrets
              key: DATABASE_URL
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: prism-secrets
              key: SECRET_KEY
        resources:
          limits:
            cpu: 1000m
            memory: 512Mi
          requests:
            cpu: 250m
            memory: 256Mi
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 6
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
```

### 5.3 Azure Container Instances部署

```yaml
# azure/container-instance.yaml
apiVersion: 2019-12-01
location: eastus
name: prism
properties:
  containers:
  - name: prism
    properties:
      image: yourregistry.azurecr.io/prism:latest
      ports:
      - port: 8000
        protocol: TCP
      environmentVariables:
      - name: DATABASE_URL
        secureValue: "postgresql://prism:${DB_PASSWORD}@${DB_HOST}:5432/prism"
      - name: SECRET_KEY
        secureValue: "${SECRET_KEY}"
      resources:
        requests:
          cpu: 1.0
          memoryInGB: 1.5
      livenessProbe:
        exec:
          command:
          - curl
          - -f
          - http://localhost:8000/health
        initialDelaySeconds: 30
        periodSeconds: 10
        failureThreshold: 3
  osType: Linux
  restartPolicy: Always
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 80
  imageRegistryCredentials:
  - server: yourregistry.azurecr.io
    username: ${REGISTRY_USERNAME}
    password: ${REGISTRY_PASSWORD}
```

---

## 6. 监控与运维

### 6.1 监控指标

```yaml
# prometheus/metrics.yaml
- job_name: 'prism'
  scrape_interval: 15s
  static_configs:
  - targets: ['prism:8000']
  metrics_path: '/metrics'
  
  # 自定义指标
  metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'prism_(.*)'
    action: keep
```

### 6.2 告警规则

```yaml
# prometheus/alerts.yaml
groups:
- name: prism_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(prism_http_requests_total{status=~"5.."}[5m]) / rate(prism_http_requests_total[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "高错误率检测"
      description: "错误率超过5% (当前值: {{ $value }})"
  
  - alert: HighLatency
    expr: histogram_quantile(0.95, rate(prism_http_request_duration_seconds_bucket[5m])) > 2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "高延迟检测"
      description: "95%分位延迟超过2秒 (当前值: {{ $value }}s)"
  
  - alert: ServiceDown
    expr: up{job="prism"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "服务下线"
      description: "棱镜服务已下线超过1分钟"
```

### 6.3 日志配置

```python
# logging_config.py
import logging
import logging.config
import json
from datetime import datetime

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/app/logs/prism.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10,
            "formatter": "json",
            "level": "DEBUG"
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/app/logs/error.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "formatter": "json",
            "level": "ERROR"
        }
    },
    "loggers": {
        "prism_sdk": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "gunicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING"
    }
}

# 应用日志配置
logging.config.dictConfig(LOGGING_CONFIG)
```

### 6.4 运维脚本

```bash
#!/bin/bash
# ops-tools.sh

# 健康检查
check_health() {
    echo "🔍 执行健康检查..."
    
    # 检查服务状态
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        echo "✅ 服务状态: 健康"
    else
        echo "❌ 服务状态: 不健康"
        return 1
    fi
    
    # 检查数据库连接
    if python -c "import psycopg2; psycopg2.connect('${DATABASE_URL}')"; then
        echo "✅ 数据库连接: 正常"
    else
        echo "❌ 数据库连接: 失败"
        return 1
    fi
    
    # 检查Redis连接
    if python -c "import redis; r = redis.from_url('${REDIS_URL}'); r.ping()"; then
        echo "✅ Redis连接: 正常"
    else
        echo "❌ Redis连接: 失败"
        return 1
    fi
    
    echo "🎉 所有检查通过！"
    return 0
}

# 性能监控
monitor_performance() {
    echo "📊 性能监控..."
    
    # CPU使用率
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU使用率: ${cpu_usage}%"
    
    # 内存使用
    memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')
    echo "内存使用率: ${memory_usage}"
    
    # 磁盘使用
    disk_usage=$(df -h / | awk 'NR==2{print $5}')
    echo "磁盘使用率: ${disk_usage}"
    
    # 网络连接
    connections=$(netstat -an | grep :8000 | wc -l)
    echo "活跃连接数: ${connections}"
}

# 备份数据库
backup_database() {
    echo "💾 备份数据库..."
    
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="/backups/prism_${timestamp}.sql"
    
    pg_dump -h localhost -U prism prism > "${backup_file}"
    
    if [ $? -eq 0 ]; then
        echo "✅ 数据库备份成功: ${backup_file}"
        
        # 压缩备份
        gzip "${backup_file}"
        echo "✅ 备份文件已压缩"
    else
        echo "❌ 数据库备份失败"
        return 1
    fi
}

# 清理日志
cleanup_logs() {
    echo "🧹 清理日志..."
    
    # 保留最近7天的日志
    find /app/logs -name "*.log" -mtime +7 -delete
    echo "✅ 已清理7天前的日志"
    
    # 清理备份（保留最近30天）
    find /backups -name "*.sql.gz" -mtime +30 -delete
    echo "✅ 已清理30天前的备份"
}

# 主菜单
main() {
    case "$1" in
        health)
            check_health
            ;;
        monitor)
            monitor_performance
            ;;
        backup)
            backup_database
            ;;
        cleanup)
            cleanup_logs
            ;;
        all)
            check_health
            monitor_performance
            backup_database
            cleanup_logs
            ;;
        *)
            echo "用法: $0 {health|monitor|backup|cleanup|all}"
            exit 1
            ;;
    esac
}

main "$@"
```

---

## 7. 安全配置

### 7.1 网络安全

```nginx
# nginx/security.conf
# 限制请求大小
client_max_body_size 10m;

# 限制请求速率
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;

# 防止DDoS
limit_conn_zone $binary_remote_addr zone=addr:10m;
limit_conn addr 100;

# 安全头
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

# 隐藏服务器信息
server_tokens off;
```

### 7.2 应用安全

```python
# security.py
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """验证JWT令牌"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="令牌已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效令牌")

# 输入验证
def sanitize_input(text: str, max_length: int = 5000) -> str:
    """清理用户输入"""
    import html
    
    # 移除HTML标签
    text = html.escape(text)
    
    # 限制长度
    if len(text) > max_length:
        text = text[:max_length]
    
    # 移除危险字符
    dangerous_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"onload=",
        r"onerror=",
        r"eval\("
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    return text.strip()

# 速率限制
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# 在FastAPI应用中配置
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### 7.3 数据库安全

```sql
-- 数据库安全配置
-- 1. 创建专用用户
CREATE USER prism_app WITH PASSWORD 'strong_password_here';
CREATE DATABASE prism_db OWNER prism_app;

-- 2. 限制权限
REVOKE ALL ON DATABASE prism_db FROM PUBLIC;
GRANT CONNECT ON DATABASE prism_db TO prism_app;

-- 3. 行级安全策略
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_messages_policy ON messages
    USING (user_id = current_setting('app.current_user_id')::integer);

-- 4. 审计日志
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(50),
    table_name VARCHAR(50),
    record_id INTEGER,
    old_data JSONB,
    new_data JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 5. 数据加密
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 加密敏感数据
INSERT INTO users (email, encrypted_password)
VALUES (
    'user@example.com',
    crypt('user_password', gen_salt('bf'))
);

-- 验证密码
SELECT id FROM users 
WHERE email = 'user@example.com' 
AND encrypted_password = crypt('user_password', encrypted_password);
```

### 7.4 网络安全配置

```bash
# iptables防火墙规则
#!/bin/bash

# 清空现有规则
iptables -F
iptables -X

# 默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许本地回环
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 允许已建立的连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允许SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 允许棱镜服务端口
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT

# 允许ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT

# 记录被拒绝的连接
iptables -A INPUT -j LOG --log-prefix "IPTABLES-DROPPED: " --log-level 4

# 保存规则
iptables-save > /etc/iptables/rules.v4
```

---

## 8. 性能优化

### 8.1 数据库优化

```sql
-- 1. 索引优化
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_users_email ON users(email);

-- 2. 查询优化
-- 使用覆盖索引
CREATE INDEX idx_spectrum_analysis ON spectrums 
    (type, confidence, created_at) 
    INCLUDE (perspective, limitations);

-- 3. 分区表
CREATE TABLE messages_y2023m01 PARTITION OF messages
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

-- 4. 物化视图
CREATE MATERIALIZED VIEW daily_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_messages,
    COUNT(DISTINCT session_id) as unique_sessions,
    AVG(LENGTH(query)) as avg_query_length
FROM messages
GROUP BY DATE(created_at);

-- 定期刷新
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_stats;
```

### 8.2 缓存优化

```python
# cache.py
import redis
from functools import wraps
import pickle
import hashlib
from datetime import timedelta

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(os.getenv("REDIS_URL"))
    
    def cache_key(self, func, *args, **kwargs):
        """生成缓存键"""
        key_parts = [
            func.__module__,
            func.__name__,
            str(args),
            str(sorted(kwargs.items()))
        ]
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def cached(self, ttl=300):
        """缓存装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键
                key = self.cache_key(func, *args, **kwargs)
                
                # 尝试从缓存获取
                cached_result = self.redis.get(key)
                if cached_result:
                    return pickle.loads(cached_result)
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 缓存结果
                self.redis.setex(
                    key,
                    timedelta(seconds=ttl),
                    pickle.dumps(result)
                )
                
                return result
            return wrapper
        return decorator
    
    # 使用示例
    @cached(ttl=600)  # 缓存10分钟
    def get_user_conversations(self, user_id: int, limit: int = 50):
        """获取用户对话历史（带缓存）"""
        # 数据库查询逻辑
        pass

# Redis连接池配置
redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD"),
    max_connections=100,
    decode_responses=True
)
```

### 8.3 异步优化

```python
# async_optimization.py
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import aiohttp
from typing import List, Dict, Any

class AsyncOptimizer:
    def __init__(self):
        # I/O密集型任务使用线程池
        self.io_executor = ThreadPoolExecutor(max_workers=50)
        
        # CPU密集型任务使用进程池
        self.cpu_executor = ProcessPoolExecutor(max_workers=4)
        
        # HTTP会话池
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def parallel_requests(self, urls: List[str]) -> List[Dict[str, Any]]:
        """并行HTTP请求"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        tasks = []
        for url in urls:
            task = asyncio.create_task(self._fetch_url(url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]
    
    async def _fetch_url(self, url: str) -> Dict[str, Any]:
        """获取单个URL"""
        try:
            async with self.session.get(url, timeout=10) as response:
                return {
                    "url": url,
                    "status": response.status,
                    "content": await response.text()[:1000]
                }
        except Exception as e:
            return {"url": url, "error": str(e)}
    
    async def batch_process(self, items: List[Any], batch_size: int = 10):
        """批量处理项目"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # 并行处理批次
            batch_tasks = []
            for item in batch:
                task = asyncio.create_task(self._process_item(item))
                batch_tasks.append(task)
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            results.extend([r for r in batch_results if not isinstance(r, Exception)])
            
            # 控制速率
            await asyncio.sleep(0.1)
        
        return results
    
    async def _process_item(self, item: Any) -> Any:
        """处理单个项目"""
        # 模拟处理逻辑
        await asyncio.sleep(0.01)
        return {"processed": True, "item": item}
```

### 8.4 数据库连接池

```python
# database_pool.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import psycopg2
from psycopg2 import pool

# SQLAlchemy连接池
engine = create_engine(
    os.getenv("DATABASE_URL"),
    poolclass=QueuePool,
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 最大溢出连接数
    pool_pre_ping=True,  # 连接前ping检查
    pool_recycle=3600,  # 连接回收时间（秒）
    pool_timeout=30,  # 获取连接超时时间
    echo=False  # 是否输出SQL日志
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Psycopg2连接池
postgresql_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", 5432)
)

def get_db_connection():
    """获取数据库连接"""
    return postgresql_pool.getconn()

def release_db_connection(conn):
    """释放数据库连接"""
    postgresql_pool.putconn(conn)
```

---

## 9. 灾难恢复

### 9.1 备份策略

```bash
#!/bin/bash
# backup-strategy.sh

# 完整备份（每周日）
full_backup() {
    echo "开始完整备份..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    
    # 备份数据库
    pg_dump -h localhost -U prism prism > /backups/full_${timestamp}.sql
    gzip /backups/full_${timestamp}.sql
    
    # 备份配置文件
    tar -czf /backups/config_${timestamp}.tar.gz /etc/prism/
    
    # 备份上传到云存储
    aws s3 cp /backups/full_${timestamp}.sql.gz s3://your-backup-bucket/
    aws s3 cp /backups/config_${timestamp}.tar.gz s3://your-backup-bucket/
    
    echo "完整备份完成"
}

# 增量备份（每天）
incremental_backup() {
    echo "开始增量备份..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    
    # 使用WAL归档进行增量备份
    pg_basebackup -D /backups/incremental_${timestamp} -Ft -z -P
    
    # 备份Redis
    redis-cli SAVE
    cp /var/lib/redis/dump.rdb /backups/redis_${timestamp}.rdb
    
    echo "增量备份完成"
}

# 恢复数据库
restore_database() {
    echo "开始恢复数据库..."
    
    # 停止应用
    systemctl stop prism
    
    # 恢复最新备份
    latest_backup=$(ls -t /backups/full_*.sql.gz | head -1)
    
    if [ -z "$latest_backup" ]; then
        echo "未找到备份文件"
        return 1
    fi
    
    # 解压并恢复
    gunzip -c ${latest_backup} | psql -h localhost -U prism prism
    
    # 启动应用
    systemctl start prism
    
    echo "数据库恢复完成"
}

# 监控备份状态
monitor_backups() {
    echo "检查备份状态..."
    
    # 检查最近备份时间
    latest_full=$(find /backups -name "full_*.sql.gz" -mtime -7 | wc -l)
    latest_inc=$(find /backups -name "incremental_*" -mtime -1 | wc -l)
    
    if [ $latest_full -eq 0 ]; then
        echo "警告: 最近7天没有完整备份"
    fi
    
    if [ $latest_inc -eq 0 ]; then
        echo "警告: 最近24小时没有增量备份"
    fi
    
    # 检查备份文件大小
    for backup in /backups/full_*.sql.gz; do
        size=$(du -h "$backup" | cut -f1)
        echo "备份文件: $(basename $backup) 大小: $size"
    done
}
```

### 9.2 故障转移

```yaml
# haproxy/haproxy.cfg
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend http_front
    bind *:80
    stats uri /haproxy?stats
    default_backend http_back

backend http_back
    balance roundrobin
    option httpchk GET /health
    server prism1 192.168.1.101:8000 check fall 3 rise 2
    server prism2 192.168.1.102:8000 check fall 3 rise 2
    server prism3 192.168.1.103:8000 check fall 3 rise 2 backup
```

### 9.3 灾难恢复演练

```python
# disaster_recovery.py
import asyncio
import random
from datetime import datetime
from typing import Dict, List

class DisasterRecoveryTest:
    """灾难恢复测试"""
    
    def __init__(self):
        self.test_cases = [
            self.test_database_failure,
            self.test_redis_failure,
            self.test_network_partition,
            self.test_high_load,
            self.test_data_corruption
        ]
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚨 开始灾难恢复测试...")
        
        results = []
        for test in self.test_cases:
            try:
                result = await test()
                results.append({
                    "test": test.__name__,
                    "status": "PASSED",
                    "details": result
                })
                print(f"✅ {test.__name__}: 通过")
            except Exception as e:
                results.append({
                    "test": test.__name__,
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"❌ {test.__name__}: 失败 - {str(e)}")
        
        # 生成报告
        report = self.generate_report(results)
        print(f"\n📊 测试报告:\n{report}")
        
        return results
    
    async def test_database_failure(self):
        """测试数据库故障恢复"""
        print("测试数据库故障恢复...")
        
        # 模拟数据库连接失败
        # 在实际测试中，这里会停止数据库服务
        
        # 验证降级模式
        response = await self.make_request("/health")
        if response.get("status") != "healthy":
            # 服务应该进入降级模式
            return "服务正确进入降级模式"
        
        # 恢复数据库
        # 在实际测试中，这里会重启数据库服务
        
        # 验证恢复
        response = await self.make_request("/health")
        if response.get("status") == "healthy":
            return "数据库恢复成功"
        
        raise Exception("数据库恢复测试失败")
    
    async def test_redis_failure(self):
        """测试Redis故障恢复"""
        print("测试Redis故障恢复...")
        
        # 模拟Redis连接失败
        # 服务应该降级到本地缓存
        
        response = await self.make_request("/api/dialogue", {
            "query": "测试Redis故障"
        })
        
        if response.get("success"):
            return "服务在Redis故障时正常工作"
        
        raise Exception("Redis故障恢复测试失败")
    
    async def test_network_partition(self):
        """测试网络分区"""
        print("测试网络分区...")
        
        # 模拟网络延迟
        import time
        start_time = time.time()
        
        try:
            response = await self.make_request("/health", timeout=2)
            elapsed = time.time() - start_time
            
            if elapsed < 5:  # 应该在超时前返回
                return f"网络分区处理正常，响应时间: {elapsed:.2f}s"
        except asyncio.TimeoutError:
            return "服务正确处理网络超时"
        
        raise Exception("网络分区测试失败")
    
    async def test_high_load(self):
        """测试高负载恢复"""
        print("测试高负载恢复...")
        
        # 发送大量并发请求
        tasks = []
        for i in range(100):
            task = asyncio.create_task(self.make_request("/health"))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in responses if not isinstance(r, Exception))
        success_rate = success_count / len(responses)
        
        if success_rate > 0.9:  # 90%成功率
            return f"高负载测试通过，成功率: {success_rate:.1%}"
        
        raise Exception(f"高负载测试失败，成功率: {success_rate:.1%}")
    
    async def test_data_corruption(self):
        """测试数据损坏恢复"""
        print("测试数据损坏恢复...")
        
        # 这里测试备份恢复机制
        # 在实际环境中，会测试从备份恢复数据
        
        return "数据恢复机制就绪（需要手动验证备份）"
    
    async def make_request(self, endpoint: str, data: Dict = None, timeout: int = 10):
        """发送HTTP请求"""
        import aiohttp
        
        url = f"http://localhost:8000{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=timeout) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")
    
    def generate_report(self, results: List[Dict]) -> str:
        """生成测试报告"""
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASSED")
        failed = total - passed
        
        report = [
            "=" * 50,
            "灾难恢复测试报告",
            "=" * 50,
            f"测试时间: {datetime.now().isoformat()}",
            f"总测试数: {total}",
            f"通过: {passed}",
            f"失败: {failed}",
            f"成功率: {passed/total:.1%}",
            "",
            "详细结果:"
        ]
        
        for result in results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            report.append(f"{status_icon} {result['test']}: {result.get('details', result.get('error', ''))}")
        
        report.append("=" * 50)
        
        return "\n".join(report)

# 运行测试
async def main():
    tester = DisasterRecoveryTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
```

### 9.4 业务连续性计划

```markdown
# 业务连续性计划 (BCP)

## 1. 风险评估

### 关键风险
1. **数据库故障**
   - 影响: 服务完全不可用
   - RTO: 1小时
   - RPO: 15分钟

2. **网络中断**
   - 影响: 服务不可访问
   - RTO: 30分钟
   - RPO: 0分钟（无数据丢失）

3. **安全事件**
   - 影响: 数据泄露或服务中断
   - RTO: 4小时
   - RPO: 根据备份点

## 2. 恢复策略

### 2.1 数据库恢复
```sql
-- 恢复步骤
1. 停止所有应用服务
2. 从最新备份恢复数据库
3. 应用WAL日志到最新状态
4. 验证数据完整性
5. 重启应用服务

-- 恢复时间目标 (RTO): 1小时
-- 恢复点目标 (RPO): 15分钟
```

### 2.2 应用恢复
```bash
# 应用恢复脚本
#!/bin/bash

# 1. 切换到备份服务器
cd /opt/prism-backup

# 2. 恢复配置
cp -r config/* /etc/prism/

# 3. 启动服务
systemctl start prism

# 4. 验证服务
curl -f http://localhost:8000/health || exit 1

# RTO: 30分钟
```

## 3. 通信计划

### 3.1 内部通信
- **即时通知**: Slack/Teams频道
- **状态页面**: https://status.prism.dev
- **邮件通知**: ops@prism.dev

### 3.2 用户通信
- **服务状态**: 应用内通知
- **预计恢复时间**: 状态页面更新
- **事后报告**: 事件结束后24小时内

## 4. 测试计划

### 4.1 定期测试
- **每月**: 数据库恢复测试
- **每季度**: 完整灾难恢复演练
- **每年**: 业务连续性全面测试

### 4.2 测试记录
```yaml
test_date: 2024-01-15
test_type: database_recovery
duration: 45分钟
result: 成功
issues_found:
  - 备份文件验证时间过长
  - 需要优化恢复脚本
actions_taken:
  - 实现增量备份验证
  - 优化恢复脚本并行处理
```

## 5. 责任矩阵

| 角色 | 主要责任 | 联系方式 |
|------|----------|----------|
| 应急负责人 | 协调恢复工作 | +1-555-0100 |
| 技术负责人 | 技术恢复执行 | +1-555-0101 |
| 沟通负责人 | 内外沟通协调 | +1-555-0102 |
| 业务负责人 | 业务影响评估 | +1-555-0103 |
```

---

## 10. 成本优化

### 10.1 云成本优化

```python
# cost_optimization.py
import boto3
from datetime import datetime, timedelta
from typing import Dict, List

class CostOptimizer:
    """云成本优化器"""
    
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.ec2_client = boto3.client('ec2')
    
    def analyze_cost(self) -> Dict:
        """分析成本"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}
            ]
        )
        
        return response
    
    def optimize_ec2_instances(self):
        """优化EC2实例"""
        # 识别未充分利用的实例
        instances = self.ec2_client.describe_instances()
        
        recommendations = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                # 获取CloudWatch指标
                # 这里简化处理，实际需要查询CPU、内存使用率
                
                # 如果使用率低，建议降级实例类型
                if self._is_underutilized(instance_id):
                    recommendations.append({
                        'instance_id': instance_id,
                        'current_type': instance_type,
                        'recommended_type': self._get_smaller_type(instance_type),
                        'estimated_savings': self._calculate_savings(instance_type)
                    })
        
        return recommendations
    
    def _is_underutilized(self, instance_id: str) -> bool:
        """检查实例是否未充分利用"""
        # 简化实现，实际需要查询CloudWatch
        return True  # 假设所有实例都未充分利用
    
    def _get_smaller_type(self, instance_type: str) -> str:
        """获取更小的实例类型"""
        type_map = {
            'm5.2xlarge': 'm5.xlarge',
            'm5.xlarge': 'm5.large',
            'm5.large': 'm5.medium',
            't3.2xlarge': 't3.xlarge',
            't3.xlarge': 't3.large',
            't3.large': 't3.medium'
        }
        return type_map.get(instance_type, instance_type)
    
    def _calculate_savings(self, instance_type: str) -> float:
        """计算节省金额"""
        # 简化实现
        savings_map = {
            'm5.2xlarge': 100.0,
            'm5.xlarge': 50.0,
            'm5.large': 25.0,
            't3.2xlarge': 80.0,
            't3.xlarge': 40.0,
            't3.large': 20.0
        }
        return savings_map.get(instance_type, 0.0)
    
    def generate_report(self) -> str:
        """生成成本优化报告"""
        cost_data = self.analyze_cost()
        ec2_recommendations = self.optimize_ec2_instances()
        
        total_savings = sum(r['estimated_savings'] for r in ec2_recommendations)
        
        report = [
            "=" * 50,
            "成本优化报告",
            "=" * 50,
            f"生成时间: {datetime.now().isoformat()}",
            f"分析周期: 最近30天",
            "",
            "EC2优化建议:"
        ]
        
        for rec in ec2_recommendations:
            report.append(
                f"- {rec['instance_id']}: "
                f"{rec['current_type']} → {rec['recommended_type']} "
                f"(预计节省: ${rec['estimated_savings']}/月)"
            )
        
        report.extend([
            "",
            f"总预计节省: ${total_savings:.2f}/月",
            f"年化节省: ${total_savings * 12:.2f}/年",
            "=" * 50
        ])
        
        return "\n".join(report)

# 使用示例
optimizer = CostOptimizer()
print(optimizer.generate_report())
```

### 10.2 资源调度优化

```yaml
# k8s/resource-scheduling.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: resource-scheduler
  namespace: prism
data:
  schedule.yaml: |
    schedules:
      # 工作日高峰时段
      - name: weekday-peak
        schedule: "0 9 * * 1-5"  # 工作日9:00
        replicas: 5
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
      
      # 工作日非高峰
      - name: weekday-offpeak
        schedule: "0 18 * * 1-5"  # 工作日18:00
        replicas: 2
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
      
      # 周末
      - name: weekend
        schedule: "0 0 * * 6"  # 周六0:00
        replicas: 1
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "250m"
            memory: "256Mi"
```

### 10.3 自动伸缩策略

```python
# auto_scaling.py
import time
from datetime import datetime
from typing import Dict, List
import boto3

class AutoScaler:
    """自动伸缩管理器"""
    
    def __init__(self):
        self.client = boto3.client('application-autoscaling')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def setup_scaling_policies(self, service_name: str):
        """设置伸缩策略"""
        
        # 基于CPU的伸缩
        self.client.put_scaling_policy(
            PolicyName=f'{service_name}-cpu-scaling',
            ServiceNamespace='ecs',
            ResourceId=f'service/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,  # 70% CPU使用率
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
                },
                'ScaleOutCooldown': 60,  # 扩展冷却时间
                'ScaleInCooldown': 300,  # 收缩冷却时间
                'DisableScaleIn': False
            }
        )
        
        # 基于内存的伸缩
        self.client.put_scaling_policy(
            PolicyName=f'{service_name}-memory-scaling',
            ServiceNamespace='ecs',
            ResourceId=f'service/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 80.0,  # 80%内存使用率
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageMemoryUtilization'
                },
                'ScaleOutCooldown': 60,
                'ScaleInCooldown': 300,
                'DisableScaleIn': False
            }
        )
        
        # 基于请求数的伸缩
        self.client.put_scaling_policy(
            PolicyName=f'{service_name}-request-scaling',
            ServiceNamespace='ecs',
            ResourceId=f'service/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 1000,  # 每秒1000个请求
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ALBRequestCountPerTarget',
                    'ResourceLabel': 'app/prism/loadbalancer'
                },
                'ScaleOutCooldown': 60,
                'ScaleInCooldown': 300,
                'DisableScaleIn': False
            }
        )
    
    def analyze_scaling_patterns(self) -> Dict:
        """分析伸缩模式"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        # 获取CPU使用率数据
        cpu_response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/ECS',
            MetricName='CPUUtilization',
            Dimensions=[
                {'Name': 'ServiceName', 'Value': 'prism'},
                {'Name': 'ClusterName', 'Value': 'prism-cluster'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # 5分钟
            Statistics=['Average']
        )
        
        # 分析模式
        patterns = {
            'peak_hours': [],
            'low_usage_hours': [],
            'average_usage': 0.0,
            'recommended_min_replicas': 2,
            'recommended_max_replicas': 10
        }
        
        # 计算平均使用率
        datapoints = cpu_response['Datapoints']
        if datapoints:
            avg_cpu = sum(d['Average'] for d in datapoints) / len(datapoints)
            patterns['average_usage'] = avg_cpu
            
            # 根据使用率调整推荐配置
            if avg_cpu < 30:
                patterns['recommended_min_replicas'] = 1
                patterns['recommended_max_replicas'] = 5
            elif avg_cpu > 70:
                patterns['recommended_min_replicas'] = 3
                patterns['recommended_max_replicas'] = 15
        
        return patterns
    
    def generate_cost_savings_report(self) -> str:
        """生成成本节省报告"""
        patterns = self.analyze_scaling_patterns()
        
        # 计算潜在节省
        # 假设每个副本每月成本为 $100
        monthly_cost_per_replica = 100.0
        
        current_min = 2  # 当前最小副本数
        current_max = 10  # 当前最大副本数
        
        recommended_min = patterns['recommended_min_replicas']
        recommended_max = patterns['recommended_max_replicas']
        
        # 计算节省
        min_savings = (current_min - recommended_min) * monthly_cost_per_replica
        max_savings = (current_max - recommended_max) * monthly_cost_per_replica
        total_savings = max(min_savings + max_savings, 0)
        
        report = [
            "=" * 50,
            "自动伸缩优化报告",
            "=" * 50,
            f"生成时间: {datetime.now().isoformat()}",
            f"分析周期: 最近7天",
            f"平均CPU使用率: {patterns['average_usage']:.1f}%",
            "",
            "当前配置:",
            f"  - 最小副本数: {current_min}",
            f"  - 最大副本数: {current_max}",
            "",
            "推荐配置:",
            f"  - 最小副本数: {recommended_min}",
            f"  - 最大副本数: {recommended_max}",
            "",
            "预计节省:",
            f"  - 最小副本节省: ${min_savings:.2f}/月",
            f"  - 最大副本节省: ${max_savings:.2f}/月",
            f"  - 总节省: ${total_savings:.2f}/月",
            f"  - 年化节省: ${total_savings * 12:.2f}/年",
            "",
            "建议操作:",
            "1. 更新自动伸缩组的最小/最大副本数",
            "2. 监控调整后的性能表现",
            "3. 定期重新评估伸缩策略",
            "=" * 50
        ]
        
        return "\n".join(report)

# 使用示例
scaler = AutoScaler()
print(scaler.generate_cost_savings_report())
```

### 10.4 存储优化

```yaml
# storage-optimization.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: prism-data-pvc
  namespace: prism
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3  # AWS GP3存储类，性价比高
  resources:
    requests:
      storage: 100Gi  # 根据实际需求调整

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: storage-optimization
  namespace: prism
data:
  cleanup-policy.yaml: |
    # 数据保留策略
    retention:
      # 会话数据
      sessions:
        active: 30d      # 活跃会话保留30天
        inactive: 7d     # 非活跃会话保留7天
        archived: 365d   # 归档会话保留1年
      
      # 消息数据
      messages:
        detailed: 30d    # 详细消息保留30天
        summary: 180d    # 消息摘要保留180天
        analytics: 365d  # 分析数据保留1年
      
      # 日志数据
      logs:
        application: 30d     # 应用日志保留30天
        access: 90d          # 访问日志保留90天
        audit: 365d          # 审计日志保留1年
      
    # 清理计划
    schedule:
      daily: "0 2 * * *"     # 每天凌晨2点
      weekly: "0 3 * * 0"    # 每周日凌晨3点
      monthly: "0 4 1 * *"   # 每月1日凌晨4点
```

### 10.5 网络成本优化

```python
# network_optimization.py
import boto3
from datetime import datetime, timedelta

class NetworkOptimizer:
    """网络成本优化器"""
    
    def __init__(self):
        self.cloudfront = boto3.client('cloudfront')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def analyze_traffic_patterns(self) -> Dict:
        """分析流量模式"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # 获取CloudFront指标
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/CloudFront',
            MetricName='BytesDownloaded',
            Dimensions=[
                {'Name': 'DistributionId', 'Value': 'YOUR_DISTRIBUTION_ID'},
                {'Name': 'Region', 'Value': 'Global'}
            ],
            StartTime=start_date,
            EndTime=end_date,
            Period=86400,  # 每天
            Statistics=['Sum']
        )
        
        # 分析流量模式
        patterns = {
            'total_traffic_gb': 0,
            'average_daily_traffic_gb': 0,
            'peak_traffic_day': None,
            'peak_traffic_gb': 0,
            'recommendations': []
        }
        
        datapoints = response['Datapoints']
        if datapoints:
            # 计算总流量（转换为GB）
            total_bytes = sum(d['Sum'] for d in datapoints)
            patterns['total_traffic_gb'] = total_bytes / (1024**3)
            patterns['average_daily_traffic_gb'] = patterns['total_traffic_gb'] / len(datapoints)
            
            # 找到流量峰值
            peak_day = max(datapoints, key=lambda x: x['Sum'])
            patterns['peak_traffic_day'] = peak_day['Timestamp']
            patterns['peak_traffic_gb'] = peak_day['Sum'] / (1024**3)
            
            # 生成建议
            if patterns['total_traffic_gb'] > 1000:  # 超过1TB
                patterns['recommendations'].append(
                    "考虑使用CloudFront价格类100TB+以获得更低单价"
                )
            
            if patterns['peak_traffic_gb'] > 50:  # 单日峰值超过50GB
                patterns['recommendations'].append(
                    "考虑启用自动压缩以减少传输数据量"
                )
        
        return patterns
    
    def optimize_cdn_configuration(self):
        """优化CDN配置"""
        recommendations = []
        
        # 检查压缩设置
        try:
            distribution = self.cloudfront.get_distribution(Id='YOUR_DISTRIBUTION_ID')
            
            # 建议启用压缩
            if not distribution['DistributionConfig']['DefaultCacheBehavior'].get('Compress', False):
                recommendations.append({
                    'action': 'enable_compression',
                    'description': '启用Gzip/Brotli压缩',
                    'estimated_savings': '减少30-70%的传输数据量',
                    'priority': 'high'
                })
            
            # 建议优化缓存策略
            ttl = distribution['DistributionConfig']['DefaultCacheBehavior']['DefaultTTL']
            if ttl < 86400:  # 小于1天
                recommendations.append({
                    'action': 'increase_cache_ttl',
                    'description': f'增加缓存TTL从{ttl}秒到86400秒',
                    'estimated_savings': '减少源站请求，降低源站成本',
                    'priority': 'medium'
                })
            
        except Exception as e:
            print(f"获取CDN配置失败: {str(e)}")
        
        return recommendations
    
    def generate_network_report(self) -> str:
        """生成网络优化报告"""
        patterns = self.analyze_traffic_patterns()
        cdn_recommendations = self.optimize_cdn_configuration()
        
        report = [
            "=" * 50,
            "网络成本优化报告",
            "=" * 50,
            f"生成时间: {datetime.now().isoformat()}",
            f"分析周期: 最近30天",
            "",
            "流量统计:",
            f"  - 总流量: {patterns['total_traffic_gb']:.2f} GB",
            f"  - 日均流量: {patterns['average_daily_traffic_gb']:.2f} GB",
            f"  - 峰值流量: {patterns['peak_traffic_gb']:.2f} GB",
            f"  - 峰值日期: {patterns['peak_traffic_day']}",
            "",
            "CDN优化建议:"
        ]
        
        for rec in cdn_recommendations:
            priority_icon = "🔴" if rec['priority'] == 'high' else "🟡"
            report.append(
                f"{priority_icon} {rec['action']}: "
                f"{rec['description']} ({rec['estimated_savings']})"
            )
        
        if patterns['recommendations']:
            report.extend([
                "",
                "其他建议:"
            ])
            for rec in patterns['recommendations']:
                report.append(f"  - {rec}")
        
        # 成本估算
        # 假设CloudFront价格为 $0.085/GB
        cloudfront_price_per_gb = 0.085
        current_cost = patterns['total_traffic_gb'] * cloudfront_price_per_gb
        
        # 估算优化后成本（假设减少30%）
        optimized_cost = current_cost * 0.7
        monthly_savings = current_cost - optimized_cost
        
        report.extend([
            "",
            "成本分析:",
            f"  - 当前月成本: ${current_cost:.2f}",
            f"  - 优化后月成本: ${optimized_cost:.2f}",
            f"  - 预计月节省: ${monthly_savings:.2f}",
            f"  - 预计年节省: ${monthly_savings * 12:.2f}",
            "",
            "实施步骤:",
            "1. 审核并实施CDN优化建议",
            "2. 监控优化后的流量模式",
            "3. 定期重新评估网络配置",
            "=" * 50
        ])
        
        return "\n".join(report)

# 使用示例
optimizer = NetworkOptimizer()
print(optimizer.generate_network_report())
```

---

## 🎯 总结

### 部署最佳实践

1. **渐进式部署**
   - 从单机部署开始验证
   - 逐步过渡到容器化
   - 最终实现云原生架构

2. **监控驱动优化**
   - 部署后立即建立监控
   - 基于数据优化配置
   - 定期审查和调整

3. **安全优先**
   - 最小权限原则
   - 深度防御策略
   - 定期安全审计

4. **成本意识**
   - 选择合适的实例类型
   - 利用自动伸缩
   - 定期成本优化审查

5. **灾难恢复就绪**
   - 定期备份测试
   - 明确的恢复流程
   - 定期演练

### 下一步行动

1. **立即行动**
   - 设置基础监控
   - 配置自动备份
   - 实施基本安全措施

2. **短期目标（1-3个月）**
   - 容器化部署
   - 性能基准测试
   - 安全加固

3. **长期目标（3-12个月）**
   - 云原生架构
   - 高级监控和告警
   - 完整的灾难恢复能力

### 支持资源

- **文档**: https://prism-interconnect.dev/docs
- **社区**: https://discord.gg/prism
- **问题跟踪**: https://github.com/Ultima0369/prism-interconnect/issues
- **商业支持**: contact@prism-interconnect.dev

---

**记住：最好的部署是能够持续改进的部署。** 🚀

定期审查、测试和优化您的部署，确保它能够随着业务增长而扩展，同时保持安全、可靠和成本效益。