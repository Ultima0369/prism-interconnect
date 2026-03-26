"""
🧠 棱镜互联协议 Python SDK
安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取版本信息
with open("prism_sdk/__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

# 读取长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# 读取依赖
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="prism-interconnect-sdk",
    version=version,
    author="璇玑实验室",
    author_email="contact@prism-interconnect.dev",
    description="🧠 棱镜互联协议 Python SDK - 意义层通信的现代实现",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ultima0369/prism-interconnect",
    packages=find_packages(),
    package_data={
        "prism_sdk": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=2.0.0",
        ],
        "performance": [
            "psutil>=5.9.0",
            "ujson>=5.0.0",
            "orjson>=3.9.0",
        ],
        "full": [
            "aiohttp>=3.9.0",
            "pydantic>=2.0.0",
            "python-dateutil>=2.8.0",
            "pyjwt>=2.8.0",
            "cryptography>=41.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prism-cli=prism_sdk.cli:main",
        ],
    },
    project_urls={
        "Documentation": "https://prism-interconnect.dev/docs",
        "Source": "https://github.com/Ultima0369/prism-interconnect",
        "Tracker": "https://github.com/Ultima0369/prism-interconnect/issues",
        "Discord": "https://discord.gg/prism",
    },
    keywords=[
        "prism",
        "interconnect",
        "protocol",
        "communication",
        "cognitive",
        "ai",
        "dialogue",
        "thinking",
        "spectrum",
        "whitespace",
        "synthesis",
    ],
)