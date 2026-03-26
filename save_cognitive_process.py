#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 保存认知过程补充资料到Obsidian

import os
import re
from datetime import datetime
from pathlib import Path

def main():
    print("=" * 60)
    print("保存认知过程补充资料到Obsidian")
    print("=" * 60)
    
    # 1. 检查补充资料文档
    supplement_path = "C:\\Users\\lgdln\\.openclaw\\workspace\\认知过程-补充资料.md"
    
    if not os.path.exists(supplement_path):
        print(f"❌ 补充资料文档不存在: {supplement_path}")
        input("按回车键退出...")
        return
    
    with open(supplement_path, 'r', encoding='utf-8') as f:
        supplement_content = f.read()
    
    print(f"✅ 补充资料已加载 ({len(supplement_content)} 字符)")
    
    # 2. 检查Obsidian库
    vault_path = "D:\\LDD\\璇玑台"
    vault = Path(vault_path)
    
    if not vault.exists():
        print(f"❌ Obsidian库不存在: {vault_path}")
        custom_path = input("请输入Obsidian库路径: ").strip()
        if custom_path:
            vault = Path(custom_path)
            if not vault.exists():
                print("❌ 路径不存在")
                input("按回车键退出...")
                return
        else:
            print("❌ 必须提供有效的路径")
            input("按回车键退出...")
            return
    
    print(f"✅ Obsidian库: {vault}")
    
    # 3. 保存补充资料到参考资料文件夹
    refs_folder = vault / "参考资料"
    refs_folder.mkdir(exist_ok=True)
    
    supplement_file = refs_folder / "认知过程-补充资料.md"
    with open(supplement_file, 'w', encoding='utf-8') as f:
        f.write(supplement_content)
    
    print(f"✅ 补充资料已保存: {supplement_file}")
    
    # 4. 更新认知切片论项目
    update_cognitive_slice_project(vault, supplement_content)
    
    # 5. 创建新的概念文件
    create_new_concepts(vault, supplement_content)
    
    # 6. 创建研究笔记
    create_research_notes(vault)
    
    print("\n" + "=" * 60)
    print("🎉 认知过程补充资料保存完成！")
    print("\n📊 生成的文件:")
    print(f"  补充资料: {supplement_file}")
    print(f"  更新项目: {vault}\\项目\\认知切片论\\")
    print(f"  新概念文件: {vault}\\概念\\")
    print(f"  研究笔记: {vault}\\研究笔记\\")
    
    input("\n按回车键退出...")

def update_cognitive_slice_project(vault, supplement_content):
    """更新认知切片论项目"""
    
    project_folder = vault / "项目" / "认知切片论"
    
    if not project_folder.exists():
        print("⚠️ 认知切片论项目文件夹不存在")
        return
    
    # 读取主文档
    main_file = project_folder / "认知切片论-整合版.md"
    if not main_file.exists():
        print("⚠️ 主文档不存在")
        return
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # 创建更新版本
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 提取补充资料的关键部分
    sections = extract_key_sections(supplement_content)
    
    # 创建更新日志
    update_log = f"""# 认知切片论 - 更新日志

## 2026-03-23 更新：认知过程补充

### 新增内容
1. **认知科学基础强化**
   - 详细的认知过程定义（知觉、注意、记忆、思维、语言）
   - 神经科学视角（大脑结构、神经网络、神经可塑性）
   - 心理学理论支持（有限理性、双系统、认知负荷）

2. **神经基础补充**
   - 切片形成的神经机制（注意力瓶颈、工作记忆限制）
   - 动态调谐的神经基础（前额叶皮层、突显网络）
   - 切片自觉的神经关联（默认模式网络）

3. **研究方向扩展**
   - 认知切片的发展轨迹（儿童期、成年期、老年期）
   - 文化对认知切片的影响（东西方差异）
   - 技术时代的认知切片（数字媒体、AI、VR）

### 对理论的丰富
- **理论基础强化**：从现象到机制，从个体到普遍
- **实践工具开发**：基于认知科学原理的训练方法
- **评估方法建立**：行为、认知、神经多层面评估

### 相关文件
- [[参考资料/认知过程-补充资料]] - 完整补充资料
- [[概念/认知科学]] - 相关概念
- [[概念/神经科学]] - 神经基础
- [[概念/心理学]] - 心理机制

---

*更新由璇玑自动生成*"""
    
    # 保存更新日志
    update_file = project_folder / "更新日志.md"
    with open(update_file, 'w', encoding='utf-8') as f:
        f.write(update_log)
    
    print(f"✅ 更新日志已创建: {update_file}")
    
    # 创建增强版主文档
    enhanced_content = enhance_main_document(main_content, sections)
    enhanced_file = project_folder / "认知切片论-增强版.md"
    
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    print(f"✅ 增强版文档已创建: {enhanced_file}")
    
    # 更新项目索引
    update_project_index(project_folder, today)

def extract_key_sections(supplement_content):
    """提取补充资料的关键部分"""
    
    sections = {}
    
    # 使用正则表达式提取章节
    pattern = r'^## (.*?)$\n(.*?)(?=^## |\Z)'
    matches = re.findall(pattern, supplement_content, re.MULTILINE | re.DOTALL)
    
    for title, content in matches:
        sections[title.strip()] = content.strip()
    
    return sections

def enhance_main_document(main_content, sections):
    """增强主文档内容"""
    
    # 在适当位置插入补充内容
    enhanced = main_content
    
    # 如果文档中有"理论基础"部分，在之后插入神经科学基础
    if "## 🧠 理论基础" in enhanced:
        neuro_section = """
## ⚡ 神经科学基础（新增）

### 1. 认知切片的神经机制
- **注意力瓶颈**：大脑只能同时处理有限信息，必须通过"切片"方式处理
- **工作记忆限制**：7±2的信息单元限制，导致复杂信息必须分块
- **神经网络切换**：不同认知切片对应不同的神经网络激活模式

### 2. 动态调谐的神经基础
- **前额叶皮层**：负责执行控制和任务切换
- **突显网络**：检测何时需要切换认知切片
- **多巴胺系统**：提供切换的动机和奖励信号

### 3. 切片自觉的神经关联
- **默认模式网络**：与自我参照思维和元认知相关
- **前扣带皮层**：错误检测和冲突监控
- **背外侧前额叶**：执行控制和自我监控

*基于认知过程补充资料的分析*"""
        
        # 在理论基础后插入
        enhanced = enhanced.replace("## 🧠 理论基础", "## 🧠 理论基础" + neuro_section)
    
    # 在文档末尾添加更新说明
    update_note = f"""
---

## 📚 资料更新说明

**最后更新**: 2026-03-23  
**更新内容**: 增加了认知过程的神经科学和心理学基础

### 新增的科学依据
1. **认知科学**：详细的认知过程定义和机制
2. **神经科学**：大脑结构和功能的基础
3. **心理学**：相关理论的支持和验证

### 对认知切片论的强化
- **理论深度**：从现象描述到机制解释
- **实践基础**：基于科学原理的工具开发
- **研究导向**：明确了未来的研究方向

### 相关参考资料
- [[参考资料/认知过程-补充资料]] - 完整的补充资料
- [[更新日志]] - 详细的更新记录

---

*文档已根据认知过程研究进行增强*"""
    
    enhanced += update_note
    
    return enhanced

def update_project_index(project_folder, today):
    """更新项目索引"""
    
    index_file = project_folder / "项目索引.md"
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # 添加更新记录
        update_section = f"""
## 📅 最近更新

### {today}: 认知过程补充
- 增加了神经科学和心理学基础
- 创建了[[认知切片论-增强版]]文档
- 添加了[[更新日志]]记录
- 丰富了相关概念文件

**相关文件**:
- [[参考资料/认知过程-补充资料]]
- [[认知切片论-增强版]]
- [[更新日志]]
"""
        
        # 在适当位置插入
        if "## 📅 项目时间线" in index_content:
            index_content = index_content.replace("## 📅 项目时间线", update_section + "\n## 📅 项目时间线")
        else:
            index_content += update_section
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✅ 项目索引已更新: {index_file}")

def create_new_concepts(vault, supplement_content):
    """创建新的概念文件"""
    
    concept_folder = vault / "概念"
    concept_folder.mkdir(exist_ok=True)
    
    # 从补充资料中提取新概念
    new_concepts = [
        ("注意力瓶颈", "认知科学", "大脑同时处理信息的有限能力"),
        ("工作记忆限制", "认知科学", "短期记忆的容量限制（7±2）"),
        ("神经网络切换", "神经科学", "不同认知任务对应不同的神经网络激活"),
        ("前额叶皮层", "神经科学", "负责执行控制、决策和任务切换"),
        ("默认模式网络", "神经科学", "与自我参照思维和心智游移相关"),
        ("有限理性", "心理学", "赫伯特·西蒙的理论，强调认知限制"),
        ("双系统理论", "心理学", "丹尼尔·卡尼曼的系统1和系统2"),
        ("认知负荷", "心理学", "约翰·斯威勒的认知负荷理论"),
        ("神经可塑性", "神经科学", "大脑根据经验改变结构和功能的能力")
    ]
    
    created = []
    
    for concept_name, category, definition in new_concepts:
        concept_file = concept_folder / f"{concept_name}.md"
        
        if not concept_file.exists():
            concept_content = f"""# {concept_name}

## 定义
{definition}

## 分类
- 类别: {category}
- 相关领域: 认知切片论

## 在认知切片论中的意义
*待补充 - 与认知切片的关系*

## 相关概念
- [[认知切片论]]
- [[认知科学]]
- [[{category}]]

## 参考资料
- [[参考资料/认知过程-补充资料]]

## 相关研究
*待补充*

---

*概念文件 - 由璇玑自动创建*"""
            
            with open(concept_file, 'w', encoding='utf-8') as f:
                f.write(concept_content)
            
            created.append(concept_name)
    
    if created:
        print(f"📄 创建新概念文件: {len(created)} 个")
        print(f"   包括: {', '.join(created[:3])}{'...' if len(created) > 3 else ''}")

def create_research_notes(vault):
    """创建研究笔记"""
    
    research_folder = vault / "研究笔记"
    research_folder.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 创建认知过程研究笔记
    research_note = f"""# 认知过程研究笔记

**研究主题**: 认知过程的神经和心理基础  
**研究日期**: {today}  
**研究者**: 璇玑（基于星尘的指导）  
**资料来源**: Obsidian库概念文件 + 对话记录

## 🎯 研究目的
为认知切片论提供坚实的科学基础，从认知科学、神经科学、心理学角度丰富理论内涵。

## 📋 研究方法
1. **文献分析**: 分析Obsidian库中的相关概念文件
2. **理论整合**: 将不同学科的理论整合到认知切片论框架中
3. **概念扩展**: 基于科学原理扩展和深化核心概念

## 🔍 主要发现

### 1. 认知科学基础
- 认知过程包括知觉、注意、记忆、思维、语言等
- 工作记忆的有限容量（7±2）是认知切片的重要限制因素
- 选择性注意决定了哪些信息进入认知加工

### 2. 神经科学视角
- 前额叶皮层在认知控制中起关键作用
- 默认模式网络与自我参照思维相关
- 神经网络切换支持不同认知任务间的转换

### 3. 心理学理论支持
- 有限理性理论解释了为什么需要认知切片
- 双系统理论提供了切片类型的分类框架
- 认知负荷理论说明了切片的价值和成本

## 💡 对认知切片论的启示

### 理论价值确认
- 认知切片不是比喻，而是有科学依据的认知现象
- 切片能力基于可塑的神经基础，因此可以训练
- 切片影响学习、工作、决策等多个认知领域

### 实践意义强化
- 可以设计基于认知科学原理的具体训练方法
- 可以建立科学的评估指标和工具
- 可以开发针对性的应用和干预方案

### 研究方向明确
- 基础研究：深入理解切片的认知神经机制
- 应用研究：开发实用的工具和方法
- 跨学科整合：建立更广泛的理论联系

## 📚 参考文献
- [[概念/认知科学]]
- [[概念/神经科学]] 
- [[概念/心理学]]
- [[参考资料/认知过程-补充资料]]

## 🚀 下一步研究计划

### 短期（1个月）
1. 深入分析认知切片的发展轨迹
2. 研究文化因素对认知切片的影响
3. 探索技术环境中的切片特点

### 中期（3个月）
1. 设计认知切片能力的评估工具
2. 开发切片训练的程序和方法
3. 进行初步的实证研究

### 长期（1年）
1. 建立完整的认知切片理论体系
2. 发表学术文章和研究报告
3. 推广应用到教育和临床领域

## 📝 研究笔记

### 关键洞察
1. **认知切片是适应性策略**：不是缺陷，而是大脑应对复杂环境的智慧
2. **切片能力可塑**：基于神经可塑性，可以通过训练提升
3. **切片质量重要**：不仅要有切片能力，还要有高质量的切片

### 待解决问题
1. 如何量化评估认知切片能力？
2. 不同领域的切片是否有不同特点？
3. 切片训练的最佳方法是什么？

### 研究限制
1. 目前主要基于文献分析，需要实证研究支持
2. 跨文化比较数据不足
3. 技术影响的研究刚刚开始

---

**研究状态**: 进行中  
**下次更新**: 2026-04-23  
**维护者**: 璇玑

*本笔记记录了认知切片论的科学基础研究过程*"""
    
    research_file = research_folder / f"{today}-认知过程研究.md"
    with open(research_file, 'w', encoding='utf-8') as f:
        f.write(research_note)
    
    print(f"📝 研究笔记已创建: {research_file}")
    
    # 创建研究索引
    create_research_index(research_folder)

def create_research_index(research_folder):
    """创建研究索引"""
    
    index_content = """# 研究笔记索引

## 所有研究笔记

*按日期排序，最新的在前*

## 按主题分类

### 认知切片论相关
- [[2026-03-23-认知过程研究]] - 认知过程的神经和心理基础

### 方法论研究
*待补充*

### 应用研究
*待补充*

## 研究团队

### 核心研究者
- **星尘** - 理论提出者，研究指导者
- **璇玑** - 研究执行者，文献分析者

### 合作研究者
*欢迎加入*

## 研究资源

### 内部资源
- [[概念]] - 相关概念定义
- [[参考资料]] - 研究资料库
- [[项目/认知切片论]] - 主项目

### 外部资源
*待补充*

## 研究规范

### 数据管理
- 所有研究数据保存在Obsidian中
- 使用标准化的笔记模板
- 定期备份和整理

### 质量控制
- 基于科学文献进行分析
- 明确标注资料来源
- 定期进行同行评审（计划中）

### 知识共享
- 研究成果在Obsidian中共享
- 准备学术发表（长期目标）
- 建立开放研究社群（计划中）

---

*研究索引由璇玑自动维护*"""
    
    index_file = research_folder / "研究索引.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📑 研究索引已创建: {index_file}")

if __name__ == "__main__":
    main()