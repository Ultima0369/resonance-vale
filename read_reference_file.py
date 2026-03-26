#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 读取参考资料文件

import os
from pathlib import Path

def read_reference_files():
    """读取参考资料文件夹中的文件"""
    
    ref_dir = Path("D:/LDD/璇玑台/参考资料")
    
    if not ref_dir.exists():
        print(f"错误: 文件夹不存在: {ref_dir}")
        return
    
    print(f"检查文件夹: {ref_dir}")
    
    # 列出所有文件
    files = list(ref_dir.glob("*"))
    print(f"找到 {len(files)} 个文件/文件夹")
    
    for file_path in files:
        print(f"\n文件: {file_path.name}")
        print(f"类型: {'文件夹' if file_path.is_dir() else '文件'}")
        print(f"大小: {file_path.stat().st_size} 字节")
        
        # 如果是 Markdown 文件，读取内容
        if file_path.suffix.lower() == '.md':
            try:
                # 尝试不同编码
                encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'utf-8-sig']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read(1000)  # 读取前1000字符
                        print(f"使用编码 {encoding} 成功读取")
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content:
                    print(f"前200字符: {content[:200]}...")
                    
                    # 提取标题
                    lines = content.split('\n')
                    for line in lines[:10]:
                        if line.startswith('# '):
                            print(f"标题: {line}")
                            break
                else:
                    print("无法读取文件内容")
                    
            except Exception as e:
                print(f"读取文件失败: {e}")
    
    return files

if __name__ == "__main__":
    read_reference_files()