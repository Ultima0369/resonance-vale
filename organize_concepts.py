#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理概念文件

import re
import shutil
from pathlib import Path

def organize_concept_files(vault_path="D:/LDD/璇玑台"):
    """整理概念文件"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("整理概念文件...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    # 概念关键词
    concept_keywords = [
        '概念', '定义', '术语', '理论', '原理',
        '方法', '技巧', '策略', '框架', '模型',
        '工具', '技术', '算法', '系统', '认知',
        '哲学', '科学', '艺术', '思维', '思考'
    ]
    
    concept_files = []
    moved_count = 0
    
    for file_path in md_files:
        # 跳过新文件夹中的文件
        if any(part.startswith(('00-', '01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '99-')) 
               for part in file_path.parts):
            continue
        
        filename = file_path.name
        
        # 检查是否包含概念关键词
        is_concept = False
        category = "概念"  # 默认分类
        
        for keyword in concept_keywords:
            if keyword in filename:
                is_concept = True
                
                # 判断具体分类
                if '概念' in filename or '定义' in filename or '术语' in filename:
                    category = "概念"
                elif '理论' in filename or '原理' in filename:
                    category = "理论"
                elif '方法' in filename or '技巧' in filename or '策略' in filename:
                    category = "方法"
                elif '工具' in filename or '技术' in filename or '算法' in filename or '系统' in filename:
                    category = "工具"
                elif '认知' in filename or '思维' in filename or '思考' in filename:
                    category = "概念"  # 认知相关归为概念
                
                break
        
        # 如果文件名没有关键词，检查文件内容
        if not is_concept:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2000)  # 读取前2000字符
                
                content_lower = content.lower()
                for keyword in concept_keywords:
                    if keyword in content_lower:
                        is_concept = True
                        
                        # 判断具体分类
                        if '概念' in content_lower or '定义' in content_lower:
                            category = "概念"
                        elif '理论' in content_lower or '原理' in content_lower:
                            category = "理论"
                        elif '方法' in content_lower or '技巧' in content_lower:
                            category = "方法"
                        elif '工具' in content_lower or '技术' in content_lower:
                            category = "工具"
                        
                        break
            except:
                pass
        
        if is_concept:
            concept_files.append({
                'path': file_path,
                'filename': filename,
                'category': category
            })
    
    print(f"找到 {len(concept_files)} 个概念相关文件")
    
    # 整理文件
    for file_info in concept_files:
        file_path = file_info['path']
        filename = file_info['filename']
        category = file_info['category']
        
        # 目标路径
        dest_dir = vault / "03-知识" / category
        dest_dir.mkdir(exist_ok=True, parents=True)
        
        dest_path = dest_dir / filename
        
        try:
            # 移动文件
            shutil.move(str(file_path), str(dest_path))
            moved_count += 1
            print(f"移动: {file_path.name} -> 03-知识/{category}/{filename}")
        except Exception as e:
            print(f"移动失败 {filename}: {e}")
    
    print(f"\n移动了 {moved_count} 个概念文件")
    
    # 统计信息
    if concept_files:
        print("\n按分类统计:")
        categories = {}
        for file_info in concept_files:
            category = file_info['category']
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} 个文件")
    
    return moved_count

if __name__ == "__main__":
    organize_concept_files()