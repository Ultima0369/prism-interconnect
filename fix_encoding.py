#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文件编码脚本
将文件转换为UTF-8编码
"""

import os
import sys
import glob
import chardet

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    result = chardet.detect(raw_data)
    return result['encoding'], result['confidence']

def convert_to_utf8(file_path, source_encoding=None):
    """将文件转换为UTF-8"""
    try:
        # 读取文件
        if source_encoding:
            with open(file_path, 'r', encoding=source_encoding, errors='ignore') as f:
                content = f.read()
        else:
            # 尝试自动检测
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            # 尝试常见编码
            encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin1']
            
            for enc in encodings_to_try:
                try:
                    content = raw_data.decode(enc)
                    print(f"  使用编码: {enc}")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                # 如果都失败，使用chardet检测
                detected_enc, confidence = detect_encoding(file_path)
                if confidence > 0.7:
                    content = raw_data.decode(detected_enc, errors='ignore')
                    print(f"  使用检测编码: {detected_enc} (置信度: {confidence:.2f})")
                else:
                    # 最后尝试utf-8 with errors ignore
                    content = raw_data.decode('utf-8', errors='ignore')
                    print(f"  使用UTF-8 (忽略错误)")
        
        # 写入UTF-8 with BOM（确保GitHub正确显示）
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  转换失败: {e}")
        return False

def main():
    print("🔧 开始修复文件编码...")
    
    # 需要修复的文件模式
    file_patterns = [
        "*.md",
        "docs/*.md",
        "*.txt",
        "*.py",
        "*.json",
        "*.yaml",
        "*.yml"
    ]
    
    all_files = []
    for pattern in file_patterns:
        all_files.extend(glob.glob(pattern, recursive=True))
    
    # 去重
    all_files = list(set(all_files))
    
    print(f"找到 {len(all_files)} 个文件需要检查")
    
    fixed_count = 0
    for file_path in sorted(all_files):
        # 跳过一些不需要修复的文件
        if any(skip in file_path for skip in ['.git', 'node_modules', '__pycache__']):
            continue
            
        print(f"处理: {file_path}")
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print("  跳过空文件")
            continue
        
        # 检测当前编码
        try:
            detected_enc, confidence = detect_encoding(file_path)
            print(f"  检测编码: {detected_enc} (置信度: {confidence:.2f})")
            
            # 如果已经是UTF-8且置信度高，跳过
            if detected_enc.lower() in ['utf-8', 'utf-8-sig'] and confidence > 0.9:
                print("  已经是UTF-8，跳过")
                continue
                
            # 转换文件
            if convert_to_utf8(file_path, detected_enc):
                fixed_count += 1
                print("  ✓ 修复成功")
            else:
                print("  ✗ 修复失败")
                
        except Exception as e:
            print(f"  处理失败: {e}")
        
        print()
    
    print(f"✅ 完成！修复了 {fixed_count} 个文件")
    
    # 特别检查README.md
    print("\n📋 特别检查关键文件:")
    key_files = ["README.md", "MANIFESTO.md", "docs/philosophy.md", "docs/two-equations-charter.md"]
    
    for key_file in key_files:
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r', encoding='utf-8') as f:
                    content = f.read(500)  # 只读前500字符
                
                # 检查是否包含中文
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in content)
                status = "✓ 正常" if has_chinese else "⚠ 可能有问题"
                
                print(f"  {key_file}: {status}")
                if has_chinese:
                    # 显示前100字符
                    preview = content[:100].replace('\n', ' ')
                    print(f"    预览: {preview}...")
                    
            except Exception as e:
                print(f"  {key_file}: ✗ 读取失败 - {e}")

if __name__ == "__main__":
    main()