#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理日期格式文件

import re
import shutil
from pathlib import Path
from datetime import datetime

def organize_date_files(vault_path="D:/LDD/璇玑台"):
    """整理日期格式文件"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("整理日期格式文件...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    # 日期模式
    date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    
    date_files = []
    moved_count = 0
    
    for file_path in md_files:
        # 跳过新文件夹中的文件
        if any(part.startswith(('00-', '01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '99-')) 
               for part in file_path.parts):
            continue
        
        filename = file_path.name
        
        # 查找日期
        match = re.search(date_pattern, filename)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            
            date_files.append({
                'path': file_path,
                'filename': filename,
                'year': year,
                'month': month,
                'day': day
            })
    
    print(f"找到 {len(date_files)} 个日期格式文件")
    
    # 整理文件
    for file_info in date_files:
        file_path = file_info['path']
        filename = file_info['filename']
        year = file_info['year']
        month = file_info['month']
        
        # 目标路径
        dest_dir = vault / "01-日记" / "每日记录" / f"{year}-{month}"
        dest_dir.mkdir(exist_ok=True, parents=True)
        
        dest_path = dest_dir / filename
        
        try:
            # 移动文件
            shutil.move(str(file_path), str(dest_path))
            moved_count += 1
            print(f"移动: {file_path.relative_to(vault)} -> {dest_path.relative_to(vault)}")
        except Exception as e:
            print(f"移动失败 {filename}: {e}")
    
    print(f"\n移动了 {moved_count} 个日期格式文件")
    
    # 统计信息
    if date_files:
        print("\n按年份统计:")
        years = {}
        for file_info in date_files:
            year = file_info['year']
            years[year] = years.get(year, 0) + 1
        
        for year, count in sorted(years.items()):
            print(f"  {year}年: {count} 个文件")
    
    return moved_count

if __name__ == "__main__":
    organize_date_files()