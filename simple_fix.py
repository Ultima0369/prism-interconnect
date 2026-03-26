#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单修复文件编码脚本
"""

import os
import sys
import glob

def fix_file_encoding(file_path):
    """修复单个文件的编码"""
    print(f"处理: {file_path}")
    
    try:
        # 尝试以二进制读取
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        # 尝试常见编码
        encodings_to_try = [
            'utf-8',
            'utf-8-sig',  # UTF-8 with BOM
            'gbk',
            'gb2312',
            'gb18030',
            'big5',
            'latin1',
            'cp1252'  # Windows Western
        ]
        
        content = None
        used_encoding = None
        
        for enc in encodings_to_try:
            try:
                content = raw_data.decode(enc)
                # 检查是否包含合理的中文字符
                if any('\u4e00' <= char <= '\u9fff' for char in content[:1000]):
                    used_encoding = enc
                    print(f"  使用编码: {enc} (包含中文)")
                    break
                elif enc == 'utf-8':  # 如果没有中文，至少用UTF-8
                    used_encoding = enc
                    print(f"  使用编码: {enc} (无中文)")
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            # 如果都失败，使用utf-8忽略错误
            content = raw_data.decode('utf-8', errors='ignore')
            used_encoding = 'utf-8 (忽略错误)'
            print(f"  使用编码: {used_encoding}")
        
        # 写入UTF-8 with BOM（确保GitHub正确显示）
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        print(f"  修复成功 ({used_encoding} -> utf-8-sig)")
        return True
        
    except Exception as e:
        print(f"  修复失败: {e}")
        return False

def main():
    print("开始修复文件编码...")
    
    # 关键文件优先修复
    key_files = [
        "README.md",
        "MANIFESTO.md",
        "docs/philosophy.md",
        "docs/two-equations-charter.md",
        "docs/compression-history.md",
        "docs/natural-law-1plus1.md",
        "docs/nature-paradox.md",
        "docs/existence-emergence.md",
        "docs/silicon-carbon-ethics.md",
        "docs/visual-materials-guide.md",
        "docs/philosophy-deep-breakthroughs.md"
    ]
    
    # 其他markdown文件
    other_md_files = glob.glob("*.md") + glob.glob("docs/*.md")
    
    # 合并并去重
    all_files = []
    for f in key_files + other_md_files:
        if os.path.exists(f) and f not in all_files:
            all_files.append(f)
    
    print(f"找到 {len(all_files)} 个文件需要检查")
    
    fixed_count = 0
    for file_path in sorted(all_files):
        # 跳过备份文件
        if file_path.endswith('.backup') or file_path.endswith('.bak'):
            continue
            
        if fix_file_encoding(file_path):
            fixed_count += 1
        print()
    
    print(f"完成！修复了 {fixed_count} 个文件")
    
    # 验证关键文件
    print("\n验证关键文件:")
    for key_file in key_files[:5]:  # 只检查前5个
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r', encoding='utf-8-sig') as f:
                    content = f.read(300)
                
                # 显示预览
                preview = content[:100].replace('\n', ' ').strip()
                print(f"  {key_file}:")
                print(f"    预览: {preview}...")
                print()
                
            except Exception as e:
                print(f"  {key_file}: 读取失败 - {e}")

if __name__ == "__main__":
    main()