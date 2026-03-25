@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo 🔥 棱镜协议一键分享脚本（Windows版）
echo ========================================
echo.

REM 检查Python
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python3
    pause
    exit /b 1
)

REM 检查Streamlit
python -c "import streamlit" >nul 2>nul
if errorlevel 1 (
    echo 📦 安装Streamlit...
    pip install streamlit
)

REM 检查pyngrok
python -c "import pyngrok" >nul 2>nul
if errorlevel 1 (
    echo 📦 安装pyngrok...
    pip install pyngrok
)

echo ✅ 环境检查完成
echo.

REM 选择应用版本
echo 请选择要启动的应用版本：
echo 1. 🔥 极简体验版（推荐给新手）
echo 2. 🧠 完整功能版（包含所有光谱和留白）
echo 3. 🎮 演示模式（预加载示例问题）
set /p app_choice="请输入选择 (1/2/3，默认1): "

if "%app_choice%"=="2" (
    set app_file=examples\streamlit_app.py
    set app_name=完整功能版
) else if "%app_choice%"=="3" (
    set app_file=examples\streamlit_demo.py
    set app_name=演示模式
) else (
    set app_file=examples\streamlit_simple_app.py
    set app_name=极简体验版
)

REM 检查应用文件是否存在
if not exist "%app_file%" (
    echo ❌ 应用文件不存在：%app_file%
    echo 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

echo 🚀 启动 %app_name% ...
echo.

REM 获取本地IP地址
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set "local_ip=%%a"
    goto :ip_found
)
:ip_found
set local_ip=%local_ip: =%
if "%local_ip%"=="" set local_ip=localhost

echo 📡 本地访问地址：
echo    http://%local_ip%:8501
echo.

REM 启动Streamlit应用
echo 启动Streamlit服务...
start /B cmd /c "streamlit run "%app_file%" --server.port 8501 --server.address 0.0.0.0 --theme.base light"

REM 等待应用启动
echo 等待应用启动...
timeout /t 5 /nobreak >nul

REM 检查应用是否启动成功
curl -s http://localhost:8501 >nul 2>nul
if errorlevel 1 (
    echo ❌ Streamlit应用启动失败
    taskkill /F /IM python.exe >nul 2>nul
    pause
    exit /b 1
)

echo ✅ Streamlit应用启动成功
echo.

REM 使用pyngrok生成公网链接
echo 🌐 生成公网访问链接...
echo.

python -c "
import sys
import time
from pyngrok import ngrok, conf, exception

print('正在生成公网链接...')

try:
    # 配置ngrok
    conf.get_default().region = 'us'
    
    # 启动ngrok隧道
    tunnel = ngrok.connect(8501, 'http')
    public_url = tunnel.public_url
    
    print('✅ 公网链接生成成功！')
    print('')
    print('========================================')
    print('🔥 棱镜协议已就绪！')
    print('========================================')
    print('')
    print('📱 公网访问链接：')
    print(f'   {public_url}')
    print('')
    print('💻 本地访问链接：')
    print(f'   http://%local_ip%:8501')
    print('')
    print('👥 分享这个链接给朋友：')
    print('   任何人都可以通过浏览器访问')
    print('')
    print('📋 快速分享文本：')
    print('   我创建了一个在线思考工具，可以帮你从不同视角看问题。')
    print(f'   点击链接立即体验：{public_url}')
    print('')
    print('🛑 停止服务：按 Ctrl+C')
    print('========================================')
    
    # 保存链接到文件
    with open('prism_share_link.txt', 'w', encoding='utf-8') as f:
        f.write(public_url)
    print('链接已保存到：prism_share_link.txt')
    print('')
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('停止服务...')
        ngrok.kill()
        
except exception.PyngrokNgrokError as e:
    print(f'⚠️ ngrok错误：{e}')
    print('')
    print('========================================')
    print('🔥 棱镜协议本地服务已启动')
    print('========================================')
    print('')
    print('💻 本地访问链接：')
    print('   http://%local_ip%:8501')
    print('')
    print('📱 在同一网络下的设备访问：')
    print('   http://%local_ip%:8501')
    print('')
    print('🌐 要生成公网链接，请：')
    print('   1. 访问 https://ngrok.com/download')
    print('   2. 下载并安装ngrok')
    print('   3. 运行：ngrok http 8501')
    print('')
    print('🛑 停止服务：按 Ctrl+C')
    print('========================================')
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        
except Exception as e:
    print(f'❌ 错误：{e}')
    print('请检查网络连接和ngrok配置')
"

REM 清理
echo.
echo 清理进程...
taskkill /F /IM python.exe >nul 2>nul
taskkill /F /IM ngrok.exe >nul 2>nul

echo ✅ 服务已停止
echo.
echo 🔥 感谢使用棱镜协议！
echo    欢迎在GitHub Discussions分享你的体验：
echo    https://github.com/Ultima0369/prism-interconnect/discussions
echo.
pause