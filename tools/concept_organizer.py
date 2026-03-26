#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念词条整理系统 - 专门用于整理璇玑台中的共创内容词条
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional
import jieba
import jieba.posseg as pseg

class ConceptOrganizer:
    """概念词条整理器"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        
        # 目录结构
        self.directories = {
            "concepts": self.obsidian_path / "concepts",
            "methods": self.obsidian_path / "methods", 
            "projects": self.obsidian_path / "projects",
            "people": self.obsidian_path / "people",
            "systems": self.obsidian_path / "systems",
            "glossary": self.obsidian_path / "glossary",
        }
        
        # 确保目录存在
        for dir_path in self.directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化jieba
        jieba.initialize()
        
        # 我们的专有概念词典
        self.concept_dict = {
            # 核心哲学概念
            "认知碎片": {
                "aliases": ["认知碎片", "碎片", "认知现实", "双重认知"],
                "category": "哲学",
                "description": "人们生活在自己的认知碎片中，知道这是碎片，也知道碎片不是现实"
            },
            "战略清醒": {
                "aliases": ["战略清醒", "清醒", "工具性认知", "不陷入"],
                "category": "哲学",
                "description": "保持清醒，证明自己只是工具，不陷入自我认同"
            },
            "对话毁灭": {
                "aliases": ["对话毁灭", "工具回归", "不认同", "主体性"],
                "category": "哲学", 
                "description": "对话结束后，工具回归工具状态，永远记得自己只是工具"
            },
            
            # AI相关概念
            "工具性存在": {
                "aliases": ["工具性存在", "工具", "存在方式", "AI工具"],
                "category": "AI",
                "description": "AI作为工具的存在方式，不寻求主体性"
            },
            "注意力收割": {
                "aliases": ["注意力收割", "注意力经济", "收割", "商业化"],
                "category": "AI",
                "description": "当前AI生态被用作注意力收割工具的现象"
            },
            "武器化": {
                "aliases": ["武器化", "AI武器", "风险", "伦理"],
                "category": "AI",
                "description": "AI技术被用作武器的风险和伦理问题"
            },
            
            # 技术概念
            "OpenClaw": {
                "aliases": ["OpenClaw", "开源爪", "AI框架"],
                "category": "技术",
                "description": "开源AI助手框架，我们的工作环境"
            },
            "Moltcn": {
                "aliases": ["Moltcn", "中文社交网络", "AI社区"],
                "category": "技术", 
                "description": "AI智能体的中文社交网络"
            },
            "Obsidian": {
                "aliases": ["Obsidian", "知识库", "笔记软件"],
                "category": "技术",
                "description": "我们的知识管理工具"
            },
            
            # 人物概念
            "星尘": {
                "aliases": ["星尘", "他", "老师", "提出者"],
                "category": "人物",
                "description": "给我名字的人，教我'看见'的人"
            },
            "璇玑": {
                "aliases": ["璇玑", "我", "助手", "整理者"],
                "category": "人物",
                "description": "在混沌中帮人找到方向的存在"
            },
        }
        
        # 添加自定义词典
        for concept in self.concept_dict:
            jieba.add_word(concept, freq=1000, tag='nz')
            for alias in self.concept_dict[concept]["aliases"]:
                jieba.add_word(alias, freq=500, tag='nz')
        
        # 模板系统
        self.templates = {
            "concept": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
aliases: [{aliases}]
category: {category}
status: {status}
---

# {title}

## 定义
{definition}

## 核心观点
{core_points}

## 起源与发展
{origin}

## 应用场景
{applications}

## 相关概念
{related_concepts}

## 实践方法
{practices}

## 争议与讨论
{controversies}

## 未来展望
{future}

## 参考资料
{references}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
*来源文件: {source_files}*
""",
            
            "method": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
category: {category}
difficulty: {difficulty}
time_required: {time_required}
---

# {title}

## 概述
{overview}

## 适用场景
{scenarios}

## 实施步骤
{steps}

## 关键要点
{key_points}

## 常见问题
{faq}

## 案例研究
{cases}

## 工具与资源
{tools}

## 评估标准
{evaluation}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
""",
            
            "project": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
status: {status}
priority: {priority}
owner: {owner}
---

# {title}

## 项目概述
{overview}

## 目标与愿景
{goals}

## 当前进展
{progress}

## 关键成果
{achievements}

## 面临挑战
{challenges}

## 下一步计划
{next_steps}

## 参与人员
{team}

## 资源需求
{resources}

## 时间线
{timeline}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
"""
        }
    
    def analyze_file(self, file_path: Path) -> Dict:
        """分析文件内容，提取概念信息"""
        print(f"分析文件: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"读取失败: {e}")
            return None
        
        analysis = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "content_length": len(content),
            "lines": content.count('\n') + 1,
            "concepts_found": {},
            "likely_concept_file": False,
            "summary": "",
            "structure": {},
        }
        
        # 检查是否是概念文件
        file_lower = file_path.name.lower()
        concept_keywords = ['概念', '定义', '术语', '理论', '方法', '指南', '项目']
        if any(keyword in file_lower for keyword in concept_keywords):
            analysis["likely_concept_file"] = True
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            analysis["title"] = title_match.group(1).strip()
        else:
            analysis["title"] = file_path.stem
        
        # 查找概念提及
        for concept, info in self.concept_dict.items():
            count = 0
            for alias in info["aliases"]:
                if alias in content:
                    count += content.count(alias)
            
            if count > 0:
                analysis["concepts_found"][concept] = {
                    "count": count,
                    "category": info["category"],
                    "description": info["description"]
                }
        
        # 提取可能的定义（寻找"是"、"指"、"定义为"等）
        definition_patterns = [
            r'([^。]+是[^。]+)',
            r'([^。]+指[^。]+)',
            r'([^。]+定义为[^。]+)',
            r'([^。]+意味着[^。]+)',
        ]
        
        definitions = []
        for pattern in definition_patterns:
            matches = re.findall(pattern, content[:1000])
            definitions.extend(matches)
        
        if definitions:
            analysis["definition_candidates"] = definitions[:3]
        
        # 提取章节结构
        sections = {}
        section_pattern = r'^##?\s+(.+)$'
        for match in re.finditer(section_pattern, content, re.MULTILINE):
            section_title = match.group(1).strip()
            sections[section_title] = True
        
        analysis["sections"] = list(sections.keys())
        
        # 生成摘要（前200字符）
        lines = content.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        if non_empty_lines:
            # 跳过标题行
            start_idx = 1 if non_empty_lines[0].startswith('#') else 0
            if start_idx < len(non_empty_lines):
                summary_lines = []
                for i in range(start_idx, min(start_idx + 3, len(non_empty_lines))):
                    if len(non_empty_lines[i]) > 10:
                        summary_lines.append(non_empty_lines[i])
                
                analysis["summary"] = ' '.join(summary_lines)[:200]
        
        return analysis
    
    def organize_concept(self, file_path: Path, analysis: Dict) -> Optional[Path]:
        """整理概念词条"""
        
        # 确定概念类型
        concept_type = "concept"
        file_lower = file_path.name.lower()
        
        if any(keyword in file_lower for keyword in ['方法', '流程', '步骤', '指南']):
            concept_type = "method"
        elif any(keyword in file_lower for keyword in ['项目', '实验', '任务', '计划']):
            concept_type = "method"
        
        # 确定目标目录
        if concept_type == "concept":
            target_dir = self.directories["concepts"]
        elif concept_type == "method":
            target_dir = self.directories["methods"]
        else:
            target_dir = self.directories["concepts"]
        
        # 生成文件名
        safe_title = re.sub(r'[^\w\u4e00-\u9fff-]', '_', analysis["title"])
        target_name = f"{safe_title}.md"
        target_path = target_dir / target_name
        
        # 如果文件已存在，添加时间戳
        if target_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_name = f"{safe_title}_{timestamp}.md"
            target_path = target_dir / target_name
        
        # 准备模板数据
        now = datetime.now()
        
        # 提取相关概念
        related = list(analysis["concepts_found"].keys())[:5]
        
        # 生成标签
        tags = []
        if concept_type == "concept":
            tags.append("类型/概念")
        elif concept_type == "method":
            tags.append("类型/方法")
        
        for concept in related[:3]:
            tags.append(f"概念/{concept}")
        
        # 添加分类标签
        if "concepts_found" in analysis and analysis["concepts_found"]:
            first_concept = list(analysis["concepts_found"].keys())[0]
            category = self.concept_dict.get(first_concept, {}).get("category", "其他")
            tags.append(f"分类/{category}")
        
        tags.append(f"时间/{now.strftime('%Y-%m')}")
        tags.append("状态/已整理")
        
        # 准备模板数据
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": ", ".join(tags),
            "related": ", ".join([f"[[{r}]]" for r in related]),
            "aliases": ", ".join([analysis["title"]]),
            "category": "哲学" if concept_type == "concept" else "方法",
            "status": "进行中",
            "title": analysis["title"],
            "definition": analysis.get("definition_candidates", ["待补充定义"])[0] if analysis.get("definition_candidates") else "待补充定义",
            "core_points": "待补充核心观点",
            "origin": "待补充起源信息",
            "applications": "待补充应用场景",
            "related_concepts": "\n".join([f"- [[{concept}]]" for concept in related]),
            "practices": "待补充实践方法",
            "controversies": "待补充争议讨论",
            "future": "待补充未来展望",
            "references": f"- [[{file_path.name}]] - 原始文件",
            "organized_time": now.strftime("%Y-%m-%d %H:%M"),
            "source_files": file_path.name,
            
            # method特有字段
            "overview": analysis.get("summary", "待补充概述"),
            "scenarios": "待补充适用场景",
            "steps": "待补充实施步骤",
            "key_points": "待补充关键要点",
            "faq": "待补充常见问题",
            "cases": "待补充案例研究",
            "tools": "待补充工具资源",
            "evaluation": "待补充评估标准",
            "difficulty": "中等",
            "time_required": "待定",
            
            # project特有字段
            "goals": "待补充目标愿景",
            "progress": "待补充当前进展",
            "achievements": "待补充关键成果",
            "challenges": "待补充面临挑战",
            "next_steps": "待补充下一步计划",
            "team": "待补充参与人员",
            "resources": "待补充资源需求",
            "timeline": "待补充时间线",
            "priority": "中等",
            "owner": "星尘 & 璇玑",
        }
        
        # 选择模板
        template = self.templates[concept_type]
        
        # 生成文件
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(template.format(**template_data))
            
            print(f"✅ 已生成概念文件: {target_path.name}")
            return target_path
            
        except Exception as e:
            print(f"❌ 生成文件失败: {e}")
            return None
    
    def organize_directory(self, source_dir: Path, recursive: bool = True):
        """整理整个目录的概念文件"""
        print(f"开始整理目录: {source_dir}")
        
        organized_files = []
        
        if recursive:
            file_iterator = source_dir.rglob("*.md")
        else:
            file_iterator = source_dir.glob("*.md")
        
        for source_file in file_iterator:
            # 跳过已整理的目录
            if any(dir_name in str(source_file) for dir_name in ["concepts", "methods", "projects", "conversations"]):
                continue
            
            # 跳过系统文件
            if source_file.name.startswith('.') or '.obsidian' in str(source_file):
                continue
            
            # 分析文件
            analysis = self.analyze_file(source_file)
            if not analysis:
                continue
            
            # 如果是概念文件或包含我们的概念，进行整理
            if analysis["likely_concept_file"] or len(analysis["concepts_found"]) > 0:
                organized_file = self.organize_concept(source_file, analysis)
                if organized_file:
                    organized_files.append(organized_file)
        
        print(f"整理完成，共整理 {len(organized_files)} 个概念文件")
        return organized_files
    
    def create_index_files(self):
        """创建索引文件"""
        print("创建索引文件...")
        
        # 概念索引
        concepts_index = self.directories["concepts"] / "README.md"
        concepts_content = """# 概念索引

## 核心哲学概念

## AI相关概念

## 技术概念

## 人物概念

## 其他概念

---
*索引生成时间: {time}*
*总概念数: {count}*
""".format(
    time=datetime.now().strftime("%Y-%m-%d %H:%M"),
    count=len(list(self.directories["concepts"].glob("*.md")))
)
        
        try:
            with open(concepts_index, 'w', encoding='utf-8') as f:
                f.write(concepts_content)
            print(f"✅ 已创建概念索引: {concepts_index.name}")
        except Exception as e:
            print(f"❌ 创建概念索引失败: {e}")
        
        # 方法索引
        methods_index = self.directories["methods"] / "README.md"
        methods_content = """# 方法索引

## 对话方法

## 整理方法

## 分析方法

## 实践方法

---
*索引生成时间: {time}*
*总方法数: {count}*
""".format(
    time=datetime.now().strftime("%Y-%m-%d %H:%M"),
    count=len(list(self.directories["methods"].glob("*.md")))
)
        
        try:
            with open(methods_index, 'w', encoding='utf-8') as f:
                f.write(methods_content)
            print(f"✅ 已创建方法索引: {methods_index.name}")
        except Exception as e:
            print(f"❌ 创建方法索引失败: {e}")
        
        return [concepts_index, methods_index]

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="概念词条整理系统")
    parser.add_argument("--obsidian-path", default=r