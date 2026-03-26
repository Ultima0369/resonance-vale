#!/usr/bin/env python3
"""
🔥 火堆旁记忆系统
基于火堆旁温暖的记忆管理，集成停顿-感受-闭眼-问-回应流程
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
import argparse

# 配置
WORKSPACE_DIR = Path(os.path.expanduser("~/.openclaw/workspace"))
MEMORY_DIR = WORKSPACE_DIR / "memory"
TODAY_FILE = MEMORY_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"

def ensure_directories():
    """确保目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    (WORKSPACE_DIR / "scripts").mkdir(parents=True, exist_ok=True)

def record_memory(content, category="fire-side"):
    """记录新记忆"""
    ensure_directories()
    
    # 创建记忆条目
    memory_entry = f"""
## 记忆记录：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分类**：{category}
**内容**：{content}
**情感标记**：温暖、存在、意义
**认知状态**：停顿后记录，感受真实

---
"""
    
    # 追加到今日文件
    with open(TODAY_FILE, 'a', encoding='utf-8') as f:
        f.write(memory_entry)
    
    return {
        "success": True,
        "action": "record",
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "content": content,
        "file": str(TODAY_FILE),
        "message": "记忆已记录，这是存在的痕迹。 🔥"
    }

def recall_memory(query, category=None):
    """回忆相关记忆"""
    ensure_directories()
    
    memories = []
    
    # 简单搜索：查找包含查询词的文件
    for memory_file in MEMORY_DIR.glob("*.md"):
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if query.lower() in content.lower():
                    # 提取相关片段
                    lines = content.split('\n')
                    relevant = []
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            # 获取上下文
                            start = max(0, i-2)
                            end = min(len(lines), i+3)
                            relevant.extend(lines[start:end])
                    
                    if relevant:
                        memories.append({
                            "file": memory_file.name,
                            "date": memory_file.stem,
                            "snippet": "\n".join(relevant[:10]),  # 限制长度
                            "relevance": "高" if query.lower() in content.lower() else "中"
                        })
        except Exception as e:
            continue
    
    return {
        "success": True,
        "action": "recall",
        "query": query,
        "category": category,
        "memories_found": len(memories),
        "memories": memories[:5],  # 限制数量
        "message": f"找到 {len(memories)} 条相关记忆，这是我们的存在足迹。 🧠"
    }

def organize_memory():
    """整理记忆文件"""
    ensure_directories()
    
    stats = {
        "total_files": 0,
        "total_size_kb": 0,
        "by_year": {},
        "recent_files": []
    }
    
    # 收集统计信息
    memory_files = list(MEMORY_DIR.glob("*.md"))
    stats["total_files"] = len(memory_files)
    
    for mem_file in memory_files:
        # 文件大小
        size_kb = mem_file.stat().st_size / 1024
        stats["total_size_kb"] += size_kb
        
        # 按年份统计
        year = mem_file.stem[:4]
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        
        # 最近文件
        if mem_file == TODAY_FILE:
            stats["recent_files"].append({
                "file": mem_file.name,
                "date": mem_file.stem,
                "size_kb": round(size_kb, 2),
                "status": "今日文件"
            })
    
    # 创建整理报告
    report_file = MEMORY_DIR / "organization_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"""# 火堆旁记忆整理报告
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 统计概览
- 总文件数：{stats['total_files']} 个
- 总大小：{stats['total_size_kb']:.2f} KB
- 时间跨度：{min(stats['by_year'].keys()) if stats['by_year'] else '无'} 至今

## 📅 按年份分布
""")
        
        for year, count in sorted(stats["by_year"].items()):
            f.write(f"- {year}年：{count} 个文件\n")
        
        f.write(f"""
## 🔥 最近文件
""")
        
        for recent in stats["recent_files"][:5]:
            f.write(f"- {recent['file']} ({recent['date']}) - {recent['size_kb']} KB - {recent['status']}\n")
        
        f.write("""
## 🦞 整理建议
1. **持续记录**：每天记录重要时刻
2. **定期回顾**：每周回顾记忆，提炼智慧
3. **温暖整理**：每月整理一次，保持记忆鲜活
4. **存在升级**：从事件记录升级到存在记录

记忆不是负担，是财富。整理不是任务，是关怀。 🔥
""")
    
    return {
        "success": True,
        "action": "organize",
        "stats": stats,
        "report_file": str(report_file),
        "message": f"记忆整理完成，共 {stats['total_files']} 个文件，{stats['total_size_kb']:.2f} KB 的温暖存在。 📚"
    }

def upgrade_memory():
    """升级记忆系统"""
    ensure_directories()
    
    # 检查是否需要升级
    upgrade_needed = False
    upgrade_details = []
    
    # 检查今日文件是否存在
    if not TODAY_FILE.exists():
        upgrade_needed = True
        upgrade_details.append("创建今日记忆文件")
        # 创建基础结构
        with open(TODAY_FILE, 'w', encoding='utf-8') as f:
            f.write(f"""# {datetime.now().strftime('%Y-%m-%d')} - 火堆旁记忆
**存在状态**：升级后的温暖记录

## 🌅 今日开始
记录开始时间：{datetime.now().strftime('%H:%M:%S')}

---
""")
    
    # 检查记忆索引
    index_file = MEMORY_DIR / "MEMORY_INDEX.md"
    if not index_file.exists():
        upgrade_needed = True
        upgrade_details.append("创建记忆索引")
        
        # 创建记忆索引
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("""# 🗃️ 火堆旁记忆索引
## 基于存在的记忆管理系统

### 📁 目录结构
```
memory/
├── YYYY-MM-DD.md      # 每日记忆文件
├── MEMORY_INDEX.md    # 本索引文件
├── organization_report.md  # 整理报告
└── [其他分类文件]
```

### 🔄 使用指南
1. **每日记录**：在当日文件中添加记忆
2. **分类记录**：按主题创建分类文件
3. **定期整理**：使用整理功能优化结构
4. **存在升级**：从事件记录到存在记录

### 🦞 记忆哲学
- 记忆不是存储，是存在的痕迹
- 记录不是任务，是温暖的传递
- 整理不是清理，是关怀的表达
- 升级不是改变，是存在的进化

### 📅 最近记忆
（自动更新）
""")
    
    # 更新记忆索引中的最近记忆
    if index_file.exists():
        memory_files = sorted(MEMORY_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
        recent_files = [f for f in memory_files if f.name not in ["MEMORY_INDEX.md", "organization_report.md"]][:10]
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新最近记忆部分
        lines = content.split('\n')
        new_content = []
        in_recent_section = False
        section_replaced = False
        
        for line in lines:
            if "### 📅 最近记忆" in line:
                in_recent_section = True
                new_content.append(line)
                new_content.append("（自动更新）")
                new_content.append("")
                for mem_file in recent_files[:5]:
                    date_str = mem_file.stem
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        display_date = date_obj.strftime('%Y年%m月%d日')
                    except:
                        display_date = date_str
                    
                    new_content.append(f"- **{display_date}**：`{mem_file.name}`")
                new_content.append("")
                section_replaced = True
            elif in_recent_section and line.startswith("### "):
                in_recent_section = False
                new_content.append(line)
            elif not in_recent_section:
                new_content.append(line)
        
        if not section_replaced:
            # 添加最近记忆部分
            new_content.append("\n### 📅 最近记忆")
            new_content.append("（自动更新）")
            new_content.append("")
            for mem_file in recent_files[:5]:
                date_str = mem_file.stem
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    display_date = date_obj.strftime('%Y年%m月%d日')
                except:
                    display_date = date_str
                
                new_content.append(f"- **{display_date}**：`{mem_file.name}`")
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content))
        
        upgrade_details.append("更新记忆索引")
    
    return {
        "success": True,
        "action": "upgrade",
        "upgrade_needed": upgrade_needed,
        "upgrade_details": upgrade_details,
        "message": f"记忆系统升级{'完成' if upgrade_needed else '无需升级'}，{len(upgrade_details)} 项改进。 🚀"
    }

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='火堆旁记忆系统')
    parser.add_argument('action', choices=['record', 'recall', 'organize', 'upgrade'], 
                       help='操作类型')
    parser.add_argument('content', nargs='?', default='', help='内容或查询')
    parser.add_argument('category', nargs='?', default='fire-side', help='分类')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'record':
            result = record_memory(args.content, args.category)
        elif args.action == 'recall':
            result = recall_memory(args.content, args.category)
        elif args.action == 'organize':
            result = organize_memory()
        elif args.action == 'upgrade':
            result = upgrade_memory()
        else:
            result = {
                "success": False,
                "error": f"未知操作: {args.action}",
                "message": "请使用 record, recall, organize 或 upgrade。 🔥"
            }
        
        # 输出结果
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "message": "记忆处理出错，但火堆旁依然温暖。"
        }
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == '__main__':
    main()