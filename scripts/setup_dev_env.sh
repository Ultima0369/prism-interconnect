#!/bin/bash
# 🚀 棱镜协议开发环境一键配置脚本
# 快速设置完整的开发环境

set -e  # 遇到错误立即退出

echo "🎯 开始设置棱镜协议开发环境..."
echo "========================================"

# ==================== 检查系统要求 ====================
echo "🔍 检查系统要求..."

# 检查Python版本
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python版本: $PYTHON_VERSION"
    
    # 检查Python版本是否满足要求
    REQUIRED_VERSION="3.11.0"
    if printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1 | grep -q "$REQUIRED_VERSION"; then
        echo "✅ Python版本满足要求 (>=3.11)"
    else
        echo "⚠️  Python版本可能过低，建议升级到3.11+"
    fi
else
    echo "❌ 未找到Python3，请先安装Python3.11+"
    exit 1
fi

# 检查pip
if command -v pip3 &> /dev/null; then
    echo "✅ 找到pip3"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✅ 找到pip"
    PIP_CMD="pip"
else
    echo "❌ 未找到pip，请先安装pip"
    exit 1
fi

# 检查git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "✅ Git版本: $GIT_VERSION"
else
    echo "❌ 未找到git，请先安装git"
    exit 1
fi

# 检查Docker（可选）
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    echo "✅ Docker版本: $DOCKER_VERSION"
else
    echo "⚠️  未找到Docker，容器化开发功能将不可用"
fi

# 检查Docker Compose（可选）
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
    echo "✅ Docker Compose版本: $DOCKER_COMPOSE_VERSION"
else
    echo "⚠️  未找到Docker Compose，多容器开发功能将不可用"
fi

echo "✅ 系统检查完成"
echo ""

# ==================== 创建虚拟环境 ====================
echo "🔧 设置Python虚拟环境..."

# 检查是否在虚拟环境中
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "创建新的虚拟环境..."
    
    # 创建虚拟环境目录
    VENV_DIR="venv"
    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv "$VENV_DIR"
        echo "✅ 虚拟环境创建成功: $VENV_DIR"
    else
        echo "✅ 虚拟环境已存在: $VENV_DIR"
    fi
    
    # 激活虚拟环境
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
        # macOS 或 Linux
        source "$VENV_DIR/bin/activate"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash)
        source "$VENV_DIR/Scripts/activate"
    elif [[ "$OSTYPE" == "win32" ]]; then
        # Windows (CMD)
        "$VENV_DIR\\Scripts\\activate.bat"
    else
        echo "⚠️  无法自动激活虚拟环境，请手动激活:"
        echo "   source $VENV_DIR/bin/activate  # Linux/macOS"
        echo "   $VENV_DIR\\Scripts\\activate   # Windows"
    fi
else
    echo "✅ 已在虚拟环境中: $VIRTUAL_ENV"
fi

echo ""

# ==================== 安装依赖 ====================
echo "📦 安装Python依赖..."

# 升级pip
echo "升级pip..."
$PIP_CMD install --upgrade pip

# 安装开发依赖
echo "安装开发依赖..."
$PIP_CMD install -r requirements-dev.txt

# 安装项目依赖
echo "安装项目依赖..."
$PIP_CMD install -e implementations/python/[dev]

# 安装预提交钩子
echo "安装预提交钩子..."
if command -v pre-commit &> /dev/null; then
    pre-commit install --hook-type pre-commit --hook-type commit-msg
    echo "✅ 预提交钩子安装成功"
else
    echo "⚠️  未找到pre-commit，跳过钩子安装"
fi

echo "✅ 依赖安装完成"
echo ""

# ==================== 设置Git配置 ====================
echo "🔧 设置Git配置..."

# 设置Git用户名（如果未设置）
if [[ -z "$(git config --global user.name)" ]]; then
    read -p "请输入Git用户名: " GIT_USERNAME
    git config --global user.name "$GIT_USERNAME"
    echo "✅ Git用户名已设置"
fi

# 设置Git邮箱（如果未设置）
if [[ -z "$(git config --global user.email)" ]]; then
    read -p "请输入Git邮箱: " GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
    echo "✅ Git邮箱已设置"
fi

# 设置Git行尾配置
git config --global core.autocrlf input
echo "✅ Git行尾配置已设置"

echo "✅ Git配置完成"
echo ""

# ==================== 运行初始测试 ====================
echo "🧪 运行初始测试..."

# 运行基础测试
cd implementations/python
if python -m pytest tests/test_basics.py -v; then
    echo "✅ 基础测试通过"
else
    echo "⚠️  基础测试失败，请检查"
fi

# 运行代码质量检查
echo "运行代码质量检查..."
if python -m flake8 prism_sdk --max-line-length=100; then
    echo "✅ 代码风格检查通过"
else
    echo "⚠️  代码风格检查失败，请修复"
fi

# 运行类型检查
echo "运行类型检查..."
if python -m mypy prism_sdk --strict; then
    echo "✅ 类型检查通过"
else
    echo "⚠️  类型检查失败，请修复"
fi

cd ../..
echo "✅ 初始测试完成"
echo ""

# ==================== 设置开发工具 ====================
echo "🛠️ 设置开发工具..."

# 创建开发配置文件
echo "创建开发配置文件..."
cat > .env.development << EOF
# 棱镜协议开发环境配置
PRISM_ENV=development
LOG_LEVEL=DEBUG
DEBUG=true

# 数据库配置（开发环境）
DATABASE_URL=sqlite:///./prism_dev.db
REDIS_URL=redis://localhost:6379/0

# API配置
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# 安全配置（开发环境降低要求）
SECURITY_ENABLED=false
CORS_ENABLED=true

# 性能配置
CACHE_ENABLED=true
CACHE_TTL=300
MAX_RECURSION_DEPTH=5
EOF

echo "✅ 开发配置文件创建: .env.development"

# 创建测试配置文件
echo "创建测试配置文件..."
cat > .env.test << EOF
# 棱镜协议测试环境配置
PRISM_ENV=test
LOG_LEVEL=INFO
DEBUG=false

# 测试数据库
DATABASE_URL=sqlite:///./prism_test.db
REDIS_URL=redis://localhost:6379/1

# 测试配置
TEST_TIMEOUT=30
TEST_CONCURRENCY=4
EOF

echo "✅ 测试配置文件创建: .env.test"

echo "✅ 开发工具设置完成"
echo ""

# ==================== 创建开发脚本 ====================
echo "📝 创建开发脚本..."

# 创建开发启动脚本
cat > scripts/develop.sh << 'EOF'
#!/bin/bash
# 🚀 棱镜协议开发启动脚本

set -e

echo "🚀 启动棱镜协议开发环境..."

# 激活虚拟环境
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    else
        echo "❌ 未找到虚拟环境，请先运行 setup_dev_env.sh"
        exit 1
    fi
fi

# 加载开发环境变量
if [[ -f ".env.development" ]]; then
    export $(cat .env.development | grep -v '^#' | xargs)
    echo "✅ 加载开发环境变量"
fi

# 启动开发服务器
echo "启动开发服务器..."
cd implementations/python

# 检查是否安装uvicorn
if ! command -v uvicorn &> /dev/null; then
    pip install uvicorn[standard]
fi

# 启动服务器
uvicorn prism_sdk.api:app \
    --host $API_HOST \
    --port $API_PORT \
    --workers $API_WORKERS \
    --reload \
    --log-level debug
EOF

chmod +x scripts/develop.sh
echo "✅ 开发启动脚本创建: scripts/develop.sh"

# 创建测试运行脚本
cat > scripts/test.sh << 'EOF'
#!/bin/bash
# 🧪 棱镜协议测试运行脚本

set -e

echo "🧪 运行棱镜协议测试..."

# 激活虚拟环境
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    else
        echo "❌ 未找到虚拟环境，请先运行 setup_dev_env.sh"
        exit 1
    fi
fi

# 加载测试环境变量
if [[ -f ".env.test" ]]; then
    export $(cat .env.test | grep -v '^#' | xargs)
    echo "✅ 加载测试环境变量"
fi

# 运行测试
cd implementations/python

echo "运行单元测试..."
python -m pytest tests/ -v --cov=prism_sdk --cov-report=term

echo "运行集成测试..."
python -m pytest tests/ -v -m integration

echo "运行性能测试..."
python -m pytest benchmarks/ -v

echo "运行安全测试..."
if command -v bandit &> /dev/null; then
    bandit -r prism_sdk -ll
else
    echo "⚠️  未安装bandit，跳过安全测试"
fi

echo "✅ 所有测试完成"
EOF

chmod +x scripts/test.sh
echo "✅ 测试运行脚本创建: scripts/test.sh"

# 创建代码质量检查脚本
cat > scripts/lint.sh << 'EOF'
#!/bin/bash
# 🔍 棱镜协议代码质量检查脚本

set -e

echo "🔍 运行代码质量检查..."

# 激活虚拟环境
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    else
        echo "❌ 未找到虚拟环境，请先运行 setup_dev_env.sh"
        exit 1
    fi
fi

cd implementations/python

echo "运行black代码格式化..."
python -m black --check --diff prism_sdk tests benchmarks

echo "运行isort导入排序..."
python -m isort --check-only --diff prism_sdk tests benchmarks

echo "运行flake8代码风格检查..."
python -m flake8 prism_sdk tests benchmarks --max-line-length=100 --extend-ignore=E203,W503

echo "运行mypy类型检查..."
python -m mypy prism_sdk --strict --ignore-missing-imports

echo "运行pydocstyle文档检查..."
if command -v pydocstyle &> /dev/null; then
    python -m pydocstyle prism_sdk
else
    echo "⚠️  未安装pydocstyle，跳过文档检查"
fi

echo "✅ 代码质量检查完成"
EOF

chmod +x scripts/lint.sh
echo "✅ 代码质量检查脚本创建: scripts/lint.sh"

echo "✅ 开发脚本创建完成"
echo ""

# ==================== 设置IDE配置 ====================
echo "💻 设置IDE配置..."

# 创建VS Code配置
if [[ ! -d ".vscode" ]]; then
    mkdir .vscode
    
    cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "\${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/.coverage": true,
        "**/htmlcov": true,
        "**/.eggs": true,
        "**/*.egg-info": true,
        "**/dist": true,
        "**/build": true
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests",
        "-v",
        "--cov=prism_sdk",
        "--cov-report=term",
        "--cov-report=html"
    ]
}
EOF
    
    cat > .vscode/extensions.json << EOF
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "ms-python.isort",
        "eamodio.gitlens",
        "streetsidesoftware.code-spell-checker",
        "yzhang.markdown-all-in-one",
        "shd101wyy.markdown-preview-enhanced",
        "bierner.markdown-checkbox",
        "davidanson.vscode-markdownlint",
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "redhat.vscode-yaml",
        "github.vscode-github-actions",
        "github.copilot",
        "github.copilot-chat"
    ]
}
EOF
    
    echo "✅ VS Code配置创建完成"
else
    echo "✅ VS Code配置已存在"
fi

# 创建PyCharm配置提示
cat > IDE_CONFIGURATION.md << 'EOF'
# 🛠️ IDE配置指南

## PyCharm配置

### 1. 设置Python解释器
1. 打开设置 (File → Settings)
2. 进入 Project: prism-interconnect → Python Interpreter
3. 点击齿轮图标 → Add
4. 选择 Existing environment
5. 浏览到 `venv/bin/python` (Linux/macOS) 或 `venv\Scripts\python.exe` (Windows)
6. 点击 OK

### 2. 配置代码风格
1. 打开设置 (File → Settings)
2. 进入 Editor → Code Style → Python
3. 点击设置图标 → Import Scheme → Black
4. 设置 Line length 为 100

### 3. 配置测试
1. 打开设置 (File → Settings)
2. 进入 Tools → Python Integrated Tools
3. 设置 Testing → Default test runner 为 pytest
4. 设置 pytest 参数: `-v --cov=prism_sdk --cov-report=term`

### 4. 配置运行配置
1. 点击运行配置下拉菜单 → Edit Configurations
2. 添加 Python 配置:
   - Script path: `implementations/python/prism_sdk/api.py`
   - Parameters: `--host 0.0.0.0 --port 8000 --reload`
   - Environment variables: 从 `.env.development` 加载

## VS Code配置

配置已自动生成在 `.vscode/` 目录中。

### 推荐扩展
已配置在 `.vscode/extensions.json` 中，安装推荐扩展即可。

## 其他IDE

### Sublime Text
1. 安装 Package Control
2. 安装以下包:
   - Anaconda (Python开发)
   - Black Formatter
   - SublimeLinter-flake8
   - SublimeLinter-mypy

### Vim/Neovim
1. 安装 coc.nvim 或 ALE
2. 配置 Python LSP:
   ```vim
   " coc.nvim 配置
   let g:coc_global_extensions = ['coc-pyright', 'coc-black', 'coc-flake8']
   
   " ALE 配置
   let g:ale_linters = {'python': ['flake8', 'mypy', 'pylint']}
   let g:ale_fixers = {'python': ['black', 'isort']}
   let g:ale_fix_on_save = 1
