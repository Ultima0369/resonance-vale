#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 创建概念索引页面

import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def create_concept_index(vault_path="D:/LDD/璇玑台"):
    """创建概念索引页面"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return
    
    print("创建概念索引页面...")
    print("=" * 50)
    
    # 查找知识文件夹中的文件
    knowledge_dir = vault / "03-知识"
    if not knowledge_dir.exists():
        print(f"错误: 知识文件夹不存在: {knowledge_dir}")
        return
    
    # 获取所有知识文件
    knowledge_files = list(knowledge_dir.rglob("*.md"))
    print(f"找到 {len(knowledge_files)} 个知识文件")
    
    # 按子分类组织
    concept_data = defaultdict(list)
    
    for file_path in knowledge_files:
        # 获取相对路径
        rel_path = file_path.relative_to(knowledge_dir)
        
        # 提取分类信息
        parts = rel_path.parts
        if len(parts) >= 2:
            category = parts[0]  # 概念/理论/方法/工具/案例
            subcategory = parts[1] if len(parts) > 2 else "其他"
        else:
            category = "未分类"
            subcategory = "其他"
        
        # 从文件名提取信息
        filename = file_path.name
        concept_name = filename.replace('.md', '')
        
        # 尝试从文件内容提取概念定义
        definition = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # 读取前1000字符
            
            # 查找定义模式
            definition_patterns = [
                r'定义[:：]\s*(.+?)(?:\n|$)',
                r'概念[:：]\s*(.+?)(?:\n|$)',
                r'^# (.+?)\n\n(.+?)(?:\n\n|$)',
                r'## 定义\n\n(.+?)(?:\n\n|$)',
            ]
            
            for pattern in definition_patterns:
                match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
                if match:
                    definition = match.group(1).strip()
                    if len(definition) > 150:
                        definition = definition[:150] + "..."
                    break
            
            # 如果没有找到定义，使用第一段
            if not definition:
                first_para = re.search(r'^(.*?)(?:\n\n|$)', content, re.MULTILINE | re.DOTALL)
                if first_para:
                    definition = first_para.group(1).strip()
                    if len(definition) > 150:
                        definition = definition[:150] + "..."
        
        except Exception as e:
            definition = f"读取失败: {str(e)[:50]}"
        
        concept_data[category].append({
            'path': file_path.relative_to(vault),
            'filename': filename,
            'name': concept_name,
            'definition': definition,
            'category': category,
            'subcategory': subcategory,
            'full_path': str(file_path.relative_to(vault))
        })
    
    print(f"概念分类: {len(concept_data)} 个")
    
    # 创建概念索引内容
    concept_content = f"""# 概念索引

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总概念文件**: {len(knowledge_files)} 个
**概念分类**: {len(concept_data)} 类

## 📚 概念库概览

### 知识体系结构
你的知识库包含以下核心分类：

| 分类 | 文件数 | 说明 | 示例概念 |
|------|--------|------|----------|
"""
    
    category_descriptions = {
        "概念": "核心概念和术语的定义与解释",
        "理论": "理论和原理的阐述与分析",
        "方法": "方法、技巧和策略的说明",
        "工具": "工具、技术和系统的介绍",
        "案例": "实际案例和应用的分析",
    }
    
    category_examples = {
        "概念": "认知切片、战壕禅、动态调谐",
        "理论": "认知科学理论、哲学原理",
        "方法": "追问法、反思法、实践法",
        "工具": "Obsidian、OpenClaw、API配置",
        "案例": "实际应用案例、问题解决方案",
    }
    
    total_files = 0
    for category in ["概念", "理论", "方法", "工具", "案例"]:
        if category in concept_data:
            files = concept_data[category]
            count = len(files)
            total_files += count
            
            description = category_descriptions.get(category, "其他知识")
            examples = category_examples.get(category, "各种知识")
            
            concept_content += f"| **{category}** | {count} | {description} | {examples} |\n"
    
    concept_content += f"| **总计** | **{total_files}** | 所有知识文件 | - |\n"
    
    # 详细概念列表
    concept_content += """
## 🔍 详细概念列表

"""
    
    for category in ["概念", "理论", "方法", "工具", "案例"]:
        if category not in concept_data:
            continue
        
        files = concept_data[category]
        
        concept_content += f"### {category}\n"
        concept_content += f"**共 {len(files)} 个{category}文件**\n\n"
        
        # 按名称排序
        sorted_files = sorted(files, key=lambda x: x['name'])
        
        # 分组显示（每行3个）
        cols = 3
        rows = (len(sorted_files) + cols - 1) // cols
        
        for i in range(rows):
            row_concepts = []
            for j in range(cols):
                idx = i + j * rows
                if idx < len(sorted_files):
                    file_info = sorted_files[idx]
                    concept_name = file_info['name']
                    link_path = file_info['full_path'].replace('\\', '/')
                    row_concepts.append(f"[[{link_path}|{concept_name}]]")
                else:
                    row_concepts.append("")
            
            concept_content += "| " + " | ".join(row_concepts) + " |\n"
        
        concept_content += "\n"
    
    # 核心概念详解
    concept_content += """
## 💎 核心概念详解

**以下是一些重要的核心概念及其简要说明**:
"""
    
    # 找出"概念"分类中的文件
    core_concepts = concept_data.get("概念", [])
    
    # 按名称长度排序（通常较短的是核心概念）
    core_concepts.sort(key=lambda x: len(x['name']))
    
    concept_content += "| 概念 | 定义/说明 | 相关链接 |\n|------|-----------|----------|\n"
    
    for concept_info in core_concepts[:30]:  # 显示前30个
        concept_name = concept_info['name']
        definition = concept_info['definition']
        link_path = concept_info['full_path'].replace('\\', '/')
        
        # 如果没有定义，使用占位符
        if not definition or len(definition) < 10:
            definition = "该概念的定义待补充..."
        
        # 查找相关概念
        related = []
        for other in core_concepts:
            if other['name'] != concept_name and concept_name in other['definition']:
                related.append(f"[[{other['full_path'].replace('\\', '/')}|{other['name']}]]")
                if len(related) >= 3:
                    break
        
        related_str = "、".join(related[:3]) if related else "暂无"
        
        concept_content += f"| **[[{link_path}|{concept_name}]]** | {definition} | {related_str} |\n"
    
    # 概念关系网络
    concept_content += """
## 🕸️ 概念关系网络

### 概念关联建议
1. **层级关系**: 使用 `[[父概念]] ← [[子概念]]` 表示层级
2. **相关关系**: 使用 `[[概念A]] ↔ [[概念B]]` 表示相关
3. **对比关系**: 使用 `[[概念A]] vs [[概念B]]` 表示对比

### 重要概念集群
基于你的知识库，以下概念可能形成重要集群：

#### 认知科学集群
- [[认知切片]]、[[战壕禅]]、[[动态调谐]]、[[元认知]]、[[认知跃迁]]

#### 哲学思想集群
- [[道家思想]]、[[儒家思想]]、[[佛学思想]]、[[西方哲学]]

#### 技术工具集群
- [[Obsidian]]、[[OpenClaw]]、[[API配置]]、[[工作流]]

#### 实践方法集群
- [[追问法]]、[[反思法]]、[[实践法]]、[[记录法]]

## 📖 概念管理指南

### 1. 概念创建标准
- **明确性**: 概念定义清晰明确
- **独特性**: 与其他概念有明确区分
- **实用性**: 有实际应用价值
- **系统性**: 能融入现有知识体系

### 2. 概念维护建议
- **定期更新**: 随着认知发展更新概念定义
- **建立链接**: 将相关概念相互链接
- **添加示例**: 为抽象概念添加具体示例
- **收集反馈**: 记录对概念的理解和疑问

### 3. 概念标签建议
- `#核心概念` - 知识体系的核心概念
- `#基础概念` - 基础性和入门性概念
- `#高级概念` - 深入和复杂的概念
- `#跨领域概念` - 跨多个领域的概念
- `#待完善概念` - 需要进一步完善的概

## 🔗 相关索引
- [[主页索引]] - 返回主页面
- [[标签索引]] - 标签分类索引
- [[时间线索引]] - 时间线查看
- [[对话索引]] - 对话记录索引

---

*本页面由璇玑自动生成，最后更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

> 🧠 **知识的价值**: 清晰的概念是思考的基石。一个好的概念索引能让你快速定位和理解知识体系的核心。
"""
    
    # 保存概念索引
    concept_path = vault / "00-索引" / "概念索引.md"
    concept_path.parent.mkdir(exist_ok=True, parents=True)
    
    with open(concept_path, 'w', encoding='utf-8') as f:
        f.write(concept_content)
    
    print(f"概念索引已创建: {concept_path.relative_to(vault)}")
    
    # 统计信息
    print(f"\n概念统计:")
    for category in ["概念", "理论", "方法", "工具", "案例"]:
        if category in concept_data:
            count = len(concept_data[category])
            print(f"  {category}: {count} 个文件")
    
    return len(knowledge_files)

if __name__ == "__main__":
    create_concept_index()