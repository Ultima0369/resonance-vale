#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行专业质量保证系统
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
import sys
sys.path.append(str(current_dir))

try:
    from professional_quality_system import ProfessionalQualitySystem, ContentType, QualityLevel
    
    print('🏆 启动专业质量保证系统')
    print('=' * 60)
    
    # 配置路径
    obsidian_path = r'D:\LDD\璇玑台'
    
    # 创建质量系统
    quality_system = ProfessionalQualitySystem(obsidian_path)
    
    # 评估核心目录
    print('评估核心知识目录...')
    
    core_directories = [
        ("concepts", ContentType.CONCEPT),
        ("methods", ContentType.METHOD),
        ("projects", ContentType.PROJECT),
        ("conversations/璇玑-星尘", ContentType.CONVERSATION)
    ]
    
    all_assessments = []
    
    for dir_name, expected_type in core_directories:
        dir_path = Path(obsidian_path) / dir_name
        
        if not dir_path.exists():
            print(f"目录不存在: {dir_name}")
            continue
        
        print(f"\n📁 评估目录: {dir_name}")
        print("-" * 40)
        
        # 获取目录下的所有Markdown文件
        md_files = list(dir_path.rglob("*.md"))
        md_files = [f for f in md_files if f.name != "README.md"]
        
        print(f"文件数量: {len(md_files)}")
        
        # 评估每个文件
        dir_assessments = []
        for i, file_path in enumerate(md_files[:20], 1):  # 只评估前20个文件
            print(f"[{i}/{min(20, len(md_files))}] 评估: {file_path.name}", end="")
            
            assessment = quality_system.assess_file(file_path)
            dir_assessments.append(assessment)
            
            # 显示简单结果
            score = assessment.overall_score
            level = assessment.quality_level.value
            
            if score >= 80:
                print(f" ✅ {score:.1f}分 ({level})")
            elif score >= 60:
                print(f" ⚠️  {score:.1f}分 ({level})")
            else:
                print(f" ❌ {score:.1f}分 ({level})")
        
        all_assessments.extend(dir_assessments)
        
        # 目录统计
        if dir_assessments:
            avg_score = sum(a.overall_score for a in dir_assessments) / len(dir_assessments)
            print(f"\n📊 目录平均分: {avg_score:.1f}")
    
    print()
    print('📈 总体质量分析')
    print('=' * 60)
    
    if not all_assessments:
        print("没有评估到任何文件")
        sys.exit(0)
    
    # 总体统计
    total_files = len(all_assessments)
    avg_score = sum(a.overall_score for a in all_assessments) / total_files
    
    print(f'评估文件: {total_files}个')
    print(f'平均分数: {avg_score:.1f}/100')
    print()
    
    # 质量等级分布
    print('🏅 质量等级分布:')
    level_counts = {}
    for level in QualityLevel:
        level_counts[level] = 0
    
    for assessment in all_assessments:
        level_counts[assessment.quality_level] += 1
    
    for level in [QualityLevel.EXCELLENT, QualityLevel.GOOD, QualityLevel.FAIR, 
                  QualityLevel.NEEDS_IMPROVEMENT, QualityLevel.POOR]:
        count = level_counts[level]
        percentage = count / total_files * 100
        bar = '█' * int(percentage / 5)  # 每5%一个方块
        print(f'  {level.value}: {bar} ({count}个, {percentage:.1f}%)')
    
    print()
    
    # 按类型统计
    print('📊 按内容类型统计:')
    type_stats = {}
    for assessment in all_assessments:
        content_type = assessment.content_type
        if content_type not in type_stats:
            type_stats[content_type] = {"count": 0, "total_score": 0, "files": []}
        
        type_stats[content_type]["count"] += 1
        type_stats[content_type]["total_score"] += assessment.overall_score
        type_stats[content_type]["files"].append(assessment.file_path.name)
    
    for content_type, stats in type_stats.items():
        avg_type_score = stats["total_score"] / stats["count"]
        print(f'  {content_type.value}: {stats["count"]}个, 平均{avg_type_score:.1f}分')
    
    print()
    
    # 最佳和最差文件
    print('🏆 最佳质量文件 (前5名):')
    best_files = sorted(all_assessments, key=lambda x: x.overall_score, reverse=True)[:5]
    
    for i, assessment in enumerate(best_files, 1):
        print(f'  {i}. {assessment.file_path.name} - {assessment.overall_score:.1f}分 ({assessment.quality_level.value})')
    
    print()
    
    print('⚠️ 最需要改进的文件 (后5名):')
    worst_files = sorted(all_assessments, key=lambda x: x.overall_score)[:5]
    
    for i, assessment in enumerate(worst_files, 1):
        print(f'  {i}. {assessment.file_path.name} - {assessment.overall_score:.1f}分 ({assessment.quality_level.value})')
    
    print()
    
    # 常见问题分析
    print('🔍 常见问题分析:')
    all_issues = []
    for assessment in all_assessments:
        all_issues.extend(assessment.issues)
    
    from collections import Counter
    issue_counts = Counter(all_issues)
    
    for issue, count in issue_counts.most_common(10):
        percentage = count / total_files * 100
        print(f'  • {issue}: {count}次 ({percentage:.1f}%)')
    
    print()
    
    # 生成专业质量报告
    print('📄 生成专业质量报告...')
    report = generate_professional_quality_report(all_assessments, quality_system)
    
    # 保存报告
    report_dir = Path(obsidian_path) / "system" / "quality" / "professional_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"专业质量报告_{report_date}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'✅ 专业质量报告已保存: {report_path}')
    print()
    
    # 生成改进行动计划
    print('🎯 生成改进行动计划...')
    action_plan = generate_quality_action_plan(all_assessments, worst_files)
    
    plan_path = report_dir / f"质量改进计划_{report_date}.md"
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(action_plan)
    
    print(f'✅ 改进计划已保存: {plan_path}')
    print()
    
    # 保存质量数据库
    quality_system.save_history()
    print('💾 质量数据已保存到数据库')
    print()
    
    print('🎉 专业质量评估完成！')
    
except ImportError as e:
    print(f'❌ 导入模块失败: {e}')
    print('请确保professional_quality_system.py在tools目录中')
except Exception as e:
    print(f'❌ 执行失败: {e}')
    import traceback
    traceback.print_exc()

def generate_professional_quality_report(assessments: list, quality_system) -> str:
    """生成专业质量报告"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_files = len(assessments)
    
    # 计算统计信息
    avg_score = sum(a.overall_score for a in assessments) / total_files if total_files > 0 else 0
    
    # 质量等级分布
    level_counts = {}
    for level in QualityLevel:
        level_counts[level] = 0
    
    for assessment in assessments:
        level_counts[assessment.quality_level] += 1
    
    report = []
    report.append(f"# 璇玑台专业质量报告")
    report.append(f"生成时间: {report_date}")
    report.append(f"评估文件: {total_files}个")
    report.append(f"平均质量分数: {avg_score:.1f}/100")
    report.append("")
    
    # 执行摘要
    report.append("## 执行摘要")
    report.append("")
    
    # 质量状态
    excellent_count = level_counts[QualityLevel.EXCELLENT]
    good_count = level_counts[QualityLevel.GOOD]
    fair_count = level_counts[QualityLevel.FAIR]
    needs_improvement_count = level_counts[QualityLevel.NEEDS_IMPROVEMENT]
    poor_count = level_counts[QualityLevel.POOR]
    
    good_above = excellent_count + good_count
    good_above_percentage = good_above / total_files * 100 if total_files > 0 else 0
    
    report.append(f"### 质量状态")
    report.append(f"- **优秀/良好文件**: {good_above}个 ({good_above_percentage:.1f}%)")
    report.append(f"- **需要改进文件**: {needs_improvement_count + poor_count}个 ({(needs_improvement_count + poor_count)/total_files*100:.1f}%)")
    report.append("")
    
    # 关键发现
    report.append("### 关键发现")
    
    if avg_score >= 80:
        report.append("✅ **整体质量优秀**: 知识库整体质量达到优秀水平")
    elif avg_score >= 70:
        report.append("⚠️ **整体质量良好**: 知识库整体质量良好，有改进空间")
    elif avg_score >= 60:
        report.append("⚠️ **整体质量中等**: 需要系统性改进")
    else:
        report.append("❌ **整体质量需要改进**: 需要重大改进")
    
    if poor_count > total_files * 0.1:  # 超过10%的文件质量较差
        report.append(f"❌ **存在质量问题**: {poor_count}个文件质量较差，需要优先处理")
    
    report.append("")
    
    # 详细分析
    report.append("## 详细质量分析")
    report.append("")
    
    # 质量等级分布
    report.append("### 质量等级分布")
    for level in [QualityLevel.EXCELLENT, QualityLevel.GOOD, QualityLevel.FAIR, 
                  QualityLevel.NEEDS_IMPROVEMENT, QualityLevel.POOR]:
        count = level_counts[level]
        percentage = count / total_files * 100
        report.append(f"- **{level.value}** ({count}个, {percentage:.1f}%): {get_level_description(level)}")
    report.append("")
    
    # 按内容类型分析
    report.append("### 按内容类型分析")
    
    type_stats = {}
    for assessment in assessments:
        content_type = assessment.content_type
        if content_type not in type_stats:
            type_stats[content_type] = {"count": 0, "total_score": 0, "files": []}
        
        type_stats[content_type]["count"] += 1
        type_stats[content_type]["total_score"] += assessment.overall_score
        type_stats[content_type]["files"].append(assessment.file_path.name)
    
    for content_type, stats in type_stats.items():
        avg_type_score = stats["total_score"] / stats["count"]
        report.append(f"- **{content_type.value}**: {stats['count']}个文件，平均{avg_type_score:.1f}分")
    
    report.append("")
    
    # 最佳实践案例
    report.append("## 最佳实践案例")
    report.append("")
    
    best_files = sorted(assessments, key=lambda x: x.overall_score, reverse=True)[:3]
    
    for i, assessment in enumerate(best_files, 1):
        report.append(f"### {i}. {assessment.file_path.name} ({assessment.overall_score:.1f}分)")
        report.append(f"- **质量等级**: {assessment.quality_level.value}")
        report.append(f"- **内容类型**: {assessment.content_type.value}")
        report.append(f"- **文件路径**: {assessment.file_path}")
        
        # 优点分析
        if assessment.metrics_scores:
            best_metrics = sorted(assessment.metrics_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            report.append(f"- **优势指标**:")
            for metric_name, score in best_metrics:
                report.append(f"  - {metric_name}: {score:.1f}分")
        
        report.append("")
    
    # 问题分析
    report.append("## 问题分析与改进建议")
    report.append("")
    
    # 收集所有问题
    all_issues = []
    for assessment in assessments:
        all_issues.extend(assessment.issues)
    
    from collections import Counter
    issue_counts = Counter(all_issues)
    
    if issue_counts:
        report.append("### 常见问题统计")
        for issue, count in issue_counts.most_common(10):
            percentage = count / total_files * 100
            report.append(f"- **{issue}**: {count}次 ({percentage:.1f}%)")
        
        report.append("")
    
    # 改进建议
    report.append("### 系统性改进建议")
    
    # 基于问题分析的建议
    if "缺少定义" in str(issue_counts):
        report.append("1. **完善概念定义**: 建立定义模板，确保每个概念都有清晰定义")
    
    if "链接不足" in str(issue_counts):
        report.append("2. **加强概念链接**: 建立概念关系网络，确保重要概念有足够链接")
    
    if "格式不规范" in str(issue_counts):
        report.append("3. **统一格式标准**: 建立格式检查工具，确保格式一致性")
    
    if avg_score < 70:
        report.append("4. **建立质量监控**: 建立定期质量评估机制")
    
    report.append("5. **开展质量培训**: 对内容创建者进行质量标准和工具培训")
    report.append("")
    
    # 技术指标
    report.append("## 技术指标与评估方法")
    report.append("")
    
    report.append("### 评估指标体系")
    report.append("质量评估基于以下指标体系:")
    report.append("- **定义清晰度** (25%): 概念定义是否清晰准确")
    report.append("- **观点完整性** (20%): 核心观点是否完整系统")
    report.append("- **应用明确性** (15%): 应用场景是否清晰具体")
    report.append("- **关系丰富度** (20%): 相关概念链接是否丰富")
    report.append("- **案例充实度** (10%): 是否有具体案例支持")
    report.append("- **格式规范性** (10%): 是否符合格式标准")
    report.append("")
    
    report.append("### 质量等级标准")
    report.append("- **优秀 (90-100分)**: 各方面表现优秀，可作为典范")
    report.append("- **良好 (80-89分)**: 质量良好，有少量改进空间")
    report.append("- **中等 (70-79分)**: 质量中等，需要一定改进")
    report.append("- **需要改进 (60-69分)**: 需要较多改进")
    report.append("- **较差 (<60分)**: 需要重大改进或重写")
    report.append("")
    
    # 后续计划
    report.append("## 后续质量提升计划")
    report.append("")
    
    report.append("### 短期计划 (1-2周)")
    report.append("1. 处理质量较差文件 (<60分)")
    report.append("2. 建立质量改进工作流")
    report.append("3. 开发自动化质量检查工具")
    report.append("")
    
    report.append("### 中期计划 (1-2月)")
    report.append("1. 实现所有文件70分以上")
    report.append("2. 建立质量监控体系")
    report.append("3. 开展质量改进培训")
    report.append("")
    
    report.append("### 长期目标 (3-6月)")
    report.append("1. 实现知识库整体质量80分以上")
    report.append("2. 建立知识质量认证体系")
    report.append("3. 实现质量自动化管理")
    report.append("")
    
    report.append(f"---")
    report.append(f"*报告版本: 1.0*")
    report.append(f"*评估系统: 专业质量保证系统*")
    report.append(f"*评估时间: {report_date}*")
    report.append(f"*下次评估建议: 每月一次*")
    
    return "\n".join(report)

def get_level_description(level: QualityLevel) -> str:
    """获取质量等级描述"""
    descriptions = {
        QualityLevel.EXCELLENT: "各方面表现优秀，可作为典范",
        QualityLevel.GOOD: "质量良好，有少量改进空间",
        QualityLevel.FAIR: "质量中等，需要一定改进",
        QualityLevel.NEEDS_IMPROVEMENT: "需要较多改进",
        QualityLevel.POOR: "需要重大改进或重写"
    }
    return descriptions.get(level, "")

def generate_quality_action_plan(assessments: list, worst_files: list) -> str:
    """生成质量改进行动计划"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%