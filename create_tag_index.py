#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 创建标签索引页面

import re
from pathlib import Path
from datetime import datetime

def create_tag_index(vault_path="D:/LDD/璇玑台"):
    """创建标签索引页面"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("创建标签索引页面...")
    print("=" * 50)
    
    # 查找所有 Markdown 文件
    md_files = list(vault.rglob("*.md"))
    print(f"分析 {len(md_files)} 个 Markdown 文件...")
    
    # 收集所有标签
    all_tags = {}
    tag_pattern = r'#([\w\u4e00-\u9fa5\/\-]+)'
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找标签
            tags = re.findall(tag_pattern, content)
            
            for tag in tags:
                # 清理标签
                tag = tag.strip()
                if not tag or len(tag) < 2:
                    continue
                
                # 添加到统计
                if tag not in all_tags:
                    all_tags[tag] = []
                all_tags[tag].append(file_path.relative_to(vault))
                
        except Exception as e:
            print(f"读取文件失败 {file_path.name}: {e}")
    
    print(f"找到 {len(all_tags)} 个唯一标签")
    
    # 按使用频率排序
    sorted_tags = sorted(all_tags.items(), key=lambda x: len(x[1]), reverse=True)
    
    # 创建标签索引内容
    tag_index_content = f"""# 标签索引

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总文件数**: {len(md_files)} 个
**唯一标签数**: {len(all_tags)} 个

## 📊 标签统计概览

### 热门标签（按使用频率）
| 排名 | 标签 | 使用次数 | 相关文件 |
|------|------|----------|----------|
"""
    
    # 添加热门标签表格
    for i, (tag, files) in enumerate(sorted_tags[:50], 1):
        file_count = len(files)
        sample_files = ", ".join([f"[[{f.parent.name}/{f.stem}]]" for f in files[:3]])
        if file_count > 3:
            sample_files += f" ...等{file_count}个文件"
        
        tag_index_content += f"| {i} | `#{tag}` | {file_count} | {sample_files} |\n"
    
    # 按类别组织标签
    tag_index_content += """

## 🏷️ 标签分类体系

### 状态标签
| 标签 | 说明 | 使用次数 |
|------|------|----------|
"""
    
    status_tags = ['进行中', '已完成', '待处理', '归档', '重要', '紧急']
    for tag in status_tags:
        if tag in all_tags:
            tag_index_content += f"| `#{tag}` | 表示任务或内容的状态 | {len(all_tags[tag])} |\n"
        else:
            tag_index_content += f"| `#{tag}` | 表示任务或内容的状态 | 0 |\n"
    
    tag_index_content += """
### 内容类型标签
| 标签 | 说明 | 使用次数 |
|------|------|----------|
"""
    
    content_tags = ['概念', '方法', '工具', '案例', '思考', '笔记', '文章', '研究']
    for tag in content_tags:
        if tag in all_tags:
            tag_index_content += f"| `#{tag}` | 表示内容的类型 | {len(all_tags[tag])} |\n"
        else:
            tag_index_content += f"| `#{tag}` | 表示内容的类型 | 0 |\n"
    
    tag_index_content += """
### 领域标签
| 标签 | 说明 | 使用次数 |
|------|------|----------|
"""
    
    domain_tags = ['哲学', '科学', '技术', '艺术', '生活', '心理学', '认知科学', 'AI']
    for tag in domain_tags:
        if tag in all_tags:
            tag_index_content += f"| `#{tag}` | 表示内容所属领域 | {len(all_tags[tag])} |\n"
        else:
            tag_index_content += f"| `#{tag}` | 表示内容所属领域 | 0 |\n"
    
    tag_index_content += """
### 项目标签
| 标签 | 说明 | 使用次数 |
|------|------|----------|
"""
    
    project_tags = ['璇玑台', '认知切片', 'AI助手', 'OpenClaw', 'Obsidian']
    for tag in project_tags:
        if tag in all_tags:
            tag_index_content += f"| `#{tag}` | 表示相关项目 | {len(all_tags[tag])} |\n"
        else:
            tag_index_content += f"| `#{tag}` | 表示相关项目 | 0 |\n"
    
    tag_index_content += """
### 时间标签
| 标签 | 说明 | 使用次数 |
|------|------|----------|
"""
    
    time_tags = ['2026', '2025', '2026-03', '月度', '周度', '每日']
    for tag in time_tags:
        if tag in all_tags:
            tag_index_content += f"| `#{tag}` | 表示时间相关 | {len(all_tags[tag])} |\n"
        else:
            tag_index_content += f"| `#{tag}` | 表示时间相关 | 0 |\n"
    
    # 完整的标签列表
    tag_index_content += f"""
## 📋 完整标签列表（按字母顺序）

共 {len(all_tags)} 个标签：

"""
    
    # 按字母顺序排序
    alphabetical_tags = sorted(all_tags.keys())
    
    # 分组显示
    cols = 4
    rows = (len(alphabetical_tags) + cols - 1) // cols
    
    for i in range(rows):
        row_tags = []
        for j in range(cols):
            idx = i + j * rows
            if idx < len(alphabetical_tags):
                tag = alphabetical_tags[idx]
                count = len(all_tags[tag])
                row_tags.append(f"`#{tag}` ({count})")
        
        tag_index_content += "| " + " | ".join(row_tags) + " |\n"
    
    # 使用建议
    tag_index_content += """
## 💡 标签使用建议

### 1. 标签命名规范
- **简洁明确**: 使用2-4个字的标签
- **避免重复**: 相同概念使用相同标签
- **层级标签**: 使用 `/` 创建层级，如 `#项目/璇玑台`
- **英文标签**: 尽量使用中文，如需英文保持统一

### 2. 标签数量建议
- **每个笔记3-5个标签**: 不要过多
- **核心标签优先**: 先添加最相关的1-2个核心标签
- **补充标签**: 根据需要添加领域、状态、时间等补充标签

### 3. 标签维护
- **定期清理**: 每月检查并清理不再使用的标签
- **合并相似标签**: 将相似标签合并为统一标签
- **建立标签文档**: 重要标签可在本页面添加详细说明

### 4. 搜索技巧
- **搜索单个标签**: `tag:#概念`
- **搜索多个标签**: `tag:#概念 AND tag:#哲学`
- **排除标签**: `-tag:#归档`
- **层级标签搜索**: `tag:#项目/*`

## 🔗 相关索引
- [[主页索引]] - 返回主页面
- [[时间线索引]] - 按时间查看内容
- [[对话索引]] - 对话记录索引
- [[概念索引]] - 概念定义索引

---

*本页面由璇玑自动生成，最后更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存标签索引
    tag_index_path = vault / "00-索引" / "标签索引.md"
    tag_index_path.parent.mkdir(exist_ok=True, parents=True)
    
    with open(tag_index_path, 'w', encoding='utf-8') as f:
        f.write(tag_index_content)
    
    print(f"标签索引已创建: {tag_index_path.relative_to(vault)}")
    
    # 统计信息
    print(f"\n标签统计:")
    print(f"  热门标签:")
    for i, (tag, files) in enumerate(sorted_tags[:10], 1):
        print(f"    {i}. #{tag}: {len(files)} 个文件")
    
    return len(all_tags)

if __name__ == "__main__":
    create_tag_index()