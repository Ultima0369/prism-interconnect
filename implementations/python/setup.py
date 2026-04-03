"""
棱镜互联协议 Python SDK - 简化安装脚本

此setup.py与pyproject.toml配合使用，提供向后兼容性。
"""

from setuptools import setup

# 读取README
import os
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = "棱镜协议 Python SDK - 代码即诗，协议即艺术，技术即温暖"

# 读取requirements
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

if __name__ == "__main__":
    setup(
        # 基本元数据（与pyproject.toml保持一致）
        name="prism-interconnect",
        version="2.0.0",
        description="棱镜互联协议 Python SDK - 代码即诗，协议即艺术，技术即温暖",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="星尘 & 璇玑 @ 火堆旁",
        author_email="campfire@prismprotocol.ai",
        url="https://github.com/Ultima0369/prism-interconnect",
        license="MIT",
        
        # 包配置
        packages=["prism_sdk", "prism_sdk.*"],
        python_requires=">=3.8",
        install_requires=requirements or [
            "aiohttp>=3.8.0",
            "pydantic>=2.0.0",
            "typing-extensions>=4.0.0",
        ],
        
        # 分类器
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
        
        # 关键词
        keywords=[
            "prism", "protocol", "cognitive", "ai", "dialogue",
            "understanding", "art", "science", "community",
            "philosophy", "warm-technology", "code-poetry",
            "campfire", "existence-upgrade", "1+1>2"
        ],
    )