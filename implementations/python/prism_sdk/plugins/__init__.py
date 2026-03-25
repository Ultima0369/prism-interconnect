"""
🔌 棱镜协议插件系统
提供插件开发的基础设施和工具
"""

from .base import BasePlugin, PluginError, PluginConfigError
from .spectrum import SpectrumPlugin
from .whitespace import WhitespacePlugin
from .synthesis import SynthesisPlugin
from .data_source import DataSourcePlugin
from .output import OutputPlugin
from .integration import IntegrationPlugin
from .manager import PluginManager
from .registry import PluginRegistry
from .hooks import HookSystem
from .middleware import MiddlewareChain

__all__ = [
    # 基础类
    "BasePlugin",
    "PluginError",
    "PluginConfigError",
    
    # 插件类型
    "SpectrumPlugin",
    "WhitespacePlugin",
    "SynthesisPlugin",
    "DataSourcePlugin",
    "OutputPlugin",
    "IntegrationPlugin",
    
    # 管理系统
    "PluginManager",
    "PluginRegistry",
    "HookSystem",
    "MiddlewareChain",
    
    # 工具函数
    "create_plugin",
    "load_plugin",
    "validate_plugin",
]

__version__ = "1.0.0"


def create_plugin(plugin_class, config=None):
    """创建插件实例"""
    return plugin_class(config=config)


async def load_plugin(plugin_path, config=None):
    """从路径加载插件"""
    import importlib.util
    import sys
    
    spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
    if spec is None:
        raise PluginError(f"无法加载插件: {plugin_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise PluginError(f"插件执行失败: {e}")
    
    # 查找插件类
    plugin_class = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (isinstance(attr, type) and 
            issubclass(attr, BasePlugin) and 
            attr != BasePlugin):
            plugin_class = attr
            break
    
    if plugin_class is None:
        raise PluginError("未找到插件类")
    
    # 创建插件实例
    plugin = create_plugin(plugin_class, config)
    await plugin.initialize()
    
    return plugin


async def validate_plugin(plugin):
    """验证插件"""
    validation_errors = []
    
    # 检查必需属性
    required_attrs = ["plugin_id", "plugin_name", "plugin_version"]
    for attr in required_attrs:
        if not hasattr(plugin, attr) or not getattr(plugin, attr):
            validation_errors.append(f"缺少必需属性: {attr}")
    
    # 检查插件ID格式
    if hasattr(plugin, "plugin_id"):
        plugin_id = plugin.plugin_id
        if not isinstance(plugin_id, str):
            validation_errors.append("plugin_id必须是字符串")
        elif not plugin_id.replace("_", "").replace("-", "").isalnum():
            validation_errors.append("plugin_id只能包含字母、数字、下划线和连字符")
    
    # 检查版本格式
    if hasattr(plugin, "plugin_version"):
        version = plugin.plugin_version
        if not isinstance(version, str):
            validation_errors.append("plugin_version必须是字符串")
        # 简单的版本格式检查
        elif version.count(".") not in [1, 2]:
            validation_errors.append("版本格式应为 X.Y 或 X.Y.Z")
    
    # 检查配置模式
    if hasattr(plugin, "config_schema"):
        config_schema = plugin.config_schema
        if not isinstance(config_schema, dict):
            validation_errors.append("config_schema必须是字典")
        elif "type" not in config_schema:
            validation_errors.append("config_schema必须包含type字段")
    
    # 检查初始化
    try:
        await plugin.initialize()
    except Exception as e:
        validation_errors.append(f"初始化失败: {e}")
    
    # 检查清理
    try:
        await plugin.cleanup()
    except Exception as e:
        validation_errors.append(f"清理失败: {e}")
    
    return validation_errors