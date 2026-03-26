# 🔌 棱镜协议插件系统

## 🎯 插件设计哲学

### 🔥 火堆旁的扩展
**核心理念**：插件不是附加功能，而是火堆旁的更多凳子，让更多人能以不同方式参与对话。

### 🧠 认知的模块化
**设计原则**：
- **最小耦合**：插件与核心系统松耦合
- **最大兼容**：向后兼容和向前兼容
- **自然集成**：插件体验像原生功能
- **安全边界**：明确的权限和安全隔离

### 🌈 光谱的扩展
**扩展维度**：
- 🔥 **红色光谱扩展**：新的直觉视角和分析方法
- 🔵 **蓝色光谱扩展**：新的分析工具和数据处理
- 🟣 **紫色光谱扩展**：新的元认知和反思工具
- 🌈 **综合扩展**：新的合成方法和整合策略

## 🏗️ 插件架构

### 核心架构
```python
# 插件系统架构概览
class PluginSystem:
    """棱镜协议插件系统"""
    
    def __init__(self):
        self.plugins = {}           # 已加载插件
        self.hooks = {}             # 钩子系统
        self.extensions = {}        # 扩展系统
        self.middleware = []        # 中间件链
        
    async def load_plugin(self, plugin_path: str):
        """加载插件"""
        
    async def unload_plugin(self, plugin_id: str):
        """卸载插件"""
        
    async def call_hook(self, hook_name: str, *args, **kwargs):
        """调用钩子"""
        
    async def register_extension(self, extension_type: str, extension):
        """注册扩展"""
```

### 插件生命周期
```python
# 插件生命周期状态机
PLUGIN_LIFECYCLE = {
    "DISCOVERED": "发现",      # 发现插件文件
    "LOADED": "已加载",        # 加载插件代码
    "INITIALIZED": "已初始化", # 插件初始化完成
    "ACTIVE": "活跃",          # 插件正在运行
    "ERROR": "错误",           # 插件出错
    "UNLOADED": "已卸载",      # 插件已卸载
}
```

## 📦 插件类型

### 1. 光谱插件
**功能**：扩展或修改光谱分析行为

#### 红色光谱插件示例
```python
from prism_sdk.plugins import SpectrumPlugin

class IntuitionEnhancerPlugin(SpectrumPlugin):
    """直觉增强插件"""
    
    plugin_id = "intuition_enhancer"
    plugin_name = "直觉增强器"
    plugin_version = "1.0.0"
    spectrum_type = "red"  # 红色光谱插件
    
    async def analyze(self, query: str, context: dict) -> dict:
        """增强直觉分析"""
        # 基础直觉分析
        base_analysis = await self.call_base_spectrum(query, context)
        
        # 增强处理
        enhanced = {
            **base_analysis,
            "enhanced_insights": await self.generate_enhanced_insights(base_analysis),
            "pattern_recognition": await self.recognize_patterns(base_analysis),
            "emotional_resonance": await self.analyze_emotional_resonance(base_analysis),
        }
        
        return enhanced
    
    async def generate_enhanced_insights(self, analysis: dict) -> List[str]:
        """生成增强洞见"""
        # 插件特定的增强逻辑
        pass
```

#### 蓝色光谱插件示例
```python
class LogicalAnalyzerPlugin(SpectrumPlugin):
    """逻辑分析增强插件"""
    
    plugin_id = "logical_analyzer"
    plugin_name = "逻辑分析器"
    plugin_version = "1.0.0"
    spectrum_type = "blue"  # 蓝色光谱插件
    
    async def analyze(self, query: str, context: dict) -> dict:
        """增强逻辑分析"""
        # 调用外部逻辑分析服务
        external_analysis = await self.call_external_service(query)
        
        # 整合分析
        integrated = {
            "logical_structure": external_analysis.get("structure"),
            "argument_quality": self.evaluate_argument_quality(external_analysis),
            "evidence_strength": self.assess_evidence_strength(external_analysis),
            "fallacy_detection": self.detect_fallacies(external_analysis),
        }
        
        return integrated
```

### 2. 留白插件
**功能**：扩展或修改留白体验

```python
from prism_sdk.plugins import WhitespacePlugin

class MeditationGuidePlugin(WhitespacePlugin):
    """冥想引导插件"""
    
    plugin_id = "meditation_guide"
    plugin_name = "冥想引导"
    plugin_version = "1.0.0"
    
    async def enhance_whitespace(self, duration: int, context: dict) -> dict:
        """增强留白体验"""
        return {
            "guided_meditation": await self.provide_meditation_guidance(duration),
            "breathing_exercises": self.generate_breathing_exercises(duration),
            "mindfulness_prompts": self.generate_mindfulness_prompts(duration),
            "ambient_sounds": self.provide_ambient_sounds(duration),
        }
    
    async def provide_meditation_guidance(self, duration: int) -> List[str]:
        """提供冥想指导"""
        # 根据时长生成冥想指导
        pass
```

### 3. 合成插件
**功能**：扩展或修改合成方法

```python
from prism_sdk.plugins import SynthesisPlugin

class CrossDomainSynthesisPlugin(SynthesisPlugin):
    """跨领域合成插件"""
    
    plugin_id = "cross_domain_synthesis"
    plugin_name = "跨领域合成"
    plugin_version = "1.0.0"
    
    async def synthesize(self, spectra_results: List[dict], 
                        whitespace_insights: List[str]) -> dict:
        """跨领域合成"""
        # 识别不同领域的视角
        domains = self.identify_domains(spectra_results)
        
        # 跨领域整合
        cross_domain_synthesis = {
            "domain_insights": await self.integrate_domain_insights(domains),
            "cross_domain_connections": self.find_cross_domain_connections(domains),
            "emergent_patterns": self.identify_emergent_patterns(domains),
            "integrative_framework": self.create_integrative_framework(domains),
        }
        
        return cross_domain_synthesis
```

### 4. 数据源插件
**功能**：集成外部数据源

```python
from prism_sdk.plugins import DataSourcePlugin

class ResearchPaperPlugin(DataSourcePlugin):
    """学术论文数据源插件"""
    
    plugin_id = "research_paper_source"
    plugin_name = "学术论文数据源"
    plugin_version = "1.0.0"
    data_source_type = "academic"
    
    async def query(self, topic: str, filters: dict = None) -> List[dict]:
        """查询学术论文"""
        # 调用学术数据库API
        papers = await self.search_academic_databases(topic, filters)
        
        return {
            "papers": papers,
            "summary": self.summarize_papers(papers),
            "key_concepts": self.extract_key_concepts(papers),
            "citation_network": self.build_citation_network(papers),
        }
```

### 5. 输出格式插件
**功能**：扩展输出格式

```python
from prism_sdk.plugins import OutputPlugin

class MindMapOutputPlugin(OutputPlugin):
    """思维导图输出插件"""
    
    plugin_id = "mindmap_output"
    plugin_name = "思维导图输出"
    plugin_version = "1.0.0"
    output_format = "mindmap"
    
    async def convert(self, prism_response: PrismResponse) -> dict:
        """转换为思维导图格式"""
        mindmap = {
            "central_topic": prism_response.query,
            "main_branches": {
                "red_spectrum": self.convert_spectrum_to_branch(prism_response.spectra["red"]),
                "blue_spectrum": self.convert_spectrum_to_branch(prism_response.spectra["blue"]),
                "purple_spectrum": self.convert_spectrum_to_branch(prism_response.spectra["purple"]),
            },
            "connections": self.find_connections(prism_response),
            "visual_style": self.generate_visual_style(),
        }
        
        return mindmap
```

### 6. 集成插件
**功能**：与其他系统集成

```python
from prism_sdk.plugins import IntegrationPlugin

class NotionIntegrationPlugin(IntegrationPlugin):
    """Notion集成插件"""
    
    plugin_id = "notion_integration"
    plugin_name = "Notion集成"
    plugin_version = "1.0.0"
    integration_target = "notion"
    
    async def sync_to_notion(self, prism_response: PrismResponse, 
                           notion_page_id: str) -> dict:
        """同步到Notion"""
        # 创建Notion页面
        notion_page = await self.create_notion_page(
            title=prism_response.query,
            content=self.format_for_notion(prism_response)
        )
        
        return {
            "notion_page_url": notion_page.get("url"),
            "sync_status": "success",
            "synced_at": datetime.now().isoformat(),
        }
```

## 🔌 插件开发指南

### 开发环境设置
```bash
# 1. 安装插件开发工具
pip install prism-sdk[plugin-dev]

# 2. 创建插件项目
prism-plugin create my-plugin

# 3. 进入插件目录
cd my-plugin

# 4. 安装开发依赖
pip install -e .[dev]

# 5. 运行开发服务器
prism-plugin dev
```

### 插件模板
```python
# my_plugin/__init__.py
"""我的棱镜插件"""

from prism_sdk.plugins import BasePlugin

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

class MyPlugin(BasePlugin):
    """我的插件"""
    
    plugin_id = "my_plugin"
    plugin_name = "我的插件"
    plugin_version = __version__
    plugin_description = "我的棱镜协议插件"
    plugin_author = __author__
    
    # 插件配置
    config_schema = {
        "type": "object",
        "properties": {
            "enabled": {"type": "boolean", "default": True},
            "api_key": {"type": "string", "default": ""},
            "timeout": {"type": "integer", "default": 30},
        },
        "required": ["enabled"]
    }
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.initialized = False
    
    async def initialize(self):
        """初始化插件"""
        if not self.config.get("enabled", True):
            self.logger.info("插件已禁用")
            return
        
        # 初始化逻辑
        self.api_client = await self.create_api_client()
        self.initialized = True
        self.logger.info("插件初始化完成")
    
    async def on_prismatic_dialogue(self, query: str, context: dict) -> dict:
        """棱镜对话钩子"""
        if not self.initialized:
            return {}
        
        # 处理逻辑
        enhanced_query = await self.enhance_query(query)
        return {"enhanced_query": enhanced_query}
    
    async def cleanup(self):
        """清理资源"""
        if hasattr(self, 'api_client'):
            await self.api_client.close()
        self.initialized = False
```

### 插件配置
```yaml
# config/plugin_config.yaml
my_plugin:
  enabled: true
  api_key: "your-api-key-here"
  timeout: 30
  log_level: "INFO"
  
another_plugin:
  enabled: false
  reason: "暂时禁用"
```

### 插件测试
```python
# tests/test_my_plugin.py
import pytest
from prism_sdk import PrismClient
from my_plugin import MyPlugin

@pytest.mark.asyncio
async def test_plugin_initialization():
    """测试插件初始化"""
    plugin = MyPlugin(config={"enabled": True})
    await plugin.initialize()
    assert plugin.initialized == True

@pytest.mark.asyncio
async def test_plugin_hook():
    """测试插件钩子"""
    plugin = MyPlugin(config={"enabled": True})
    await plugin.initialize()
    
    result = await plugin.on_prismatic_dialogue(
        query="测试问题",
        context={"user_id": "test_user"}
    )
    
    assert "enhanced_query" in result
```

## 🚀 插件部署

### 本地部署
```bash
# 1. 构建插件
python setup.py sdist bdist_wheel

# 2. 安装插件
pip install dist/my_plugin-1.0.0-py3-none-any.whl

# 3. 配置插件
echo 'my_plugin:
  enabled: true
  api_key: "your-key"' > ~/.prism/plugins.yaml

# 4. 重启棱镜服务
prism-server restart
```

### Docker部署
```dockerfile
# Dockerfile.plugin
FROM python:3.11-slim

# 安装插件
COPY dist/my_plugin-1.0.0-py3-none-any.whl /tmp/
RUN pip install /tmp/my_plugin-1.0.0-py3-none-any.whl

# 插件配置
COPY config/plugin_config.yaml /etc/prism/plugins.yaml

# 运行棱镜服务
CMD ["prism-server", "--plugins-config", "/etc/prism/plugins.yaml"]
```

### Kubernetes部署
```yaml
# k8s/plugin-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism-with-plugins
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: prism
        image: prism-with-plugins:latest
        volumeMounts:
        - name: plugin-config
          mountPath: /etc/prism/plugins.yaml
          subPath: plugins.yaml
        - name: plugin-secrets
          mountPath: /etc/prism/secrets
      volumes:
      - name: plugin-config
        configMap:
          name: plugin-config
      - name: plugin-secrets
        secret:
          secretName: plugin-secrets
```

## 📊 插件管理

### 插件发现
```python
# 发现可用插件
from prism_sdk.plugin_manager import PluginManager

manager = PluginManager()

# 从目录发现插件
plugins = await manager.discover_plugins(
    directories=["~/.prism/plugins", "/usr/local/share/prism/plugins"]
)

# 从PyPI发现插件
pypi_plugins = await manager.discover_from_pypi(
    search_query="prism-plugin"
)
```

### 插件加载
```python
# 加载和管理插件
async def manage_plugins():
    manager = PluginManager()
    
    # 加载插件
    await manager.load_plugin("my_plugin")
    
    # 启用/禁用插件
    await manager.enable_plugin("my_plugin")
    await manager.disable_plugin("another_plugin")
    
    # 获取插件状态
    status = await manager.get_plugin_status("my_plugin")
    print(f"插件状态: {status}")
    
    # 列出所有插件
    plugins = await manager.list_plugins()
    for plugin_id, plugin_info in plugins.items():
        print(f"{plugin_id}: {plugin_info['name']} v{plugin_info['version']}")
```

### 插件配置管理
```python
# 管理插件配置
async def manage_plugin_config():
    manager = PluginManager()
    
    # 获取插件配置
    config = await manager.get_plugin_config("my_plugin")
    
    # 更新插件配置
    new_config = {**config, "timeout": 60}
    await manager.update_plugin_config("my_plugin", new_config)
    
    # 验证配置
    is_valid = await manager.validate_plugin_config("my_plugin", new_config)
    
    # 保存配置
    await manager.save_plugin_configs()
```

### 插件监控
```python
# 监控插件性能
async def monitor_plugins():
    manager = PluginManager()
    
    # 获取插件指标
    metrics = await manager.get_plugin_metrics()
    
    for plugin_id, plugin_metrics in metrics.items():
        print(f"\n插件: {plugin_id}")
        print(f"  调用次数: {plugin_metrics.get('call_count', 0)}")
        print(f"  平均耗时: {plugin_metrics.get('avg_duration', 0):.2f}ms")
        print(f"  错误率: {plugin_metrics.get('error_rate', 0):.2%}")
        print(f"  内存使用: {plugin_metrics.get('memory_usage', 0)}MB")
    
    # 获取插件健康状态
    health = await manager.get_plugin_health()
    for plugin_id, plugin_health in health.items():
        status = "✅ 健康" if plugin_health["healthy"] else "❌ 不健康"
        print(f"{plugin_id}: {status}")
```

## 🔒 插件安全

### 安全沙箱
```python
# 插件安全沙箱
from prism