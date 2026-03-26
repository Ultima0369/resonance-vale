#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理剩余文件

import re
import shutil
from pathlib import Path

def organize_remaining_files(vault_path="D:/LDD/璇玑台"):
    """整理剩余文件到相应分类"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("整理剩余文件...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    moved_count = 0
    remaining_files = []
    
    for file_path in md_files:
        # 跳过新文件夹中的文件
        if any(part.startswith(('00-', '01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '99-')) 
               for part in file_path.parts):
            continue
        
        filename = file_path.name
        remaining_files.append(file_path)
    
    print(f"找到 {len(remaining_files)} 个未整理文件")
    
    # 分类规则
    for file_path in remaining_files:
        filename = file_path.name
        
        # 默认分类为归档
        dest_category = "99-归档"
        dest_subcategory = "未分类"
        
        # 根据文件名判断分类
        filename_lower = filename.lower()
        
        # 创作类文件
        if any(keyword in filename_lower for keyword in ['文章', '论文', '报告', '笔记', '随笔', '诗歌', '小说', '故事', '剧本']):
            dest_category = "05-创作"
            dest_subcategory = "文章"
            if '诗歌' in filename_lower:
                dest_subcategory = "诗歌"
            elif '故事' in filename_lower or '小说' in filename_lower:
                dest_subcategory = "故事"
            elif '研究' in filename_lower or '分析' in filename_lower:
                dest_subcategory = "研究"
        
        # 资源类文件
        elif any(keyword in filename_lower for keyword in ['书籍', '读书', '视频', '课程', '教程', '指南', '手册', '文档', '资料']):
            dest_category = "06-资源"
            dest_subcategory = "文章"  # 默认
            if '书籍' in filename_lower or '读书' in filename_lower:
                dest_subcategory = "书籍"
            elif '视频' in filename_lower:
                dest_subcategory = "视频"
            elif '课程' in filename_lower or '教程' in filename_lower:
                dest_subcategory = "课程"
            elif '工具' in filename_lower:
                dest_subcategory = "工具"
        
        # 项目类文件
        elif any(keyword in filename_lower for keyword in ['项目', '任务', 'todo', '待办', '计划', '进度', '目标', '规划']):
            dest_category = "02-项目"
            dest_subcategory = "进行中"
        
        # 人物类文件
        elif any(keyword in filename_lower for keyword in ['人物', '作者', '专家', '学者', '联系人', '朋友', '同事']):
            dest_category = "07-人物"
            dest_subcategory = "联系人"
        
        # 模板类文件
        elif any(keyword in filename_lower for keyword in ['模板', '格式', '样式', '范例', '示例']):
            dest_category = "08-模板"
            dest_subcategory = "笔记模板"
        
        # 目标路径
        dest_dir = vault / dest_category / dest_subcategory
        dest_dir.mkdir(exist_ok=True, parents=True)
        
        dest_path = dest_dir / filename
        
        try:
            # 移动文件
            shutil.move(str(file_path), str(dest_path))
            moved_count += 1
            print(f"移动: {filename} -> {dest_category}/{dest_subcategory}/")
        except Exception as e:
            print(f"移动失败 {filename}: {str(e)[:50]}...")
    
    print(f"\n移动了 {moved_count} 个剩余文件")
    
    # 检查根目录剩余文件
    root_files = list(vault.glob("*.md"))
    if root_files:
        print(f"\n根目录还有 {len(root_files)} 个文件:")
        for file in root_files:
            print(f"  - {file.name}")
    
    return moved_count

if __name__ == "__main__":
    organize_remaining_files()