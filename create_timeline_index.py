#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 创建时间线索引页面

import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def create_timeline_index(vault_path="D:/LDD/璇玑台"):
    """创建时间线索引页面"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("创建时间线索引页面...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"分析 {len(md_files)} 个 Markdown 文件...")
    
    # 按时间组织文件
    timeline_data = defaultdict(list)
    date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    
    for file_path in md_files:
        filename = file_path.name
        
        # 从文件名提取日期
        match = re.search(date_pattern, filename)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            
            timeline_data[f"{year}-{month}"].append({
                'path': file_path.relative_to(vault),
                'filename': filename,
                'year': year,
                'month': month,
                'day': day,
                'full_date': f"{year}-{month}-{day}"
            })
        
        # 从文件内容提取创建/修改时间（如果存在）
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)  # 读取前5000字符
                
                # 查找常见的时间标记
                time_markers = [
                    r'创建时间[:：]\s*(\d{4}[-/]\d{2}[-/]\d{2})',
                    r'更新时间[:：]\s*(\d{4}[-/]\d{2}[-/]\d{2})',
                    r'日期[:：]\s*(\d{4}[-/]\d{2}[-/]\d{2})',
                    r'(\d{4}年\d{1,2}月\d{1,2}日)',
                ]
                
                found_date = None
                for pattern in time_markers:
                    match = re.search(pattern, content)
                    if match:
                        found_date = match.group(1)
                        # 标准化日期格式
                        found_date = re.sub(r'[年月日]', '-', found_date)
                        found_date = re.sub(r'[-/]+', '-', found_date)
                        
                        # 提取年月
                        date_match = re.search(r'(\d{4})-(\d{1,2})', found_date)
                        if date_match:
                            year = date_match.group(1)
                            month = date_match.group(2).zfill(2)
                            timeline_data[f"{year}-{month}"].append({
                                'path': file_path.relative_to(vault),
                                'filename': filename,
                                'year': year,
                                'month': month,
                                'day': '??',
                                'full_date': found_date,
                                'source': 'content'
                            })
                        break
                
                # 如果没有找到日期，使用文件修改时间
                if not found_date:
                    mtime = file_path.stat().st_mtime
                    dt = datetime.fromtimestamp(mtime)
                    year = dt.strftime('%Y')
                    month = dt.strftime('%m')
                    timeline_data[f"{year}-{month}"].append({
                        'path': file_path.relative_to(vault),
                        'filename': filename,
                        'year': year,
                        'month': month,
                        'day': dt.strftime('%d'),
                        'full_date': dt.strftime('%Y-%m-%d'),
                        'source': 'mtime'
                    })
                    
            except Exception as e:
                print(f"处理文件失败 {filename}: {e}")
    
    print(f"按时间组织了 {len(timeline_data)} 个月份的数据")
    
    # 创建时间线索引内容
    timeline_content = f"""# 时间线索引

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总文件数**: {len(md_files)} 个
**覆盖月份**: {len(timeline_data)} 个月

## 📅 时间线概览

### 按年份统计
"""
    
    # 按年份统计
    year_stats = defaultdict(int)
    for month_key in timeline_data.keys():
        year = month_key.split('-')[0]
        year_stats[year] += len(timeline_data[month_key])
    
    timeline_content += "| 年份 | 文件数 | 月份数 |\n|------|--------|--------|\n"
    for year in sorted(year_stats.keys(), reverse=True):
        year_months = [m for m in timeline_data.keys() if m.startswith(year)]
        timeline_content += f"| **{year}年** | {year_stats[year]} | {len(year_months)} |\n"
    
    # 详细时间线
    timeline_content += """
## 🗓️ 详细时间线（按时间倒序）

"""
    
    # 按时间倒序排列月份
    sorted_months = sorted(timeline_data.keys(), key=lambda x: x, reverse=True)
    
    for month_key in sorted_months:
        year, month = month_key.split('-')
        files = timeline_data[month_key]
        
        # 按日期排序
        sorted_files = sorted(files, key=lambda x: x.get('day', '00'), reverse=True)
        
        timeline_content += f"### {year}年{month}月\n"
        timeline_content += f"**文件数**: {len(files)} 个\n\n"
        
        # 按日期分组
        day_groups = defaultdict(list)
        for file_info in sorted_files:
            day = file_info.get('day', '??')
            day_groups[day].append(file_info)
        
        for day in sorted(day_groups.keys(), reverse=True):
            day_files = day_groups[day]
            
            if day == '??':
                timeline_content += f"#### 日期未知\n"
            else:
                timeline_content += f"#### {year}年{month}月{day}日\n"
            
            for file_info in day_files:
                file_path = file_info['path']
                filename = file_info['filename']
                
                # 创建链接
                link_path = str(file_path).replace('\\', '/')
                timeline_content += f"- [[{link_path}|{filename}]]"
                
                # 添加来源标记
                source = file_info.get('source', 'filename')
                if source != 'filename':
                    timeline_content += f" *({source})*"
                
                timeline_content += "\n"
        
        timeline_content += "\n"
    
    # 最近更新
    timeline_content += """
## 🔄 最近更新

**最近30天活跃的文件**（按修改时间）:
"""
    
    # 获取最近30天修改的文件
    recent_files = []
    for file_path in md_files:
        try:
            mtime = file_path.stat().st_mtime
            dt = datetime.fromtimestamp(mtime)
            days_ago = (datetime.now() - dt).days
            
            if days_ago <= 30:
                recent_files.append({
                    'path': file_path.relative_to(vault),
                    'filename': file_path.name,
                    'mtime': dt,
                    'days_ago': days_ago
                })
        except:
            pass
    
    # 按修改时间排序
    recent_files.sort(key=lambda x: x['mtime'], reverse=True)
    
    timeline_content += "| 文件 | 最后修改 | 天数前 |\n|------|----------|--------|\n"
    for file_info in recent_files[:20]:
        file_path = file_info['path']
        filename = file_info['filename']
        mtime_str = file_info['mtime'].strftime('%Y-%m-%d %H:%M')
        days_ago = file_info['days_ago']
        
        link_path = str(file_path).replace('\\', '/')
        timeline_content += f"| [[{link_path}|{filename}]] | {mtime_str} | {days_ago}天前 |\n"
    
    # 时间线可视化建议
    timeline_content += """
## 📈 时间线可视化建议

### 1. Obsidian 时间线插件
- **Timelines**: 创建交互式时间线
- **Calendar**: 日历视图查看每日笔记
- **Daily Notes**: 自动创建每日笔记

### 2. 时间标签体系
建议使用以下时间标签：
- `#2026` - 2026年的内容
- `#2026-03` - 2026年3月的内容
- `#月度` - 月度总结
- `#周度` - 周度记录
- `#每日` - 每日记录

### 3. 定期回顾
- **每日回顾**: 查看当天的笔记
- **每周回顾**: 查看本周的进展
- **每月回顾**: 查看本月的成果
- **年度回顾**: 查看全年的成长

## 🔗 相关索引
- [[主页索引]] - 返回主页面
- [[标签索引]] - 标签分类索引
- [[对话索引]] - 对话记录索引
- [[概念索引]] - 概念定义索引

---

*本页面由璇玑自动生成，最后更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

> 💡 **提示**: 时间是最好的组织者。通过时间线，你可以看到思想的演进和成长的轨迹。
"""
    
    # 保存时间线索引
    timeline_path = vault / "00-索引" / "时间线索引.md"
    timeline_path.parent.mkdir(exist_ok=True, parents=True)
    
    with open(timeline_path, 'w', encoding='utf-8') as f:
        f.write(timeline_content)
    
    print(f"时间线索引已创建: {timeline_path.relative_to(vault)}")
    
    # 统计信息
    print(f"\n时间线统计:")
    print(f"  覆盖年份: {len(year_stats)} 年")
    print(f"  覆盖月份: {len(timeline_data)} 个月")
    print(f"  最近30天活跃文件: {len(recent_files)} 个")
    
    return len(timeline_data)

if __name__ == "__main__":
    create_timeline_index()