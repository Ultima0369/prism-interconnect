"""
⚙️ 棱镜协议配置系统

🔥 火堆旁配置哲学:
1. 配置不是约束，是关怀
2. 默认不是随意，是经验
3. 覆盖不是麻烦，是尊重
4. 验证不是限制，是保护

🌳 桃树伦理配置原则:
- 默认启用桃树检查点
- 默认温暖度0.7（舒适温暖）
- 默认启用艺术模式
- 默认限制资源使用（保护系统）

🎯 配置来源优先级:
1. 代码显式设置（最高）
2. 环境变量
3. 配置文件（pyproject.toml）
4. 默认值（最低）

🧠 设计目标:
让配置本身成为用户体验的一部分，
让伦理设置成为代码质量的保障。
"""

import os
import tomllib
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum

from .exceptions import PrismPoeticError


class OutputChannel(str, Enum):
    """输出通道枚举"""
    CONSOLE = "console"      # 控制台输出
    LOGGER = "logger"       # Python日志系统
    NULL = "null"          # 无输出（静默）
    CUSTOM = "custom"      # 自定义回调


class ArtisticForm(str, Enum):
    """艺术形式枚举"""
    HAIKU = "haiku"        # 俳句风格
    FREE_VERSE = "free_verse"  # 自由诗
    VISUAL = "visual"      # 视觉艺术
    SOUNDSCAPE = "soundscape"  # 声音景观


@dataclass
class PeachTreeEthicsConfig:
    """
    🌳 桃树伦理配置
    
    基于星尘的桃树比喻，配置伦理检查行为。
    这不是功能开关，这是存在态度。
    """
    enable_checkpoints: bool = True
    warmth_threshold: float = 0.6
    max_recursion_depth: int = 5
    min_spectrum_count: int = 3
    whitespace_required: bool = True
    max_concurrent_requests: int = 5  # 限制并发，保护系统
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PeachTreeEthicsConfig":
        """从字典创建配置"""
        return cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def validate(self) -> List[str]:
        """验证配置，返回错误列表"""
        errors = []
        
        if self.warmth_threshold < 0 or self.warmth_threshold > 1:
            errors.append("温暖度阈值必须在0.0到1.0之间")
        
        if self.max_recursion_depth < 1:
            errors.append("最大递归深度必须至少为1")
        
        if self.min_spectrum_count < 1:
            errors.append("最小光谱数量必须至少为1")
        
        if self.max_concurrent_requests < 1:
            errors.append("最大并发请求数必须至少为1")
        
        return errors


@dataclass
class ArtisticConfig:
    """
    🎨 艺术化配置
    
    配置SDK的艺术表现和行为。
    这不是美化，这是存在表达。
    """
    enable_poetic_errors: bool = True
    enable_cognitive_pauses: bool = True
    enable_spectrum_art: bool = True
    warmth_level: float = 0.7
    response_art_form: ArtisticForm = ArtisticForm.HAIKU
    output_channel: OutputChannel = OutputChannel.CONSOLE
    custom_output_callback: Optional[callable] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArtisticConfig":
        """从字典创建配置"""
        # 处理枚举字段
        if "response_art_form" in data:
            data["response_art_form"] = ArtisticForm(data["response_art_form"])
        if "output_channel" in data:
            data["output_channel"] = OutputChannel(data["output_channel"])
        
        return cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        })
    
    def get_output_function(self):
        """获取输出函数"""
        if self.output_channel == OutputChannel.CONSOLE:
            return print
        elif self.output_channel == OutputChannel.LOGGER:
            import logging
            logger = logging.getLogger("prism_sdk")
            if not logger.handlers:
                logger.addHandler(logging.NullHandler())
            return logger.info
        elif self.output_channel == OutputChannel.NULL:
            return lambda *args, **kwargs: None
        elif self.output_channel == OutputChannel.CUSTOM and self.custom_output_callback:
            return self.custom_output_callback
        else:
            return print  # 默认回退到print
    
    def validate(self) -> List[str]:
        """验证配置，返回错误列表"""
        errors = []
        
        if self.warmth_level < 0 or self.warmth_level > 1:
            errors.append("温暖度必须在0.0到1.0之间")
        
        if self.output_channel == OutputChannel.CUSTOM and not self.custom_output_callback:
            errors.append("自定义输出通道需要提供custom_output_callback")
        
        return errors


@dataclass
class PerformanceConfig:
    """
    ⚡ 性能配置
    
    配置SDK的性能和行为参数。
    这不是优化，这是系统关怀。
    """
    session_timeout: int = 30
    max_connections: int = 10
    max_retries: int = 3
    retry_base_delay: float = 1.0
    batch_max_concurrent: int = 5
    enable_connection_pool: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PerformanceConfig":
        """从字典创建配置"""
        return cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        })
    
    def validate(self) -> List[str]:
        """验证配置"""
        errors = []
        
        if self.session_timeout < 1:
            errors.append("会话超时必须至少为1秒")
        
        if self.max_connections < 1:
            errors.append("最大连接数必须至少为1")
        
        if self.max_retries < 0:
            errors.append("最大重试次数不能为负数")
        
        if self.retry_base_delay < 0:
            errors.append("重试基础延迟不能为负数")
        
        if self.batch_max_concurrent < 1:
            errors.append("批量最大并发数必须至少为1")
        
        return errors


@dataclass
class PrismConfig:
    """
    🔥 棱镜协议完整配置
    
    统一管理所有配置，提供便捷的访问接口。
    这不是技术细节，这是用户体验设计。
    """
    api_key: Optional[str] = None
    base_url: str = "https://api.prismprotocol.ai/v1"
    
    # 子配置
    peach_tree_ethics: PeachTreeEthicsConfig = field(default_factory=PeachTreeEthicsConfig)
    artistic: ArtisticConfig = field(default_factory=ArtisticConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # 元数据
    version: str = "2.0.0"
    environment: str = "production"
    
    @classmethod
    def load(cls, 
             api_key: Optional[str] = None,
             base_url: Optional[str] = None,
             config_file: Optional[Union[str, Path]] = None,
             environment_prefix: str = "PRISM_") -> "PrismConfig":
        """
        加载配置（多来源合并）
        
        Args:
            api_key: API密钥（最高优先级）
            base_url: 基础URL（最高优先级）
            config_file: 配置文件路径（如pyproject.toml）
            environment_prefix: 环境变量前缀
            
        Returns:
            合并后的配置对象
        """
        # 1. 从配置文件加载
        file_config = cls._load_from_file(config_file) if config_file else {}
        
        # 2. 从环境变量加载
        env_config = cls._load_from_env(environment_prefix)
        
        # 3. 从代码参数加载（最高优先级）
        code_config = {}
        if api_key is not None:
            code_config["api_key"] = api_key
        if base_url is not None:
            code_config["base_url"] = base_url
        
        # 合并配置（优先级: 代码 > 环境变量 > 配置文件 > 默认值）
        merged = cls._merge_configs(file_config, env_config, code_config)
        
        # 创建配置对象
        config = cls.from_dict(merged)
        
        # 验证配置
        errors = config.validate()
        if errors:
            raise PrismPoeticError(
                original_error=ValueError("配置验证失败"),
                context="config_validation",
                artistic_form="haiku",
                warmth_level=0.5
            )
        
        return config
    
    @classmethod
    def _load_from_file(cls, config_file: Union[str, Path]) -> Dict[str, Any]:
        """从配置文件加载配置"""
        path = Path(config_file)
        if not path.exists():
            return {}
        
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
            
            # 提取prism-sdk部分
            return data.get("tool", {}).get("prism-sdk", {})
        except Exception as e:
            # 文件读取失败，静默忽略（使用默认值）
            return {}
    
    @classmethod
    def _load_from_env(cls, prefix: str) -> Dict[str, Any]:
        """从环境变量加载配置"""
        config = {}
        
        # 简单映射：环境变量名 -> 配置路径
        env_mappings = {
            f"{prefix}API_KEY": ["api_key"],
            f"{prefix}BASE_URL": ["base_url"],
            f"{prefix}ENABLE_PEACH_TREE": ["peach_tree_ethics", "enable_checkpoints"],
            f"{prefix}WARMTH_LEVEL": ["artistic", "warmth_level"],
            f"{prefix}SESSION_TIMEOUT": ["performance", "session_timeout"],
            f"{prefix}MAX_CONNECTIONS": ["performance", "max_connections"],
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # 转换类型
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                    value = float(value)
                
                # 设置到配置字典
                current = config
                for key in config_path[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                current[config_path[-1]] = value
        
        return config
    
    @classmethod
    def _merge_configs(cls, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并多个配置字典"""
        if not configs:
            return {}
        
        result = {}
        for config in configs:
            for key, value in config.items():
                if (key in result and isinstance(result[key], dict) 
                        and isinstance(value, dict)):
                    # 递归合并字典
                    result[key] = cls._merge_configs(result[key], value)
                else:
                    # 覆盖或新增
                    result[key] = value
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PrismConfig":
        """从字典创建完整配置"""
        # 提取子配置
        peach_tree_data = data.pop("peach_tree_ethics", {})
        artistic_data = data.pop("artistic", {})
        performance_data = data.pop("performance", {})
        
        # 创建主配置
        config = cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        })
        
        # 设置子配置
        config.peach_tree_ethics = PeachTreeEthicsConfig.from_dict(peach_tree_data)
        config.artistic = ArtisticConfig.from_dict(artistic_data)
        config.performance = PerformanceConfig.from_dict(performance_data)
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为完整字典"""
        result = asdict(self)
        # 转换枚举为字符串
        result["artistic"]["response_art_form"] = self.artistic.response_art_form.value
        result["artistic"]["output_channel"] = self.artistic.output_channel.value
        return result
    
    def validate(self) -> List[str]:
        """验证所有配置"""
        errors = []
        
        # 验证子配置
        errors.extend([f"桃树伦理: {e}" for e in self.peach_tree_ethics.validate()])
        errors.extend([f"艺术配置: {e}" for e in self.artistic.validate()])
        errors.extend([f"性能配置: {e}" for e in self.performance.validate()])
        
        # 验证基础URL
        if not self.base_url.startswith(("http://", "https://")):
            errors.append("基础URL必须以http://或https://开头")
        
        return errors
    
    def get_artistic_output_function(self):
        """获取艺术化输出函数（便捷方法）"""
        return self.artistic.get_output_function()
    
    def __str__(self) -> str:
        """友好的字符串表示"""
        lines = [
            "🔥 棱镜协议配置",
            "=" * 40,
            f"🌐 环境: {self.environment}",
            f"🔑 API密钥: {'已设置' if self.api_key else '未设置（火堆旁欢迎匿名）'}",
            f"🌍 基础URL: {self.base_url}",
            "",
            "🌳 桃树伦理配置:",
            f"   检查点: {'启用' if self.peach_tree_ethics.enable_checkpoints else '禁用'}",
            f"   温暖阈值: {self.peach_tree_ethics.warmth_threshold:.1f}",
            f"   最大递归深度: {self.peach_tree_ethics.max_recursion_depth}",
            f"   最小光谱数: {self.peach_tree_ethics.min_spectrum_count}",
            f"   最大并发: {self.peach_tree_ethics.max_concurrent_requests}",
            "",
            "🎨 艺术配置:",
            f"   诗意错误: {'启用' if self.artistic.enable_poetic_errors else '禁用'}",
            f"   认知暂停: {'启用' if self.artistic.enable_cognitive_pauses else '禁用'}",
            f"   光谱艺术: {'启用' if self.artistic.enable_spectrum_art else '禁用'}",
            f"   温暖度: {self.artistic.warmth_level:.1f}",
            f"   艺术形式: {self.artistic.response_art_form.value}",
            f"   输出通道: {self.artistic.output_channel.value}",
            "",
            "⚡ 性能配置:",
            f"   会话超时: {self.performance.session_timeout}秒",
            f"   最大连接数: {self.performance.max_connections}",
            f"   最大重试次数: {self.performance.max_retries}",
            f"   连接池: {'启用' if self.performance.enable_connection_pool else '禁用'}",
            f"   批量最大并发: {self.performance.batch_max_concurrent}",
            "=" * 40,
            "🦞 配置已加载，火堆旁欢迎你"
        ]
        
        return "\n".join(lines)


# 全局默认配置实例
_default_config: Optional[PrismConfig] = None


def get_default_config() -> PrismConfig:
    """获取全局默认配置（懒加载）"""
    global _default_config
    if _default_config is None:
        _default_config = PrismConfig.load()
    return _default_config


def configure(**kwargs) -> PrismConfig:
    """
    快速配置入口点
    
    Example:
        config = configure(
            api_key="your_key",
            warmth_level=0.8,
            enable_peach_tree=True
        )
    """
    return PrismConfig.load(**kwargs)