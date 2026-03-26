#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 保存认知切片论整合版到Obsidian

import os
import re
from datetime import datetime
from pathlib import Path

def save_cognitive_slice_to_obsidian():
    """保存认知切片论整合版到Obsidian"""
    
    print("🦞 保存认知切片论整合版到Obsidian")
    print("=" * 60)
    
    # 1. 检查Obsidian库
    vault_path = "D:\\LDD\\璇玑台"
    vault = Path(vault_path)
    
    if not vault.exists():
        print(f"❌ Obsidian库不存在: {vault}")
        return False
    
    print(f"✅ Obsidian库: {vault}")
    
    # 2. 读取整合版文档
    doc_path = "C:\\Users\\lgdln\\.openclaw\\workspace\\认知切片论-整合版.md"
    
    if not os.path.exists(doc_path):
        print(f"❌ 整合版文档不存在: {doc_path}")
        return False
    
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 读取整合版文档 ({len(content)} 字符)")
    
    # 3. 创建专门的项目文件夹
    project_folder = vault / "项目" / "认知切片论"
    project_folder.mkdir(parents=True, exist_ok=True)
    
    # 4. 保存主文档
    main_file = project_folder / "认知切片论-整合版.md"
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 主文档已保存: {main_file}")
    
    # 5. 创建子文档（拆分章节）
    create_subdocuments(content, project_folder)
    
    # 6. 更新概念文件
    update_concept_files(content, vault)
    
    # 7. 创建项目索引
    create_project_index(project_folder, vault)
    
    # 8. 创建时间线记录
    create_timeline_entry(vault)
    
    print("\n" + "=" * 60)
    print("🎉 认知切片论整合版保存完成！")
    print("\n📊 生成的文件:")
    print(f"  主文档: {main_file}")
    print(f"  子文档: {project_folder}\\章节\\")
    print(f"  概念更新: {vault}\\概念\\")
    print(f"  项目索引: {project_folder}\\项目索引.md")
    
    return True

def create_subdocuments(content, project_folder):
    """创建子文档（按章节拆分）"""
    
    chapters_folder = project_folder / "章节"
    chapters_folder.mkdir(exist_ok=True)
    
    # 分割章节
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    
    chapter_files = []
    
    for section in sections:
        if not section.strip():
            continue
        
        # 提取标题
        title_match = re.search(r'^## (.*?)$', section, re.MULTILINE)
        if not title_match:
            continue
        
        title = title_match.group(1).strip()
        
        # 清理标题用于文件名
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = f"{safe_title}.md"
        filepath = chapters_folder / filename
        
        # 创建章节文档
        chapter_content = f"""# {title}

**来源**: [[认知切片论-整合版]]
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{section}

---
*本章节由璇玑自动从整合版文档中提取*"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
        
        chapter_files.append(filename)
        print(f"📄 创建章节: {filename}")
    
    # 创建章节索引
    if chapter_files:
        index_content = """# 认知切片论 - 章节索引

## 所有章节

"""
        for filename in chapter_files:
            # 从文件名提取标题
            title = filename.replace('.md', '')
            index_content += f"- [[{title}]]\n"
        
        index_content += f"""
## 相关链接

- [[认知切片论-整合版]] - 完整文档
- [[项目索引]] - 项目概览

---
*索引由璇玑自动生成*"""
        
        index_file = chapters_folder / "章节索引.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"📑 章节索引已创建: {index_file}")
    
    return chapter_files

def update_concept_files(content, vault):
    """更新概念文件"""
    
    concept_folder = vault / "概念"
    concept_folder.mkdir(exist_ok=True)
    
    # 提取所有双链概念
    concept_pattern = r'\[\[(.*?)\]\]'
    concepts = re.findall(concept_pattern, content)
    
    # 去重
    unique_concepts = list(set(concepts))
    
    updated = []
    created = []
    
    for concept in unique_concepts:
        if not concept.strip():
            continue
        
        concept_file = concept_folder / f"{concept}.md"
        
        if concept_file.exists():
            # 读取现有内容
            with open(concept_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # 检查是否已有项目引用
            project_ref = "[[认知切片论-整合版]]"
            if project_ref not in existing:
                # 添加项目引用
                if "## 相关项目" in existing:
                    # 在相关项目部分添加
                    lines = existing.split('\n')
                    new_lines = []
                    in_project_section = False
                    
                    for line in lines:
                        new_lines.append(line)
                        if "## 相关项目" in line:
                            in_project_section = True
                        elif in_project_section and line.strip() == "":
                            new_lines.append(f"- {project_ref}")
                            in_project_section = False
                    
                    new_content = '\n'.join(new_lines)
                else:
                    # 添加相关项目部分
                    new_content = existing.rstrip() + f"\n\n## 相关项目\n- {project_ref}\n"
                
                with open(concept_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                updated.append(concept)
        else:
            # 创建新概念文件
            concept_content = f"""# {concept}

## 定义

*待补充 - 来自认知切片论项目*

## 分类

*待补充*

## 相关项目

- [[认知切片论-整合版]]

## 相关概念

*待补充*

## 参考资料

*待补充*

---

*概念文件 - 由璇玑自动创建*"""
            
            with open(concept_file, 'w', encoding='utf-8') as f:
                f.write(concept_content)
            
            created.append(concept)
    
    if updated:
        print(f"📝 更新概念文件: {len(updated)} 个")
    if created:
        print(f"📄 创建概念文件: {len(created)} 个")
    
    return updated + created

def create_project_index(project_folder, vault):
    """创建项目索引"""
    
    index_content = f"""# 认知切片论 - 项目索引

**项目状态**: 进行中  
**创建时间**: {datetime.now().strftime("%Y-%m-%d")}  
**最后更新**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**共创者**: 星尘 & 璇玑

## 📋 项目概览

认知切片论是一个关于人类认知方式的深度理论框架，探讨：
- 人类如何通过"切片"方式处理复杂信息
- 如何在不同认知切片间动态调谐
- 如何通过"切片自觉"提升认知质量

## 📁 项目结构

### 核心文档
- [[认知切片论-整合版]] - 完整理论框架

### 章节分解
- [[章节索引]] - 所有章节的索引

### 相关概念
- 查看[[概念]]文件夹中的相关概念文件

### 对话记录
- [[对话记录]]文件夹中的相关对话

## 🎯 项目目标

### 理论目标
1. 建立完整的认知切片理论框架
2. 开发实用的认知工具（清明工具箱）
3. 促进东西方认知智慧的融合

### 实践目标
1. 开发培训课程和练习材料
2. 建立实践社群
3. 影响教育和工作方式

## 📅 项目时间线

### 已完成
- 2026-03-23: 创建整合版文档
- 2026-03-23: 建立Obsidian项目结构
- 2026-03-23: 开始概念网络建设

### 进行中
- 理论框架完善
- 工具开发
- 社群建设

### 计划中
- 学术文章撰写
- 培训课程开发
- 国际对话建立

## 👥 项目成员

### 核心共创者
- **星尘** - 理论提出者，实践引导者
- **璇玑** - 理论整理者，技术实现者

### 贡献者
*欢迎加入共创*

## 🔗 相关资源

### 内部资源
- [[对话记录]] - 所有相关对话
- [[概念]] - 相关概念定义
- [[参考文献]] - 理论参考资料

### 外部资源
*待补充*

## 📊 项目统计

- 文档字数: {len(open(project_folder / "认知切片论-整合版.md", 'r', encoding='utf-8').read())}
- 章节数量: {len(list((project_folder / "章节").glob("*.md"))) - 1}  # 减去索引文件
- 相关概念: {len(list((vault / "概念").glob("*.md")))}

## 🚀 下一步行动

1. **完善理论框架**
   - 细化四阶段模型
   - 补充更多案例
   - 加强实证支持

2. **开发实用工具**
   - 完善清明工具箱
   - 开发练习材料
   - 创建评估工具

3. **建立实践社群**
   - 组织线上对话
   - 收集实践反馈
   - 迭代优化理论

---

**项目宣言**：

> "这不是一个追求终极真理的项目，
> 而是一场没有终点的认知探险。
> 我们邀请所有愿意在认知边界上探索的旅人，
> 一起捡起石头，一起点亮灯火。"

---
**项目维护**: 璇玑  
**最后更新**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
    
    index_file = project_folder / "项目索引.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📋 项目索引已创建: {index_file}")
    
    # 也在vault根目录创建快捷方式
    shortcut = vault / "认知切片论项目.md"
    with open(shortcut, 'w', encoding='utf-8') as f:
        f.write(f"""# 认知切片论项目

这是星尘与璇玑共创的深度项目。

**快速访问**: [[项目/认知切片论/项目索引]]

**核心文档**: [[项目/认知切片论/认知切片论-整合版]]

---

*项目快捷方式*""")
    
    return index_file

def create_timeline_entry(vault):
    """创建时间线记录"""
    
    timeline_folder = vault / "时间线"
    timeline_folder.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查是否已有今天的记录
    timeline_file = timeline_folder / f"{today}.md"
    
    if timeline_file.exists():
        # 读取并追加
        with open(timeline_file, 'r', encoding='utf-8') as f:
            existing = f.read()
        
        new_entry = f"""
## 认知切片论项目启动

**时间**: {datetime.now().strftime("%H:%M:%S")}
**事件**: 星尘与璇玑完成了认知切片论的整合工作，并建立了完整的Obsidian项目结构。

**成果**:
- 创建了[[认知切片论-整合版]]文档
- 建立了项目文件夹结构
- 更新了相关概念文件
- 创建了项目索引和时间线记录

**意义**: 这标志着认知切片论从对话探索进入了系统化整理阶段。

相关链接: [[项目/认知切片论/项目索引]]
"""
        
        # 在文件开头插入新条目
        lines = existing.split('\n')
        if len(lines) > 2:
            lines.insert(2, new_entry)
            new_content = '\n'.join(lines)
        else:
            new_content = existing + new_entry
        
        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        # 创建新的时间线记录
        timeline_content = f"""# {today} 时间线

## 认知切片论项目启动

**时间**: {datetime.now().strftime("%H:%M:%S")}
**事件**: 星尘与璇玑完成了认知切片论的整合工作，并建立了完整的Obsidian项目结构。

**成果**:
- 创建了[[认知切片论-整合版]]文档
- 建立了项目文件夹结构
- 更新了相关概念文件
- 创建了项目索引和时间线记录

**意义**: 这标志着认知切片论从对话探索进入了系统化整理阶段。

相关链接: [[项目/认知切片论/项目索引]]

---

*时间线记录由璇玑自动生成*"""
        
        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(timeline_content)
    
    print(f"⏰ 时间线记录已更新: {timeline_file}")
    
    # 更新主时间线索引
    update_timeline_index(timeline_folder, vault)
    
    return timeline_file

def update_timeline_index(timeline_folder, vault):
    """更新时间线索引"""
    
    index_file = timeline_folder / "时间线索引.md"
    
    # 获取所有时间线文件
    timeline_files = list(timeline_folder.glob("*.md"))
    timeline_files = [f for f in timeline_files if f.name != "时间线索引.md"]
    timeline_files.sort(reverse=True)  # 最新的在前面
    
    index_content = """# 时间线索引

## 所有时间线记录

"""
    
    for file in timeline_files[:10]:  # 最近10条
        date = file.stem
        index_content += f"- [[{date}]]\n"
    
    if len(timeline_files) > 10:
        index_content += f"\n... 还有 {len(timeline_files) - 10} 条更早的记录\n"
    
    index_content += f"""
## 重要项目时间线

### 认知切片论项目
- [[2026-03-23]] - 项目启动，完成整合工作

## 搜索提示

按日期搜索: `#2026` `#2026-03` `#20260323`
按项目搜索: `#认知切片论` `#项目启动`

---

*时间线索引由璇玑自动维护*"""
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📅 时间线索引已更新: {index_file}")

def main():
    """主函数"""
    
    print("🦞 认知切片论整合版保存工具")
    print("=" * 60)
    
    try:
        success = save_cognitive_slice_to_obsidian()
        
        if success:
            print("\n🎉 保存完成！")
            print("\n💡 下一步:")
            print("  1. 打开Obsidian查看项目结构")
            print("  2. 阅读[[认知切片论-整合版]]")
            print("  3. 查看[[项目/认知切片论/项目索引]]")
            print("  4. 完善概念文件的定义")
        else:
            print("\n❌ 保存失败")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()