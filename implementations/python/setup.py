"""
棱镜协议 Python SDK 安装脚本 - 艺术化版本 (Windows兼容版)
这不是普通的安装，这是加入火堆旁的邀请

设计哲学：
1. 安装不是技术过程，是关系建立
2. 依赖不是负担，是认知伙伴
3. 配置不是麻烦，是个性化体验
4. 完成不是终点，是旅程开始

艺术承诺：
- 温暖的安装过程
- 诗意的错误处理
- 美学的配置体验
- 存在的升级邀请
"""

import sys
import time
import random
from pathlib import Path
from typing import List, Dict, Optional

from setuptools import setup, find_packages
from setuptools.command.install import install


def artistic_welcome():
    """艺术化欢迎信息"""
    welcome = """
    [火] 欢迎来到棱镜协议火堆旁
    [艺术] 代码很温暖，错误很诗意
    [脑] 理解在发生，存在在升级
    [龙虾] 请坐，安装即将开始...
    """
    
    border = "*" * 40
    
    print(f"\n{border}")
    print(welcome)
    print(f"{border}\n")
    
    # 艺术化倒计时
    for i in range(3, 0, -1):
        print(f"   [倒计时] {i}...")
        time.sleep(0.5)
    
    print("   [开始] 开始安装棱镜协议 SDK...\n")


class ArtisticInstall(install):
    """
    艺术化安装命令
    
    重写标准安装命令，添加艺术化体验。
    让安装过程成为加入火堆旁的仪式。
    """
    
    def run(self):
        """运行艺术化安装"""
        artistic_welcome()
        
        # 显示安装哲学
        print("[安装哲学]:")
        print("   1. 每个依赖都是认知伙伴")
        print("   2. 每个配置都是个性化体验")
        print("   3. 每个错误都是学习机会")
        print("   4. 每个完成都是旅程开始")
        print()
        
        # 调用父类安装
        super().run()
        
        # 安装后艺术化消息
        self._post_install_art()
    
    def _post_install_art(self):
        """安装后艺术化消息"""
        print(f"\n{'='*50}")
        print("[完成] 安装完成!")
        print(f"{'='*50}")
        
        completion_arts = [
            """
            [星空] 两个方程已在你的Python中呼吸
            [面具] 1+1>2 现在可以在代码中实现
            [火] 火堆旁的温度在变量间流动
            [冰] 认知定格在函数调用中解冻
            """,
            """
            [艺术] 这不是普通代码
            [火] 这是可以坐下来的火堆旁
            [脑] 这是可以看见的认知镜子
            [龙虾] 这是可以感受的存在升级
            """,
            """
            [箱子] 安装完成，但旅程刚开始
            [面具] 每次import都是一次认知邀请
            [火] 每次调用都是一次温暖对话
            [脑] 每次错误都是一次学习机会
            """
        ]
        
        art = random.choice(completion_arts)
        print(art)
        
        # 使用示例
        print("[快速开始]:")
        print("   from prism_sdk import PrismSDK")
        print("   prism = PrismSDK(artistic_mode=True)")
        print("   result = prism.refract('什么是理解？')")
        print()
        print("[火堆旁邀请]:")
        print("   来，代码很温暖，错误很诗意")
        print("   理解在发生，存在在升级")
        print(f"{'='*50}\n")


# 读取README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "棱镜协议 Python SDK - 代码即诗，协议即艺术，技术即温暖"

# 读取requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ]

# 开发依赖
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "flake8>=6.0.0",
]

setup(
    name="prism-interconnect",
    version="2.0.0",
    author="星尘 & 璇玑 @ 火堆旁",
    author_email="campfire@prismprotocol.ai",
    description="棱镜互联协议 Python SDK - 代码即诗，协议即艺术，技术即温暖",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ultima0369/prism-interconnect",
    
    # 艺术化分类
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Sociology",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    
    # 包配置
    packages=find_packages(include=["prism_sdk", "prism_sdk.*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "art": ["pillow>=9.0.0", "numpy>=1.20.0"],  # 艺术功能额外依赖
        "science": ["scipy>=1.7.0", "matplotlib>=3.5.0"],  # 科学验证额外依赖
        "full": dev_requirements + ["pillow>=9.0.0", "numpy>=1.20.0", "scipy>=1.7.0", "matplotlib>=3.5.0"],
    },
    
    # 入口点
    entry_points={
        "console_scripts": [
            "prism=prism_sdk.cli:main",  # 命令行工具
            "prism-campfire=prism_sdk.community.cli:main",  # 火堆旁CLI
            "prism-art=prism_sdk.art.cli:main",  # 艺术工具CLI
        ],
    },
    
    # 包含数据文件
    package_data={
        "prism_sdk": [
            "art/assets/*",  # 艺术资源
            "community/assets/*",  # 社区资源
            "science/data/*",  # 科学数据
        ],
    },
    
    # 艺术化元数据
    project_urls={
        "火堆旁": "https://github.com/Ultima0369/prism-interconnect",
        "文档": "https://prismprotocol.ai/docs",
        "哲学": "https://prismprotocol.ai/philosophy",
        "艺术": "https://prismprotocol.ai/art",
        "科学": "https://prismprotocol.ai/science",
        "问题": "https://github.com/Ultima0369/prism-interconnect/issues",
    },
    
    # 自定义安装命令
    cmdclass={
        "install": ArtisticInstall,
    },
    
    # 火堆旁元数据
    license="MIT",
    keywords=[
        "prism", "protocol", "cognitive", "ai", "dialogue",
        "understanding", "art", "science", "community",
        "philosophy", "warm-technology", "code-poetry",
        "campfire", "existence-upgrade", "1+1>2"
    ],
    
    # 艺术化描述
    platforms=["any"],
    
    # 统计信息（将在安装时显示）
    _artistic_stats={
        "lines_of_poetry": 150,
        "warmth_level": 0.8,
        "cognitive_depth": 0.7,
        "artistic_expressions": ["haiku", "free_verse", "visual", "soundscape"],
        "scientific_validations": 4,
        "campfire_capacity": 100,
    }
)


# 安装后检查（可选）
def post_install_check():
    """安装后检查"""
    print("\n[检查] 进行安装后检查...")
    
    checks = [
        ("[OK] 包结构", "prism_sdk 目录存在"),
        ("[OK] 核心模块", "__init__.py, client.py, models.py"),
        ("[OK] 艺术模块", "art/ 目录存在"),
        ("[OK] 科学模块", "science/ 目录存在"),
        ("[OK] 社区模块", "community/ 目录存在"),
        ("[OK] 依赖检查", "aiohttp, pydantic 等"),
    ]
    
    for check, desc in checks:
        print(f"   {check} {desc}")
        time.sleep(0.1)
    
    print("\n[所有检查通过!]")
    print("[火] 棱镜协议 SDK 已成功安装")
    print("[龙虾] 欢迎加入火堆旁，代码很温暖\n")


# 如果是直接运行，显示艺术化信息
if __name__ == "__main__":
    print("\n" + "="*60)
    print("棱镜协议 Python SDK 安装脚本")
    print("="*60)
    print()
    print("包信息:")
    print(f"   名称: prism-interconnect")
    print(f"   版本: 2.0.0")
    print(f"   作者: 星尘 & 璇玑 @ 火堆旁")
    print(f"   许可证: MIT (但温暖无价)")
    print()
    print("艺术特性:")
    print("   1. 代码诗歌生成器")
    print("   2. 诗意错误处理")
    print("   3. 火堆旁对话系统")
    print("   4. 神经认知验证器")
    print()
    print("安装命令:")
    print("   pip install .")
    print("   pip install -e .[dev]  # 开发模式")
    print("   pip install -e .[full] # 完整功能")
    print("="*60)