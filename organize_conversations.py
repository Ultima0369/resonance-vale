#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理对话文件

import re
import shutil
from pathlib import Path

def organize_conversation_files(vault_path="D:/LDD/璇玑台"):
    """整理对话文件"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("整理对话文件...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    # 对话关键词
    conversation_keywords = [
        '对话', '聊天', '讨论', '交流', '访谈',
        '会议', '对谈', '问答', '咨询', '璇玑',
        '星尘', 'AI', '助手', 'GPT', 'Claude',
        'DeepSeek', '对话记录', '聊天记录'
    ]
    
    conversation_files = []
    moved_count = 0
    
    for file_path in md_files:
        # 跳过新文件夹中的文件
        if any(part.startswith(('00-', '01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '99-')) 
               for part in file_path.parts):
            continue
        
        filename = file_path.name
        
        # 检查是否包含对话关键词
        is_conversation = False
        category = "外部对话"  # 默认分类
        
        for keyword in conversation_keywords:
            if keyword in filename:
                is_conversation = True
                
                # 判断具体分类
                if '璇玑' in filename or 'AI' in filename or '助手' in filename or 'GPT' in filename or 'Claude' in filename or 'DeepSeek' in filename:
                    category = "璇玑对话"
                elif '会议' in filename:
                    category = "会议记录"
                
                break
        
        # 如果文件名没有关键词，检查文件内容
        if not is_conversation:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2000)  # 读取前2000字符
                
                content_lower = content.lower()
                for keyword in conversation_keywords:
                    if keyword in content_lower:
                        is_conversation = True
                        
                        # 判断具体分类
                        if '璇玑' in content_lower or 'ai' in content_lower or '助手' in content_lower:
                            category = "璇玑对话"
                        elif '会议' in content_lower:
                            category = "会议记录"
                        
                        break
            except:
                pass
        
        if is_conversation:
            conversation_files.append({
                'path': file_path,
                'filename': filename,
                'category': category
            })
    
    print(f"找到 {len(conversation_files)} 个对话相关文件")
    
    # 整理文件
    for file_info in conversation_files:
        file_path = file_info['path']
        filename = file_info['filename']
        category = file_info['category']
        
        # 目标路径
        dest_dir = vault / "04-对话" / category
        dest_dir.mkdir(exist_ok=True, parents=True)
        
        dest_path = dest_dir / filename
        
        try:
            # 移动文件
            shutil.move(str(file_path), str(dest_path))
            moved_count += 1
            print(f"移动: {file_path.relative_to(vault)} -> {dest_path.relative_to(vault)} ({category})")
        except Exception as e:
            print(f"移动失败 {filename}: {e}")
    
    print(f"\n移动了 {moved_count} 个对话文件")
    
    # 统计信息
    if conversation_files:
        print("\n按分类统计:")
        categories = {}
        for file_info in conversation_files:
            category = file_info['category']
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} 个文件")
    
    return moved_count

if __name__ == "__main__":
    organize_conversation_files()