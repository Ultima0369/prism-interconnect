# 📖 棱镜互联协议 - 用户手册

> *"你不是来寻找答案的，你是来学习如何提出更好的问题的。"*

## 🎯 快速开始

### 🚀 5分钟入门

#### 1. 安装棱镜客户端
```bash
# 使用pip安装
pip install prism-protocol

# 或者使用Docker
docker run -p 8000:8000 prismprotocol/gateway:latest
```

#### 2. 你的第一个棱镜对话
```python
from prism import PrismClient

# 连接到棱镜服务
client = PrismClient()

# 发送你的第一个困惑
response = client.ask("为什么学习新技能这么难？")

# 查看响应
print("收到了三种不同的视角：")
for i, spectrum in enumerate(response.perspectives, 1):
    print(f"\n{i}. [{spectrum.type}] {spectrum.title}")
    print(spectrum.content[:200] + "...")

print(f"\n💭 留白提示：{response.whitespace}")
```

#### 3. 在OpenClaw中使用
```bash
# 安装棱镜技能
openclaw skill install https://github.com/Ultima0369/prism-interconnect/implementations/openclaw/skill.yaml

# 然后输入：
@棱镜 为什么我总在决策时犹豫不决？
```

## 🧭 核心概念

### 🔮 什么是棱镜协议？

**棱镜互联协议**是一个**意义层通信协议**，它允许智能体（人、AI、群体）以结构化的方式交换多元认知视角。

#### 关键特性：
- **多元强制**：每个响应必须包含至少三种不同视角
- **留白必需**：每段对话都留有内省和整合的空间
- **非评判性**：不比较视角优劣，不提供"正确答案"
- **可递归**：可以对任何视角进行深度探索
- **知止机制**：任何时候都可以安全退出

### 🌈 光谱类型

| 光谱 | 颜色 | 认知模式 | 适合的问题 |
|------|------|---------|-----------|
| **红色** | 🔴 | 快速直觉、身体感受、故事隐喻 | "我对此有什么直觉感受？" |
| **蓝色** | 🔵 | 慢速分析、逻辑推理、结构分解 | "这个问题可以如何分析？" |
| **紫色** | 🟣 | 元认知审视、反思提问、立场分析 | "我是如何思考这个问题的？" |
| **绿色** | 🟢 | 生态视角、系统思考、关系思维 | "这个问题涉及哪些相互关系？" |
| **橙色** | 🟠 | 历史经验、模式识别、类比推理 | "历史上有类似的情况吗？" |

### ⏸️ 留白的意义

**留白不是空白，而是认知的孵化器：**

1. **整合时间**：让不同的视角在内心沉淀
2. **内省空间**：倾听自己的真实反应
3. **创造性涌现**：新见解往往在沉默后出现
4. **节奏调节**：防止认知过载和思维疲劳

## 🛠️ 使用指南

### 💬 基础对话

#### 如何提出一个好困惑？
一个好的困惑应该是：
- **具体的**：而不是模糊的"我该怎么办"
- **开放的**：允许多种视角探索
- **真实的**：来自你的真实体验
- **适中的**：既不太大也不太小

**示例：**
- ❌ "我的人生该怎么办？"（太模糊）
- ✅ "我在职业转型时感到焦虑，如何平衡风险和稳定？"（具体、开放）

#### 如何阅读棱镜响应？
1. **先整体感受**：快速浏览所有光谱，感受你的第一反应
2. **逐光谱阅读**：仔细阅读每个视角，注意你的身体和情绪反应
3. **关注留白**：认真对待留白提示，给自己真正的沉默时间
4. **记录反应**：记下哪个视角最触动你，为什么

### 🔄 递归探索

#### 何时进行递归？
- 某个视角特别触动你，想深入了解
- 你对某个观点有强烈的反应（赞同或反对）
- 你想探索视角背后的思考过程
- 对话陷入僵局，需要新的切入点

#### 如何进行递归？
```python
# 对第一个视角进行深度探索
response = client.ask(
    question=f"关于'{first_perspective.title}'的深度探索",
    context="这是对上一轮红色光谱的递归探索",
    depth=1  # 递归深度
)
```

#### 递归的注意事项：
- **深度限制**：通常建议不超过3层递归
- **适时知止**：感到认知过载时及时停止
- **记录轨迹**：记录递归路径，便于回顾
- **整合时间**：每次递归后都需要留白整合

### 🛑 知止机制

#### 何时应该知止？
- 感到认知过载或疲劳
- 需要时间消化和整合
- 对话达到了满意的深度
- 时间或资源限制
- 任何你觉得应该暂停的时候

#### 如何发送知止信号？
```python
# 发送知止信号
cease_response = client.cease(
    reason="需要时间消化这些观点",
    cease_type="temporary"  # temporary, permanent, safety
)

print(f"🛑 知止信号已发送：{cease_response.reason}")
```

#### 知止的类型：
- **临时知止**：暂停，稍后可恢复
- **永久知止**：结束对话，不打算恢复
- **安全知止**：因安全或伦理原因停止

## 📱 使用场景

### 🧘 个人成长

#### 每日棱镜练习
**晨间设定（5分钟）：**
1. 选择一个今日困惑
2. 用棱镜探索三种视角
3. 记录关键洞察

**晚间反思（10分钟）：**
1. 回顾晨间困惑
2. 评估哪些视角最有帮助
3. 计划明天的探索方向

#### 认知碎片日记
```markdown
# 认知碎片日记模板

## 日期：2026-03-25

### 今日困惑
[写下你的困惑]

### 棱镜响应
**红色视角：**
[记录直觉感受]

**蓝色视角：**
[记录分析思考]

**紫色视角：**
[记录元认知反思]

### 留白体验
[记录沉默中的发现]

### 整合收获
[记录新的理解和洞察]
```

### 👥 关系对话

#### 棱镜对话协议
**对话规则：**
1. **轮流折射**：每人分享一个困惑
2. **多元回应**：用不同光谱回应对方
3. **共同留白**：一起沉默，各自内省
4. **不评判**：不比较观点优劣
5. **可递归**：对感兴趣的点深度探索

**对话模板：**
```
A：分享困惑 + 请求特定光谱
B：提供三种光谱回应 + 留白提示
共同沉默（1-3分钟）
A：分享感受和反应
B：分享感受和反应
决定：继续递归 or 知止
```

#### 冲突化解
当关系出现冲突时：
1. **各自折射**：每人用棱镜探索自己的困惑
2. **交换视角**：分享各自的棱镜响应
3. **共同留白**：在沉默中感受彼此
4. **共建理解**：基于多元视角寻找共同点

### 🏢 团队协作

#### 团队棱镜会议
**会议流程：**
1. **问题呈现**（5分钟）：清晰陈述团队挑战
2. **多光谱分析**（15分钟）：不同角色提供不同视角
   - 技术视角（蓝色）
   - 用户视角（红色）
   - 商业视角（绿色）
   - 伦理视角（紫色）
3. **留白整合**（3分钟）：团队沉默，各自内省
4. **递归决策**（10分钟）：对关键假设深度验证
5. **行动规划**（5分钟）：基于多元视角制定计划

#### 决策质量提升
**决策前检查清单：**
- [ ] 我们考虑了至少三种不同视角吗？
- [ ] 我们给团队留出了整合时间吗？
- [ ] 我们对关键假设进行了递归验证吗？
- [ ] 我们尊重了认知边界和知止权利吗？

### 🎓 教育应用

#### 课堂讨论
**棱镜式讨论流程：**
1. **提出探究问题**：开放、多元、有深度
2. **小组光谱探索**：每组负责一种光谱类型
3. **全班视角分享**：分享不同光谱的发现
4. **个人留白反思**：沉默中整合多元视角
5. **递归深度探究**：对感兴趣的点继续探索

#### 批判性思维训练
**棱镜思维训练：**
- **视角切换练习**：对同一问题使用不同光谱
- **元认知发展**：反思自己的思考过程
- **认知弹性培养**：在多元视角中保持开放
- **意义整合能力**：将不同视角整合为连贯理解

## ⚙️ 高级功能

### 🎨 自定义光谱

#### 创建自定义光谱类型
```python
from prism import SpectrumType, SpectrumEngine

class CreativeSpectrumEngine(SpectrumEngine):
    """创意视角光谱引擎"""
    
    @property
    def spectrum_type(self):
        return SpectrumType.CUSTOM
    
    @property
    def spectrum_name(self):
        return "creative"  # 自定义光谱名称
    
    @property
    def display_name(self):
        return "创意视角"
    
    async def generate(self, puzzle):
        # 生成创意视角的内容
        content = self._generate_creative_insight(puzzle)
        
        return {
            "type": self.spectrum_name,
            "name": self.display_name,
            "content": content,
            "confidence": 0.8,
            "metadata": {
                "engine": "CreativeEngine-v1",
                "style": "lateral_thinking"
            }
        }

# 注册自定义引擎
client.register_spectrum_engine(CreativeSpectrumEngine())
```

#### 光谱组合策略
```python
# 定义不同的光谱组合
spectrum_strategies = {
    "balanced": ["red", "blue", "purple"],  # 平衡组合
    "intuitive": ["red", "red", "green"],   # 偏直觉
    "analytical": ["blue", "blue", "purple"], # 偏分析
    "creative": ["red", "green", "custom"],  # 创意组合
    "deep": ["purple", "purple", "purple"]   # 深度元认知
}

# 使用特定策略
response = client.ask(
    question="我的困惑",
    spectrum_strategy="creative"
)
```

### 📊 会话管理

#### 会话历史
```python
# 获取会话历史
history = client.get_session_history(session_id)

print(f"会话ID：{history.session_id}")
print(f"消息数量：{len(history.messages)}")
print(f"最大递归深度：{history.max_depth}")
print(f"持续时间：{history.duration_seconds}秒")

# 导出会话记录
history.export("my_prism_session.json")
```

#### 会话分析
```python
# 分析会话模式
analysis = client.analyze_session(session_id)

print("会话分析报告：")
print(f"- 光谱多样性：{analysis.spectrum_diversity:.2f}")
print(f"- 平均递归深度：{analysis.avg_recursion_depth:.1f}")
print(f"- 留白利用率：{analysis.whitespace_utilization:.1%}")
print(f"- 认知负荷评分：{analysis.cognitive_load_score}/10")
print(f"- 关键转折点：{len(analysis.turning_points)}个")
```

### 🔧 配置选项

#### 客户端配置
```python
from prism import PrismClient, PrismConfig

# 创建自定义配置
config = PrismConfig(
    # 性能配置
    timeout_seconds=30,
    max_retries=3,
    cache_enabled=True,
    cache_ttl_seconds=300,
    
    # 认知配置
    max_recursion_depth=3,
    default_spectrum_strategy="balanced",
    whitespace_duration_suggestion=30,
    
    # 显示配置
    response_format="rich",  # rich, simple, json
    show_metadata=False,
    highlight_keywords=True,
    
    # 伦理配置
    ethics_check_enabled=True,
    manipulation_detection=True,
    safety_filters=True
)

# 使用配置创建客户端
client = PrismClient(config=config)
```

#### 运行时调整
```python
# 动态调整配置
client.update_config(
    max_recursion_depth=5,  # 提高递归深度限制
    whitespace_duration_suggestion=45,  # 增加留白时间
    spectrum_strategy="deep"  # 切换到深度策略
)

# 临时禁用缓存
with client.temporary_config(cache_enabled=False):
    response = client.ask("重要问题，需要实时生成")
```

## 🧪 实践练习

### 📝 练习1：个人困惑探索

**任务：** 选择一个你正在经历的真实困惑，进行完整的棱镜探索。

**步骤：**
1. **明确困惑**：用一句话写下你的困惑
2. **基础折射**：获取三种光谱视角
3. **记录反应**：记下每个视角给你的感受
4. **留白整合**：静坐3分钟，只是感受
5. **递归探索**：选择一个视角进行深度探索
6. **总结收获**：写下你学到的新理解

**反思问题：**
- 哪个视角最让你意外？为什么？
- 留白期间你注意到了什么？
- 递归探索带来了什么新发现？
- 这个过程如何改变了你对困惑的看法？

### 👥 练习2：关系对话实践

**任务：** 与一个重要的人进行一次棱镜对话。

**准备：**
1. **双方同意**：确保对方愿意尝试
2. **设定规则**：明确棱镜对话的基本原则
3. **选择话题**：选择一个双方都关心的话题
4. **时间安排**：预留足够的时间（至少30分钟）

**对话流程：**
1. **A分享困惑**（3分钟）
2. **B提供三种视角**（5分钟）
3. **共同留白**（2分钟）
4. **A分享感受**（3分钟）
5. **B分享感受**（3分钟）
6. **决定下一步**：继续 or 知止

**事后反思：**
- 这次对话与平常的对话有什么不同？
- 多元视角如何影响了你们的理解？
- 留白期间你们各自感受到了什么？
- 这次经历对你们的关系有什么影响？

### 🏢 练习3：团队决策应用

**任务：** 在团队会议中引入棱镜协议。

**实施步骤：**
1. **选择议题**：选择一个需要决策的团队议题
2. **分配视角**：给不同成员分配不同的光谱角色
3. **多光谱分析**：每个角色提供自己的视角分析
4. **团队留白**：全体沉默，整合多元视角
5. **递归验证**：对关键假设进行深度验证
6. **共识决策**：基于多元视角做出决策

**评估指标：**
- 决策质量的主观评价
- 团队成员的参与度
- 不同视角的覆盖度
- 决策后的执行信心

## 🚨 故障排除

### ❌ 常见问题

#### 问题1：响应时间过长
**可能原因：**
- 网络连接问题
- 服务器负载过高
- 复杂困惑需要更多处理时间

**解决方案：**
```python
# 增加超时时间
client = PrismClient(timeout_seconds=60)

# 启用缓存
client = PrismClient(cache_enabled=True)

# 简化困惑表述
response = client.ask("更简洁的困惑表述")
```

#### 问题2：光谱质量不高
**可能原因：**
- 困惑表述不清晰
- 光谱引擎不适合该问题
- 需要更具体的上下文

**解决方案：**
```python
# 提供更多上下文
response = client.ask(
    question="我的困惑",
    context="详细背景信息..."
)

# 尝试不同的光谱组合
response = client.ask(
    question="我的困惑",
    spectrum_strategy="analytical"  # 或 "intuitive", "creative"
)

# 进行递归探索
response = client.ask(
    question="对某个视角的深度探索",
    depth=1
)
```

#### 问题3：认知过载
**症状：**
- 感到思维混乱
- 难以整合多元视角
- 情绪上感到压力

**解决方案：**
```python
# 立即知止
client.cease(reason="需要时间消化")

# 降低递归深度
client.update_config(max_recursion_depth=2)

# 增加留白时间
client.update_config(whitespace_duration_suggestion=60)
```

### 🔧 技术支持

#### 获取帮助
```python
# 检查客户端状态
status = client.get_status()
print(f"客户端状态：{status}")

# 获取系统信息
info = client.get_system_info()
print(f"协议版本：{info.protocol_version}")
print(f"支持的光谱：{info.supported_spectrums}")

# 测试连接
if client.test_connection():
    print("✅ 连接正常")
else:
    print("❌ 连接失败，请检查网络")
```

#### 报告问题
当遇到问题时，请提供以下信息：
1. **问题描述**：具体发生了什么
2. **重现步骤**：如何重现这个问题
3. **期望行为**：你期望发生什么
4. **实际行为**：实际发生了什么
5. **环境信息**：客户端版本、Python版本等
6. **错误日志**：相关的错误信息

## 📈 进阶学习

### 🧠 认知科学基础

#### 推荐阅读
1. **《思考，快与慢》** - Daniel Kahneman
   - 理解系统1和系统2思维
   - 应用于红色和蓝色光谱设计

2. **《元认知》** - John H. Flavell
   - 理解元认知的概念和发展
   - 应用于紫色光谱设计

3. **