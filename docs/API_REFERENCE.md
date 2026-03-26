# 📚 棱镜协议API参考

## 🎯 API设计哲学

棱镜协议的API设计遵循以下原则：

### 1. 🔥 **火堆旁的对话**
- **自然性**：API调用应该像对话一样自然
- **渐进性**：从简单到复杂，逐步深入
- **反馈性**：每一步都有清晰的反馈和状态

### 2. 🧠 **认知友好**
- **一致性**：相似的操作用相似的接口
- **可预测性**：行为可预测，错误可理解
- **自描述性**：API本身说明其用途和用法

### 3. 🌈 **光谱完整性**
- **多元视角**：支持不同视角的数据访问
- **过程透明**：思考过程可观察和调试
- **结果丰富**：返回丰富的信息和元数据

### 4. ⏸️ **留白设计**
- **异步友好**：支持异步和同步两种模式
- **超时控制**：可配置的超时和取消机制
- **进度反馈**：长时间操作的进度反馈

## 🚀 快速API概览

### 核心API调用
```python
from prism_sdk import PrismClient

# 创建客户端
client = PrismClient()

# 核心对话API
response = await client.prismatic_dialogue(
    query="如何平衡工作与生活？",
    max_depth=3,
    whitespace_duration=45
)

# 光谱分析API
spectra = await client.analyze_spectra(
    query="什么是真正的创造力？",
    spectra=["red", "blue", "purple"]
)

# 留白体验API
whitespace = await client.experience_whitespace(
    insights=["初步想法1", "初步想法2"],
    duration=60
)

# 综合视角API
synthesis = await client.synthesize_perspectives(
    spectra_results=[red_result, blue_result, purple_result],
    whitespace_insights=whitespace_insights
)
```

### 配置API
```python
# 客户端配置
client = PrismClient(
    api_key="your-api-key",          # API密钥
    base_url="https://api.prism.dev", # API基础URL
    timeout=30,                      # 超时时间（秒）
    max_retries=3,                   # 最大重试次数
    cache_enabled=True,              # 启用缓存
    cache_ttl=300,                   # 缓存TTL（秒）
    logging_level="INFO",            # 日志级别
    user_agent="prism-client/1.0.0"  # 用户代理
)

# 运行时配置
config = {
    "max_recursion_depth": 5,        # 最大递归深度
    "whitespace_min_duration": 30,   # 最小留白时长
    "whitespace_max_duration": 180,  # 最大留白时长
    "confidence_threshold": 0.7,     # 置信度阈值
    "temperature": 0.8,              # 创造性温度
    "top_p": 0.9,                    # 核采样参数
    "max_tokens": 2000,              # 最大token数
    "stream": False                  # 是否流式响应
}
```

## 📋 API详细参考

### PrismClient类

#### 构造函数
```python
PrismClient(
    api_key: Optional[str] = None,
    base_url: str = "https://api.prism.dev",
    timeout: int = 30,
    max_retries: int = 3,
    cache_enabled: bool = True,
    cache_ttl: int = 300,
    logging_level: str = "INFO",
    user_agent: str = "prism-client/1.0.0",
    **kwargs
) -> None
```

**参数说明：**
- `api_key` (str, optional): API密钥，用于认证
- `base_url` (str): API基础URL，默认生产环境
- `timeout` (int): 请求超时时间（秒）
- `max_retries` (int): 失败请求的最大重试次数
- `cache_enabled` (bool): 是否启用响应缓存
- `cache_ttl` (int): 缓存生存时间（秒）
- `logging_level` (str): 日志级别（DEBUG, INFO, WARNING, ERROR）
- `user_agent` (str): 自定义用户代理字符串
- `**kwargs`: 其他HTTP客户端配置

**示例：**
```python
# 生产环境客户端
prod_client = PrismClient(
    api_key="prod-key-123",
    base_url="https://api.prism.dev",
    timeout=60
)

# 开发环境客户端
dev_client = PrismClient(
    api_key="dev-key-456",
    base_url="http://localhost:8000",
    timeout=120,
    logging_level="DEBUG"
)

# 测试环境客户端
test_client = PrismClient(
    base_url="http://test.prism.local",
    cache_enabled=False
)
```

#### prismatic_dialogue方法
```python
async def prismatic_dialogue(
    self,
    query: str,
    max_depth: int = 3,
    whitespace_duration: int = 45,
    spectra: List[str] = None,
    config: Optional[Dict] = None,
    session_id: Optional[str] = None,
    metadata: Optional[Dict] = None,
    **kwargs
) -> PrismResponse
```

**参数说明：**
- `query` (str): 用户查询的问题或话题
- `max_depth` (int): 最大递归思考深度（1-5）
- `whitespace_duration` (int): 留白时长（秒，30-180）
- `spectra` (List[str], optional): 使用的光谱列表，默认全部
- `config` (Dict, optional): 运行时配置覆盖
- `session_id` (str, optional): 会话ID，用于对话连续性
- `metadata` (Dict, optional): 附加元数据
- `**kwargs`: 其他API参数

**返回：** `PrismResponse`对象

**示例：**
```python
# 基本对话
response = await client.prismatic_dialogue(
    query="如何做出重要的人生决策？",
    max_depth=3
)

# 深度对话
deep_response = await client.prismatic_dialogue(
    query="人工智能的伦理边界在哪里？",
    max_depth=5,
    whitespace_duration=90,
    config={
        "temperature": 0.9,
        "max_tokens": 3000
    }
)

# 特定光谱对话
focused_response = await client.prismatic_dialogue(
    query="从直觉角度分析这个商业机会",
    spectra=["red"],  # 只使用红色光谱
    max_depth=2
)
```

#### analyze_spectra方法
```python
async def analyze_spectra(
    self,
    query: str,
    spectra: List[str] = None,
    depth: int = 1,
    include_confidence: bool = True,
    include_reasoning: bool = True,
    **kwargs
) -> Dict[str, SpectrumAnalysis]
```

**参数说明：**
- `query` (str): 要分析的问题
- `spectra` (List[str], optional): 要分析的光谱列表
- `depth` (int): 分析深度（1-3）
- `include_confidence` (bool): 是否包含置信度
- `include_reasoning` (bool): 是否包含推理过程
- `**kwargs`: 其他分析参数

**返回：** 光谱名称到分析结果的字典

**示例：**
```python
# 分析所有光谱
all_spectra = await client.analyze_spectra(
    query="什么是真正的友谊？",
    depth=2
)

# 分析特定光谱
specific_spectra = await client.analyze_spectra(
    query="从逻辑角度分析这个数学问题",
    spectra=["blue"],
    include_reasoning=True
)

# 获取详细分析
detailed = await client.analyze_spectra(
    query="反思我的学习过程",
    spectra=["purple"],
    depth=3,
    include_confidence=True,
    include_reasoning=True
)
```

#### experience_whitespace方法
```python
async def experience_whitespace(
    self,
    insights: List[str] = None,
    duration: int = 60,
    prompts: List[str] = None,
    background: Optional[str] = None,
    include_timer: bool = True,
    **kwargs
) -> WhitespaceExperience
```

**参数说明：**
- `insights` (List[str], optional): 初始洞见列表
- `duration` (int): 留白时长（秒，30-300）
- `prompts` (List[str], optional): 反思提示列表
- `background` (str, optional): 背景信息或上下文
- `include_timer` (bool): 是否包含计时器功能
- `**kwargs`: 其他留白参数

**返回：** `WhitespaceExperience`对象

**示例：**
```python
# 基础留白体验
whitespace = await client.experience_whitespace(
    duration=60
)

# 带初始洞见的留白
whitespace_with_insights = await client.experience_whitespace(
    insights=["初步想法1", "初步想法2"],
    duration=90,
    prompts=["这些想法如何连接？", "你注意到什么模式？"]
)

# 上下文留白
contextual_whitespace = await client.experience_whitespace(
    background="刚才我们讨论了工作与生活的平衡",
    duration=120,
    include_timer=True
)
```

#### synthesize_perspectives方法
```python
async def synthesize_perspectives(
    self,
    spectra_results: List[SpectrumAnalysis],
    whitespace_insights: List[str] = None,
    synthesis_method: str = "integrated",
    include_new_questions: bool = True,
    include_confidence: bool = True,
    **kwargs
) -> SynthesisResult
```

**参数说明：**
- `spectra_results` (List[SpectrumAnalysis]): 光谱分析结果列表
- `whitespace_insights` (List[str], optional): 留白洞见列表
- `synthesis_method` (str): 合成方法（integrated, hierarchical, emergent）
- `include_new_questions` (bool): 是否包含新问题
- `include_confidence` (bool): 是否包含置信度
- `**kwargs`: 其他合成参数

**返回：** `SynthesisResult`对象

**示例：**
```python
# 基础合成
synthesis = await client.synthesize_perspectives(
    spectra_results=[red_result, blue_result, purple_result]
)

# 完整合成
full_synthesis = await client.synthesize_perspectives(
    spectra_results=all_spectra_results,
    whitespace_insights=whitespace.insights,
    synthesis_method="emergent",
    include_new_questions=True,
    include_confidence=True
)

# 特定方法合成
hierarchical_synthesis = await client.synthesize_perspectives(
    spectra_results=spectra_results,
    synthesis_method="hierarchical"
)
```

### 数据模型

#### PrismResponse类
```python
class PrismResponse:
    """棱镜对话响应"""
    
    query: str                      # 原始查询
    spectra: Dict[str, Spectrum]    # 光谱分析结果
    whitespace: Whitespace          # 留白体验结果
    synthesis: Synthesis            # 综合视角结果
    metadata: Dict[str, Any]        # 元数据
    session_id: Optional[str]       # 会话ID
    timestamp: datetime             # 时间戳
    duration: float                 # 处理时长（秒）
    confidence: float               # 总体置信度
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        
    def to_json(self) -> str:
        """转换为JSON字符串"""
        
    def save(self, path: str) -> None:
        """保存到文件"""
        
    @classmethod
    def load(cls, path: str) -> "PrismResponse":
        """从文件加载"""
```

#### Spectrum类
```python
class Spectrum:
    """光谱分析结果"""
    
    name: str                       # 光谱名称（red, blue, purple）
    content: str                    # 分析内容
    confidence: float               # 置信度（0-1）
    reasoning: Optional[str]        # 推理过程
    key_points: List[str]           # 关键点
    assumptions: List[str]          # 假设
    limitations: List[str]          # 限制
    duration: float                 # 分析时长（秒）
    
    def summary(self) -> str:
        """生成摘要"""
        
    def validate(self) -> bool:
        """验证结果有效性"""
```

#### Whitespace类
```python
class Whitespace:
    """留白体验结果"""
    
    duration: int                   # 留白时长（秒）
    insights: List[str]             # 涌现的洞见
    prompts: List[str]              # 反思提示
    background: Optional[str]       # 背景信息
    start_time: datetime            # 开始时间
    end_time: datetime              # 结束时间
    timer_enabled: bool             # 计时器是否启用
    
    def get_elapsed_time(self) -> float:
        """获取已过时间"""
        
    def is_complete(self) -> bool:
        """检查是否完成"""
        
    def add_insight(self, insight: str) -> None:
        """添加洞见"""
```

#### Synthesis类
```python
class Synthesis:
    """综合视角结果"""
    
    integrated_view: str            # 整合的理解
    new_questions: List[str]        # 新涌现的问题
    confidence: float               # 综合置信度
    method: str                     # 合成方法
    spectra_contributions: Dict[str, float]  # 各光谱贡献度
    whitespace_contributions: float # 留白贡献度
    key_connections: List[str]      # 关键连接
    
    def get_main_insights(self) -> List[str]:
        """获取主要洞见"""
        
    def prioritize_questions(self) -> List[str]:
        """对新问题进行优先级排序"""
```

## 🔧 高级API功能

### 会话管理
```python
# 创建会话
session = await client.create_session(
    user_id="user123",
    context="个人反思日记",
    metadata={"goal": "深度自我认知"}
)

# 继续会话
continuation = await client.continue_session(
    session_id=session.id,
    query="基于上次的讨论，我想进一步探索...",
    previous_response=last_response
)

# 获取会话历史
history = await client.get_session_history(
    session_id=session.id,
    limit=50,
    include_responses=True
)

# 结束会话
await client.end_session(session_id=session.id)
```

### 批量处理
```python
# 批量对话
queries = [
    "问题1: 如何保持工作动力？",
    "问题2: 什么是真正的领导力？",
    "问题3: 如何培养创造性思维？"
]

batch_results = await client.batch_prismatic_dialogue(
    queries=queries,
    max_depth=2,
    concurrency=3  # 并发数
)

# 流式处理
async for chunk in client.stream_prismatic_dialogue(
    query="请详细分析人工智能的未来发展",
    chunk_size=100  # 每块token数
):
    print(f"收到块: {chunk}")
    # 实时处理...
```

### 自定义配置
```python
# 创建自定义配置
custom_config = await client.create_configuration(
    name="深度分析配置",
    parameters={
        "max_depth": 5,
        "whitespace_duration": 120,
        "temperature": 0.7,
        "spectra_weights": {
            "red": 0.3,
            "blue": 0.4,
            "purple": 0.3
        }
    },
    description="用于深度哲学问题的分析配置"
)

# 使用自定义配置
response = await client.prismatic_dialogue(
    query="生命的意义是什么？",
    config_id=custom_config.id
)

# 管理配置
configs = await client.list_configurations()
await client.update_configuration(config_id, new_parameters)
await client.delete_configuration(config_id)
```

### 分析和监控
```python
# 获取使用统计
stats = await client.get_usage_statistics(
    start_date="2026-01-01",
    end_date="2026-03-25",
    group_by="day"
)

# 性能监控
metrics = await client.get_performance_metrics(
    endpoint="prismatic_dialogue",
    time_range="last_7_days"
)

# 错误分析
errors = await client.get_error_reports(
    error_type="timeout",
    limit=100
)

# 健康检查
health = await client.health_check()
```

## 🎯 使用示例

### 示例1：完整的个人反思