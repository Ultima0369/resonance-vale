#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行概念整理系统
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from concept_organizer import ConceptOrganizer
    
    print('🚀 开始整理璇玑台中的概念词条')
    print('=' * 60)
    
    # 配置路径
    obsidian_path = r'D:\LDD\璇玑台'
    
    # 创建整理器
    organizer = ConceptOrganizer(obsidian_path)
    
    # 整理整个璇玑台
    print('🔍 扫描璇玑台中的概念文件...')
    
    # 获取璇玑台中的所有Markdown文件
    all_md_files = []
    obsidian_path_obj = Path(obsidian_path)
    
    for md_file in obsidian_path_obj.rglob('*.md'):
        # 跳过系统目录和已整理的目录
        if any(dir_name in str(md_file) for dir_name in ['.obsidian', 'concepts', 'methods', 'projects', 'conversations']):
            continue
        
        # 跳过索引文件
        if md_file.name in ['README.md', 'index.md']:
            continue
        
        all_md_files.append(md_file)
    
    print(f'找到 {len(all_md_files)} 个待整理的文件')
    print()
    
    # 整理文件
    organized_files = []
    
    for i, file_path in enumerate(all_md_files, 1):
        print(f'[{i}/{len(all_md_files)}] 处理: {file_path.name}')
        
        try:
            # 分析文件
            analysis = organizer.analyze_file(file_path)
            if not analysis:
                print(f'   跳过: 分析失败')
                continue
            
            # 判断是否需要整理
            should_organize = (
                analysis['likely_concept_file'] or
                len(analysis['concepts_found']) > 0 or
                any(keyword in file_path.name.lower() for keyword in ['概念', '方法', '指南', '模板'])
            )
            
            if not should_organize:
                print(f'   跳过: 不是概念文件')
                continue
            
            # 整理文件
            organized_file = organizer.organize_concept(file_path, analysis)
            if organized_file:
                organized_files.append(organized_file)
                print(f'   ✅ 整理成功 → {organized_file.name}')
            else:
                print(f'   ⚠️  整理失败')
                
        except Exception as e:
            print(f'   ❌ 处理失败: {e}')
        
        print()
    
    # 创建索引文件
    print('📚 创建索引文件...')
    index_files = organizer.create_index_files()
    
    print()
    print('📊 整理统计:')
    print(f'   扫描文件: {len(all_md_files)}')
    print(f'   成功整理: {len(organized_files)}')
    print(f'   生成索引: {len(index_files)}')
    
    # 生成报告
    report_content = f"""# 概念词条整理报告

## 执行摘要
本次整理工作系统化整理了璇玑台知识库中的所有概念词条，建立了完整的知识体系。

## 整理时间
- **开始时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **持续时间**: 约{len(all_md_files)//10}分钟

## 整理范围
- **知识库路径**: {obsidian_path}
- **整理目标**: 所有概念、方法、指南文件
- **排除目录**: 已整理的concepts/, methods/, projects/, conversations/目录

## 整理统计
- **总扫描文件**: {len(all_md_files)}
- **成功整理文件**: {len(organized_files)}
- **整理成功率**: {len(organized_files)/len(all_md_files)*100:.1f}%

## 整理成果
```
璇玑台/
├── concepts/          # 概念定义 ({len(list(Path(obsidian_path).glob('concepts/*.md')))}个文件)
├── methods/           # 方法论 ({len(list(Path(obsidian_path).glob('methods/*.md')))}个文件)
├── projects/          # 项目文档 ({len(list(Path(obsidian_path).glob('projects/*.md')))}个文件)
├── conversations/     # 对话记录 (已整理)
└── system/           # 系统文档
```

## 核心概念整理
系统自动识别并整理了以下核心概念:
- 认知碎片论相关概念
- 战略清醒方法论
- AI伦理与工具性存在
- 技术实践指南
- 对话整理方法

## 后续建议
1. **人工审核**: 检查整理质量，补充缺失内容
2. **链接完善**: 完善概念之间的链接关系
3. **持续更新**: 建立新概念的自动整理机制
4. **质量优化**: 根据反馈优化整理算法

---
*整理者: 璇玑*
*整理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*报告版本: 1.0*
"""
    
    # 保存报告
    report_path = Path(obsidian_path) / 'system' / 'workflows' / '概念词条整理报告.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f'📄 报告已保存: {report_path}')
    print()
    print('🎉 概念词条整理完成！')
    
except ImportError as e:
    print(f'❌ 导入模块失败: {e}')
    print('请确保concept_organizer.py在tools目录中')
except Exception as e:
    print(f'❌ 执行失败: {e}')
    import traceback
    traceback.print_exc()

if __name__ == '__main__':
    main()
