#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 创建对话索引页面

import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def create_conversation_index(vault_path="D:/LDD/璇玑台"):
    """创建对话索引页面"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("创建对话索引页面...")
    print("=" * 50)
    
    # 查找对话文件夹中的文件
    conversation_dir = vault / "04-对话"
    if not conversation_dir.exists():
        print(f"错误: 对话文件夹不存在: {conversation_dir}")
        return
    
    # 获取所有对话文件
    conversation_files = list(conversation_dir.rglob("*.md"))
    print(f"找到 {len(conversation_files)} 个对话文件")
    
    # 按子分类组织
    conversation_data = defaultdict(list)
    
    for file_path in conversation_files:
        # 获取相对路径
        rel_path = file_path.relative_to(conversation_dir)
        
        # 提取分类信息
        parts = rel_path.parts
        if len(parts) >= 2:
            category = parts[0]  # 璇玑对话/外部对话/会议记录
            subcategory = parts[1] if len(parts) > 2 else "其他"
        else:
            category = "未分类"
            subcategory = "其他"
        
        # 从文件名提取信息
        filename = file_path.name
        
        # 尝试提取日期
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
        if date_match:
            year, month, day = date_match.groups()
            date_str = f"{year}年{month}月{day}日"
        else:
            date_str = "日期未知"
        
        # 尝试提取主题
        theme = filename.replace('.md', '')
        
        conversation_data[category].append({
            'path': file_path.relative_to(vault),
            'filename': filename,
            'theme': theme,
            'date': date_str,
            'category': category,
            'subcategory': subcategory,
            'full_path': str(file_path.relative_to(vault))
        })
    
    print(f"对话分类: {len(conversation_data)} 个")
    
    # 创建对话索引内容
    conversation_content = f"""# 对话索引

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总对话文件**: {len(conversation_files)} 个
**对话分类**: {len(conversation_data)} 类

## 📊 对话统计概览

### 按分类统计
| 分类 | 文件数 | 说明 |
|------|--------|------|
"""
    
    total_files = 0
    for category in sorted(conversation_data.keys()):
        files = conversation_data[category]
        count = len(files)
        total_files += count
        
        # 分类说明
        if category == "璇玑对话":
            description = "与璇玑AI的深度对话和讨论"
        elif category == "外部对话":
            description = "与其他人的对话和交流"
        elif category == "会议记录":
            description = "会议记录和讨论纪要"
        elif category == "思考对话":
            description = "深度思考和自我对话"
        else:
            description = "其他对话记录"
        
        conversation_content += f"| **{category}** | {count} | {description} |\n"
    
    conversation_content += f"| **总计** | **{total_files}** | 所有对话文件 |\n"
    
    # 详细对话列表
    conversation_content += """
## 💬 详细对话列表

"""
    
    for category in sorted(conversation_data.keys()):
        files = conversation_data[category]
        
        conversation_content += f"### {category}\n"
        conversation_content += f"**共 {len(files)} 个对话**\n\n"
        
        # 按日期排序（如果可能）
        dated_files = []
        undated_files = []
        
        for file_info in files:
            if "日期未知" not in file_info['date']:
                dated_files.append(file_info)
            else:
                undated_files.append(file_info)
        
        # 按日期排序（倒序）
        dated_files.sort(key=lambda x: x['date'], reverse=True)
        
        # 显示有日期的文件
        if dated_files:
            conversation_content += "#### 按时间排序\n"
            for file_info in dated_files[:50]:  # 限制显示数量
                file_path = file_info['path']
                filename = file_info['filename']
                date_str = file_info['date']
                theme = file_info['theme'][:50]  # 截断长主题
                
                link_path = str(file_path).replace('\\', '/')
                conversation_content += f"- **{date_str}**: [[{link_path}|{theme}]]\n"
            
            if len(dated_files) > 50:
                conversation_content += f"\n... 还有 {len(dated_files) - 50} 个对话\n"
        
        # 显示无日期的文件
        if undated_files:
            conversation_content += "\n#### 未标注日期\n"
            for file_info in undated_files[:30]:
                file_path = file_info['path']
                filename = file_info['filename']
                theme = file_info['theme'][:50]
                
                link_path = str(file_path).replace('\\', '/')
                conversation_content += f"- [[{link_path}|{theme}]]\n"
            
            if len(undated_files) > 30:
                conversation_content += f"\n... 还有 {len(undated_files) - 30} 个对话\n"
        
        conversation_content += "\n"
    
    # 热门对话主题
    conversation_content += """
## 🔥 热门对话主题

**基于对话文件名的关键词分析**:
"""
    
    # 分析主题关键词
    theme_keywords = defaultdict(int)
    keyword_patterns = [
        r'认知', r'哲学', r'科学', r'AI', r'人工智能', r'思考', r'思维',
        r'对话', r'讨论', r'交流', r'会议', r'访谈', r'咨询',
        r'方法', r'工具', r'技术', r'理论', r'概念', r'实践'
    ]
    
    for file_info in conversation_data.get("璇玑对话", []):
        theme = file_info['theme']
        for pattern in keyword_patterns:
            if re.search(pattern, theme):
                theme_keywords[pattern] += 1
    
    conversation_content += "| 主题关键词 | 出现次数 | 相关对话示例 |\n|------------|----------|--------------|\n"
    
    sorted_keywords = sorted(theme_keywords.items(), key=lambda x: x[1], reverse=True)
    for keyword, count in sorted_keywords[:15]:
        # 找几个示例
        examples = []
        for file_info in conversation_data.get("璇玑对话", []):
            if keyword in file_info['theme'] and len(examples) < 2:
                examples.append(f"[[{file_info['full_path'].replace('\\', '/')}|{file_info['theme'][:30]}...]]")
        
        example_str = "、".join(examples) if examples else "暂无示例"
        conversation_content += f"| **{keyword}** | {count} | {example_str} |\n"
    
    # 对话质量评估
    conversation_content += """
## 📝 对话质量评估指南

### 高质量对话的特征
1. **深度思考**: 涉及核心概念和根本问题
2. **结构清晰**: 有明确的逻辑和层次
3. **实用价值**: 提供可操作的建议或见解
4. **启发性强**: 能引发新的思考和探索
5. **记录完整**: 包含完整的对话过程和结论

### 对话整理建议
1. **添加元数据**: 为每个对话添加日期、参与者、主题标签
2. **提取要点**: 对话后总结关键观点和结论
3. **创建链接**: 将相关对话和概念文件链接起来
4. **定期回顾**: 定期回顾重要对话，更新认知

### 对话标签建议
- `#深度对话` - 深度思考和讨论
- `#实用对话` - 提供具体建议和方案
- `#启发对话` - 启发新思路和视角
- `#技术对话` - 技术讨论和方案
- `#哲学对话` - 哲学思考和探讨

## 🔗 相关索引
- [[主页索引]] - 返回主页面
- [[标签索引]] - 标签分类索引
- [[时间线索引]] - 时间线查看
- [[概念索引]] - 概念定义索引

---

*本页面由璇玑自动生成，最后更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

> 💬 **对话的价值**: 每一次深度对话都是一次认知的碰撞和成长的机会。好的对话记录是宝贵的知识资产。
"""
    
    # 保存对话索引
    conversation_path = vault / "00-索引" / "对话索引.md"
    conversation_path.parent.mkdir(exist_ok=True, parents=True)
    
    with open(conversation_path, 'w', encoding='utf-8') as f:
        f.write(conversation_content)
    
    print(f"对话索引已创建: {conversation_path.relative_to(vault)}")
    
    # 统计信息
    print(f"\n对话统计:")
    for category in sorted(conversation_data.keys()):
        count = len(conversation_data[category])
        print(f"  {category}: {count} 个文件")
    
    return len(conversation_files)

if __name__ == "__main__":
    create_conversation_index()