#!/usr/bin/env python3
"""
棱镜协议 PyPI 发布脚本

使用说明:
1. 确保已安装 twine: pip install twine
2. 设置 PyPI 认证 (三选一):
   a) 环境变量:
        export TWINE_USERNAME=__token__
        export TWINE_PASSWORD=pypi-你的令牌
   b) .pypirc 文件: ~/.pypirc
   c) 命令行参数: --username __token__ --password pypi-你的令牌
3. 运行: python release_to_pypi.py

注意: 首次发布建议先测试到 test.pypi.org
"""

import os
import sys
import subprocess
import argparse

def check_prerequisites():
    """检查前置条件"""
    errors = []
    
    # 检查dist目录
    if not os.path.exists("dist"):
        errors.append("dist目录不存在，请先运行: python -m build")
    
    # 检查twine是否安装
    try:
        import twine
    except ImportError:
        errors.append("twine未安装，请运行: pip install twine")
    
    return errors

def get_dist_files():
    """获取dist目录中的发布文件"""
    dist_dir = "dist"
    files = []
    if os.path.exists(dist_dir):
        for f in os.listdir(dist_dir):
            if f.endswith(".tar.gz") or f.endswith(".whl"):
                files.append(os.path.join(dist_dir, f))
    return files

def upload_to_pypi(test=False, username=None, password=None):
    """上传到PyPI"""
    dist_files = get_dist_files()
    
    if not dist_files:
        print("❌ 没有找到发布文件")
        return False
    
    print(f"📦 找到 {len(dist_files)} 个发布文件:")
    for f in dist_files:
        print(f"   - {os.path.basename(f)}")
    
    # 构建twine命令
    repo_url = "https://test.pypi.org/legacy/" if test else "https://upload.pypi.org/legacy/"
    cmd = ["twine", "upload", "--repository-url", repo_url]
    
    # 添加认证信息
    if username:
        cmd.extend(["--username", username])
    if password:
        cmd.extend(["--password", password])
    
    # 添加文件
    cmd.extend(dist_files)
    
    print(f"\n🚀 准备上传到 {'TestPyPI' if test else 'PyPI'}: {repo_url}")
    print(f"📋 命令: {' '.join(cmd[:4])} [用户名] [密码] {len(dist_files)}个文件")
    
    # 询问确认
    if not test:  # 正式发布需要额外确认
        response = input(f"\n⚠️  确认上传到正式 PyPI? (输入 'yes' 继续): ")
        if response.lower() != 'yes':
            print("❌ 发布取消")
            return False
    
    # 执行上传
    try:
        print("\n📤 开始上传...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ 上传成功!")
        print(result.stdout)
        
        if test:
            print("\n🔗 测试安装命令:")
            print(f"   pip install --index-url https://test.pypi.org/simple/ prism-interconnect")
        else:
            print("\n🔗 正式安装命令:")
            print(f"   pip install prism-interconnect")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 上传失败:")
        print(f"   错误代码: {e.returncode}")
        print(f"   标准输出: {e.stdout}")
        print(f"   标准错误: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="棱镜协议 PyPI 发布工具")
    parser.add_argument("--test", action="store_true", help="发布到 TestPyPI")
    parser.add_argument("--username", help="PyPI 用户名 (使用 __token__ 作为用户名)")
    parser.add_argument("--password", help="PyPI 密码/令牌")
    parser.add_argument("--build", action="store_true", help="构建包后再发布")
    
    args = parser.parse_args()
    
    # 检查前置条件
    errors = check_prerequisites()
    if errors:
        print("❌ 前置条件检查失败:")
        for error in errors:
            print(f"   - {error}")
        return 1
    
    # 如果需要，先构建
    if args.build or not os.path.exists("dist"):
        print("🔨 构建包...")
        try:
            subprocess.run([sys.executable, "-m", "build"], check=True)
            print("✅ 构建成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ 构建失败: {e}")
            return 1
    
    # 上传
    success = upload_to_pypi(args.test, args.username, args.password)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())