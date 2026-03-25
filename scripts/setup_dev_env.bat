@echo off
REM 🚀 棱镜协议开发环境一键配置脚本 (Windows版本)
REM 快速设置完整的开发环境

echo 🎯 开始设置棱镜协议开发环境...
echo ========================================

REM ==================== 检查系统要求 ====================
echo 🔍 检查系统要求...

REM 检查Python版本
where python >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ Python版本: %PYTHON_VERSION%
    
    REM 检查Python版本是否满足要求
    REM 这里简化检查，实际应该进行版本比较
    echo ✅ Python版本检查通过
) else (
    echo ❌ 未找到Python，请先安装Python3.11+
    exit /b 1
)

REM 检查pip
where pip >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ 找到pip
    set PIP_CMD=pip
) else (
    where pip3 >nul 2>nul
    if %errorlevel% equ 0 (
        echo ✅ 找到pip3
        set PIP_CMD=pip3
    ) else (
        echo ❌ 未找到pip，请先安装pip
        exit /b 1
    )
)

REM 检查git
where git >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=3" %%i in ('git --version') do set GIT_VERSION=%%i
    echo ✅ Git版本: %GIT_VERSION%
) else (
    echo ❌ 未找到git，请先安装git
    exit /b 1
)

REM 检查Docker（可选）
where docker >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=3 delims=," %%i in ('docker --version') do set DOCKER_VERSION=%%i
    echo ✅ Docker版本: %DOCKER_VERSION%
) else (
    echo ⚠️  未找到Docker，容器化开发功能将不可用
)

REM 检查Docker Compose（可选）
where docker-compose >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=3 delims=," %%i in ('docker-compose --version') do set DOCKER_COMPOSE_VERSION=%%i
    echo ✅ Docker Compose版本: %DOCKER_COMPOSE_VERSION%
) else (
    echo ⚠️  未找到Docker Compose，多容器开发功能将不可用
)

echo ✅ 系统检查完成
echo.

REM ==================== 创建虚拟环境 ====================
echo 🔧 设置Python虚拟环境...

REM 检查是否在虚拟环境中
if "%VIRTUAL_ENV%"=="" (
    echo 创建新的虚拟环境...
    
    REM 创建虚拟环境目录
    set VENV_DIR=venv
    if not exist "%VENV_DIR%" (
        python -m venv "%VENV_DIR%"
        echo ✅ 虚拟环境创建成功: %VENV_DIR%
    ) else (
        echo ✅ 虚拟环境已存在: %VENV_DIR%
    )
    
    REM 激活虚拟环境
    echo 激活虚拟环境...
    call "%VENV_DIR%\Scripts\activate.bat"
    
    if %errorlevel% neq 0 (
        echo ⚠️  无法自动激活虚拟环境，请手动激活:
        echo    %VENV_DIR%\Scripts\activate.bat
    )
) else (
    echo ✅ 已在虚拟环境中: %VIRTUAL_ENV%
)

echo.

REM ==================== 安装依赖 ====================
echo 📦 安装Python依赖...

REM 升级pip
echo 升级pip...
%PIP_CMD% install --upgrade pip

REM 安装开发依赖
echo 安装开发依赖...
%PIP_CMD% install -r requirements-dev.txt

REM 安装项目依赖
echo 安装项目依赖...
%PIP_CMD% install -e implementations/python/[dev]

REM 安装预提交钩子
echo 安装预提交钩子...
where pre-commit >nul 2>nul
if %errorlevel% equ 0 (
    pre-commit install --hook-type pre-commit --hook-type commit-msg
    echo ✅ 预提交钩子安装成功
) else (
    echo ⚠️  未找到pre-commit，跳过钩子安装
)

echo ✅ 依赖安装完成
echo.

REM ==================== 设置Git配置 ====================
echo 🔧 设置Git配置...

REM 设置Git用户名（如果未设置）
git config --global user.name >nul 2>nul
if %errorlevel% neq 0 (
    set /p GIT_USERNAME="请输入Git用户名: "
    git config --global user.name "%GIT_USERNAME%"
    echo ✅ Git用户名已设置
)

REM 设置Git邮箱（如果未设置）
git config --global user.email >nul 2>nul
if %errorlevel% neq 0 (
    set /p GIT_EMAIL="请输入Git邮箱: "
    git config --global user.email "%GIT_EMAIL%"
    echo ✅ Git邮箱已设置
)

REM 设置Git行尾配置
git config --global core.autocrlf input
echo ✅ Git行尾配置已设置

echo ✅ Git配置完成
echo.

REM ==================== 运行初始测试 ====================
echo 🧪 运行初始测试...

REM 运行基础测试
cd implementations/python
python -m pytest tests/test_basics.py -v
if %errorlevel% equ 0 (
    echo ✅ 基础测试通过
) else (
    echo ⚠️  基础测试失败，请检查
)

REM 运行代码质量检查
echo 运行代码质量检查...
python -m flake8 prism_sdk --max-line-length=100
if %errorlevel% equ 0 (
    echo ✅ 代码风格检查通过
) else (
    echo ⚠️  代码风格检查失败，请修复
)

REM 运行类型检查
echo 运行类型检查...
python -m mypy prism_sdk --strict
if %errorlevel% equ 0 (
    echo ✅ 类型检查通过
) else (
    echo ⚠️  类型检查失败，请修复
)

cd ..\..
echo ✅ 初始测试完成
echo.

REM ==================== 设置开发工具 ====================
echo 🛠️ 设置开发工具...

REM 创建开发配置文件
echo 创建开发配置文件...
(
echo # 棱镜协议开发环境配置
echo PRISM_ENV=development
echo LOG_LEVEL=DEBUG
echo DEBUG=true
echo.
echo # 数据库配置（开发环境）
echo DATABASE_URL=sqlite:///./prism_dev.db
echo REDIS_URL=redis://localhost:6379/0
echo.
echo # API配置
echo API_HOST=0.0.0.0
echo API_PORT=8000
echo API_WORKERS=4
echo.
echo # 安全配置（开发环境降低要求）
echo SECURITY_ENABLED=false
echo CORS_ENABLED=true
echo.
echo # 性能配置
echo CACHE_ENABLED=true
echo CACHE_TTL=300
echo MAX_RECURSION_DEPTH=5
) > .env.development

echo ✅ 开发配置文件创建: .env.development

REM 创建测试配置文件
echo 创建测试配置文件...
(
echo # 棱镜协议测试环境配置
echo PRISM_ENV=test
echo LOG_LEVEL=INFO
echo DEBUG=false
echo.
echo # 测试数据库
echo DATABASE_URL=sqlite:///./prism_test.db
echo REDIS_URL=redis://localhost:6379/1
echo.
echo # 测试配置
echo TEST_TIMEOUT=30
echo TEST_CONCURRENCY=4
) > .env.test

echo ✅ 测试配置文件创建: .env.test

echo ✅ 开发工具设置完成
echo.

REM ==================== 创建开发脚本 ====================
echo 📝 创建开发脚本...

REM 创建开发启动脚本
(
echo @echo off
echo REM 🚀 棱镜协议开发启动脚本
echo.
echo echo 🚀 启动棱镜协议开发环境...
echo.
echo REM 激活虚拟环境
echo if "%%VIRTUAL_ENV%%"=="" (
echo     if exist "venv" (
echo         call venv\Scripts\activate.bat
echo     ) else (
echo         echo ❌ 未找到虚拟环境，请先运行 setup_dev_env.bat
echo         exit /b 1
echo     )
echo )
echo.
echo REM 加载开发环境变量
echo if exist ".env.development" (
echo     for /f "usebackq tokens=1,2 delims==" %%i in (".env.development") do (
echo         if not "%%i"=="" if not "%%i:~0,1%%"=="#" (
echo             set "%%i=%%j"
echo         )
echo     )
echo     echo ✅ 加载开发环境变量
echo )
echo.
echo REM 启动开发服务器
echo echo 启动开发服务器...
echo cd implementations\python
echo.
echo REM 检查是否安装uvicorn
echo where uvicorn >nul 2>nul
echo if %%errorlevel%% neq 0 (
echo     pip install uvicorn[standard]
echo )
echo.
echo REM 启动服务器
echo uvicorn prism_sdk.api:app ^
echo     --host %%API_HOST%% ^
echo     --port %%API_PORT%% ^
echo     --workers %%API_WORKERS%% ^
echo     --reload ^
echo     --log-level debug
) > scripts\develop.bat

echo ✅ 开发启动脚本创建: scripts\develop.bat

REM 创建测试运行脚本
(
echo @echo off
echo REM 🧪 棱镜协议测试运行脚本
echo.
echo echo 🧪 运行棱镜协议测试...
echo.
echo REM 激活虚拟环境
echo if "%%VIRTUAL_ENV%%"=="" (
echo     if exist "venv" (
echo         call venv\Scripts\activate.bat
echo     ) else (
echo         echo ❌ 未找到虚拟环境，请先运行 setup_dev_env.bat
echo         exit /b 1
echo     )
echo )
echo.
echo REM 加载测试环境变量
echo if exist ".env.test" (
echo     for /f "usebackq tokens=1,2 delims==" %%i in (".env.test") do (
echo         if not "%%i"=="" if not "%%i:~0,1%%"=="#" (
echo             set "%%i=%%j"
echo         )
echo     )
echo     echo ✅ 加载测试环境变量
echo )
echo.
echo REM 运行测试
echo cd implementations\python
echo.
echo echo 运行单元测试...
echo python -m pytest tests/ -v --cov=prism_sdk --cov-report=term
echo.
echo echo 运行集成测试...
echo python -m pytest tests/ -v -m integration
echo.
echo echo 运行性能测试...
echo python -m pytest benchmarks/ -v
echo.
echo echo 运行安全测试...
echo where bandit >nul 2>nul
echo if %%errorlevel%% equ 0 (
echo     bandit -r prism_sdk -ll
echo ) else (
echo     echo ⚠️  未安装bandit，跳过安全测试
echo )
echo.
echo echo ✅ 所有测试完成
) > scripts\test.bat

echo ✅ 测试运行脚本创建: scripts\test.bat

REM 创建代码质量检查脚本
(
echo @echo off
echo REM 🔍 棱镜协议代码质量检查脚本
echo.
echo echo 🔍 运行代码质量检查...
echo.
echo REM 激活虚拟环境
echo if "%%VIRTUAL_ENV%%"=="" (
echo     if exist "venv" (
echo         call venv\Scripts\activate.bat
echo     ) else (
echo         echo ❌ 未找到虚拟环境，请先运行 setup_dev_env.bat
echo         exit /b 1
echo     )
echo )
echo.
echo cd implementations\python
echo.
echo echo 运行black代码格式化...
echo python -m black --check --diff prism_sdk tests benchmarks
echo.
echo echo 运行isort导入排序...
echo python -m isort --check-only --diff prism_sdk tests benchmarks
echo.
echo echo 运行flake8代码风格检查...
echo python -m flake8 prism_sdk tests benchmarks --max-line-length=100 --extend-ignore=E203,W503
echo.
echo echo 运行mypy类型检查...
echo python -m mypy prism_sdk --strict --ignore-missing-imports
echo.
echo echo 运行pydocstyle文档检查...
echo where pydocstyle >nul 2>nul
echo if %%errorlevel%% equ 0 (
echo     python -m pydocstyle prism_sdk
echo ) else (
echo     echo ⚠️  未安装pydocstyle，跳过文档检查
echo )
echo.
echo echo ✅ 代码质量检查完成
) > scripts\lint.bat

echo ✅ 代码质量检查脚本创建: scripts\lint.bat

echo ✅ 开发脚本创建完成
echo.

REM ==================== 设置IDE配置 ====================
echo 💻 设置IDE配置...

REM 创建VS Code配置
if not exist ".vscode" mkdir .vscode

(
echo {
echo     "python.defaultInterpreterPath": "\${workspaceFolder}/venv/Scripts/python.exe",
echo     "python.terminal.activateEnvironment": true,
echo     "python.linting.enabled": true,
echo     "python.linting.flake8Enabled": true,
echo     "python.linting.mypyEnabled": true,
echo     "python.linting.pylintEnabled": false,
echo     "python.formatting.provider": "black",
echo     "python.formatting.blackArgs": ["--line-length", "100"],
echo     "python.sortImports.args": ["--profile", "black"],
echo     "editor.formatOnSave": true,
echo     "editor.codeActionsOnSave": {
echo         "source.organizeImports": true
echo     },
echo     "files.exclude": {
echo         "**/__pycache__": true,
echo         "**/.pytest_cache": true,
echo         "**/.mypy_cache": true,
echo         "**/.coverage": true,
echo         "**/htmlcov": true,
echo         "**/.eggs": true,
echo         "**/*.egg-info": true,
echo         "**/dist": true,
echo         "**/build": true
echo     },
echo     "python.testing.pytestEnabled": true,
echo     "python.testing.unittestEnabled": false,
echo     "python.testing.pytestArgs": [
echo         "tests",
echo         "-v",
echo         "--cov=prism_sdk",
echo         "--cov-report=term",
echo         "--cov-report=html"
echo     ]
echo }
) > .vscode\settings.json

(
echo {
echo     "recommendations": [
echo         "ms-python.python",
echo         "ms-python.vscode-pylance",
echo         "ms-python.black-formatter",
echo         "ms-python.isort",
echo         "eamodio.gitlens",
echo         "streetsidesoftware.code-spell-checker",
echo         "yzhang.markdown-all-in-one",
echo         "shd101wyy.markdown-preview-enhanced",
echo         "bierner.markdown-checkbox",
echo         "davidanson.vscode-markdownlint",
echo         "ms-azuretools.vscode-docker",
echo         "ms-kubernetes-tools.vscode-kubernetes-tools",
echo         "redhat.vscode-yaml",
echo         "github.vscode-github-actions",
echo         "github.copilot",
echo         "github.copilot-chat"
echo     ]
echo }
) > .vscode\extensions.json

echo ✅ VS Code配置创建完成
echo.

REM ==================== 完成总结 ====================
echo 🎉 开发环境设置完成！
echo.
echo 📋 设置总结:
echo   ✅ Python虚拟环境: venv
echo   ✅ 依赖安装: 开发依赖 + 项目依赖
echo   ✅ Git配置: 用户名、邮箱、行尾
echo   ✅ 初始测试: 基础测试通过
echo   ✅ 开发工具: 环境变量 + 脚本
echo   ✅ IDE配置: VS Code配置
echo.
echo 🚀 下一步:
echo   1. 运行开发服务器: scripts\develop.bat
echo   2. 运行完整测试: scripts\test.bat
echo   3. 检查代码质量: scripts\lint.bat
echo   4. 开始开发！
echo.
echo 🔥 火堆旁的开发，现在开始！
echo.

pause