"""
🧠 棱镜互联协议 Python SDK
意义层通信的完整实现

版本: 1.0.0
作者: 璇玑实验室
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "璇玑实验室"
__license__ = "MIT"

from .client import PrismClient
from .models import (
    PrismMessage,
    Spectrum,
    Whitespace,
    Synthesis,
    PrismResponse,
    ValidationResult,
    SpectrumType,
    WhitespaceType,
    ErrorCode
)
from .exceptions import (
    PrismError,
    SpectrumGenerationError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    RecursionDepthError
)
from .validators import validate_message, validate_spectrum
from .generators import (
    generate_spectrums,
    generate_whitespace,
    generate_synthesis
)
from .utils import (
    create_session_id,
    calculate_recursion_depth,
    format_timestamp,
    anonymize_user_data
)

__all__ = [
    # 客户端
    "PrismClient",
    
    # 数据模型
    "PrismMessage",
    "Spectrum",
    "Whitespace",
    "Synthesis",
    "PrismResponse",
    "ValidationResult",
    "SpectrumType",
    "WhitespaceType",
    "ErrorCode",
    
    # 异常
    "PrismError",
    "SpectrumGenerationError",
    "ValidationError",
    "AuthenticationError",
    "RateLimitError",
    "RecursionDepthError",
    
    # 验证器
    "validate_message",
    "validate_spectrum",
    
    # 生成器
    "generate_spectrums",
    "generate_whitespace",
    "generate_synthesis",
    
    # 工具函数
    "create_session_id",
    "calculate_recursion_depth",
    "format_timestamp",
    "anonymize_user_data"
]

# 初始化日志
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

print(f"""
✨ 棱镜互联协议 Python SDK v{__version__}
🧠 意义层通信的现代实现
🌌 基于道家智慧与认知科学
🛡️ 内置伦理护栏与安全机制

快速开始:
>>> from prism_sdk import PrismClient
>>> client = PrismClient(api_key="your_key")
>>> response = await client.prismatic_dialogue("如何平衡工作与生活？")

文档: https://prism-interconnect.dev/docs
GitHub: https://github.com/Ultima0369/prism-interconnect
社区: https://discord.gg/prism
""")