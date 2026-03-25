# 🎮 棱镜协议演示环境

## 🎯 演示目标

提供多种方式体验棱镜协议，从快速体验到完整部署。

## 🚀 快速体验

### 1. 🌐 在线演示（最简单）
**无需安装，立即体验**

#### Streamlit Cloud 演示
```
https://prism-interconnect.streamlit.app
```

#### GitHub Codespaces
1. 点击 GitHub 仓库的 "Code" → "Codespaces"
2. 创建新的 Codespace
3. 运行：`streamlit run examples/streamlit_app.py`
4. 访问弹出的链接

#### Replit 演示
```
https://replit.com/@yourusername/prism-demo
```

### 2. 🐳 Docker 快速启动
**一键启动完整演示环境**

```bash
# 拉取演示镜像
docker pull prisminterconnect/demo:latest

# 运行演示
docker run -p 8501:8501 prisminterconnect/demo:latest

# 访问 http://localhost:8501
```

### 3. 📦 本地快速启动
**在本地快速运行演示**

```bash
# 克隆仓库
git clone https://github.com/Ultima0369/prism-interconnect.git
cd prism-interconnect

# 安装依赖
pip install -r examples/requirements.txt

# 运行演示
streamlit run examples/streamlit_app.py

# 访问 http://localhost:8501
```

## 🏗️ 完整演示环境

### 1. 🐳 Docker Compose 环境
**完整的开发和生产环境**

```bash
# 启动开发环境
docker-compose -f examples/docker-compose.yml up prism-dev

# 启动生产环境
docker-compose -f examples/docker-compose.yml up prism-prod nginx

# 启动完整监控栈
docker-compose -f examples/docker-compose.yml up
```

### 2. ☸️ Kubernetes 环境
**生产就绪的Kubernetes部署**

```bash
# 部署到Kubernetes
kubectl apply -f deploy/kubernetes/prism-sdk-deployment.yaml

# 查看部署状态
kubectl get all -n prism-production

# 端口转发访问
kubectl port-forward service/prism-sdk-service 8000:80 -n prism-production
```

### 3. ☁️ 云平台部署
**一键部署到云平台**

#### Vercel 部署
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel
```

#### Railway 部署
```bash
# 安装Railway CLI
npm i -g @railway/cli

# 部署
railway up
```

#### Heroku 部署
```bash
# 创建Heroku应用
heroku create prism-demo

# 部署
git push heroku main
```

## 🎨 演示场景

### 1. 🧠 个人思考演示
**体验棱镜对话的核心功能**

#### 演示问题
- "如何平衡工作与生活？"
- "什么是真正的创造力？"
- "人工智能会改变人类认知吗？"
- "如何建立有意义的对话？"

#### 体验重点
- 🔥 **三种光谱**：体验不同思考视角
- ⏸️ **留白时刻**：体验思考停顿的价值
- 📊 **认知可视化**：查看思考过程的可视化
- 📜 **对话历史**：回顾思考历程

### 2. 👨‍🏫 教育场景演示
**在课堂环境中使用棱镜协议**

#### 课堂活动设计
1. **问题提出**：教师提出开放性问题
2. **个人思考**：学生使用棱镜协议独立思考
3. **小组讨论**：分享不同光谱的思考结果
4. **全班整合**：整合多元视角，形成完整理解

#### 教学资源
- **课程计划模板**
- **学生指导手册**
- **评估量表**
- **案例研究库**

### 3. 🧪 研究场景演示
**使用棱镜协议进行认知研究**

#### 研究设计
1. **研究问题**：设计研究问题
2. **数据收集**：使用棱镜协议收集认知数据
3. **数据分析**：分析认知模式和思考过程
4. **结果报告**：生成研究报告

#### 研究工具
- **数据导出工具**
- **统计分析脚本**
- **可视化工具**
- **报告模板**

### 4. 💼 企业场景演示
**在企业环境中应用棱镜协议**

#### 应用场景
- **团队决策**：多角度分析决策问题
- **产品设计**：从不同视角理解用户需求
- **战略规划**：全面分析战略选择
- **问题解决**：系统化的问题解决方法

#### 企业工具
- **团队协作模板**
- **项目管理集成**
- **数据分析仪表板**
- **报告生成工具**

## 🔧 演示配置

### 1. 环境变量配置
```bash
# 开发环境
export PRISM_ENV=development
export LOG_LEVEL=DEBUG
export DEMO_MODE=true

# 生产环境
export PRISM_ENV=production
export LOG_LEVEL=INFO
export SECURITY_ENABLED=true
```

### 2. 功能开关配置
```python
# config/demo_config.py
DEMO_CONFIG = {
    "features": {
        "spectra_enabled": True,      # 启用光谱功能
        "whitespace_enabled": True,   # 启用留白功能
        "synthesis_enabled": True,    # 启用合成功能
        "history_enabled": True,      # 启用历史功能
        "export_enabled": True,       # 启用导出功能
    },
    "limits": {
        "max_query_length": 1000,     # 最大查询长度
        "max_history_items": 50,      # 最大历史记录
        "whitespace_duration": 45,    # 留白时长（秒）
        "max_recursion_depth": 3,     # 最大递归深度
    },
    "ui": {
        "theme": "fire",              # 界面主题
        "language": "zh",             # 界面语言
        "accessibility": True,        # 可访问性支持
        "responsive": True,           # 响应式设计
    }
}
```

### 3. 数据模拟配置
```python
# demo/data_simulator.py
class DemoDataSimulator:
    """演示数据模拟器"""
    
    def generate_sample_queries(self):
        """生成示例问题"""
        return [
            "如何做出重要的人生决策？",
            "什么是真正的幸福？",
            "科技发展如何影响人际关系？",
            "如何培养深度思考能力？",
            "人工智能的伦理边界在哪里？"
        ]
    
    def generate_sample_responses(self):
        """生成示例响应"""
        return {
            "spectra": {
                "red": "直觉视角的快速判断",
                "blue": "分析视角的详细推理",
                "purple": "元认知视角的过程反思"
            },
            "whitespace": {
                "duration": 45,
                "insights": ["新连接形成", "模式识别", "假设浮现"]
            },
            "synthesis": {
                "integrated_view": "综合多元视角的完整理解",
                "new_questions": ["进一步探索的问题"]
            }
        }
```

## 📊 演示指标

### 1. 用户体验指标
```python
DEMO_METRICS = {
    "performance": {
        "load_time": "< 3s",          # 页面加载时间
        "response_time": "< 2s",      # 响应时间
        "uptime": "> 99.9%",          # 可用性
        "error_rate": "< 0.1%",       # 错误率
    },
    "engagement": {
        "session_duration": "> 5m",   # 会话时长
        "queries_per_session": "> 3", # 每会话查询数
        "return_rate": "> 30%",       # 返回率
        "satisfaction": "> 4.5/5",    # 满意度
    },
    "learning": {
        "concept_understanding": "> 80%",  # 概念理解率
        "skill_acquisition": "> 70%",      # 技能掌握率
        "knowledge_retention": "> 60%",    # 知识保留率
        "behavior_change": "> 40%",        # 行为改变率
    }
}
```

### 2. 技术性能指标
```python
TECH_METRICS = {
    "scalability": {
        "concurrent_users": "> 100",      # 并发用户数
        "requests_per_second": "> 50",    # 每秒请求数
        "data_throughput": "> 10 MB/s",   # 数据吞吐量
        "cache_hit_rate": "> 90%",        # 缓存命中率
    },
    "reliability": {
        "mean_time_between_failures": "> 30d",  # 平均故障间隔
        "mean_time_to_recovery": "< 5m",        # 平均恢复时间
        "data_consistency": "> 99.99%",         # 数据一致性
        "backup_frequency": "hourly",           # 备份频率
    },
    "security": {
        "vulnerability_count": "0",             # 漏洞数量
        "security_incidents": "0",              # 安全事件
        "compliance_score": "100%",             # 合规分数
        "audit_frequency": "quarterly",         # 审计频率
    }
}
```

## 🎥 演示视频

### 1. 快速开始视频（2分钟）
**内容**：如何在2分钟内开始使用棱镜协议
**链接**：https://youtube.com/watch?v=prism-quickstart

### 2. 功能演示视频（5分钟）
**内容**：完整的功能演示和用例展示
**链接**：https://youtube.com/watch?v=prism-features

### 3. 技术深度视频（15分钟）
**内容**：技术架构和实现原理深度解析
**链接**：https://youtube.com/watch?v=prism-tech-deepdive

### 4. 哲学思考视频（30分钟）
**内容**：棱镜协议的哲学基础和文明愿景
**链接**：https://youtube.com/watch?v=prism-philosophy

## 📚 演示资源

### 1. 演示脚本
```bash
# 运行演示脚本
python demo/scripts/demo_script.py

# 脚本内容
1. 欢迎和介绍（1分钟）
2. 核心功能演示（3分钟）
3. 用例展示（2分钟）
4. 技术亮点（2分钟）
5. Q&A环节（2分钟）
```

### 2. 演示材料
- **演示PPT**：`demo/slides/prism-demo.pptx`
- **宣传单页**：`demo/flyers/prism-flyer.pdf`
- **案例研究**：`demo/case-studies/`
- **教学材料**：`demo/teaching-materials/`

### 3. 演示工具
- **屏幕录制**：OBS Studio 配置
- **直播设置**：StreamYard 配置
- **互动工具**：Miro 白板模板
- **反馈收集**：Typeform 问卷

## 🚨 故障排除

### 常见问题

#### Q: 演示无法启动
```bash
# 检查端口占用
netstat -ano | findstr :8501

# 使用其他端口
streamlit run app.py --server.port 8502
```

#### Q: 依赖安装失败
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

#### Q: 性能问题
```python
# 调整性能参数
import prism_sdk
client = prism_sdk.PrismClient(
    max_workers=2,      # 减少并发数
    timeout=60,         # 增加超时时间
    cache_size=100      # 调整缓存大小
)
```

### 紧急恢复
```bash
# 快速恢复脚本
./demo/scripts/emergency_recovery.sh

# 脚本内容
1. 停止所有服务
2. 清理临时文件
3. 重启服务
4. 验证恢复
```

## 🤝 演示支持

### 技术支持
- **实时聊天**：演示期间的实时技术支持
- **备用方案**：多个演示环境的备用方案
- **监控告警**：演示期间的实时监控
- **应急响应**：快速应急响应团队

### 内容支持
- **演示脚本**：完整的演示脚本和讲稿
- **问答准备**：预准备的Q&A问题
- **案例准备**：多个用例的详细准备
- **材料准备**：所有演示材料的准备

### 后勤支持
- **时间安排**：演示时间安排和提醒
- **设备检查**：演示设备的事前检查
- **网络保障**：网络连接的质量保障
- **环境测试**：演示环境的全面测试

## 🦞 最后的话

**演示不是表演，而是对话的开始。**

在棱镜协议演示中，我们展示的不仅是功能，更是：
- 🔥 **火堆旁的邀请**：邀请更多人加入火堆旁的对话
- 🧠 **认知的镜子**：展示思考过程的可视化和反思
- 🌐 **连接的桥梁**：连接不同背景和领域的人们
- 🌱 **成长的起点**：每个演示都是认知成长的起点

**我们相信，最好的演示是让观众也想参与对话。**
**我们精心准备演示环境，让每个人都能轻松开始棱镜之旅。**

---

**演示环境版本**：v1.0.0  
**最后更新**：2026年3月25日  
**演示团队**：棱镜协议社区  
**支持语言**：中文、英文  
**可用时间**：7×24小时（在线演示）  

**记住：演示的目的是开始对话，而不是结束对话。** 🎮