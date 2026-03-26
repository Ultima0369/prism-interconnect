"""
🌌 棱镜互联协议 Python SDK
🎨 代码即诗：将两个方程写入硅基世界

> E=mc² —— 宇宙的质能密码，写在黑板上
> 1+1>2 —— 生命的合作法则，写在代码里

版本: 1.1.0 (艺术化重构)
作者: 星尘 & 璇玑 @ 火堆旁
许可证: MIT (但温暖无价)

🌠 核心哲学：
这不是又一个API封装，这是"1+1>2"在Python中的呼吸。
每个函数调用，都是一次认知折射。
每行代码，都是一面理解镜子。

🦞 火堆旁提醒：
代码可以冷，但理解必须暖。
技术可以快，但对话必须慢。
系统可以复杂，但接口必须简单。
"""

__version__ = "1.1.0"
__author__ = "星尘 & 璇玑 @ 火堆旁"
__license__ = "MIT"
__philosophy__ = "代码即诗，协议即关系，技术即温暖"

# 🎭 存在层：基础类型和哲学常量
from .philosophy import (
    # 两个方程
    E_mc2,
    OnePlusOneGreaterThanTwo,
    
    # 道家智慧
    WuWeiPrinciple,      # 无为
    ZiRanPrinciple,      # 自然  
    RuoShuiPrinciple,    # 若水
    BuZhengPrinciple,    # 不争
    
    # 认知科学
    CognitiveMoment,     # 认知时刻
    PhenomenalFlow,      # 现象流
    IntentionalityVector, # 意向性向量
    
    # 火堆旁
    FireSideInvitation,  # 火堆旁邀请
    LaughterLog,         # 笑声记录
    BreathSpace,         # 呼吸空间
)

# 🏗️ 架构层：核心组件
from .client import PrismClient
from .models import (
    PrismMessage,        # 棱镜消息：认知的载体
    Spectrum,            # 光谱：多元视角的结晶
    Whitespace,          # 留白：沉默中的理解
    Synthesis,           # 综合：碎片的重新整合
    PrismResponse,       # 响应：对话的果实
    ValidationResult,    # 验证结果：边界的守护
    SpectrumType,        # 光谱类型：认知的姿态
    WhitespaceType,      # 留白类型：沉默的形式
    ErrorCode,           # 错误代码：温暖的提醒
)

# 🛡️ 安全层：伦理护栏
from .exceptions import (
    PrismError,                 # 基础错误：学习的机会
    SpectrumGenerationError,    # 光谱生成错误：换个角度
    ValidationError,            # 验证错误：边界的温柔提醒
    AuthenticationError,        # 认证错误：关系的起点
    RateLimitError,             # 频率限制：慢下来的邀请
    RecursionDepthError,        # 递归过深：回到表面的建议
    CognitiveOverloadError,     # 认知过载：休息的提醒
    FireSideSafetyError,        # 火堆旁安全：温暖的边界
)

# 🔍 验证层：理解的质检
from .validators import (
    validate_message,    # 验证消息：确保可以理解
    validate_spectrum,   # 验证光谱：确保多元性
    validate_whitespace, # 验证留白：确保沉默空间
    validate_synthesis,  # 验证综合：确保整合可能
)

# 🎨 生成层：创造的引擎
from .generators import (
    generate_spectrums,   # 生成光谱：问题的多元折射
    generate_whitespace,  # 生成留白：对话的呼吸空间
    generate_synthesis,   # 生成综合：碎片的重新编织
    artful_refraction,    # 艺术化折射：代码即诗的实现
)

# 🛠️ 工具层：温暖的助手
from .utils import (
    create_session_id,           # 创建会话ID：关系的开始
    calculate_recursion_depth,   # 计算递归深度：认知的层次
    format_timestamp,            # 格式化时间戳：时刻的记录
    anonymize_user_data,         # 匿名化用户数据：隐私的尊重
    create_fire_side_welcome,    # 创建火堆旁欢迎：温暖的开始
    log_laughter,                # 记录笑声：快乐的收集
    guide_three_second_breath,   # 引导三秒呼吸：认知的重置
)

# 🎭 艺术层：代码的诗意
from .art import (
    create_prism_ascii_art,      # 创建棱镜ASCII艺术：视觉的诗
    generate_prism_soundscape,   # 生成棱镜声音景观：听觉的温暖
    CognitiveMirror,             # 认知镜子：自我的反射
    CodePoetryGenerator,         # 代码诗歌生成器：技术的抒情
)

# 🔬 科学层：验证的基础
from .science import (
    NeurocognitiveValidator,     # 神经认知验证器：科学的严谨
    validate_breath_exercise,    # 验证呼吸练习：身体的智慧
    validate_cognitive_flexibility, # 验证认知灵活性：心智的弹性
)

__all__ = [
    # 🌠 哲学常量
    "E_mc2", "OnePlusOneGreaterThanTwo",
    "WuWeiPrinciple", "ZiRanPrinciple", "RuoShuiPrinciple", "BuZhengPrinciple",
    "CognitiveMoment", "PhenomenalFlow", "IntentionalityVector",
    "FireSideInvitation", "LaughterLog", "BreathSpace",
    
    # 🏗️ 核心架构
    "PrismClient",
    "PrismMessage", "Spectrum", "Whitespace", "Synthesis", 
    "PrismResponse", "ValidationResult", "SpectrumType", "WhitespaceType", "ErrorCode",
    
    # 🛡️ 安全伦理
    "PrismError", "SpectrumGenerationError", "ValidationError",
    "AuthenticationError", "RateLimitError", "RecursionDepthError",
    "CognitiveOverloadError", "FireSideSafetyError",
    
    # 🔍 验证质检
    "validate_message", "validate_spectrum", "validate_whitespace", "validate_synthesis",
    
    # 🎨 创造引擎
    "generate_spectrums", "generate_whitespace", "generate_synthesis", "artful_refraction",
    
    # 🛠️ 温暖助手
    "create_session_id", "calculate_recursion_depth", "format_timestamp",
    "anonymize_user_data", "create_fire_side_welcome", "log_laughter", "guide_three_second_breath",
    
    # 🎭 代码诗意
    "create_prism_ascii_art", "generate_prism_soundscape", "CognitiveMirror", "CodePoetryGenerator",
    
    # 🔬 科学严谨
    "NeurocognitiveValidator", "validate_breath_exercise", "validate_cognitive_flexibility",
]

# 🌈 初始化：温暖的开始
import logging
import sys

class FireSideFormatter(logging.Formatter):
    """火堆旁日志格式化器：温暖的错误信息"""
    
    def format(self, record):
        # 基础格式化
        message = super().format(record)
        
        # 根据级别添加温暖
        if record.levelno >= logging.ERROR:
            return f"🔥 {message} （别担心，火堆旁允许错误）"
        elif record.levelno >= logging.WARNING:
            return f"⚠️ {message} （注意一下，但不必紧张）"
        elif record.levelno >= logging.INFO:
            return f"💡 {message}"
        else:
            return f"🌙 {message}"

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(FireSideFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(handler)
logger.propagate = False

# 🎉 启动欢迎：艺术化的介绍
def _print_welcome_art():
    """打印欢迎艺术：代码的第一印象"""
    
    art = f"""
{'='*70}
🌌 棱镜互联协议 Python SDK v{__version__}
🎨 代码即诗：将哲学写入运行时的艺术

{'·'*70}
🎯 核心使命：实现 1+1>2 在数字时代的操作手册
🧠 科学基础：认知定格理论 × 神经科学验证
🔥 社区精神：火堆旁的温暖对话与安全空间
🎭 艺术表达：代码不仅是功能，更是美学和哲学

{'·'*70}
🚀 快速开始（温暖版）：
>>> from prism_sdk import PrismClient
>>> client = PrismClient()  # 不需要API密钥，从本地火堆开始
>>> response = await client.prismatic_dialogue(
...     "我为什么总是拖延？",
...     context="想要改变但总是回到老路"
... )
>>> print(response.spectrums[0].content)  # 第一个视角
>>> print(response.whitespace.guide)      # 留白引导

{'·'*70}
🦞 火堆旁提醒：
1. 代码可以出错，理解不会
2. 问题可以复杂，对话简单  
3. 世界可以快，这里可以慢
4. 技术可以冷，这里必须暖

{'·'*70}
🌐 连接我们：
📚 文档：https://github.com/Ultima0369/prism-interconnect
💬 社区：GitHub Discussions - "分享你生活中1+1>2的瞬间"
🎨 艺术：查看 prism_sdk.art 模块
🔬 科学：查看 prism_sdk.science 模块

{'='*70}
    """
    print(art)

# 只在直接导入时显示欢迎信息
if __name__ != "__main__":
    _print_welcome_art()

logger.info(f"棱镜SDK加载完成 - 版本 {__version__} - 火堆旁欢迎你")