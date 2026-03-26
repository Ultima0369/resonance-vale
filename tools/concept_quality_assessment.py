#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念质量评估系统 - 评估和提升概念文件的质量
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
import statistics

class ConceptQualityAssessment:
    """概念质量评估器"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.concepts_dir = self.obsidian_path / "concepts"
        self.quality_standards = self.load_quality_standards()
        
    def load_quality_standards(self) -> Dict:
        """加载质量标准"""
        standards = {
            "required_sections": [
                "定义",
                "核心观点", 
                "应用场景",
                "相关概念"
            ],
            
            "section_requirements": {
                "定义": {
                    "min_length": 50,
                    "max_length": 500,
                    "required_keywords": [],
                    "prohibited_phrases": ["待补充定义"]
                },
                "核心观点": {
                    "min_length": 100,
                    "max_length": 1000,
                    "required_keywords": [],
                    "prohibited_phrases": ["待补充核心观点"]
                },
                "应用场景": {
                    "min_length": 100,
                    "max_length": 1000,
                    "required_keywords": [],
                    "prohibited_phrases": ["待补充应用场景"]
                }
            },
            
            "metadata_requirements": {
                "required_fields": ["created", "updated", "tags", "related"],
                "tag_requirements": {
                    "min_tags": 3,
                    "max_tags": 10,
                    "required_categories": ["概念"]
                }
            },
            
            "linking_requirements": {
                "min_links": 3,
                "max_links": 15,
                "required_link_types": ["concept", "method", "project"]
            },
            
            "style_requirements": {
                "max_line_length": 100,
                "heading_levels": ["#", "##", "###"],
                "prohibited_formats": ["<html>", "<script>"]
            }
        }
        
        return standards
    
    def assess_concept_file(self, file_path: Path) -> Dict:
        """评估单个概念文件"""
        print(f"评估概念文件: {file_path.name}")
        
        assessment = {
            "file_name": file_path.name,
            "file_path": str(file_path.relative_to(self.obsidian_path)),
            "assessment_time": datetime.now().isoformat(),
            "scores": {},
            "issues": [],
            "suggestions": [],
            "overall_score": 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基础检查
            assessment.update(self.assess_basics(content))
            
            # 章节检查
            assessment.update(self.assess_sections(content))
            
            # 元数据检查
            assessment.update(self.assess_metadata(content))
            
            # 链接检查
            assessment.update(self.assess_links(content))
            
            # 风格检查
            assessment.update(self.assess_style(content))
            
            # 计算总分
            assessment["overall_score"] = self.calculate_overall_score(assessment)
            
            # 生成建议
            assessment["suggestions"] = self.generate_suggestions(assessment)
            
        except Exception as e:
            assessment["error"] = str(e)
            assessment["issues"].append(f"文件读取失败: {e}")
        
        return assessment
    
    def assess_basics(self, content: str) -> Dict:
        """基础检查"""
        basics = {
            "basics_score": 0,
            "basics_issues": [],
            "basics_details": {}
        }
        
        # 检查文件大小
        file_size = len(content)
        basics["basics_details"]["file_size"] = file_size
        
        if file_size < 500:
            basics["basics_issues"].append("文件过小，可能内容不完整")
        elif file_size > 10000:
            basics["basics_issues"].append("文件过大，可能过于冗长")
        else:
            basics["basics_score"] += 25
        
        # 检查标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            basics["basics_details"]["title"] = title
            
            if len(title) < 5:
                basics["basics_issues"].append("标题过短")
            elif len(title) > 50:
                basics["basics_issues"].append("标题过长")
            else:
                basics["basics_score"] += 25
        else:
            basics["basics_issues"].append("缺少标题")
        
        # 检查段落数量
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        basics["basics_details"]["paragraph_count"] = len(paragraphs)
        
        if len(paragraphs) < 5:
            basics["basics_issues"].append("段落数量不足，内容可能不充分")
        else:
            basics["basics_score"] += 25
        
        # 检查代码块
        code_blocks = re.findall(r'```[\s\S]+?```', content)
        basics["basics_details"]["code_block_count"] = len(code_blocks)
        
        # 检查列表
        list_items = re.findall(r'^\s*[-*+]\s+.+$', content, re.MULTILINE)
        basics["basics_details"]["list_item_count"] = len(list_items)
        
        if len(list_items) > 0:
            basics["basics_score"] += 25
        
        return basics
    
    def assess_sections(self, content: str) -> Dict:
        """章节检查"""
        sections = {
            "sections_score": 0,
            "sections_issues": [],
            "sections_details": {}
        }
        
        required_sections = self.quality_standards["required_sections"]
        section_requirements = self.quality_standards["section_requirements"]
        
        sections_found = {}
        
        for section_name in required_sections:
            # 查找章节
            pattern = rf'## {re.escape(section_name)}\s*\n(.+?)(?=\n##|\n#|$)'
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            
            if match:
                section_content = match.group(1).strip()
                sections_found[section_name] = {
                    "content": section_content,
                    "length": len(section_content)
                }
                
                # 检查章节要求
                if section_name in section_requirements:
                    req = section_requirements[section_name]
                    
                    # 检查长度
                    if req["min_length"] > 0 and len(section_content) < req["min_length"]:
                        sections["sections_issues"].append(f"章节'{section_name}'内容过短")
                    elif req["max_length"] > 0 and len(section_content) > req["max_length"]:
                        sections["sections_issues"].append(f"章节'{section_name}'内容过长")
                    else:
                        sections["sections_score"] += 10
                    
                    # 检查禁止短语
                    for prohibited in req["prohibited_phrases"]:
                        if prohibited in section_content:
                            sections["sections_issues"].append(f"章节'{section_name}'包含禁止短语: {prohibited}")
                            sections["sections_score"] -= 5
                
            else:
                sections["sections_issues"].append(f"缺少必要章节: {section_name}")
        
        sections["sections_details"]["sections_found"] = sections_found
        sections["sections_details"]["required_sections_count"] = len(required_sections)
        sections["sections_details"]["found_sections_count"] = len(sections_found)
        
        # 额外加分：找到的章节比例
        if sections_found:
            found_ratio = len(sections_found) / len(required_sections)
            sections["sections_score"] += int(found_ratio * 50)
        
        return sections
    
    def assess_metadata(self, content: str) -> Dict:
        """元数据检查"""
        metadata = {
            "metadata_score": 0,
            "metadata_issues": [],
            "metadata_details": {}
        }
        
        # 提取YAML frontmatter
        frontmatter_match = re.search(r'^---\s*\n([\s\S]+?)\n---', content)
        
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            metadata["metadata_details"]["has_frontmatter"] = True
            
            # 解析字段
            fields = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    fields[key.strip()] = value.strip()
            
            metadata["metadata_details"]["fields"] = fields
            
            # 检查必要字段
            required_fields = self.quality_standards["metadata_requirements"]["required_fields"]
            for field in required_fields:
                if field in fields:
                    metadata["metadata_score"] += 10
                else:
                    metadata["metadata_issues"].append(f"缺少必要元数据字段: {field}")
            
            # 检查标签
            if "tags" in fields:
                tags_text = fields["tags"]
                # 解析标签列表
                if tags_text.startswith('[') and tags_text.endswith(']'):
                    tags = [tag.strip().strip("'\"") for tag in tags_text[1:-1].split(',')]
                    metadata["metadata_details"]["tags"] = tags
                    
                    tag_req = self.quality_standards["metadata_requirements"]["tag_requirements"]
                    
                    # 检查标签数量
                    if len(tags) < tag_req["min_tags"]:
                        metadata["metadata_issues"].append(f"标签数量不足，至少需要{tag_req['min_tags']}个")
                    elif len(tags) > tag_req["max_tags"]:
                        metadata["metadata_issues"].append(f"标签数量过多，最多{tag_req['max_tags']}个")
                    else:
                        metadata["metadata_score"] += 10
                    
                    # 检查必要分类
                    required_categories = tag_req["required_categories"]
                    has_required = any(any(cat in tag for cat in required_categories) for tag in tags)
                    if has_required:
                        metadata["metadata_score"] += 10
                    else:
                        metadata["metadata_issues"].append(f"缺少必要分类标签，如{required_categories}")
            
        else:
            metadata["metadata_issues"].append("缺少YAML frontmatter")
            metadata["metadata_details"]["has_frontmatter"] = False
        
        return metadata
    
    def assess_links(self, content: str) -> Dict:
        """链接检查"""
        links = {
            "links_score": 0,
            "links_issues": [],
            "links_details": {}
        }
        
        # 查找所有链接
        wiki_links = re.findall(r'\[\[(.+?)\]\]', content)
        markdown_links = re.findall(r'\[(.+?)\]\((.+?)\)', content)
        
        links["links_details"]["wiki_links"] = wiki_links
        links["links_details"]["markdown_links"] = markdown_links
        links["links_details"]["total_links"] = len(wiki_links) + len(markdown_links)
        
        # 检查链接数量
        link_req = self.quality_standards["linking_requirements"]
        total_links = links["links_details"]["total_links"]
        
        if total_links < link_req["min_links"]:
            links["links_issues"].append(f"链接数量不足，至少需要{link_req['min_links']}个")
        elif total_links > link_req["max_links"]:
            links["links_issues"].append(f"链接数量过多，最多{link_req['max_links']}个")
        else:
            links["links_score"] += 50
        
        # 检查链接类型
        if wiki_links:
            links["links_score"] += 25
        
        # 检查自链接（链接到自己的概念）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            concept_title = title_match.group(1).strip()
            if f"[[{concept_title}]]" in wiki_links:
                links["links_issues"].append("包含自链接，可能没有必要")
        
        return links
    
    def assess_style(self, content: str) -> Dict:
        """风格检查"""
        style = {
            "style_score": 0,
            "style_issues": [],
            "style_details": {}
        }
        
        lines = content.split('\n')
        
        # 检查行长度
        long_lines = []
        for i, line in enumerate(lines, 1):
            if len(line) > self.quality_standards["style_requirements"]["max_line_length"]:
                long_lines.append((i, len(line)))
        
        style["style_details"]["long_lines"] = long_lines
        style["style_details"]["total_lines"] = len(lines)
        
        if long_lines:
            long_line_count = len(long_lines)
            if long_line_count > 5:
                style["style_issues"].append(f"有{long_line_count}行过长，建议拆分")
                style["style_score"] -= long_line_count * 2
        else:
            style["style_score"] += 20
        
        # 检查标题级别
        heading_levels = []
        for line in lines:
            if line.startswith('#'):
                level = len(line.split(' ')[0])
                heading_levels.append(level)
        
        style["style_details"]["heading_levels"] = heading_levels
        
        # 检查标题顺序
        if heading_levels:
            expected_level = 1
            for level in heading_levels:
                if level > expected_level + 1:
                    style["style_issues"].append("标题级别跳跃，建议按顺序使用标题")
                    break
                expected_level = level
        
        # 检查禁止格式
        for prohibited in self.quality_standards["style_requirements"]["prohibited_formats"]:
            if prohibited in content:
                style["style_issues"].append(f"包含禁止格式: {prohibited}")
                style["style_score"] -= 10
        
        # 加分：良好的格式
        if not style["style_issues"]:
            style["style_score"] += 30
        
        return style
    
    def calculate_overall_score(self, assessment: Dict) -> int:
        """计算总分"""
        scores = []
        
        if "basics_score" in assessment:
            scores.append(assessment["basics_score"])
        
        if "sections_score" in assessment:
            scores.append(assessment["sections_score"])
        
        if "metadata_score" in assessment:
            scores.append(assessment["metadata_score"])
        
        if "links_score" in assessment:
            scores.append(assessment["links_score"])
        
        if "style_score" in assessment:
            scores.append(assessment["style_score"])
        
        if scores:
            # 加权平均
            weights = [0.15, 0.25, 0.20, 0.25, 0.15]  # 基础15%，章节25%，元数据20%，链接25%，风格15%
            weighted_sum = sum(score * weight for score, weight in zip(scores, weights[:len(scores)]))
            return min(100, max(0, int(weighted_sum)))
        else:
            return 0
    
    def generate_suggestions(self, assessment: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 根据问题生成建议
        all_issues = []
        for key in ["basics_issues", "sections_issues", "metadata_issues", "links_issues", "style_issues"]:
            if key in assessment and assessment[key]:
                all_issues.extend(assessment[key])
        
        # 基础建议
        if assessment.get("overall_score", 0) < 60:
            suggestions.append("整体质量较低，建议全面修订")
        elif assessment.get("overall_score", 0) < 80:
            suggestions.append("质量中等，建议针对性改进")
        else:
            suggestions.append("质量良好，建议保持并继续优化")
        
        # 具体问题建议
        for issue in all_issues[:5]:  # 只处理前5个问题
            if "过短" in issue:
                suggestions.append(f"增加内容长度: {issue}")
            elif "过长" in issue:
                suggestions.append(f"精简内容: {issue}")
            elif "缺少" in issue:
                suggestions.append(f"补充缺失内容: {issue}")
            elif "不足" in issue:
                suggestions.append(f"增加数量: {issue}")
            elif "过多" in issue:
                suggestions.append(f"减少数量: {issue}")
            elif "包含禁止" in issue:
                suggestions.append(f"移除禁止内容: {issue}")
            else:
                suggestions.append(f"处理问题: {issue}")
        
        # 额外建议
        if assessment.get("links_details", {}).get("total_links", 0) < 5:
            suggestions.append("建议增加更多概念链接，建立知识网络")
        
        if assessment.get("sections_details", {}).get("found_sections_count", 0) < 4:
            suggestions.append("建议补充缺失的章节，完善概念结构")
        
        return suggestions[:10]  # 最多10条建议
    
    def assess_all_concepts(self) -> Dict:
        """评估所有概念文件"""
        print("开始评估所有概念文件...")
        
        if not self.concepts_dir.exists():
            return {"error": "concepts目录不存在"}
        
        assessments = {}
        concept_files = list(self.concepts_dir.glob("*.md"))
        concept_files = [f for f in concept_files if f.name