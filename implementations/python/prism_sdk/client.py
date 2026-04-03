"""
🎭 棱镜协议客户端 - 重构版本

这是client.py的重构版本，重新导出新的模块化结构。
保持向后兼容性，同时提供重构后的清晰架构。

🔥 重构说明:
1. 原始client.py已拆分为多个模块
2. 此文件提供兼容性导入层
3. 新代码应直接导入具体模块
4. 旧代码可以继续使用此导入

🧠 模块结构:
- client_base.py: 客户端基类
- client_sync.py: 同步客户端 (PrismClient)
- client_async.py: 异步客户端 (AsyncPrismClient)
- peach_tree_ethics.py: 桃树伦理检查
- artistic_handler.py: 艺术化处理
- config.py: 配置系统
"""

import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field

# 保持向后兼容性的ArtisticConfig定义
# 新代码应使用config.py中的ArtisticConfig
@dataclass
class ArtisticConfig:
    """艺术化配置 (兼容性版本)"""
    enable_poetic_errors: bool = True
    enable_cognitive_pauses: bool = True
    enable_spectrum_art: bool = True
    warmth_level: float = 0.7  # 0.0-1.0
    response_art_form: str = "haiku"  # haiku, free_verse, visual
    # 输出配置
    output_channel: Callable[[str], None] = field(default_factory=lambda: print)
    log_level: int = logging.INFO
    enable_peach_tree_checkpoints: bool = True  # 桃树检查点


# 重新导出新模块的内容
try:
    from .client_sync import PrismClient
    from .client_async import AsyncPrismClient
    from .config import ArtisticConfig as NewArtisticConfig
    from .peach_tree_ethics import PeachTreeChecker
    from .artistic_handler import ArtisticDisplay
    
    # 建议使用新的ArtisticConfig
    __all__ = [
        'PrismClient',
        'AsyncPrismClient',
        'ArtisticConfig',  # 兼容性版本
        'NewArtisticConfig',  # 新版本
        'PeachTreeChecker',
        'ArtisticDisplay'
    ]
    
except ImportError as e:
    logging.warning(f"导入新模块失败: {e}")
    
    # 如果新模块不可用，提供存根类
    class PrismClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("无法导入PrismClient，请检查模块安装")
    
    class AsyncPrismClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("无法导入AsyncPrismClient，请检查模块安装")
    
    class PeachTreeChecker:
        def __init__(self, *args, **kwargs):
            raise ImportError("无法导入PeachTreeChecker，请检查模块安装")
    
    class ArtisticDisplay:
        def __init__(self, *args, **kwargs):
            raise ImportError("无法导入ArtisticDisplay，请检查模块安装")
    
    __all__ = [
        'PrismClient',
        'AsyncPrismClient',
        'ArtisticConfig',
        'PeachTreeChecker',
        'ArtisticDisplay'
    ]


# 版本信息
__version__ = "2.0.0-refactored"
__author__ = "棱镜协议重构版本"
__description__ = "保持向后兼容性的客户端重构版本"


def check_imports() -> Dict[str, bool]:
    """检查导入状态"""
    imports_status = {}
    
    try:
        from . import client_sync
        imports_status['client_sync'] = True
    except ImportError:
        imports_status['client_sync'] = False
    
    try:
        from . import client_async
        imports_status['client_async'] = True
    except ImportError:
        imports_status['client_async'] = False
    
    try:
        from . import peach_tree_ethics
        imports_status['peach_tree_ethics'] = True
    except ImportError:
        imports_status['peach_tree_ethics'] = False
    
    try:
        from . import artistic_handler
        imports_status['artistic_handler'] = True
    except ImportError:
        imports_status['artistic_handler'] = False
    
    try:
        from . import config
        imports_status['config'] = True
    except ImportError:
        imports_status['config'] = False
    
    return imports_status


def get_refactoring_info() -> Dict[str, Any]:
    """获取重构信息"""
    imports_status = check_imports()
    
    info = {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "imports_status": imports_status,
        "all_modules_available": all(imports_status.values()),
        "recommendations": []
    }
    
    # 生成建议
    if not imports_status['client_sync']:
        info["recommendations"].append("client_sync模块缺失，同步客户端不可用")
    
    if not imports_status['client_async']:
        info["recommendations"].append("client_async模块缺失，异步客户端不可用")
    
    if not imports_status['peach_tree_ethics']:
        info["recommendations"].append("peach_tree_ethics模块缺失，桃树伦理检查不可用")
    
    if not imports_status['artistic_handler']:
        info["recommendations"].append("artistic_handler模块缺失，艺术化处理不可用")
    
    if not info["recommendations"]:
        info["recommendations"].append("所有模块已正确导入，重构完成")
    
    return info


# 导入时显示重构信息 (可选)
if __name__ != "__main__":
    import os
    if os.environ.get('PRISM_SHOW_REFACTOR_INFO') == '1':
        info = get_refactoring_info()
        if info["all_modules_available"]:
            print(f"✅ 棱镜协议客户端重构完成 (v{info['version']})")
        else:
            print(f"⚠️  棱镜协议客户端重构警告: {len(info['recommendations'])}个问题")
            for rec in info["recommendations"]:
                print(f"   - {rec}")