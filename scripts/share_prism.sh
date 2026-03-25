#!/bin/bash

# 🔥 棱镜协议一键分享脚本
# 启动Streamlit应用并通过ngrok生成公网链接

set -e

echo "🔥 启动棱镜协议分享服务..."
echo "========================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Streamlit
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 安装Streamlit..."
    pip install streamlit
fi

# 检查ngrok
if ! command -v ngrok &> /dev/null; then
    echo "📦 安装ngrok..."
    
    # 根据系统安装ngrok
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
        tar -xzf ngrok-v3-stable-linux-amd64.tgz
        sudo mv ngrok /usr/local/bin/
        rm ngrok-v3-stable-linux-amd64.tgz
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install ngrok/ngrok/ngrok
        
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        echo "⚠️  Windows用户请手动安装ngrok："
        echo "   1. 访问 https://ngrok.com/download"
        echo "   2. 下载并安装ngrok"
        echo "   3. 添加ngrok到系统PATH"
        echo ""
        echo "或者使用Python版ngrok："
        pip install pyngrok
    else
        echo "❌ 不支持的操作系统：$OSTYPE"
        exit 1
    fi
fi

# 检查pyngrok（备用方案）
if ! python3 -c "import pyngrok" &> /dev/null; then
    echo "📦 安装pyngrok（备用方案）..."
    pip install pyngrok
fi

echo "✅ 环境检查完成"
echo ""

# 选择应用版本
echo "请选择要启动的应用版本："
echo "1. 🔥 极简体验版（推荐给新手）"
echo "2. 🧠 完整功能版（包含所有光谱和留白）"
echo "3. 🎮 演示模式（预加载示例问题）"
read -p "请输入选择 (1/2/3，默认1): " app_choice

case $app_choice in
    2)
        app_file="examples/streamlit_app.py"
        app_name="完整功能版"
        ;;
    3)
        app_file="examples/streamlit_demo.py"
        app_name="演示模式"
        ;;
    *)
        app_file="examples/streamlit_simple_app.py"
        app_name="极简体验版"
        ;;
esac

# 检查应用文件是否存在
if [ ! -f "$app_file" ]; then
    echo "❌ 应用文件不存在：$app_file"
    echo "请确保在项目根目录运行此脚本"
    exit 1
fi

echo "🚀 启动 $app_name ..."
echo ""

# 获取本地IP地址
local_ip=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "127.0.0.1")
if [ -z "$local_ip" ] || [ "$local_ip" == "127.0.0.1" ]; then
    local_ip="localhost"
fi

echo "📡 本地访问地址："
echo "   http://$local_ip:8501"
echo ""

# 启动Streamlit应用（后台运行）
echo "启动Streamlit服务..."
streamlit run "$app_file" --server.port 8501 --server.address 0.0.0.0 --theme.base light &
STREAMLIT_PID=$!

# 等待应用启动
echo "等待应用启动..."
sleep 5

# 检查应用是否启动成功
if ! curl -s http://localhost:8501 > /dev/null; then
    echo "❌ Streamlit应用启动失败"
    kill $STREAMLIT_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Streamlit应用启动成功"
echo ""

# 尝试使用ngrok生成公网链接
echo "🌐 生成公网访问链接..."
echo ""

# 方法1：使用ngrok命令行
if command -v ngrok &> /dev/null; then
    echo "使用ngrok生成链接..."
    ngrok http 8501 --log=stdout > ngrok.log &
    NGROK_PID=$!
    
    sleep 3
    
    # 获取ngrok链接
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$NGROK_URL" ]; then
        echo "✅ 公网链接生成成功！"
        echo ""
        echo "========================================"
        echo "🔥 棱镜协议已就绪！"
        echo "========================================"
        echo ""
        echo "📱 公网访问链接："
        echo "   $NGROK_URL"
        echo ""
        echo "💻 本地访问链接："
        echo "   http://$local_ip:8501"
        echo ""
        echo "👥 分享这个链接给朋友："
        echo "   任何人都可以通过浏览器访问"
        echo ""
        echo "📋 快速分享文本："
        echo "   我创建了一个在线思考工具，可以帮你从不同视角看问题。"
        echo "   点击链接立即体验：$NGROK_URL"
        echo ""
        echo "🛑 停止服务：按 Ctrl+C"
        echo "========================================"
        
        # 保存链接到文件
        echo "$NGROK_URL" > prism_share_link.txt
        echo "链接已保存到：prism_share_link.txt"
        
        # 等待用户中断
        wait $NGROK_PID
        
    else
        echo "⚠️ ngrok链接获取失败，尝试备用方案..."
        kill $NGROK_PID 2>/dev/null || true
    fi
fi

# 方法2：使用pyngrok（备用）
if [ -z "$NGROK_URL" ] && python3 -c "import pyngrok" &> /dev/null; then
    echo "使用pyngrok生成链接..."
    
    python3 -c "
import sys
from pyngrok import ngrok

# 启动ngrok隧道
public_url = ngrok.connect(8501, 'http')
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
print(f'   http://$local_ip:8501')
print('')
print('👥 分享这个链接给朋友：')
print('   任何人都可以通过浏览器访问')
print('')
print('📋 快速分享文本：')
print(f'   我创建了一个在线思考工具，可以帮你从不同视角看问题。')
print(f'   点击链接立即体验：{public_url}')
print('')
print('🛑 停止服务：按 Ctrl+C')
print('========================================')

# 保存链接
with open('prism_share_link.txt', 'w') as f:
    f.write(str(public_url))
print('链接已保存到：prism_share_link.txt')

# 保持运行
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\\n停止服务...')
    ngrok.kill()
    "
    
else
    if [ -z "$NGROK_URL" ]; then
        echo "⚠️ 无法生成公网链接，但本地服务已启动"
        echo ""
        echo "========================================"
        echo "🔥 棱镜协议本地服务已启动"
        echo "========================================"
        echo ""
        echo "💻 本地访问链接："
        echo "   http://$local_ip:8501"
        echo ""
        echo "📱 在同一网络下的设备访问："
        echo "   http://$(hostname -I | awk '{print $1}'):8501"
        echo ""
        echo "🌐 要生成公网链接，请："
        echo "   1. 手动安装ngrok：https://ngrok.com/download"
        echo "   2. 运行：ngrok http 8501"
        echo ""
        echo "🛑 停止服务：按 Ctrl+C"
        echo "========================================"
        
        # 等待用户中断
        wait $STREAMLIT_PID
    fi
fi

# 清理
echo "清理进程..."
kill $STREAMLIT_PID 2>/dev/null || true
kill $NGROK_PID 2>/dev/null || true

echo "✅ 服务已停止"
echo ""
echo "🔥 感谢使用棱镜协议！"
echo "   欢迎在GitHub Discussions分享你的体验："
echo "   https://github.com/Ultima0369/prism-interconnect/discussions"