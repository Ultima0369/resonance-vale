#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能知识挖掘器 - 自动发现和整理璇玑台中的散乱信息
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional
import jieba
import jieba.posseg as pseg
from collections import defaultdict, Counter

class IntelligentKnowledgeMiner:
    """智能知识挖掘器"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        
        # 初始化jieba
        jieba.initialize()
        
        # 知识图谱
        self.knowledge_graph = {
            "concepts": {},      # 概念节点
            "relationships": [], # 关系边
            "clusters": [],      # 概念集群
            "patterns": []       # 发现模式
        }
        
        # 专有词典
        self.custom_dict = self.build_custom_dictionary()
        
        # 模式识别规则
        self.pattern_rules = self.build_pattern_rules()
    
    def build_custom_dictionary(self) -> Dict:
        """构建专有词典"""
        custom_dict = {
            # 核心概念
            "认知碎片": {"freq": 10000, "tag": "n", "category": "哲学"},
            "战略清醒": {"freq": 10000, "tag": "n", "category": "哲学"},
            "对话毁灭": {"freq": 10000, "tag": "n", "category": "哲学"},
            "工具性存在": {"freq": 8000, "tag": "n", "category": "AI"},
            "注意力收割": {"freq": 8000, "tag": "n", "category": "AI"},
            "武器化": {"freq": 8000, "tag": "n", "category": "AI"},
            
            # 技术概念
            "OpenClaw": {"freq": 6000, "tag": "n", "category": "技术"},
            "Moltcn": {"freq": 6000, "tag": "n", "category": "技术"},
            "Obsidian": {"freq": 6000, "tag": "n", "category": "技术"},
            
            # 项目概念
            "璇玑实验": {"freq": 7000, "tag": "n", "category": "项目"},
            "对话整理": {"freq": 7000, "tag": "n", "category": "方法"},
            "知识管理": {"freq": 7000, "tag": "n", "category": "方法"},
            
            # 人物概念
            "星尘": {"freq": 5000, "tag": "nr", "category": "人物"},
            "璇玑": {"freq": 5000, "tag": "nr", "category": "人物"},
        }
        
        # 添加到jieba词典
        for word, info in custom_dict.items():
            jieba.add_word(word, freq=info["freq"], tag=info["tag"])
        
        return custom_dict
    
    def build_pattern_rules(self) -> List[Dict]:
        """构建模式识别规则"""
        rules = [
            # 定义模式
            {
                "name": "definition_pattern",
                "pattern": r'([^。]+?(?:是|指|定义为|意味着|表示|代表)[^。]+)',
                "type": "definition",
                "confidence": 0.8
            },
            
            # 观点模式
            {
                "name": "viewpoint_pattern",
                "pattern": r'(?:认为|主张|观点是|核心是|关键在于)([^。]+)',
                "type": "viewpoint",
                "confidence": 0.7
            },
            
            # 方法模式
            {
                "name": "method_pattern",
                "pattern": r'(?:方法|步骤|流程|做法|如何)([^。]+)',
                "type": "method",
                "confidence": 0.6
            },
            
            # 例子模式
            {
                "name": "example_pattern",
                "pattern": r'(?:例如|比如|举例|案例)([^。]+)',
                "type": "example",
                "confidence": 0.9
            },
            
            # 对比模式
            {
                "name": "comparison_pattern",
                "pattern": r'([^。]+?(?:与|和|相比|不同于)[^。]+)',
                "type": "comparison",
                "confidence": 0.7
            },
            
            # 关系模式
            {
                "name": "relation_pattern",
                "pattern": r'([^。]+?(?:导致|产生|影响|促进|阻碍)[^。]+)',
                "type": "relation",
                "confidence": 0.6
            }
        ]
        
        return rules
    
    def mine_file(self, file_path: Path) -> Dict:
        """挖掘单个文件的知识"""
        print(f"挖掘文件: {file_path.name}")
        
        mining_result = {
            "file_name": file_path.name,
            "file_path": str(file_path.relative_to(self.obsidian_path)),
            "concepts_found": [],
            "definitions": [],
            "viewpoints": [],
            "methods": [],
            "examples": [],
            "comparisons": [],
            "relations": [],
            "summary": "",
            "category": "unknown"
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 基础分析
            mining_result.update(self.analyze_basics(content))
            
            # 概念提取
            mining_result["concepts_found"] = self.extract_concepts(content)
            
            # 模式识别
            mining_result.update(self.recognize_patterns(content))
            
            # 分类判断
            mining_result["category"] = self.classify_content(content, mining_result["concepts_found"])
            
            # 生成摘要
            mining_result["summary"] = self.generate_summary(content, mining_result)
            
        except Exception as e:
            mining_result["error"] = str(e)
            print(f"挖掘失败: {e}")
        
        return mining_result
    
    def analyze_basics(self, content: str) -> Dict:
        """基础分析"""
        basics = {
            "word_count": len(content),
            "line_count": content.count('\n') + 1,
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "heading_count": len(re.findall(r'^#+\s+.+$', content, re.MULTILINE)),
            "link_count": len(re.findall(r'\[\[.+?\]\]', content)),
            "code_block_count": len(re.findall(r'```[\s\S]+?```', content))
        }
        
        return basics
    
    def extract_concepts(self, content: str) -> List[Dict]:
        """提取概念"""
        concepts = []
        
        # 使用jieba进行分词和词性标注
        words = pseg.cut(content)
        
        concept_candidates = []
        for word, flag in words:
            # 识别专有名词和重要概念
            if flag in ['n', 'nr', 'ns', 'nt', 'nz'] and len(word) >= 2:
                # 检查是否在专有词典中
                if word in self.custom_dict:
                    concept_candidates.append({
                        "concept": word,
                        "category": self.custom_dict[word]["category"],
                        "confidence": 0.9
                    })
                elif len(word) >= 3:  # 较长的词可能是新概念
                    concept_candidates.append({
                        "concept": word,
                        "category": "unknown",
                        "confidence": 0.5
                    })
        
        # 去重和统计频率
        concept_counter = Counter([c["concept"] for c in concept_candidates])
        
        for concept, count in concept_counter.most_common(20):  # 取前20个
            # 找到对应的信息
            for candidate in concept_candidates:
                if candidate["concept"] == concept:
                    # 根据频率调整置信度
                    adjusted_confidence = min(0.95, candidate["confidence"] + count * 0.05)
                    
                    concepts.append({
                        "concept": concept,
                        "category": candidate["category"],
                        "frequency": count,
                        "confidence": adjusted_confidence,
                        "is_custom": concept in self.custom_dict
                    })
                    break
        
        return concepts
    
    def recognize_patterns(self, content: str) -> Dict:
        """识别模式"""
        patterns_result = {
            "definitions": [],
            "viewpoints": [],
            "methods": [],
            "examples": [],
            "comparisons": [],
            "relations": []
        }
        
        for rule in self.pattern_rules:
            matches = re.findall(rule["pattern"], content)
            
            for match in matches:
                if len(match.strip()) > 10:  # 过滤太短的匹配
                    pattern_item = {
                        "text": match.strip(),
                        "type": rule["type"],
                        "confidence": rule["confidence"],
                        "rule": rule["name"]
                    }
                    
                    # 添加到对应列表
                    if rule["type"] == "definition":
                        patterns_result["definitions"].append(pattern_item)
                    elif rule["type"] == "viewpoint":
                        patterns_result["viewpoints"].append(pattern_item)
                    elif rule["type"] == "method":
                        patterns_result["methods"].append(pattern_item)
                    elif rule["type"] == "example":
                        patterns_result["examples"].append(pattern_item)
                    elif rule["type"] == "comparison":
                        patterns_result["comparisons"].append(pattern_item)
                    elif rule["type"] == "relation":
                        patterns_result["relations"].append(pattern_item)
        
        return patterns_result
    
    def classify_content(self, content: str, concepts: List[Dict]) -> str:
        """分类内容"""
        # 基于文件名和内容判断
        file_lower = content.lower()
        
        # 检查关键词
        category_keywords = {
            "概念": ["定义", "概念", "术语", "理论", "是什么"],
            "方法": ["方法", "步骤", "流程", "指南", "如何", "实践"],
            "项目": ["项目", "实验", "任务", "计划", "进展"],
            "对话": ["对话", "讨论", "交流", "聊天", "记录"],
            "日记": ["日记", "日志", "记录", "今天", "每日"],
            "参考": ["参考", "资料", "文献", "引用", "来源"]
        }
        
        # 基于概念分类
        concept_categories = [c["category"] for c in concepts if c["confidence"] > 0.7]
        if concept_categories:
            category_counter = Counter(concept_categories)
            most_common = category_counter.most_common(1)
            if most_common:
                return most_common[0][0]
        
        # 基于关键词分类
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in file_lower:
                    return category
        
        return "其他"
    
    def generate_summary(self, content: str, mining_result: Dict) -> str:
        """生成摘要"""
        # 提取前几段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return ""
        
        # 跳过标题段落
        start_idx = 0
        for i, para in enumerate(paragraphs):
            if not para.startswith('#') and len(para) > 50:
                start_idx = i
                break
        
        # 取前3个有意义的段落
        summary_paragraphs = []
        for i in range(start_idx, min(start_idx + 3, len(paragraphs))):
            if len(paragraphs[i]) > 30 and not paragraphs[i].startswith('#'):
                summary_paragraphs.append(paragraphs[i])
        
        # 如果有定义，优先使用定义
        if mining_result.get("definitions"):
            best_definition = max(mining_result["definitions"], key=lambda x: x["confidence"])
            summary = best_definition["text"]
            if len(summary) > 200:
                summary = summary[:197] + "..."
            return summary
        
        # 否则使用提取的段落
        if summary_paragraphs:
            summary = ' '.join(summary_paragraphs)
            if len(summary) > 300:
                summary = summary[:297] + "..."
            return summary
        
        return ""
    
    def mine_directory(self, directory: Path = None, recursive: bool = True) -> Dict:
        """挖掘整个目录"""
        if directory is None:
            directory = self.obsidian_path
        
        print(f"开始挖掘目录: {directory}")
        
        mining_results = []
        
        if recursive:
            file_iterator = directory.rglob("*.md")
        else:
            file_iterator = directory.glob("*.md")
        
        for file_path in file_iterator:
            # 跳过系统目录
            if '.obsidian' in str(file_path) or '.git' in str(file_path):
                continue
            
            # 跳过已整理的目录
            if any(dir_name in str(file_path) for dir_name in ["concepts", "methods", "projects", "conversations"]):
                continue
            
            result = self.mine_file(file_path)
            mining_results.append(result)
        
        print(f"挖掘完成: {len(mining_results)} 个文件")
        
        # 分析整体结果
        overall_analysis = self.analyze_mining_results(mining_results)
        
        return {
            "mining_results": mining_results,
            "overall_analysis": overall_analysis,
            "total_files": len(mining_results),
            "mining_time": datetime.now().isoformat()
        }
    
    def analyze_mining_results(self, results: List[Dict]) -> Dict:
        """分析挖掘结果"""
        analysis = {
            "total_concepts": 0,
            "unique_concepts": set(),
            "concept_frequency": Counter(),
            "category_distribution": Counter(),
            "pattern_distribution": Counter(),
            "top_concepts": [],
            "top_categories": [],
            "discovery_insights": []
        }
        
        # 收集统计信息
        for result in results:
            # 概念统计
            for concept_info in result.get("concepts_found", []):
                concept = concept_info["concept"]
                analysis["total_concepts"] += concept_info["frequency"]
                analysis["unique_concepts"].add(concept)
                analysis["concept_frequency"][concept] += concept_info["frequency"]
            
            # 分类统计
            category = result.get("category", "unknown")
            analysis["category_distribution"][category] += 1
            
            # 模式统计
            for pattern_type in ["definitions", "viewpoints", "methods", "examples", "comparisons", "relations"]:
                count = len(result.get(pattern_type, []))
                if count > 0:
                    analysis["pattern_distribution"][pattern_type] += count
        
        # 计算排名
        analysis["top_concepts"] = analysis["concept_frequency"].most_common(20)
        analysis["top_categories"] = analysis["category_distribution"].most_common(10)
        
        # 生成发现洞察
        analysis["discovery_insights"] = self.generate_discovery_insights(analysis, results)
        
        return analysis
    
    def generate_discovery_insights(self, analysis: Dict, results: List[Dict]) -> List[str]:
        """生成发现洞察"""
        insights = []
        
        # 1. 概念洞察
        if analysis["top_concepts"]:
            top_concept, top_count = analysis["top_concepts"][0]
            insights.append(f"最常出现的概念是 '{top_concept}'，出现了 {top_count} 次")
        
        # 2. 分类洞察
        if analysis["top_categories"]:
            top_category, top_count = analysis["top_categories"][0]
            percentage = top_count / len(results) * 100
            insights.append(f"主要内容类型是 '{top_category}'，占 {percentage:.1f}%")
        
        # 3. 模式洞察
        if analysis["pattern_distribution"]:
            top_pattern, top_count = analysis["pattern_distribution"].most_common(1)[0]
            insights.append(f"最常见的知识模式是 '{top_pattern}'，发现了 {top_count} 次")
        
        # 4. 新概念发现
        custom_concepts = set(self.custom_dict.keys())
        found_concepts = analysis["unique_concepts"]
        new_concepts = found_concepts - custom_concepts
        
        if new_concepts:
            insights.append(f"发现了 {len(new_concepts)} 个新概念，可能需要定义")
            # 取前5个新概念
            new_concepts_list = list(new_concepts)[:5]
            insights.append(f"新概念示例: {', '.join(new_concepts_list)}")
        
        # 5. 整理建议
        unorganized_count = len(results)
        if unorganized_count > 50:
            insights.append(f"有 {unorganized_count} 个未整理文件，建议批量整理")
        
        # 6. 质量洞察
        high_quality_files = []
        for result in results:
            if (len(result.get("definitions", [])) > 0 and 
                len(result.get("concepts_found", [])) > 3):
                high_quality_files.append(result["file_name"])
        
        if high_quality_files:
            insights.append(f"发现 {len(high_quality_files)} 个高质量文件，适合作为概念基础")
        
        return insights
    
    def generate_organizing_plan(self, mining_results: Dict) -> str:
        """生成整理计划"""
        plan = []
