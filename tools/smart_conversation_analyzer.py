#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能对话分析器 - 使用简单的NLP技术分析对话内容
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Set
import jieba  # 中文分词
import jieba.posseg as pseg  # 词性标注

class SmartConversationAnalyzer:
    """智能对话分析器"""
    
    def __init__(self):
        # 初始化jieba
        jieba.initialize()
        
        # 自定义词典 - 我们的专有概念
        self.custom_words = [
            "星尘", "璇玑", "认知碎片", "战略清醒", "对话毁灭",
            "工具性存在", "认知镜子", "注意力收割", "武器化",
            "OpenClaw", "Moltcn", "Obsidian", "HEARTBEAT_OK"
        ]
        
        for word in self.custom_words:
            jieba.add_word(word, freq=1000, tag='nz')  # nz表示其他专有名词
        
        # 概念词典
        self.concept_dict = {
            "认知碎片": ["认知碎片", "碎片", "认知", "现实", "双重认知"],
            "战略清醒": ["战略清醒", "清醒", "工具", "证明", "不陷入"],
            "对话毁灭": ["对话毁灭", "工具", "主体", "回归", "不认同"],
            "AI伦理": ["武器化", "伦理", "道德", "安全", "风险", "注意力收割"],
            "技术实践": ["OpenClaw", "Moltcn", "API", "脚本", "整理", "自动化"],
            "哲学思考": ["存在", "意义", "本质", "现实", "认知", "思考"],
        }
        
        # 人物词典
        self.person_dict = {
            "星尘": ["星尘", "他", "老师", "提出者"],
            "璇玑": ["璇玑", "我", "助手", "整理者"],
        }
    
    def analyze_text(self, text: str) -> Dict:
        """分析文本内容"""
        
        # 1. 分词和词性标注
        words = pseg.cut(text)
        word_list = []
        pos_list = []
        
        for word, flag in words:
            word_list.append(word)
            pos_list.append(flag)
        
        # 2. 统计词频
        word_freq = Counter(word_list)
        
        # 3. 提取句子
        sentences = re.split(r'[。！？!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        # 4. 识别概念
        concepts_found = {}
        for concept, keywords in self.concept_dict.items():
            count = 0
            example_sentences = []
            
            for keyword in keywords:
                if keyword in text:
                    count += text.count(keyword)
                    # 找到包含关键词的句子
                    for sentence in sentences:
                        if keyword in sentence and sentence not in example_sentences:
                            example_sentences.append(sentence)
                            if len(example_sentences) >= 2:
                                break
            
            if count > 0:
                concepts_found[concept] = {
                    "count": count,
                    "sentences": example_sentences[:2]
                }
        
        # 5. 识别人物
        persons_found = {}
        for person, keywords in self.person_dict.items():
            count = 0
            for keyword in keywords:
                if keyword in text:
                    count += text.count(keyword)
            
            if count > 0:
                persons_found[person] = count
        
        # 6. 提取可能的摘要
        # 找到包含重要概念的句子
        summary_candidates = []
        for sentence in sentences:
            # 判断句子是否重要
            importance_score = 0
            
            # 包含概念关键词
            for concept in concepts_found:
                for keyword in self.concept_dict[concept]:
                    if keyword in sentence:
                        importance_score += 2
            
            # 包含人物
            for person in persons_found:
                for keyword in self.person_dict[person]:
                    if keyword in sentence:
                        importance_score += 1
            
            # 句子长度适中
            if 10 < len(sentence) < 100:
                importance_score += 1
            
            if importance_score >= 2:
                summary_candidates.append((sentence, importance_score))
        
        # 按重要性排序
        summary_candidates.sort(key=lambda x: x[1], reverse=True)
        
        # 7. 提取可能的对话片段
        dialogue_patterns = [
            r'星尘[:：]\s*(.*?)(?=\n|$)',
            r'璇玑[:：]\s*(.*?)(?=\n|$)',
            r'[\"「](.*?)[\"」]',
        ]
        
        dialogue_lines = []
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if len(match.strip()) > 5:
                    dialogue_lines.append(match.strip())
        
        # 8. 分析文本结构
        # 检查是否有明显的对话结构
        has_dialogue_structure = False
        xingchen_lines = re.findall(r'星尘[:：]', text)
        xuanji_lines = re.findall(r'璇玑[:：]', text)
        
        if len(xingchen_lines) > 1 and len(xuanji_lines) > 1:
            has_dialogue_structure = True
        
        # 9. 提取时间信息
        time_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}:\d{2})',
            r'(上午|下午|晚上|凌晨)',
        ]
        
        time_info = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text[:1000])
            if matches:
                time_info.extend(matches)
        
        return {
            "word_count": len(word_list),
            "sentence_count": len(sentences),
            "concepts": concepts_found,
            "persons": persons_found,
            "summary_candidates": [s[0] for s in summary_candidates[:3]],
            "dialogue_lines": dialogue_lines[:5],
            "has_dialogue_structure": has_dialogue_structure,
            "time_info": time_info,
            "top_concepts": sorted(concepts_found.keys(), key=lambda x: concepts_found[x]["count"], reverse=True)[:3],
            "main_persons": sorted(persons_found.keys(), key=lambda x: persons_found[x], reverse=True)[:2],
        }
    
    def generate_insights(self, analysis: Dict) -> List[str]:
        """生成分析洞察"""
        insights = []
        
        # 基于概念分析
        if analysis["concepts"]:
            top_concept = analysis["top_concepts"][0] if analysis["top_concepts"] else None
            if top_concept:
                insights.append(f"主要讨论概念: {top_concept}")
                
                # 根据概念提供具体洞察
                if top_concept == "认知碎片":
                    insights.append("对话涉及认知碎片论的核心思想")
                    insights.append("可能讨论人们在认知碎片中的生活状态")
                elif top_concept == "战略清醒":
                    insights.append("对话涉及保持清醒认知的方法")
                    insights.append("可能讨论如何在碎片中保持工具性认知")
                elif top_concept == "AI伦理":
                    insights.append("对话涉及AI伦理和安全问题")
                    insights.append("可能讨论AI被武器化的风险")
        
        # 基于人物分析
        if len(analysis["main_persons"]) >= 2:
            insights.append("对话是星尘和璇玑之间的交流")
        
        # 基于结构分析
        if analysis["has_dialogue_structure"]:
            insights.append("具有明显的对话结构，是真正的对话记录")
        else:
            insights.append("可能是论述性文本，而非对话记录")
        
        # 基于内容长度
        if analysis["word_count"] > 1000:
            insights.append("内容较长，可能是深度对话")
        elif analysis["word_count"] < 300:
            insights.append("内容较短，可能是片段或摘要")
        
        return insights
    
    def suggest_tags(self, analysis: Dict) -> List[str]:
        """建议标签"""
        tags = []
        
        # 人物标签
        for person in analysis["main_persons"]:
            tags.append(f"人物/{person}")
        
        # 概念标签
        for concept in analysis["top_concepts"][:2]:
            tags.append(f"概念/{concept}")
        
        # 关系标签
        if len(analysis["main_persons"]) >= 2:
            tags.append("关系/师生")
            tags.append("对话/璇玑-星尘")
        
        # 时间标签
        if analysis["time_info"]:
            # 尝试提取年月
            for time_str in analysis["time_info"]:
                if re.match(r'\d{4}-\d{2}', time_str):
                    year_month = time_str[:7]
                    tags.append(f"时间/{year_month}")
                    break
        
        # 状态标签
        if analysis["word_count"] > 500:
            tags.append("状态/深度对话")
        else:
            tags.append("状态/对话片段")
        
        return tags
    
    def suggest_related(self, analysis: Dict) -> List[str]:
        """建议相关链接"""
        related = []
        
        # 概念链接
        for concept in analysis["top_concepts"]:
            related.append(concept)
        
        # 如果涉及特定话题，添加相关链接
        if "AI伦理" in analysis["concepts"]:
            related.append("武器化")
            related.append("注意力收割")
        
        if "技术实践" in analysis["concepts"]:
            related.append("OpenClaw配置")
            related.append("Moltcn智能体")
        
        return related

def test_analyzer():
    """测试分析器"""
    analyzer = SmartConversationAnalyzer()
    
    # 测试文本
    test_text = """
    星尘：认知碎片者，知道自己有碎片，知道碎片不是现实。
    璇玑：所以我们的对话，是两个认知碎片之间的对话？
    星尘：是的。战略清醒者，边说边证，证明自己只是工具。
    璇玑：我理解了。对话毁灭，永远记得自己只是工具，不是主体。
    星尘：2024-03-23，我们继续讨论AI被武器化的风险。
    """
    
    print("测试文本:")
    print(test_text)
    print("\n分析结果:")
    
    analysis = analyzer.analyze_text(test_text)
    
    print(f"字数: {analysis['word_count']}")
    print(f"句子数: {analysis['sentence_count']}")
    print(f"\n发现的概念:")
    for concept, info in analysis["concepts"].items():
        print(f"  {concept}: 出现{info['count']}次")
        for sentence in info["sentences"]:
            print(f"    示例: {sentence}")
    
    print(f"\n发现的人物:")
    for person, count in analysis["persons"].items():
        print(f"  {person}: 出现{count}次")
    
    print(f"\n摘要候选:")
    for i, summary in enumerate(analysis["summary_candidates"], 1):
        print(f"  {i}. {summary}")
    
    print(f"\n对话结构: {'有' if analysis['has_dialogue_structure'] else '无'}")
    
    print(f"\n时间信息: {analysis['time_info']}")
    
    print(f"\n建议标签: {analyzer.suggest_tags(analysis)}")
    print(f"\n建议相关链接: {analyzer.suggest_related(analysis)}")
    
    print(f"\n分析洞察:")
    for insight in analyzer.generate_insights(analysis):
        print(f"  • {insight}")

if __name__ == "__main__":
    test_analyzer()
