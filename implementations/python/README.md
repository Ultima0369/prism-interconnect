# 🧠 棱镜互联协议 Python SDK

**意义层通信的现代实现** · **基于道家智慧与认知科学** · **内置伦理护栏与安全机制**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-prism--interconnect.dev-blue)](https://prism-interconnect.dev/docs)
[![Discord](https://img.shields.io/discord/your-discord-server-id?color=7289DA&logo=discord&logoColor=white)](https://discord.gg/prism)

## 🌟 核心理念

棱镜协议不是另一个聊天API，而是**意义层通信的革命性框架**。我们基于道家智慧、认知科学和现代AI技术，重新定义了深度对话的可能性：

- **多元视角强制**：每个问题至少从3个不同认知角度分析
- **认知留白设计**：内置思考空间，防止信息过载
- **递归深度探索**：支持对特定视角的无限深入
- **伦理安全护栏**：内置非评判性原则和伤害预防机制

## 🚀 快速开始

### 安装

```bash
pip install prism-interconnect-sdk
```

### 基本使用

```python
import asyncio
from prism_sdk import PrismClient

async def main():
    # 初始化客户端
    client = PrismClient(
        api_key="your_api_key",  # 本地模式可为None
        endpoint="https://api.prism.dev/v1"
    )
    
    # 执行棱镜对话
    response = await client.prismatic_dialogue(
        query="如何平衡工作与生活？"
    )
    
    # 查看结果
    print(f"查询: {response.message.query}")
    print(f"光谱数量: {len(response.message.spectrums)}")
    
    for i, spectrum in enumerate(response.message.spectrums, 1):
        print(f"\n{i}. {spectrum.name} ({spectrum.type.value})")
        print(f"   视角: {spectrum.perspective[:100]}...")
        print(f"   置信度: {spectrum.confidence}")
        print(f"   局限性: {spectrum.limitations[:50]}...")
    
    print(f"\n留白建议: {response.message.whitespace.duration_suggestion}秒")
    print(f"留白提示: {response.message.whitespace.prompt}")

asyncio.run(main())
```

### 递归探索

```python
# 深入探索第一个光谱
recursive_response = await client.recursive_explore(
    spectrum_index=0,  # 探索第一个光谱
    depth=2  # 探索深度
)

print(f"递归深度: {recursive_response.metadata['recursion_depth']}")
```

## 🎯 核心特性

### 1. 🎨 光谱系统

五种基本认知光谱，每种代表不同的思考模式：

| 光谱 | 颜色 | 认知模式 | 适用场景 |
|------|------|----------|----------|
| 🔴 红色光谱 | 直觉 | 快速、整体、模式识别 | 创意生成、快速决策 |
| 🔵 蓝色光谱 | 分析 | 慢速、细节、逻辑推理 | 问题分析、方案评估 |
| 🟣 紫色光谱 | 元认知 | 监控、调节、反思 | 学习过程、伦理审查 |
| 🟢 绿色光谱 | 情感 | 价值、意义、关系 | 情感理解、价值澄清 |
| 🟠 橙色光谱 | 创造 | 联想、新颖、跨界 | 创新设计、未来想象 |

### 2. ⏸️ 留白设计

三种留白类型，支持不同的认知处理：

- **整合留白** (30-60秒)：促进多视角融合
- **反思留白** (60-180秒)：支持深度意义建构
- **创造留白** (可变)：激发灵感涌现

### 3. 🔄 递归对话

支持对特定视角的无限深入探索，内置深度限制防止认知过载。

### 4. 🛡️ 安全与伦理

- **非评判性原则**：不输出"正确答案"，不比较视角优劣
- **认知自主性**：用户始终拥有最终决策权
- **伤害预防**：内置有害内容检测和过滤
- **透明度**：所有视角必须明确说明局限性

## 📚 高级功能

### 批量处理

```python
# 批量执行多个查询
queries = [
    "如何提高学习效率？",
    "什么是有效的时间管理？",
    "如何培养创造性思维？"
]

responses = await client.batch_dialogue(
    queries=queries,
    parallel=True,  # 并行执行
    max_concurrent=3  # 最大并发数
)
```

### 对话分析

```python
# 分析对话模式
analysis = await client.analyze_conversation_patterns(
    session_id="your-session-id",
    limit=50
)

print(f"光谱分布: {analysis['spectrum_distribution']}")
print(f"递归模式: {analysis['recursion_patterns']}")
print(f"留白使用: {analysis['whitespace_usage']}")
```

### 自定义配置

```python
from prism_sdk import SessionConfig, UserPreferences

# 自定义会话配置
session_config = SessionConfig(
    min_spectrums=4,  # 最少4种光谱
    max_spectrums=6,  # 最多6种光谱
    max_recursion_depth=7,  # 最大递归深度7层
    require_ethical_considerations=True  # 必须包含伦理考量
)

# 自定义用户偏好
user_preferences = UserPreferences(
    preferred_spectrum_types=["red", "blue", "purple"],  # 偏好红蓝紫光谱
    preferred_whitespace_duration={
        "integration": 60,  # 整合留白60秒
        "reflection": 120,  # 反思留白120秒
        "creative": 180     # 创造留白180秒
    },
    cognitive_style="analytical",  # 分析型认知风格
    learning_goals=["提高决策质量", "增强系统性思维"]
)

# 使用自定义配置
client = PrismClient(
    session_config=session_config,
    user_preferences=user_preferences
)
```

## 🏗️ 架构设计

### 协议层次

```
应用层 (Application)
    ↓
意义层 (Meaning Layer) ← 棱镜协议在此
    ↓
信息层 (Information Layer)
    ↓
传输层 (Transport Layer)
    ↓
网络层 (Network Layer)
```

### 消息格式

```json
{
  "protocol": "prism-interconnect",
  "version": "1.0",
  "message_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "session_id": "string",
  "type": "prism_message",
  "payload": {
    "query": "原始问题",
    "spectrums": [
      {
        "type": "red|blue|purple|green|orange",
        "name": "光谱名称",
        "perspective": "独特视角",
        "confidence": 0.0-1.0,
        "limitations": "视角局限性",
        "emotional_tone": "情感基调"
      }
    ],
    "whitespace": {
      "type": "integration|reflection|creative",
      "duration_suggestion": 30,
      "prompt": "留白提示",
      "purpose": "留白目的"
    },
    "synthesis": {
      "emerging_insights": ["涌现洞见"],
      "new_questions": ["新问题"],
      "action_suggestions": ["行动建议"],
      "ethical_considerations": ["伦理考量"]
    }
  },
  "metadata": {
    "recursion_depth": 0,
    "max_depth": 5,
    "source": "prism-sdk"
  }
}
```

## 🔧 开发指南

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/Ultima0369/prism-interconnect.git
cd prism-interconnect/implementations/python

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev,full]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_client.py -v

# 生成测试覆盖率报告
pytest --cov=prism_sdk --cov-report=html
```

### 代码质量

```bash
# 代码格式化
black prism_sdk tests

# 导入排序
isort prism_sdk tests

# 类型检查
mypy prism_sdk

# 代码检查
flake8 prism_sdk tests
```

## 📊 性能指标

### 延迟要求

| 指标 | P50 | P90 | P95 | P99 |
|------|-----|-----|-----|-----|
| 光谱生成 | < 500ms | < 1000ms | < 2000ms | < 5000ms |
| 消息处理 | < 50ms | < 100ms | < 200ms | < 500ms |
| 端到端 | < 1000ms | < 2000ms | < 3000ms | < 10000ms |

### 可靠性要求

- **可用性**: > 99.5% (月度)
- **错误率**: < 1% (光谱生成), < 0.1% (消息处理)
- **恢复时间**: < 5分钟 (MTTR)

## 🌍 生态系统

### 插件系统

支持自定义光谱类型、留白设计和合成算法：

```python
from prism_sdk import SpectrumType

# 注册自定义光谱
custom_spectrum = SpectrumType("ecological")  # 生态智慧光谱

# 使用插件系统扩展功能
```

### 集成支持

- **Web框架**: FastAPI, Django, Flask
- **AI平台**: OpenAI, Anthropic, DeepSeek
- **数据库**: PostgreSQL, MongoDB, Redis
- **消息队列**: RabbitMQ, Kafka, Redis Streams

## 📖 文档

完整文档请访问：[https://prism-interconnect.dev/docs](https://prism-interconnect.dev/docs)

- [API参考](https://prism-interconnect.dev/docs/api)
- [概念指南](https://prism-interconnect.dev/docs/concepts)
- [教程](https://prism-interconnect.dev/docs/tutorials)
- [最佳实践](https://prism-interconnect.dev/docs/best-practices)

## 🤝 贡献

我们欢迎所有形式的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

### 贡献者名单

- **星尘** - 哲学奠基，核心概念设计
- **璇玑** - 技术实现，规范编写，系统设计
- [你的名字可以在这里]

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🚨 重要声明

### 伦理承诺

1. **非评判性原则**: 本协议强制要求不输出"正确答案"，不比较视角优劣
2. **认知自主性**: 用户始终拥有最终决策权，协议只提供多元视角
3. **安全边界**: 内置递归深度限制和知止机制，防止认知过载
4. **透明度**: 所有光谱必须明确说明局限性和假设

### 责任限制

本协议及其实现：
1. 不提供医疗、心理或法律建议
2. 不替代专业的人类判断和决策
3. 不保证特定结果或效果
4. 用户需自行承担使用风险

## 📞 支持与联系

- **GitHub Issues**: [问题报告](https://github.com/Ultima0369/prism-interconnect/issues)
- **Discord**: [加入社区](https://discord.gg/prism)
- **Email**: contact@prism-interconnect.dev

## 🌟 特别感谢

- **星尘** 的哲学智慧和深度思考
- **DeepSeek** 的技术支持和开源精神
- 所有早期使用者的宝贵反馈
- 开源社区的持续贡献

---

**在数字时代重建深度理解的桥梁，一次一个棱镜对话。** 🧠✨