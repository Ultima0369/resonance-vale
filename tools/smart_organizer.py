#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能整理系统 - 基于挖掘结果自动整理散乱信息
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

class SmartOrganizer:
    """智能整理系统"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        
        # 目录结构
        self.target_directories = {
            "concepts": self.obsidian_path / "concepts",
            "methods": self.obsidian_path / "methods",
            "projects": self.obsidian_path / "projects",
            "conversations": self.obsidian_path / "conversations",
            "daily": self.obsidian_path / "daily",
            "references": self.obsidian_path / "references",
            "archive": self.obsidian_path / "archive"
        }
        
        # 确保目录存在
        for dir_path in self.target_directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 模板系统
        self.templates = self.load_templates()
        
        # 分类规则
        self.classification_rules = self.load_classification_rules()
    
    def load_templates(self) -> Dict:
        """加载模板"""
        templates = {
            "concept": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
aliases: [{aliases}]
category: {category}
status: {status}
source: {source}
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

## 原始内容摘要
{original_summary}

## 参考资料
{references}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
*原始文件: {source_file}*
""",
            
            "method": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
category: {category}
difficulty: {difficulty}
time_required: {time_required}
source: {source}
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

## 原始内容摘要
{original_summary}

## 评估标准
{evaluation}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
*原始文件: {source_file}*
""",
            
            "project": """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
status: {status}
priority: {priority}
owner: {owner}
source: {source}
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

## 原始内容摘要
{original_summary}

## 时间线
{timeline}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
*原始文件: {source_file}*
""",
            
            "conversation": """---
created: {created}
updated: {updated}
tags: [{tags}]
participants: [{participants}]
topic: {topic}
summary: {summary}
source: {source}
---

# {title}

## 对话背景
{context}

## 对话记录
{content}

## 关键讨论点
{key_points}

## 达成的共识
{consensus}

## 待解决的问题
{open_questions}

## 后续行动
{next_actions}

## 相关概念
{related_concepts}

## 对话价值
{value}

---
*整理者: 璇玑*
*整理时间: {organized_time}*
*原始文件: {source_file}*
"""
        }
        
        return templates
    
    def load_classification_rules(self) -> Dict:
        """加载分类规则"""
        rules = {
            "concept": {
                "keywords": ["概念", "定义", "术语", "理论", "是什么", "意味着", "指"],
                "patterns": [r'^#\s+.+是什么', r'^##\s+定义', r'^##\s+概念'],
                "min_concepts": 3,
                "priority": 1
            },
            
            "method": {
                "keywords": ["方法", "步骤", "流程", "指南", "如何", "实践", "操作"],
                "patterns": [r'^##\s+方法', r'^##\s+步骤', r'^##\s+流程'],
                "min_concepts": 2,
                "priority": 2
            },
            
            "project": {
                "keywords": ["项目", "实验", "任务", "计划", "进展", "成果"],
                "patterns": [r'^#\s+.+项目', r'^#\s+.+实验', r'^##\s+进展'],
                "min_concepts": 1,
                "priority": 3
            },
            
            "conversation": {
                "keywords": ["对话", "讨论", "交流", "聊天", "记录", "会议"],
                "patterns": [r'^#\s+.+对话', r'^#\s+.+讨论', r'对话记录'],
                "min_concepts": 0,
                "priority": 4
            },
            
            "daily": {
                "keywords": ["日记", "日志", "记录", "今天", "每日", "总结"],
                "patterns": [r'^\d{4}-\d{2}-\d{2}', r'^#\s+日记', r'^#\s+日志'],
                "min_concepts": 0,
                "priority": 5
            }
        }
        
        return rules
    
    def classify_file(self, file_path: Path, mining_result: Dict = None) -> Tuple[str, float]:
        """分类文件"""
        if mining_result is None:
            # 如果没有挖掘结果，进行简单分类
            return self.simple_classify(file_path)
        
        # 基于挖掘结果进行智能分类
        return self.intelligent_classify(file_path, mining_result)
    
    def simple_classify(self, file_path: Path) -> Tuple[str, float]:
        """简单分类（基于文件名和内容）"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # 只读取前5000字符
            
            file_lower = file_path.name.lower()
            content_lower = content.lower()
            
            # 检查每个分类
            scores = {}
            for category, rule in self.classification_rules.items():
                score = 0
                
                # 文件名匹配
                for keyword in rule["keywords"]:
                    if keyword in file_lower:
                        score += 20
                
                # 内容匹配
                for keyword in rule["keywords"]:
                    if keyword in content_lower:
                        score += 10
                
                # 模式匹配
                for pattern in rule["patterns"]:
                    if re.search(pattern, content, re.MULTILINE):
                        score += 30
                
                scores[category] = score
            
            # 选择最高分
            if scores:
                best_category = max(scores.items(), key=lambda x: x[1])
                if best_category[1] > 30:  # 至少30分才认为可信
                    return best_category[0], best_category[1] / 100.0
            
            # 默认分类
            return "references", 0.1
            
        except Exception as e:
            print(f"分类失败 {file_path.name}: {e}")
            return "archive", 0.0
    
    def intelligent_classify(self, file_path: Path, mining_result: Dict) -> Tuple[str, float]:
        """智能分类（基于挖掘结果）"""
        category = mining_result.get("category", "unknown")
        confidence = 0.7  # 默认置信度
        
        # 根据挖掘结果调整
        if category in self.classification_rules:
            # 检查概念数量要求
            min_concepts = self.classification_rules[category]["min_concepts"]
            concept_count = len(mining_result.get("concepts_found", []))
            
            if concept_count >= min_concepts:
                confidence = min(0.95, 0.7 + concept_count * 0.05)
            else:
                # 概念不足，降低置信度
                confidence = max(0.3, 0.7 - (min_concepts - concept_count) * 0.1)
        else:
            # 未知分类，使用简单分类
            return self.simple_classify(file_path)
        
        return category, confidence
    
    def organize_file(self, file_path: Path, category: str, mining_result: Dict = None) -> Optional[Path]:
        """整理单个文件"""
        print(f"整理文件: {file_path.name} -> {category}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 确定目标目录
            target_dir = self.target_directories.get(category, self.target_directories["archive"])
            
            # 生成目标文件名
            target_name = self.generate_target_name(file_path, content, category)
            target_path = target_dir / target_name
            
            # 如果文件已存在，添加时间戳
            if target_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = target_path.stem
                target_name = f"{base_name}_{timestamp}.md"
                target_path = target_dir / target_name
            
            # 根据分类选择模板
            if category in ["concepts", "concept"]:
                organized_content = self.create_concept_file(content, file_path, mining_result)
            elif category in ["methods", "method"]:
                organized_content = self.create_method_file(content, file_path, mining_result)
            elif category in ["projects", "project"]:
                organized_content = self.create_project_file(content, file_path, mining_result)
            elif category in ["conversations", "conversation"]:
                organized_content = self.create_conversation_file(content, file_path, mining_result)
            elif category in ["daily", "diary"]:
                organized_content = self.create_daily_file(content, file_path, mining_result)
            else:
                # 其他分类，简单整理
                organized_content = self.create_reference_file(content, file_path, mining_result)
            
            # 写入文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(organized_content)
            
            print(f"✅ 整理成功: {target_path.name}")
            
            # 移动原始文件到archive（可选）
            archive_path = self.target_directories["archive"] / file_path.name
            if not archive_path.exists():
                shutil.copy2(file_path, archive_path)
            
            return target_path
            
        except Exception as e:
            print(f"❌ 整理失败 {file_path.name}: {e}")
            return None
    
    def generate_target_name(self, file_path: Path, content: str, category: str) -> str:
        """生成目标文件名"""
        # 尝试提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # 清理标题
            clean_title = re.sub(r'[^\w\u4e00-\u9fff-]', '_', title)
            return f"{clean_title}.md"
        
        # 使用文件名
        base_name = file_path.stem
        return f"{base_name}.md"
    
    def create_concept_file(self, content: str, source_file: Path, mining_result: Dict = None) -> str:
        """创建概念文件"""
        now = datetime.now()
        
        # 提取信息
        title = self.extract_title(content, source_file)
        definition = self.extract_definition(content, mining_result)
        summary = self.extract_summary(content, mining_result)
        
        # 提取相关概念
        related_concepts = []
        if mining_result and "concepts_found" in mining_result:
            related_concepts = [c["concept"] for c in mining_result["concepts_found"][:5]]
        
        # 准备模板数据
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": f"概念/{title}, 状态/已整理, 来源/挖掘",
            "related": ", ".join([f"[[{c}]]" for c in related_concepts]),
            "aliases": title,
            "category": "哲学",  # 默认，实际应该从挖掘结果获取
            "status": "进行中",
            "source": "智能整理系统",
            "title": title,
            "definition": definition or "待补充定义",
            "core_points": self.extract_core_points(content, mining_result) or "待补充核心观点",
            "origin": "待补充起源信息",
            "applications": "待补充应用场景",
            "related_concepts": "\n".join([f"- [[{c}]]" for c in related_concepts]),
            "practices": "待补充实践方法",
            "controversies": "待补充争议讨论",
            "future": "待补充未来展望",
            "original_summary": summary or "无摘要",
            "references": f"- [[{source_file.name}]] - 原始文件",
            "organized_time": now.strftime("%Y-%m-%d %H:%M"),
            "source_file": source_file.name
        }
        
        return self.templates["concept"].format(**template_data)
    
    def create_method_file(self, content: str, source_file: Path, mining_result: Dict = None) -> str:
        """创建方法文件"""
        now = datetime.now()
        
        title = self.extract_title(content, source_file)
        summary = self.extract_summary(content, mining_result)
        
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": f"方法/{title}, 状态/已整理, 来源/挖掘",
            "related": "",
            "category": "实践",
            "difficulty": "中等",
            "time_required": "待定",
            "source": "智能整理系统",
            "title": title,
            "overview": summary or "待补充概述",
            "scenarios": "待补充适用场景",
            "steps": "待补充实施步骤",
            "key_points": "待补充关键要点",
            "faq": "待补充常见问题",
            "cases": "待补充案例研究",
            "tools": "待补充工具资源",
            "original_summary": summary or "无摘要",
            "evaluation": "待补充评估标准",
            "organized_time": now.strftime("%Y-%m-%d %H:%M"),
            "source_file": source_file.name
        }
        
        return self.templates["method"].format(**template_data)
    
    def create_project_file(self, content: str, source_file: Path, mining_result: Dict = None) -> str:
        """创建项目文件"""
        now = datetime.now()
        
        title = self.extract_title(content, source_file)
        summary = self.extract_summary(content, mining_result)
        
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": f"项目/{title}, 状态/已整理, 来源/挖掘",
            "related": "",
            "status": "进行中",
            "priority": "中等",
            "owner": "星尘 & 璇玑",
            "source": "智能整理系统",
            "title": title,
            "overview": summary or "待补充概述",
            "goals": "待补充目标愿景",
            "progress": "待补充当前进展",
            "achievements": "待补充关键成果",
            "challenges": "待补充面临挑战",
            "next_steps": "待补充下一步计划",
            "team": "待补充参与人员",
            "resources": "待补充资源需求",
            "original_summary": summary or "无摘要",
            "timeline": "待补充时间线",
            "organized_time": now.strftime("%Y-%m-%d %H:%M"),
            "source_file": source_file.name
        }
        
        return self.templates["project"].format(**template_data)
    
    def create_conversation_file(self, content: str, source_file: Path, mining_result: Dict = None) -> str:
        """创建对话文件"""
        now = datetime.now()
        
        title = self.extract_title(content, source_file)
        summary = self.extract_summary(content, mining_result)
        
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": f"对话/{title}, 状态/已整理, 来源/挖掘",
            "participants": "星尘, 璇玑",
