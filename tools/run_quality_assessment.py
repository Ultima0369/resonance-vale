#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行概念质量评估
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
    from concept_quality_assessment import ConceptQualityAssessment
    
    print('🔍 开始概念质量评估')
    print('=' * 60)
    
    # 配置路径
    obsidian_path = r'D:\LDD\璇玑台'
    
    # 创建评估器
    assessor = ConceptQualityAssessment(obsidian_path)
    
    # 评估所有概念
    print('评估所有概念文件...')
    result = assessor.assess_all_concepts()
    
    if "error" in result:
        print(f"❌ 评估失败: {result['error']}")
        sys.exit(1)
    
    print()
    print('📊 评估结果总览')
    print('=' * 60)
    
    # 总体统计
    total_files = result["summary"]["total_files"]
    assessed_files = result["summary"]["assessed_files"]
    avg_score = result["summary"]["average_score"]
    quality_distribution = result["summary"]["quality_distribution"]
    
    print(f'评估文件: {assessed_files}/{total_files}')
    print(f'平均分数: {avg_score:.1f}/100')
    print()
    
    print('📈 质量分布:')
    for range_name, count in quality_distribution.items():
        percentage = count / assessed_files * 100 if assessed_files > 0 else 0
        bar = '█' * int(percentage / 5)  # 每5%一个方块
        print(f'  {range_name}: {bar} ({count}个, {percentage:.1f}%)')
    
    print()
    
    # 最佳和最差概念
    print('🏆 最佳概念 (前5名):')
    best_concepts = sorted(
        [(name, data["overall_score"]) for name, data in result["assessments"].items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    for i, (concept_name, score) in enumerate(best_concepts, 1):
        print(f'  {i}. {concept_name}: {score}/100')
    
    print()
    
    print('⚠️ 需要改进的概念 (后5名):')
    worst_concepts = sorted(
        [(name, data["overall_score"]) for name, data in result["assessments"].items()],
        key=lambda x: x[1]
    )[:5]
    
    for i, (concept_name, score) in enumerate(worst_concepts, 1):
        print(f'  {i}. {concept_name}: {score}/100')
    
    print()
    
    # 常见问题
    print('🔧 常见问题统计:')
    all_issues = []
    for assessment in result["assessments"].values():
        for key in ["basics_issues", "sections_issues", "metadata_issues", "links_issues", "style_issues"]:
            if key in assessment:
                all_issues.extend(assessment[key])
    
    from collections import Counter
    issue_counts = Counter(all_issues)
    
    for issue, count in issue_counts.most_common(10):
        percentage = count / assessed_files * 100 if assessed_files > 0 else 0
        print(f'  • {issue}: {count}次 ({percentage:.1f}%)')
    
    print()
    
    # 生成详细报告
    print('📄 生成详细报告...')
    report = generate_detailed_report(result)
    
    # 保存报告
    report_dir = Path(obsidian_path) / "system" / "quality" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"概念质量评估报告_{report_date}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'✅ 报告已保存: {report_path}')
    print()
    
    # 生成改进计划
    print('🎯 生成改进计划...')
    improvement_plan = generate_improvement_plan(result)
    
    plan_path = report_dir / f"概念改进计划_{report_date}.md"
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(improvement_plan)
    
    print(f'✅ 改进计划已保存: {plan_path}')
    print()
    
    print('🎉 概念质量评估完成！')
    
except ImportError as e:
    print(f'❌ 导入模块失败: {e}')
    print('请确保concept_quality_assessment.py在tools目录中')
except Exception as e:
    print(f'❌ 执行失败: {e}')
    import traceback
    traceback.print_exc()

def generate_detailed_report(result: dict) -> str:
    """生成详细报告"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = []
    report.append(f"# 概念质量评估报告")
    report.append(f"生成时间: {report_date}")
    report.append(f"评估文件: {result['summary']['assessed_files']}/{result['summary']['total_files']}")
    report.append(f"平均分数: {result['summary']['average_score']:.1f}/100")
    report.append("")
    
    # 质量分布
    report.append("## 质量分布")
    for range_name, count in result["summary"]["quality_distribution"].items():
        percentage = count / result["summary"]["assessed_files"] * 100
        report.append(f"- **{range_name}**: {count}个 ({percentage:.1f}%)")
    report.append("")
    
    # 各维度平均分
    report.append("## 各维度平均分")
    dimension_scores = result["summary"]["dimension_averages"]
    for dimension, score in dimension_scores.items():
        report.append(f"- **{dimension}**: {score:.1f}/100")
    report.append("")
    
    # 最佳概念
    report.append("## 最佳概念 (前10名)")
    best_concepts = sorted(
        [(name, data["overall_score"]) for name, data in result["assessments"].items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    for i, (concept_name, score) in enumerate(best_concepts, 1):
        assessment = result["assessments"][concept_name]
        report.append(f"### {i}. {concept_name} ({score}/100)")
        report.append(f"- **文件路径**: {assessment['file_path']}")
        report.append(f"- **评估时间**: {assessment['assessment_time']}")
        
        # 各维度分数
        dimension_scores = []
        for dim in ["basics_score", "sections_score", "metadata_score", "links_score", "style_score"]:
            if dim in assessment:
                dimension_scores.append(f"{dim.replace('_score', '')}: {assessment[dim]}")
        
        if dimension_scores:
            report.append(f"- **维度分数**: {', '.join(dimension_scores)}")
        
        # 主要优点
        strengths = []
        if assessment.get("basics_score", 0) >= 80:
            strengths.append("基础结构良好")
        if assessment.get("sections_score", 0) >= 80:
            strengths.append("章节完整")
        if assessment.get("links_score", 0) >= 80:
            strengths.append("链接丰富")
        
        if strengths:
            report.append(f"- **主要优点**: {', '.join(strengths)}")
        
        report.append("")
    
    # 需要改进的概念
    report.append("## 需要改进的概念 (后10名)")
    worst_concepts = sorted(
        [(name, data["overall_score"]) for name, data in result["assessments"].items()],
        key=lambda x: x[1]
    )[:10]
    
    for i, (concept_name, score) in enumerate(worst_concepts, 1):
        assessment = result["assessments"][concept_name]
        report.append(f"### {i}. {concept_name} ({score}/100)")
        report.append(f"- **主要问题**:")
        
        # 收集所有问题
        all_issues = []
        for key in ["basics_issues", "sections_issues", "metadata_issues", "links_issues", "style_issues"]:
            if key in assessment and assessment[key]:
                all_issues.extend(assessment[key])
        
        for issue in all_issues[:5]:  # 只显示前5个问题
            report.append(f"  - {issue}")
        
        # 改进建议
        if "suggestions" in assessment and assessment["suggestions"]:
            report.append(f"- **改进建议**:")
            for suggestion in assessment["suggestions"][:3]:  # 只显示前3条建议
                report.append(f"  - {suggestion}")
        
        report.append("")
    
    # 常见问题分析
    report.append("## 常见问题分析")
    
    # 收集所有问题
    all_issues = []
    for assessment in result["assessments"].values():
        for key in ["basics_issues", "sections_issues", "metadata_issues", "links_issues", "style_issues"]:
            if key in assessment:
                all_issues.extend(assessment[key])
    
    from collections import Counter
    issue_counts = Counter(all_issues)
    
    report.append("### 问题频率统计")
    for issue, count in issue_counts.most_common(15):
        percentage = count / result["summary"]["assessed_files"] * 100
        report.append(f"- **{issue}**: {count}次 ({percentage:.1f}%)")
    report.append("")
    
    # 改进建议总结
    report.append("## 总体改进建议")
    report.append("### 1. 立即处理的问题")
    report.append("- 完善评分低于60的概念文件")
    report.append("- 补充缺失的必要章节")
    report.append("- 增加概念之间的链接")
    report.append("")
    
    report.append("### 2. 短期优化目标")
    report.append("- 将所有概念提升到70分以上")
    report.append("- 建立概念质量监控机制")
    report.append("- 开发自动化改进工具")
    report.append("")
    
    report.append("### 3. 长期质量目标")
    report.append("- 实现所有概念80分以上")
    report.append("- 建立概念质量评估标准")
    report.append("- 实现质量自动化管理")
    report.append("")
    
    # 技术细节
    report.append("## 技术细节")
    report.append("### 评估标准")
    report.append("- **基础结构** (15%): 文件大小、标题、段落等")
    report.append("- **章节完整性** (25%): 必要章节的存在和质量")
    report.append("- **元数据** (20%): frontmatter完整性和标签")
    report.append("- **链接网络** (25%): 内部链接的数量和质量")
    report.append("- **风格规范** (15%): 格式、长度、一致性")
    report.append("")
    
    report.append("### 质量等级定义")
    report.append("- **优秀 (90-100)**: 结构完整，内容充实，链接丰富")
    report.append("- **良好 (80-89)**: 基本完整，有少量改进空间")
    report.append("- **中等 (70-79)**: 需要一定改进")
    report.append("- **需要改进 (60-69)**: 需要较多改进")
    report.append("- **较差 (<60)**: 需要重大改进或重写")
    report.append("")
    
    report.append(f"---")
    report.append(f"*报告版本: 1.0*")
    report.append(f"*评估工具: 概念质量评估系统*")
    report.append(f"*下次评估建议: 每周一次*")
    
    return "\n".join(report)

def generate_improvement_plan(result: dict) -> str:
    """生成改进计划"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    plan = []
    plan.append(f"# 概念改进计划")
    plan.append(f"生成时间: {report_date}")
    plan.append(f"基于概念质量评估报告生成")
    plan.append("")
    
    # 按优先级分组
    high_priority = []  # <60分
    medium_priority = []  # 60-79分
    low_priority = []  # 80-89分
    maintenance = []  # 90+分
    
    for concept_name, assessment in result["assessments"].items():
        score = assessment["overall_score"]
        
        if score < 60:
            high_priority.append((concept_name, assessment))
        elif score < 70:
            medium_priority.append((concept_name, assessment))
        elif score < 80:
            low_priority.append((concept_name, assessment))
        else:
            maintenance.append((concept_name, assessment))
    
    # 高优先级改进
    plan.append("## 🔴 高优先级改进 (分数 < 60)")
    plan.append("这些概念需要立即改进，质量较差。")
    plan.append("")
    
    if high_priority:
        for concept_name, assessment in sorted(high_priority, key=lambda x: x[1]["overall_score"]):
            plan.append(f"### {concept_name} ({assessment['overall_score']}/100)")
            plan.append(f"**文件**: {assessment['file_path']}")
            
            # 主要问题
            all_issues = []
            for key in ["basics_issues", "sections_issues", "metadata_issues", "links_issues", "style_issues"]:
                if key in assessment and assessment[key]:
                    all_issues.extend(assessment[key])
            
            if all_issues:
                plan.append("**主要问题**:")
                for issue in all_issues[:3]:
                    plan.append(f"- {issue}")
            
            # 改进建议
            if "suggestions" in assessment and assessment["suggestions"]:
                plan.append("**改进建议**:")
                for suggestion in assessment["suggestions"][:3]:
                    plan.append(f"- {suggestion}")
            
            plan.append("**行动计划**:")
            plan.append("1. 重新审查概念定义和结构")
            plan.append("2. 补充缺失的必要内容")
            plan.append("3. 增加相关概念链接")
            plan.append("4. 重新评估质量")
            plan.append("")
    else:
        plan.append("✅ 无高优先级改进任务")
        plan.append("")
    
    # 中优先级改进
    plan.append("## 🟡 中优先级改进 (分数 60-79)")
    plan.append("这些概念需要改进，质量中等。")
    plan.append("")
    
    if medium_priority:
        for concept_name, assessment in sorted(medium_priority, key=lambda x: x[1]["overall_score"]):
            plan.append(f"### {concept_name} ({assessment['overall_score']}/100)")
            
            # 改进建议
            if "suggestions" in assessment and assessment["suggestions"]:
                plan.append("**改进重点**:")
                for suggestion in assessment["suggestions"][:2]:
                    plan.append(f"- {suggestion}")
            
            plan.append("**行动计划**:")
            plan.append("1. 针对性改进主要问题")
            plan.append("2. 优化章节结构和内容")
            plan.append("3. 完善元数据和标签")
            plan.append("")
    else:
        plan.append("✅ 无中优先级改进任务")
        plan.append("")
    
    # 低优先级优化
    plan.append("## 🟢 低优先级优化 (分数 80-89)")
    plan.append("这些概念质量良好，可以进一步优化。")
    plan.append("")
    
    if low_priority:
        for concept_name, assessment in sorted(low_priority, key=lambda x: x[1]["overall_score"], reverse=True)[:10]:  # 只显示前10个
            plan.append(f"- **{concept_name}** ({assessment['overall_score']}/100): {assessment['file_path']}")
        
        if len(low_priority) > 10:
            plan.append(f"- ... 还有{len(low_priority)-10}个概念")
        plan.append("")
    else:
        plan.append("✅ 无低优先级优化任务")
        plan.append("")
    
    # 维护任务
    plan.append("## 🔵 维护任务 (分数 ≥ 90)")
    plan.append("这些概念质量优秀，需要保持和维护。")
    plan.append("")
    
    if maintenance:
        for concept_name, assessment in sorted(maintenance, key=lambda x: x[1]["overall_score"], reverse=True)[:5]:  # 只显示前5个
            plan.append(f"- **{concept_name}** ({assessment['overall_score']}/100): 优秀示例，可作为参考")
        
        if len(maintenance) > 5:
            plan.append(f"- ... 还有{len(maintenance)-5}个优秀概念")
        plan.append("")
    else:
        plan.append("⚠️ 暂无达到优秀标准的概念")
        plan.append("")
    
    # 时间安排
    plan.append("## 📅 改进时间安排")
    plan.append("")
    plan.append("### 第一周 (2026-03-24 至 2026-03-30)")
    plan.append("- **目标**: 完成所有高优先级改进")
    plan.append("- **任务**:")
    plan.append("  1. 处理分数<60的概念")
    plan.append("  2. 建立改进工作流")
    plan.append("  3. 开发自动化改进工具")
    plan.append("")
    
    plan.append("### 第二周 (2026-03-31 至 2026-04