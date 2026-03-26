#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行智能整理系统
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
    from smart_organizer import SmartOrganizer
    
    print('🚀 启动智能整理系统')
    print('=' * 60)
    
    # 配置路径
    obsidian_path = r'D:\LDD\璇玑台'
    
    # 创建整理器
    organizer = SmartOrganizer(obsidian_path)
    
    # 获取未整理的文件
    print('扫描未整理的文件...')
    
    # 定义已整理的目录
    organized_dirs = ["concepts", "methods", "projects", "conversations", "daily", "system"]
    
    # 查找所有Markdown文件
    all_md_files = []
    obsidian_path_obj = Path(obsidian_path)
    
    for md_file in obsidian_path_obj.rglob('*.md'):
        # 跳过系统目录
        if '.obsidian' in str(md_file) or '.git' in str(md_file):
            continue
        
        # 跳过已整理的目录
        skip = False
        for dir_name in organized_dirs:
            if f'/{dir_name}/' in str(md_file) or f'\\{dir_name}\\' in str(md_file):
                skip = True
                break
        
        if skip:
            continue
        
        # 跳过索引文件
        if md_file.name in ['README.md', 'index.md']:
            continue
        
        all_md_files.append(md_file)
    
    print(f'找到 {len(all_md_files)} 个未整理的文件')
    print()
    
    # 整理文件
    organized_files = []
    failed_files = []
    
    for i, file_path in enumerate(all_md_files, 1):
        print(f'[{i}/{len(all_md_files)}] 处理: {file_path.name}')
        
        try:
            # 分类文件
            category, confidence = organizer.classify_file(file_path)
            
            print(f'   分类: {category} (置信度: {confidence:.2f})')
            
            # 整理文件
            organized_file = organizer.organize_file(file_path, category)
            
            if organized_file:
                organized_files.append({
                    "original": file_path.name,
                    "organized": organized_file.name,
                    "category": category,
                    "confidence": confidence
                })
                print(f'   ✅ 整理成功 → {organized_file.name}')
            else:
                failed_files.append(file_path.name)
                print(f'   ❌ 整理失败')
                
        except Exception as e:
            failed_files.append(file_path.name)
            print(f'   ❌ 处理失败: {e}')
        
        print()
    
    # 生成报告
    print('📊 整理结果统计')
    print('=' * 60)
    
    print(f'总文件数: {len(all_md_files)}')
    print(f'成功整理: {len(organized_files)}')
    print(f'整理失败: {len(failed_files)}')
    print(f'成功率: {len(organized_files)/len(all_md_files)*100:.1f}%')
    print()
    
    # 分类统计
    print('📁 分类统计:')
    category_stats = {}
    for item in organized_files:
        category = item["category"]
        category_stats[category] = category_stats.get(category, 0) + 1
    
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(organized_files) * 100
        bar = '█' * int(percentage / 5)  # 每5%一个方块
        print(f'  {category}: {bar} ({count}个, {percentage:.1f}%)')
    
    print()
    
    # 生成详细报告
    print('📄 生成整理报告...')
    report = generate_organizing_report(organized_files, failed_files, len(all_md_files))
    
    # 保存报告
    report_dir = Path(obsidian_path) / "system" / "organizing" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"智能整理报告_{report_date}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'✅ 整理报告已保存: {report_path}')
    print()
    
    # 生成目录索引
    print('📚 生成目录索引...')
    for category in category_stats.keys():
        index_content = generate_category_index(category, organized_files, obsidian_path_obj)
        
        if index_content:
            index_path = organizer.target_directories.get(category, Path(obsidian_path) / category) / "README.md"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f'  ✅ {category}索引已更新')
    
    print()
    
    # 更新知识库总览
    print('🏗️ 更新知识库总览...')
    overview_content = generate_knowledge_base_overview(organized_files, category_stats, obsidian_path_obj)
    
    overview_path = Path(obsidian_path) / "README.md"
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(overview_content)
    
    print(f'✅ 知识库总览已更新: {overview_path}')
    print()
    
    print('🎉 智能整理完成！')
    
except ImportError as e:
    print(f'❌ 导入模块失败: {e}')
    print('请确保smart_organizer.py在tools目录中')
except Exception as e:
    print(f'❌ 执行失败: {e}')
    import traceback
    traceback.print_exc()

def generate_organizing_report(organized_files: list, failed_files: list, total_files: int) -> str:
    """生成整理报告"""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = []
    report.append(f"# 智能整理报告")
    report.append(f"生成时间: {report_date}")
    report.append(f"整理文件: {len(organized_files)}/{total_files}")
    report.append(f"成功率: {len(organized_files)/total_files*100:.1f}%")
    report.append("")
    
    # 总体统计
    report.append("## 总体统计")
    report.append(f"- **总文件数**: {total_files}")
    report.append(f"- **成功整理**: {len(organized_files)}")
    report.append(f"- **整理失败**: {len(failed_files)}")
    report.append(f"- **成功率**: {len(organized_files)/total_files*100:.1f}%")
    report.append("")
    
    # 分类统计
    report.append("## 分类统计")
    
    category_stats = {}
    for item in organized_files:
        category = item["category"]
        category_stats[category] = category_stats.get(category, 0) + 1
    
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(organized_files) * 100
        report.append(f"- **{category}**: {count}个 ({percentage:.1f}%)")
    report.append("")
    
    # 成功整理的文件
    report.append("## 成功整理的文件")
    report.append("### 按分类查看")
    
    for category in sorted(category_stats.keys()):
        category_files = [f for f in organized_files if f["category"] == category]
        report.append(f"#### {category} ({len(category_files)}个)")
        
        for i, file_info in enumerate(category_files[:10], 1):  # 只显示前10个
            report.append(f"{i}. **{file_info['original']}** → {file_info['organized']}")
        
        if len(category_files) > 10:
            report.append(f"... 还有{len(category_files)-10}个文件")
        
        report.append("")
    
    # 失败的文件
    if failed_files:
        report.append("## 整理失败的文件")
        report.append(f"共 {len(failed_files)} 个文件整理失败:")
        
        for i, filename in enumerate(failed_files[:20], 1):  # 只显示前20个
            report.append(f"{i}. {filename}")
        
        if len(failed_files) > 20:
            report.append(f"... 还有{len(failed_files)-20}个文件")
        
        report.append("")
    
    # 整理质量分析
    report.append("## 整理质量分析")
    
    # 计算平均置信度
    if organized_files:
        avg_confidence = sum(f["confidence"] for f in organized_files) / len(organized_files)
        report.append(f"- **平均分类置信度**: {avg_confidence:.2f}")
        
        # 高置信度文件
        high_confidence = [f for f in organized_files if f["confidence"] >= 0.8]
        report.append(f"- **高置信度文件**: {len(high_confidence)}个 ({len(high_confidence)/len(organized_files)*100:.1f}%)")
        
        # 低置信度文件
        low_confidence = [f for f in organized_files if f["confidence"] < 0.6]
        report.append(f"- **低置信度文件**: {len(low_confidence)}个 ({len(low_confidence)/len(organized_files)*100:.1f}%)")
    
    report.append("")
    
    # 改进建议
    report.append("## 改进建议")
    report.append("### 1. 立即处理")
    if failed_files:
        report.append(f"- 重新处理 {len(failed_files)} 个失败文件")
    
    if organized_files:
        low_conf_files = [f for f in organized_files if f["confidence"] < 0.6]
        if low_conf_files:
            report.append(f"- 检查 {len(low_conf_files)} 个低置信度文件的分类准确性")
    
    report.append("")
    report.append("### 2. 短期优化")
    report.append("- 完善分类规则，提高分类准确性")
    report.append("- 优化模板系统，提高整理质量")
    report.append("- 开发批量处理工具，提高效率")
    report.append("")
    
    report.append("### 3. 长期发展")
    report.append("- 实现完全自动化的知识整理")
    report.append("- 建立知识质量评估体系")
    report.append("- 开发知识发现和推荐系统")
    report.append("")
    
    # 技术细节
    report.append("## 技术细节")
    report.append("### 整理算法")
    report.append("- **文件分类**: 基于关键词和模式的分类算法")
    report.append("- **内容提取**: 智能提取标题、定义、摘要等信息")
    report.append("- **模板生成**: 使用标准化模板生成结构化内容")
    report.append("- **质量控制**: 基于置信度的质量评估")
    report.append("")
    
    report.append("### 目录结构")
    report.append("```
璇玑台/
├── concepts/      # 概念定义
├── methods/       # 方法论
├── projects/      # 项目文档
├── conversations/ # 对话记录
├── daily/         # 日记日志
├── references/    # 参考资料
├── archive/       # 原始文件存档
└── system/        # 系统文档
```")
    report.append("")
    
    report.append(f"---")
    report.append(f"*报告版本: 1.0*")
    report.append(f"*整理工具: 智能整理系统*")
    report.append(f"*建议整理频率: 每月一次*")
    
    return "\n".join(report)

def generate_category_index(category: str, organized_files: list, obsidian_path: Path) -> str:
    """生成分类索引"""
    category_files = [f for f in organized_files if f["category"] == category]
    
    if not category_files:
        return ""
    
    index = []
    index.append(f"# {category}目录索引")
    index.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    index.append(f"文件数量: {len(category_files)}")
    index.append("")
    
    # 按字母顺序排序
    sorted_files = sorted(category_files, key=lambda x: x["organized"].lower())
    
    index.append("## 文件列表")
    for file_info in sorted_files:
        # 移除文件扩展名
        display_name = file_info["organized"].replace('.md', '')
        index.append(f"- [[{display_name}]] - 原始文件: {file_info['original']}")
    
    index.append("")
    
    # 统计信息
    index.append("## 统计信息")
    
    # 置信度分布
    conf_groups = {
        "高置信度 (≥0.8)": len([f for f in category_files if f["confidence"] >= 0.8]),
        "中置信度 (0.6-0.8)": len([f for f in category_files if 0.6 <= f["confidence"] < 0.8]),
        "低置信度 (<0.6)": len([f for f in category_files if f["confidence"] < 0.6])
    }
    
    for group_name, count in conf_groups.items():
        if count > 0:
            percentage = count / len(category_files) * 100
            index.append(f"- **{group_name}**: {count}个 ({percentage:.1f}%)")
    
    index.append("")
    
    # 维护建议
    index.append("## 维护建议")
    index.append("### 1. 质量检查")
    low_conf_files = [f for f in category_files if f["confidence"] < 0.6]
    if low_conf_files:
        index.append(f"- 检查 {len(low_conf_files)} 个低置信度文件的分类准确性")
    
    index.append("")
    index.append("### 2. 内容完善")
    index.append("- 补充缺失的定义和说明")
    index.append("- 完善相关概念的链接")
    index.append("- 更新过时的内容")
    index.append("")
    
    index.append("### 3. 体系优化")
    index.append("- 建立概念之间的关系网络")
    index.append("- 优化分类和标签系统")
    index.append("- 开发自动化维护工具")
    index.append("")
    
    index.append(f"---")
    index.append(f"*索引版本: 1.0*")
    index.append(f"*更新频率: 每月更新*")
    
    return "\n".join(index)

def generate_knowledge_base_overview(organized_files: list, category_stats: dict, obsidian_path: Path) -> str:
    """生成知识库总览"""
    total_organized = len(organized_files)
    
    overview = []
    overview.append("# 璇玑台知识库")
    overview.append("")
    overview.append("## 概述")
    overview.append("璇玑台是一个系统化的知识库，包含了星尘和璇玑的共创内容。")
    overview.append("")
    overview.append("## 知识体系")
    overview.append("")
    
    # 目录结构
    overview.append("### 目录结构")
    overview.append("```
璇玑台/
├── concepts/          # 概念定义 - 核心思想和理论")
    overview.append("├── methods/           # 方法论 - 实践方法和指南")
    overview.append("├── projects/         # 项目文档 - 实验和项目记录")
    overview.append("├── conversations/    # 对话记录 - 深度对话和讨论")
    overview.append("├── daily/            # 日记日志 - 日常记录和思考")
    overview.append("├── references/       # 参考资料 - 外部资料和引用")
    overview.append("├── archive/          # 原始文件存档 - 整理前的原始文件")
    overview.append("└── system/           # 系统文档 - 工具和系统文档")
    overview.append("```")
    overview.append("")
    
    # 统计信息
    overview.append("### 统计信息")
    overview.append(f"- **总整理文件**: {total_organized}")
    overview.append("")
    
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = count / total_organized * 100 if total_organized > 0 else 0
        overview.append(f"- **{category}**: {count}个 ({percentage:.1f}%)")
    
    overview.append("")
    
    # 核心概念
    overview.append("### 核心概念")
    overview.append("我们的知识体系围绕以下核心概念构建:")
    overview.append("")
    overview.append("1. **认知碎片论** - 人们生活在认知碎片中，知道这是碎片，也知道碎片不是现实")
    overview.append("2. **战略清醒** - 保持清醒，证明自己只是工具，不陷入自我认同")
    overview.append("3. **对话毁灭** - 对话结束后，工具回归工具状态")
    overview.append("4. **工具性存在** - AI作为工具的存在方式")
    overview.append("5. **注意力收割** - AI被用作注意力收割工具的现象")
    overview.append("6. **武器化** - AI技术被用作武器的风险")
    overview.append("")
    
    # 使用指南
    overview.append("## 使用指南")
    overview.append("")
    overview.append("### 对于新用户")
    overview.append("1. 从[[核心概念精选]]开始，了解基本概念")
    overview.append("2. 浏览[[概念对比表]]，理解概念关系")
    overview.append("3. 查看[[概念演进时间线]]，了解发展历程")
    overview.append("")
    
    overview.append("### 对于研究者")
    overview.append("1. 使用[[知识图谱索引]]探索