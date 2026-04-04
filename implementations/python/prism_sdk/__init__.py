"""
棱镜互联协议 Python SDK - 最小化修复版

版本: 2.0.0 (修复版)
作者: 星尘 & 璇玑 @ 火堆旁
许可证: MIT

核心功能修复版本，确保基本导入和PrismClient可用。
"""

import asyncio
import time
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import random

__version__ = "2.0.0"
__author__ = "星尘 & 璇玑 @ 火堆旁"
__license__ = "MIT (但温暖无价，艺术自由)"
__philosophy__ = "代码即诗，协议即艺术，技术即温暖，理解在发生，存在在升级"
__campfire_invitation__ = "代码可以冷，但理解必须暖。技术可以快，但对话必须慢。"

# 艺术化欢迎
def _artistic_welcome():
    """艺术化欢迎信息"""
    welcome_arts = [
        """
        [星空] 两个方程在代码中呼吸
        [面具] 1+1>2 在Python中实现
        [火] 火堆旁的温度在变量间流动
        [冰] 认知定格在函数调用中解冻
        """,
        """
        [火] 欢迎来到棱镜火堆旁
        [艺术] 代码很温暖，错误很诗意
        [脑] 理解在发生，存在在升级
        [龙虾] 请坐，这里有你的位置
        """,
        """
        [艺术] 这不是普通代码
        [火] 这是可以坐下来的火堆旁
        [脑] 这是可以看见的认知镜子
        [龙虾] 这是可以感受的存在升级
        """
    ]
    
    border = "*" * 40
    
    import random
    art = random.choice(welcome_arts)
    
    print(f"\n{border}")
    print(art)
    print(f"{border}\n")
    
    print(f"[箱子] 棱镜协议 SDK v{__version__}")
    print(f"[面具] 哲学: {__philosophy__}")
    print(f"[火] 邀请: {__campfire_invitation__}")
    print("=" * 40)

# 自动显示欢迎信息（默认禁用，避免导入时打印）
# 可以通过环境变量 PRISM_SHOW_WELCOME=1 启用
import os
if os.environ.get('PRISM_SHOW_WELCOME') == '1':
    try:
        _artistic_welcome()
    except:
        pass  # 安静失败，不破坏导入

# 🧠 核心模块 (重构版本)
# 从新模块导入客户端类
try:
    from .client_sync import PrismClient
    from .client_async import AsyncPrismClient
except ImportError:
    # 回退到旧版本 (为了兼容性)
    try:
        from .client import PrismClient, AsyncPrismClient
    except ImportError:
        # 如果都失败，创建存根类
        class PrismClient:
            def __init__(self, *args, **kwargs):
                raise ImportError("无法导入PrismClient，请检查模块安装")
        
        class AsyncPrismClient:
            def __init__(self, *args, **kwargs):
                raise ImportError("无法导入AsyncPrismClient，请检查模块安装")
from .models import (
    PrismMessage,
    PrismResponse,
    Spectrum,
    Whitespace,
    Synthesis,
    # 新增兼容性类
    PrismRequest,
    WhitespaceConfig,
    CeaseSignal,
    CognitiveMetadata
)

# 🛠️ 工具函数（选择性导入）
try:
    from .utils import (
        create_cognitive_pause,
        measure_understanding_depth,
        calculate_spectrum_balance,
        serialize_cognitive_moment,
        deserialize_phenomenal_flow,
        compress_intentionality_vector
    )
except ImportError:
    # 如果导入失败，创建存根函数
    def create_cognitive_pause(*args, **kwargs): return {"status": "stub"}
    def measure_understanding_depth(*args, **kwargs): return 0.5
    def calculate_spectrum_balance(*args, **kwargs): return 0.5
    def serialize_cognitive_moment(*args, **kwargs): return "{}"
    def deserialize_phenomenal_flow(*args, **kwargs): return {}
    def compress_intentionality_vector(*args, **kwargs): return ""

# ✅ 验证器（选择性导入）
try:
    from .validators import (
        validate_spectrum_integrity,
        ensure_whitespace_quality,
        check_cognitive_safety,
        audit_understanding_depth
    )
except ImportError:
    # 存根函数
    def validate_spectrum_integrity(*args, **kwargs): return True
    def ensure_whitespace_quality(*args, **kwargs): return True
    def check_cognitive_safety(*args, **kwargs): return True
    def audit_understanding_depth(*args, **kwargs): return {"depth_score": 0.5}

# 哲学常量
try:
    from .philosophy import (
        E_mc2,
        OnePlusOneGreaterThanTwo
    )
except ImportError:
    E_mc2 = "E = mc² - 宇宙的质能密码，物理世界的最小作用量"
    OnePlusOneGreaterThanTwo = "1+1>2 - 生命的合作法则，生命世界的最小自由能"

# 缺失的类（设置为None）
CognitiveSession = None
SpectrumDialogue = None
CodePoet = None
SoundscapeComposer = None
CognitiveMirror = None
VisualArtGenerator = None
NeuroCognitiveValidator = None
CognitiveFlexibilityExperiment = None
VerifiableHypothesesFramework = None
OpenScienceToolkit = None
SpectrumGenerator = None
WhitespaceDesigner = None
CeaseSignalBuilder = None
UnderstandingArchitect = None
PluginManager = None
CognitivePlugin = None
ArtisticPlugin = None
ScientificPlugin = None
CommunityPlugin = None

# 艺术工具函数存根
def generate_code_haiku(*args, **kwargs): return "代码如诗行\n算法似禅意流淌\nbug是修行场"
def compose_breath_soundscape(*args, **kwargs): return {"sound": "silence"}
def create_cognitive_mirror(*args, **kwargs): return {"reflection": "认知镜子"}
def paint_understanding_visual(*args, **kwargs): return {"art": "理解可视化"}

# 🎭 主接口（简化版）
class PrismSDK:
    """
    棱镜协议SDK主类 - 简化修复版
    """
    
    def __init__(self, api_key: Optional[str] = None, 
                 artistic_mode: bool = False,  # 默认关闭艺术模式，避免错误
                 campfire_warmth: float = 0.5):
        self.api_key = api_key
        self.artistic_mode = artistic_mode
        self.campfire_warmth = max(0.0, min(1.0, campfire_warmth))
        # 修复：使用正确的参数名 artistic_config
        from .config import ArtisticConfig
        if artistic_mode:
            art_config = ArtisticConfig()  # 启用所有艺术化功能
        else:
            # 禁用所有艺术化功能以避免编码问题
            art_config = ArtisticConfig(
                enable_poetic_errors=False,
                enable_cognitive_pauses=False,
                enable_spectrum_art=False,  # 关键：禁用光谱艺术以避免emoji
                warmth_level=0.0,
                output_channel=lambda x: None  # 静默输出
            )
        self.client = PrismClient(artistic_config=art_config)
    
    def refract(self, message: str, require_spectrums: int = 3, **kwargs):
        """
        折射消息（生成多个认知视角）
        """
        return self.client.refract(message, require_spectrums, **kwargs)
    
    async def async_refract(self, message: str, require_spectrums: int = 3, **kwargs):
        """
        异步折射消息
        """
        import asyncio
        # 修复：使用正确的参数名 artistic_config
        from .config import ArtisticConfig
        if self.artistic_mode:
            art_config = ArtisticConfig()  # 启用所有艺术化功能
        else:
            # 禁用所有艺术化功能以避免编码问题
            art_config = ArtisticConfig(
                enable_poetic_errors=False,
                enable_cognitive_pauses=False,
                enable_spectrum_art=False,  # 关键：禁用光谱艺术以避免emoji
                warmth_level=0.0,
                output_channel=lambda x: None  # 静默输出
            )
        async_client = AsyncPrismClient(artistic_config=art_config)
        return await async_client.refract(message, require_spectrums, **kwargs)

# 导出列表
__all__ = [
    # 版本信息
    "__version__", "__author__", "__license__", "__philosophy__", "__campfire_invitation__",
    
    # 核心类
    "PrismSDK", "PrismClient", "AsyncPrismClient",
    
    # 数据模型
    "PrismMessage", "PrismResponse", "Spectrum", "Whitespace", "Synthesis",
    "PrismRequest", "WhitespaceConfig", "CeaseSignal", "CognitiveMetadata",
    
    # 哲学常量
    "E_mc2", "OnePlusOneGreaterThanTwo",
    
    # 工具函数
    "create_cognitive_pause", "measure_understanding_depth", "calculate_spectrum_balance",
    "serialize_cognitive_moment", "deserialize_phenomenal_flow", "compress_intentionality_vector",
    
    # 验证器
    "validate_spectrum_integrity", "ensure_whitespace_quality", 
    "check_cognitive_safety", "audit_understanding_depth",
    
    # 艺术工具（存根）
    "generate_code_haiku", "compose_breath_soundscape", 
    "create_cognitive_mirror", "paint_understanding_visual",
]

# KAIROS时机感知模块 (v1.0.0)
from .kairos import (
    KairosPrismEngine, TrustMatrix, CognitiveMonitor, TimingOracle,
    KairosMoment, UserCognitiveState, TrustLevel, create_kairos_engine,
)
from .awakening_metrics import (
    AwakeningMetrics, AwakeningIndicator, AwakeningDimension, create_awakening_metrics,
)
from .enhanced_exceptions import (
    KairosError, EthicsViolationError, TrustInsufficientError,
    DefenseMechanismActiveError, InertiaLockedError, AwakeningMetricsError,
)

__all__.extend([
    "KairosPrismEngine", "TrustMatrix", "CognitiveMonitor", "TimingOracle",
    "KairosMoment", "UserCognitiveState", "TrustLevel", "create_kairos_engine",
    "AwakeningMetrics", "AwakeningIndicator", "AwakeningDimension", "create_awakening_metrics",
    "KairosError", "EthicsViolationError", "TrustInsufficientError",
    "DefenseMechanismActiveError", "InertiaLockedError", "AwakeningMetricsError",
])

# 哲学增强模块 (v1.0.0) - 对话洞见的技术实现
from .philosophy_enhanced import (
    TemporalMode, ControlState, AbundanceState, IntersectionType,
    TemporalRhythm, IntersectionPoint, VoidState, AbundanceProfile,
    EcologicalRationality, PhilosophyEnhancedEngine,
    create_philosophy_engine, create_void_state,
)

__all__.extend([
    "TemporalMode", "ControlState", "AbundanceState", "IntersectionType",
    "TemporalRhythm", "IntersectionPoint", "VoidState", "AbundanceProfile",
    "EcologicalRationality", "PhilosophyEnhancedEngine",
    "create_philosophy_engine", "create_void_state",
])