#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 读取完整文件内容

from pathlib import Path

def read_full_content():
    """读取完整文件内容"""
    
    file_path = Path("D:/LDD/璇玑台/参考资料/ǿ�߼�����̽��.md")
    
    if not file_path.exists():
        print(f"错误: 文件不存在: {file_path}")
        return
    
    print(f"读取文件: {file_path}")
    print(f"文件大小: {file_path.stat().st_size} 字节")
    print("=" * 80)
    
    try:
        # 使用 UTF-8 编码读取
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 显示文件结构
        lines = content.split('\n')
        print(f"总行数: {len(lines)}")
        
        # 提取标题和章节
        print("\n📖 文件结构:")
        for i, line in enumerate(lines[:100]):  # 检查前100行
            if line.startswith('# '):
                print(f"  主标题: {line}")
            elif line.startswith('## '):
                print(f"  章节: {line}")
            elif line.startswith('### '):
                print(f"    子节: {line}")
        
        # 显示前2000字符的内容概览
        print(f"\n📝 内容概览 (前2000字符):")
        print("=" * 80)
        print(content[:2000])
        print("=" * 80)
        
        # 统计关键词
        keywords = ['认知', '逻辑', '思维', 'AI', '智能体', '璇玑', '星尘', '对话', '思考']
        print(f"\n🔍 关键词出现次数:")
        for keyword in keywords:
            count = content.count(keyword)
            if count > 0:
                print(f"  {keyword}: {count} 次")
        
        return content
        
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None

if __name__ == "__main__":
    read_full_content()