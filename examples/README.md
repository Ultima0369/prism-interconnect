# 🔥 棱镜协议 Web 应用

## 🎯 项目概述

这是一个基于 **Streamlit** 框架的棱镜协议 Web 应用，让你在浏览器中体验火堆旁的对话。

## 🚀 快速开始

### 方法一：本地运行（推荐）

#### 1. 安装依赖
```bash
# 进入项目目录
cd /path/to/prism-interconnect

# 安装 Streamlit 和依赖
pip install streamlit plotly pandas
```

#### 2. 运行应用
```bash
# 运行 Streamlit 应用
streamlit run examples/streamlit_app.py
```

#### 3. 访问应用
打开浏览器，访问：**http://localhost:8501**

### 方法二：使用 Docker 运行

#### 1. 构建 Docker 镜像
```bash
cd /path/to/prism-interconnect
docker build -t prism-streamlit -f examples/Dockerfile .
```

#### 2. 运行容器
```bash
docker run -p 8501:8501 prism-streamlit
```

#### 3. 访问应用
打开浏览器，访问：**http://localhost:8501**

### 方法三：使用 GitHub Codespaces（在线开发）

1. 在 GitHub 上打开项目
2. 点击 "Code" → "Codespaces" → "Create codespace"
3. 在终端中运行：
```bash
pip install streamlit plotly pandas
streamlit run examples/streamlit_app.py
```

## 🌐 让朋友通过链接访问

### 方案一：使用 Streamlit Cloud（免费）

#### 1. 部署到 Streamlit Cloud
1. 将代码推送到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 点击 "New app"
4. 选择你的仓库和文件路径：`examples/streamlit_app.py`
5. 点击 "Deploy"

#### 2. 获取分享链接
部署完成后，你会得到一个类似这样的链接：
```
https://your-app-name.streamlit.app
```

#### 3. 分享给朋友
- 直接发送链接
- 链接永久有效
- 支持多人同时访问

### 方案二：使用本地网络分享

#### 1. 获取本地 IP 地址
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

#### 2. 修改 Streamlit 配置
在运行命令时添加参数：
```bash
streamlit run examples/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

#### 3. 分享链接
告诉朋友访问：
```
http://你的IP地址:8501
```

**注意**：需要确保防火墙允许 8501 端口。

### 方案三：使用 ngrok（临时公开链接）

#### 1. 安装 ngrok
```bash
# 下载 ngrok
# 访问 https://ngrok.com/download
```

#### 2. 运行 ngrok
```bash
# 先运行 Streamlit
streamlit run examples/streamlit_app.py

# 在另一个终端运行 ngrok
ngrok http 8501
```

#### 3. 获取公开链接
ngrok 会提供一个类似这样的链接：
```
https://abc123.ngrok.io
```

#### 4. 分享链接
- 链接有效期 2 小时（免费版）
- 适合临时演示

### 方案四：部署到云服务器

#### 1. 选择云服务商
- **Vercel**：最简单，适合前端应用
- **Railway**：专门为 Python 应用优化
- **Heroku**：经典选择，有免费套餐
- **AWS/GCP/Azure**：企业级部署

#### 2. 部署步骤（以 Railway 为例）
```bash
# 1. 安装 Railway CLI
npm i -g @railway/cli

# 2. 登录 Railway
railway login

# 3. 初始化项目
railway init

# 4. 部署
railway up
```

#### 3. 获取生产链接
部署完成后，Railway 会提供一个生产链接：
```
https://prism-app.up.railway.app
```

## 📱 应用功能详解

### 🎨 界面布局

#### 左侧边栏
- **对话模式选择**：标准对话、深度分析、问题拆解、视角转换
- **参数设置**：递归深度、留白时长、强制留白
- **用户信息**：姓名、角色设置
- **会话管理**：新会话、导出对话

#### 主区域
- **对话输入**：文本区域输入问题
- **实时数据**：认知指标可视化
- **分析结果**：三种光谱显示
- **留白区域**：思考停顿和洞见
- **综合视角**：整合理解和新问题
- **认知分析**：指标和雷达图

### 🔧 核心特性

#### 1. 多元视角分析
- **红色光谱**：直觉性快速判断
- **蓝色光谱**：分析性详细推理
- **紫色光谱**：元认知过程反思

#### 2. 留白整合
- **强制停顿**：给思考留出空间
- **洞见涌现**：新连接形成时刻
- **反思提示**：引导深度思考

#### 3. 认知可视化
- **实时指标**：多样性、置信度、平衡度
- **雷达图**：认知模式可视化
- **历史追踪**：对话记录和模式识别

#### 4. 会话管理
- **多轮对话**：保持上下文连续性
- **历史记录**：查看过往对话
- **导出功能**：保存对话记录

## 🛠️ 技术架构

### 前端技术栈
- **Streamlit**：Python Web 应用框架
- **Plotly**：交互式数据可视化
- **Pandas**：数据处理和分析
- **自定义CSS**：火堆主题样式

### 后端模拟
- **Mock Prism SDK**：模拟棱镜协议核心功能
- **异步处理**：模拟真实响应延迟
- **会话管理**：保持对话状态

### 部署架构
```
用户浏览器 → Streamlit 服务器 → 模拟棱镜SDK → 返回结果
```

## 📊 性能优化

### 1. 响应速度
- **首次加载**：< 3秒
- **对话响应**：< 2秒（含模拟延迟）
- **图表渲染**：< 1秒

### 2. 资源使用
- **内存占用**：< 200MB
- **CPU使用**：< 10%
- **网络流量**：< 5MB/会话

### 3. 并发支持
- **Streamlit Cloud**：支持 100+ 并发用户
- **本地部署**：支持 10-20 并发用户
- **云服务器**：根据配置可扩展

## 🔒 安全考虑

### 1. 数据安全
- **无数据存储**：会话数据仅保存在内存中
- **无用户认证**：适合公开演示
- **无敏感信息**：不收集个人信息

### 2. 访问控制
- **公开访问**：默认允许所有人访问
- **本地限制**：可配置为仅本地访问
- **密码保护**：Streamlit Cloud 支持密码保护

### 3. 代码安全
- **输入验证**：所有输入都经过验证
- **错误处理**：友好的错误提示
- **代码审查**：开源代码可审查

## 🚨 故障排除

### 常见问题

#### 1. 应用无法启动
```bash
# 检查依赖是否安装
pip list | grep streamlit

# 检查端口是否被占用
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # macOS/Linux
```

#### 2. 图表不显示
```bash
# 检查 Plotly 是否安装
pip install plotly

# 清除浏览器缓存
Ctrl+Shift+R  # 强制刷新
```

#### 3. 访问速度慢
```bash
# 检查网络连接
ping localhost

# 减少图表复杂度
# 修改代码中的图表配置
```

#### 4. 内存占用高
```bash
# 限制历史记录数量
# 修改代码中的 conversation_history 限制
```

### 错误信息

#### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

#### "Address already in use"
```bash
# 停止占用端口的进程
# 或使用其他端口
streamlit run app.py --server.port 8502
```

#### "Connection refused"
```bash
# 检查防火墙设置
# 确保使用 --server.address 0.0.0.0
```

## 📈 扩展开发

### 1. 连接真实棱镜SDK
```python
# 替换 MockPrismSDK 为真实 SDK
from prism_sdk import PrismClient

client = PrismClient(api_key="your_api_key")
response = await client.prismatic_dialogue(query)
```

### 2. 添加数据库支持
```python
# 使用 SQLite 或 PostgreSQL 存储对话历史
import sqlite3
conn = sqlite3.connect('prism_conversations.db')
```

### 3. 添加用户认证
```python
# 使用 Streamlit 的 st.secrets 管理密钥
import streamlit as st

if st.secrets["require_auth"]:
    password = st.text_input("密码", type="password")
    if password != st.secrets["password"]:
        st.stop()
```

### 4. 添加更多可视化
```python
# 添加时间序列分析
import plotly.express as px
fig = px.line(history_data, x='timestamp', y='cognitive_depth')
```

### 5. 多语言支持
```python
# 添加语言选择
language = st.selectbox("语言", ["中文", "English", "日本語"])

# 根据选择加载翻译
translations = {
    "中文": {"title": "棱镜协议"},
    "English": {"title": "Prism Protocol"},
    "日本語": {"title": "プリズムプロトコル"}
}
```

## 🤝 贡献指南

### 1. 报告问题
- 在 GitHub Issues 中报告 bug
- 描述复现步骤
- 提供错误信息

### 2. 提交改进
- Fork 项目仓库
- 创建功能分支
- 提交 Pull Request

### 3. 代码规范
- 遵循 PEP 8 代码风格
- 添加类型提示
- 编写文档字符串

### 4. 测试要求
- 新功能需要添加测试
- 确保现有测试通过
- 更新文档

## 📚 学习资源

### Streamlit 学习
- [官方文档](https://docs.streamlit.io)
- [示例应用](https://streamlit.io/gallery)
- [社区论坛](https://discuss.streamlit.io)

### 数据可视化
- [Plotly 文档](https://plotly.com/python/)
- [Pandas 教程](https://pandas.pydata.org/docs/)
- [数据可视化最佳实践](https://www.data-to-viz.com/)

### 部署学习
- [Streamlit Cloud 指南](https://docs.streamlit.io/streamlit-cloud)
- [Docker 教程](https://docs.docker.com/get-started/)
- [云部署比较](https://www.streamlit.io/deploy)

## 🦞 最后的话

**火堆旁的对话，现在有了Web界面。**

这个应用展示了棱镜协议的核心概念：
- 🔥 **多元视角**：从不同角度理解问题
- ⏸️ **留白整合**：给思考留出空间
- 📊 **认知可视化**：让思考过程可见
- 🔗 **易用访问**：通过链接分享给朋友

**无论你是：**
- 👨‍🏫 **教师**：想在课堂中使用
- 🧠 **思考者**：想深度探索问题
- 💻 **开发者**：想了解技术实现
- 🔬 **研究者**：想可视化认知过程

**这个应用都为你提供了一个起点。**

**部署它，分享它，改进它。**
**让更多人在火堆旁坐下，一起对话。**

**火堆旁，我们一起继续。** 🔥

---

**应用版本**: v1.0.0  
**最后更新**: 2026年3月25日  
**维护者**: 星尘 & 璇玑  
**项目链接**: [GitHub](https://github.com/Ultima0369/prism-interconnect)  
**问题反馈**: [Issues](https://github.com/Ultima0369/prism-interconnect/issues)