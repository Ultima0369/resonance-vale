#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行智能知识挖掘器
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
import sys
sys.path.append(str(current_dir))

try:
    from intelligent_knowledge_miner import IntelligentKnowledgeMiner
    
    print('🔍 启动智能知识挖掘器')
    print('=' * 60)
    
    # 配置路径
    obsidian_path = r'D:\LDD\璇玑台'
    
    # 创建挖掘器
    miner = IntelligentKnowledgeMiner(obsidian_path)
    
    # 挖掘整个知识库
    print('开始挖掘璇玑台知识库...')
    mining_results = miner.mine_directory()
    
    print()
    print('📊 挖掘结果总览')
    print('=' * 60)
    
    overall = mining_results["overall_analysis"]
    
    print(f'挖掘文件: {mining_results["total_files"]}个')
    print(f'发现概念: {overall["total_concepts"]}次提及')
    print(f'独特概念: {len(overall["unique_concepts"])}个')
    print()
    
    # 分类分布
    print('📁 内容分类分布:')
    for category, count in overall["top_categories"]:
        percentage = count / mining_results["total_files"] * 100
        bar = '█' * int(percentage / 5)  # 每5%一个方块
        print(f'  {category}: {bar} ({count}个, {percentage:.1f}%)')
    
    print()
    
    # 热门概念
    print('🔥 热门概念 (前10名):')
    for i, (concept, count) in enumerate(overall["top_concepts"][:10], 1):
        print(f'  {i}. {concept}: {count}次')
    
    print()
    
    # 模式发现
    print('🎯 知识模式发现:')
    for pattern_type, count in overall["pattern_distribution"].most_common(5):
        print(f'  • {pattern_type}: {count}次')
    
    print()
    
    # 发现洞察
    print('💡 发现洞察:')
    for insight in overall["discovery_insights"][:5]:
        print(f'  • {insight}')
    
    print()
    
    # 生成详细报告
    print('📄 生成详细挖掘报告...')
    report = generate_mining_report(mining_results)
    
    # 保存报告
    report_dir = Path(obsidian_path) / "system" / "mining" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"知识挖掘报告_{report_date}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'✅ 挖掘报告已保存: {report_path}')
    print()
    
    # 生成整理建议
    print('🎯 生成整理建议...')
    organizing_plan = generate_organizing_plan(mining_results)
    
    plan_path = report_dir / f"整理建议_{report_date}.md"
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(organizing_plan)
    
    print(f'✅ 整理建议已保存: {plan_path}')
    print()
    
    # 发现高质量内容
    print('🌟 发现高质量内容...')
    high_quality_files = find_high_quality_files(mining_results["mining_results"])
    
    if high_quality_files:
        print(f'发现 {len(high_quality_files)} 个高质量文件:')
        for i, file_info in enumerate(high_quality_files[:5], 1):
            print(f'  {i}. {file_info["file_name"]} - {file_info["score"]:.1f}分')
        
        # 保存高质量文件列表
        hq_path = report_dir / f"高质量文件列表_{report_date}.md"
        with open(hq_path, 'w', encoding='utf-8') as f:
            hq_content = generate_high_quality_list(high_quality_files)
            f.write(hq_content)
        
        print(f'✅ 高质量文件列表已保存: {hq_path}')
    else:
        print('未发现高质量文件')
    
    print()
    print('🎉 智能知识挖掘完成！')
    
except ImportError as e:
    print(f'❌ 导入模块失败: {e}')
    print('请确保intelligent_knowledge_miner.py在tools目录中')
except Exception as e:
    print(f'❌ 执行失败: {e}')
    import traceback
    traceback.print_exc()

def generate_mining_report(mining_results: dict) -> str:
    """生成详细挖掘报告"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    overall = mining_results["overall_analysis"]
    
    report = []
    report.append(f"# 智能知识挖掘报告")
    report.append(f"生成时间: {report_date}")
    report.append(f"挖掘文件: {mining_results['total_files']}个")
    report.append(f"发现概念: {overall['total_concepts']}次提及")
    report.append(f"独特概念: {len(overall['unique_concepts'])}个")
    report.append("")
    
    # 分类分布
    report.append("## 内容分类分布")
    for category, count in overall["top_categories"]:
        percentage = count / mining_results["total_files"] * 100
        report.append(f"- **{category}**: {count}个 ({percentage:.1f}%)")
    report.append("")
    
    # 热门概念
    report.append("## 热门概念分析")
    report.append("### 前20个最常出现的概念:")
    for i, (concept, count) in enumerate(overall["top_concepts"][:20], 1):
        report.append(f"{i}. **{concept}**: {count}次")
    report.append("")
    
    # 知识模式
    report.append("## 知识模式发现")
    for pattern_type, count in overall["pattern_distribution"].most_common():
        report.append(f"- **{pattern_type}**: {count}次")
    report.append("")
    
    # 发现洞察
    report.append("## 发现洞察")
    for insight in overall["discovery_insights"]:
        report.append(f"- {insight}")
    report.append("")
    
    # 新概念发现
    report.append("## 新概念发现")
    
    # 假设我们有一个专有词典（实际应该从模块获取）
    custom_concepts = {
        "认知碎片", "战略清醒", "对话毁灭", "工具性存在", 
        "注意力收割", "武器化", "OpenClaw", "Moltcn", 
        "Obsidian", "璇玑实验", "对话整理", "知识管理",
        "星尘", "璇玑"
    }
    
    found_concepts = overall["unique_concepts"]
    new_concepts = found_concepts - custom_concepts
    
    if new_concepts:
        report.append(f"发现了 {len(new_concepts)} 个新概念:")
        new_concepts_list = sorted(list(new_concepts))
        for i, concept in enumerate(new_concepts_list[:30], 1):  # 只显示前30个
            report.append(f"{i}. {concept}")
        
        if len(new_concepts) > 30:
            report.append(f"... 还有{len(new_concepts)-30}个新概念")
    else:
        report.append("未发现新概念")
    report.append("")
    
    # 高质量文件
    report.append("## 高质量文件发现")
    high_quality_files = find_high_quality_files(mining_results["mining_results"])
    
    if high_quality_files:
        report.append(f"发现 {len(high_quality_files)} 个高质量文件 (评分≥70):")
        for i, file_info in enumerate(high_quality_files[:10], 1):
            report.append(f"### {i}. {file_info['file_name']} ({file_info['score']:.1f}分)")
            report.append(f"- **路径**: {file_info['file_path']}")
            report.append(f"- **分类**: {file_info['category']}")
            report.append(f"- **概念数**: {len(file_info['concepts_found'])}")
            report.append(f"- **定义数**: {len(file_info['definitions'])}")
            
            if file_info['concepts_found']:
                top_concepts = [c['concept'] for c in file_info['concepts_found'][:3]]
                report.append(f"- **主要概念**: {', '.join(top_concepts)}")
            
            if file_info['summary']:
                summary = file_info['summary']
                if len(summary) > 200:
                    summary = summary[:197] + "..."
                report.append(f"- **摘要**: {summary}")
            
            report.append("")
    else:
        report.append("未发现高质量文件")
    report.append("")
    
    # 整理建议
    report.append("## 整理建议")
    
    # 按分类建议
    report.append("### 按分类整理建议:")
    for category, count in overall["top_categories"]:
        if count > 5:  # 只有数量较多的分类才建议
            report.append(f"- **{category}** ({count}个): 建议建立专门的{category}目录")
    report.append("")
    
    # 按概念建议
    report.append("### 按概念整理建议:")
    for concept, count in overall["top_concepts"][:10]:
        if count >= 3:  # 出现3次以上的概念
            report.append(f"- **{concept}**: 出现{count}次，建议创建概念文件")
    report.append("")
    
    # 技术细节
    report.append("## 技术细节")
    report.append("### 挖掘算法")
    report.append("- **概念提取**: 使用jieba分词和专有词典")
    report.append("- **模式识别**: 基于正则表达式的模式匹配")
    report.append("- **内容分类**: 基于关键词和概念的分类")
    report.append("- **质量评估**: 基于概念密度和模式丰富度")
    report.append("")
    
    report.append("### 质量评分标准")
    report.append("- **概念密度** (40%): 文件中概念的丰富程度")
    report.append("- **模式丰富度** (30%): 定义、观点、方法等模式的数量")
    report.append("- **结构完整性** (20%): 标题、段落、链接等结构")
    report.append("- **内容独特性** (10%): 新概念和新模式")
    report.append("")
    
    report.append(f"---")
    report.append(f"*报告版本: 1.0*")
    report.append(f"*挖掘工具: 智能知识挖掘器*")
    report.append(f"*建议挖掘频率: 每周一次*")
    
    return "\n".join(report)

def find_high_quality_files(mining_results: list) -> list:
    """发现高质量文件"""
    high_quality_files = []
    
    for result in mining_results:
        # 计算质量分数
        score = calculate_quality_score(result)
        
        if score >= 70:  # 70分以上认为是高质量
            result["score"] = score
            high_quality_files.append(result)
    
    # 按分数排序
    high_quality_files.sort(key=lambda x: x["score"], reverse=True)
    
    return high_quality_files

def calculate_quality_score(result: dict) -> float:
    """计算质量分数"""
    score = 0
    
    # 1. 概念密度 (40分)
    concept_count = len(result.get("concepts_found", []))
    if concept_count >= 10:
        score += 40
    elif concept_count >= 5:
        score += 30
    elif concept_count >= 3:
        score += 20
    elif concept_count >= 1:
        score += 10
    
    # 2. 模式丰富度 (30分)
    pattern_score = 0
    for pattern_type in ["definitions", "viewpoints", "methods", "examples", "comparisons", "relations"]:
        if len(result.get(pattern_type, [])) > 0:
            pattern_score += 5
    
    score += min(30, pattern_score)
    
    # 3. 结构完整性 (20分)
    if result.get("heading_count", 0) >= 3:
        score += 10
    
    if result.get("paragraph_count", 0) >= 5:
        score += 5
    
    if result.get("link_count", 0) >= 3:
        score += 5
    
    # 4. 内容独特性 (10分)
    # 检查是否有新概念
    custom_concepts = {
        "认知碎片", "战略清醒", "对话毁灭", "工具性存在", 
        "注意力收割", "武器化", "OpenClaw", "Moltcn", 
        "Obsidian", "璇玑实验", "对话整理", "知识管理",
        "星尘", "璇玑"
    }
    
    found_concepts = {c["concept"] for c in result.get("concepts_found", [])}
    new_concepts = found_concepts - custom_concepts
    
    if len(new_concepts) >= 2:
        score += 10
    elif len(new_concepts) >= 1:
        score += 5
    
    return min(100, score)

def generate_organizing_plan(mining_results: dict) -> str:
    """生成整理建议"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    overall = mining_results["overall_analysis"]
    
    plan = []
    plan.append(f"# 知识库整理建议")
    plan.append(f"生成时间: {report_date}")
    plan.append(f"基于智能知识挖掘报告生成")
    plan.append("")
    
    # 总体建议
    plan.append("## 总体整理策略")
    plan.append("")
    plan.append("### 1. 优先级排序")
    plan.append("- **第一优先级**: 高质量文件 (评分≥70)")
    plan.append("- **第二优先级**: 包含核心概念的文件")
    plan.append("- **第三优先级**: 分类明确的文件")
    plan.append("- **第四优先级**: 其他文件")
    plan.append("")
    
    plan.append("### 2. 整理方法")
    plan.append("- **批量处理**: 按分类批量整理")
    plan.append("- **模板化**: 使用标准化模板")
    plan.append("- **自动化**: 使用整理工具自动化处理")
    plan.append("- **质量控制**: 整理后质量评估")
    plan.append("")
    
    # 具体建议
    plan.append("## 具体整理建议")
    plan.append("")
    
    # 按分类整理
    plan.append("### 按分类整理")
    for category, count in overall["top_categories"]:
        if count >= 3:  # 只有数量较多的分类才建议
            plan.append(f"#### {category}类 ({count}个文件)")
            plan.append(f"- **目标目录**: `{category}/`")
            plan.append(f"- **整理方法**: 使用`{category}`模板")
            plan.append(f"- **预计时间**: {count * 2}分钟")
            plan.append("")
    
    # 按概念整理
    plan.append("### 按概念整理")
    for concept, count in overall["top_concepts"][:15]:
        if count >= 3:  # 出现3次以上的概念
            plan.append(f"- **{concept}** (出现{count}次):")
            plan.append(f"  - 创建概念文件: `concepts/{concept}.md`")
            plan.append(f"  - 收集相关讨论")
            plan.append(f"  - 建立概念关系")
            plan.append("")
    
    # 时间安排
    plan.append("## 时间安排建议")
    plan.append("")
    plan.append("### 第一周: 基础整理")
    plan.append("- **目标**: 整理所有高质量文件")
    plan.append("- **任务**:")
    plan.append("  1. 整理评分≥70的文件")
    plan.append("  2. 建立核心概念体系")
    plan.append("  3. 创建分类目录结构")
    plan.append("")
    
    plan.append("### 第二周: 系统整理")
    plan.append("- **目标**: 整理主要分类文件")
    plan.append("- **任务**:")
    plan.append("  1. 按分类批量整理")
    plan.append("  2. 完善概念关系网络")
    plan.append("  3. 建立知识索引系统")
    plan.append("")
    
    plan.append("### 第三周: 优化完善")
    plan.append("- **目标**: 完成所有整理工作")
    plan.append("- **任务**:")
    plan.append("  1. 整理剩余文件")
    plan.append("  2. 优化知识体系结构")
    plan.append("  3. 建立维护机制")
    plan.append("")
    
    # 工具建议
    plan.append("## 工具使用建议")
    plan.append("")
    plan.append("### 现有工具")
    plan.append("- **对话整理工具**: `conversation_organizer.py`")
    plan.append("- **概念整理工具**: `concept_organizer.py`")
    plan.append("- **知识发现工具**: `knowledge_discovery.py`")
    plan.append("- **质量评估工具**: `concept_quality_assessment.py`")
    plan.append("")
    
    plan.append("### 建议开发的新工具")
    plan.append("- **批量整理工具**: 按分类批量处理")
    plan.append("- **关系建立工具**: 自动建立概念关系")
    plan.append("- **知识图谱工具**: 可视化知识网络")
    plan.append("- **自动化工作流**: 端到