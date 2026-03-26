#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业质量保证系统 - 璇玑台知识库的质量管理体系
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict, Counter

class QualityLevel(Enum):
    """质量等级"""
    EXCELLENT = "优秀"      # 90-100分
    GOOD = "良好"          # 80-89分
    FAIR = "中等"          # 70-79分
    NEEDS_IMPROVEMENT = "需要改进"  # 60-69分
    POOR = "较差"          # <60分

class ContentType(Enum):
    """内容类型"""
    CONCEPT = "概念"
    METHOD = "方法"
    PROJECT = "项目"
    CONVERSATION = "对话"
    DAILY = "日记"
    REFERENCE = "参考"

@dataclass
class QualityMetric:
    """质量指标"""
    name: str
    weight: float  # 权重 0-1
    min_score: int = 0
    max_score: int = 100
    description: str = ""
    
@dataclass
class QualityAssessment:
    """质量评估结果"""
    file_path: Path
    content_type: ContentType
    overall_score: float
    quality_level: QualityLevel
    metrics_scores: Dict[str, float]
    issues: List[str]
    suggestions: List[str]
    assessment_time: datetime
    assessor: str = "璇玑质量系统"

@dataclass
class QualityReport:
    """质量报告"""
    assessment: QualityAssessment
    details: Dict
    recommendations: List[str]
    next_review_date: datetime

class ProfessionalQualitySystem:
    """专业质量保证系统"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        
        # 质量标准配置
        self.quality_standards = self.load_quality_standards()
        
        # 质量指标
        self.metrics = self.define_metrics()
        
        # 质量数据库
        self.quality_db_path = self.obsidian_path / "system" / "quality" / "quality_database.json"
        self.quality_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载历史数据
        self.history = self.load_history()
    
    def load_quality_standards(self) -> Dict:
        """加载质量标准"""
        standards_path = self.obsidian_path / "system" / "quality" / "quality_standards.yaml"
        
        if standards_path.exists():
            with open(standards_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # 默认标准
        return {
            "concept": {
                "required_sections": ["定义", "核心观点", "应用场景", "相关概念"],
                "min_length": 500,
                "max_length": 5000,
                "min_links": 3,
                "max_links": 20,
                "min_tags": 3,
                "max_tags": 10
            },
            "method": {
                "required_sections": ["概述", "实施步骤", "适用场景", "关键要点"],
                "min_length": 300,
                "max_length": 3000,
                "min_links": 2,
                "max_links": 15,
                "min_tags": 2,
                "max_tags": 8
            },
            "project": {
                "required_sections": ["项目概述", "当前进展", "下一步计划"],
                "min_length": 200,
                "max_length": 2000,
                "min_links": 1,
                "max_links": 10,
                "min_tags": 2,
                "max_tags": 6
            }
        }
    
    def define_metrics(self) -> Dict[ContentType, List[QualityMetric]]:
        """定义质量指标"""
        metrics = {
            ContentType.CONCEPT: [
                QualityMetric("定义清晰度", 0.25, description="概念定义是否清晰准确"),
                QualityMetric("观点完整性", 0.20, description="核心观点是否完整系统"),
                QualityMetric("应用明确性", 0.15, description="应用场景是否清晰具体"),
                QualityMetric("关系丰富度", 0.20, description="相关概念链接是否丰富"),
                QualityMetric("案例充实度", 0.10, description="是否有具体案例支持"),
                QualityMetric("格式规范性", 0.10, description="是否符合格式标准")
            ],
            ContentType.METHOD: [
                QualityMetric("步骤清晰度", 0.30, description="实施步骤是否清晰可操作"),
                QualityMetric("适用性", 0.20, description="适用场景是否明确广泛"),
                QualityMetric("工具支持", 0.15, description="是否有具体工具支持"),
                QualityMetric("案例验证", 0.15, description="是否有成功案例验证"),
                QualityMetric("风险评估", 0.10, description="是否有风险评估和应对"),
                QualityMetric("格式规范性", 0.10, description="是否符合格式标准")
            ],
            ContentType.PROJECT: [
                QualityMetric("目标明确性", 0.25, description="项目目标是否清晰可衡量"),
                QualityMetric("进展透明性", 0.20, description="进展记录是否完整透明"),
                QualityMetric("成果明确性", 0.20, description="成果定义是否清晰可验证"),
                QualityMetric("团队协作性", 0.15, description="团队协作记录是否完整"),
                QualityMetric("经验总结性", 0.10, description="是否有经验教训总结"),
                QualityMetric("格式规范性", 0.10, description="是否符合格式标准")
            ],
            ContentType.CONVERSATION: [
                QualityMetric("主题明确性", 0.25, description="对话主题是否明确"),
                QualityMetric("内容完整性", 0.20, description="对话内容是否完整"),
                QualityMetric("价值提炼度", 0.20, description="是否提炼了对话价值"),
                QualityMetric("结构清晰度", 0.15, description="结构是否清晰"),
                QualityMetric("链接丰富度", 0.10, description="相关链接是否丰富"),
                QualityMetric("格式规范性", 0.10, description="是否符合格式标准")
            ]
        }
        
        return metrics
    
    def load_history(self) -> Dict:
        """加载历史数据"""
        if self.quality_db_path.exists():
            try:
                with open(self.quality_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "assessments": {},
            "statistics": {},
            "trends": {}
        }
    
    def save_history(self):
        """保存历史数据"""
        with open(self.quality_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def assess_file(self, file_path: Path) -> QualityAssessment:
        """评估单个文件"""
        print(f"专业评估: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 确定内容类型
            content_type = self.determine_content_type(file_path, content)
            
            # 执行评估
            metrics_scores = self.assess_metrics(content_type, content, file_path)
            
            # 计算总分
            overall_score = self.calculate_overall_score(metrics_scores)
            
            # 确定质量等级
            quality_level = self.determine_quality_level(overall_score)
            
            # 识别问题
            issues = self.identify_issues(content_type, content, metrics_scores)
            
            # 生成建议
            suggestions = self.generate_suggestions(content_type, issues, metrics_scores)
            
            # 创建评估结果
            assessment = QualityAssessment(
                file_path=file_path,
                content_type=content_type,
                overall_score=overall_score,
                quality_level=quality_level,
                metrics_scores=metrics_scores,
                issues=issues,
                suggestions=suggestions,
                assessment_time=datetime.now()
            )
            
            # 保存到历史
            self.save_assessment(assessment)
            
            return assessment
            
        except Exception as e:
            print(f"评估失败 {file_path.name}: {e}")
            # 返回一个基本的失败评估
            return QualityAssessment(
                file_path=file_path,
                content_type=ContentType.REFERENCE,
                overall_score=0,
                quality_level=QualityLevel.POOR,
                metrics_scores={},
                issues=[f"评估失败: {str(e)}"],
                suggestions=["重新评估或手动检查"],
                assessment_time=datetime.now()
            )
    
    def determine_content_type(self, file_path: Path, content: str) -> ContentType:
        """确定内容类型"""
        # 基于目录
        file_str = str(file_path)
        if "concepts" in file_str:
            return ContentType.CONCEPT
        elif "methods" in file_str:
            return ContentType.METHOD
        elif "projects" in file_str:
            return ContentType.PROJECT
        elif "conversations" in file_str:
            return ContentType.CONVERSATION
        elif "daily" in file_str:
            return ContentType.DAILY
        
        # 基于内容
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ["概念", "定义", "术语"]):
            return ContentType.CONCEPT
        elif any(keyword in content_lower for keyword in ["方法", "步骤", "流程"]):
            return ContentType.METHOD
        elif any(keyword in content_lower for keyword in ["项目", "实验", "任务"]):
            return ContentType.PROJECT
        elif any(keyword in content_lower for keyword in ["对话", "讨论", "交流"]):
            return ContentType.CONVERSATION
        
        return ContentType.REFERENCE
    
    def assess_metrics(self, content_type: ContentType, content: str, file_path: Path) -> Dict[str, float]:
        """评估各个指标"""
        metrics_scores = {}
        
        if content_type not in self.metrics:
            # 对于不支持的类型，返回基本评估
            return {"基础评估": 50.0}
        
        for metric in self.metrics[content_type]:
            score = self.assess_single_metric(metric, content_type, content, file_path)
            metrics_scores[metric.name] = score
        
        return metrics_scores
    
    def assess_single_metric(self, metric: QualityMetric, content_type: ContentType, 
                           content: str, file_path: Path) -> float:
        """评估单个指标"""
        metric_name = metric.name
        
        if metric_name == "定义清晰度":
            return self.assess_definition_clarity(content)
        elif metric_name == "观点完整性":
            return self.assess_viewpoint_completeness(content)
        elif metric_name == "应用明确性":
            return self.assess_application_clarity(content)
        elif metric_name == "关系丰富度":
            return self.assess_relation_richness(content)
        elif metric_name == "案例充实度":
            return self.assess_case_richness(content)
        elif metric_name == "格式规范性":
            return self.assess_format_standardization(content, file_path)
        elif metric_name == "步骤清晰度":
            return self.assess_step_clarity(content)
        elif metric_name == "适用性":
            return self.assess_applicability(content)
        elif metric_name == "工具支持":
            return self.assess_tool_support(content)
        elif metric_name == "案例验证":
            return self.assess_case_verification(content)
        elif metric_name == "风险评估":
            return self.assess_risk_assessment(content)
        elif metric_name == "目标明确性":
            return self.assess_goal_clarity(content)
        elif metric_name == "进展透明性":
            return self.assess_progress_transparency(content)
        elif metric_name == "成果明确性":
            return self.assess_result_clarity(content)
        elif metric_name == "团队协作性":
            return self.assess_team_collaboration(content)
        elif metric_name == "经验总结性":
            return self.assess_experience_summary(content)
        elif metric_name == "主题明确性":
            return self.assess_topic_clarity(content)
        elif metric_name == "内容完整性":
            return self.assess_content_completeness(content)
        elif metric_name == "价值提炼度":
            return self.assess_value_extraction(content)
        elif metric_name == "结构清晰度":
            return self.assess_structure_clarity(content)
        elif metric_name == "链接丰富度":
            return self.assess_link_richness(content)
        
        return 50.0  # 默认分数
    
    def assess_definition_clarity(self, content: str) -> float:
        """评估定义清晰度"""
        # 查找定义部分
        definition_patterns = [
            r'## 定义\s*\n(.+?)(?=\n##|\n#|$)',
            r'^定义[:：]\s*(.+)$',
            r'([^。]+?(?:是|指|定义为|意味着)[^。]+)'
        ]
        
        definitions = []
        for pattern in definition_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            definitions.extend(matches)
        
        if not definitions:
            return 20.0
        
        # 评估定义质量
        score = 40.0  # 基础分
        
        for definition in definitions[:3]:  # 只评估前3个定义
            definition = definition.strip()
            
            # 长度适中
            if 20 <= len(definition) <= 200:
                score += 10
            
            # 包含核心关键词
            if any(keyword in definition for keyword in ["是", "指", "意味着", "定义为"]):
                score += 10
            
            # 清晰明确
            if "待补充" not in definition and "..." not in definition:
                score += 10
        
        return min(100.0, score)
    
    def assess_viewpoint_completeness(self, content: str) -> float:
        """评估观点完整性"""
        # 查找观点部分
        viewpoint_section = re.search(r'## 核心观点\s*\n(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
        
        if not viewpoint_section:
            return 30.0
        
        viewpoint_content = viewpoint_section.group(1)
        
        # 计算列表项数量
        list_items = re.findall(r'^\s*[-*+]\s+.+$', viewpoint_content, re.MULTILINE)
        
        score = 30.0  # 基础分
        
        if list_items:
            # 有列表项
            score += 20
            
            # 数量适中
            if 3 <= len(list_items) <= 10:
                score += 20
            
            # 内容质量
            good_items = 0
            for item in list_items:
                if len(item.strip()) > 10 and "待补充" not in item:
                    good_items += 1
            
            if good_items >= 3:
                score += 30
        
        return min(100.0, score)
    
    def assess_application_clarity(self, content: str) -> float:
        """评估应用明确性"""
        # 查找应用场景部分
        application_section = re.search(r'## 应用场景\s*\n(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
        
        if not application_section:
            return 30.0
        
        application_content = application_section.group(1)
        
        # 计算子标题数量
        subheadings = re.findall(r'^###\s+.+$', application_content, re.MULTILINE)
        
        score = 30.0  # 基础分
        
        if subheadings:
            # 有子标题
            score += 20
            
            # 数量适中
            if 2 <= len(subheadings) <= 5:
                score += 20
            
            # 内容质量
            lines = application_content.split('\n')
            content_lines = [line for line in lines if line.strip() and not line.startswith('#')]
            
            if len(content_lines) >= 3:
                score += 30
        
        return min(100.0, score)
    
    def assess_relation_richness(self, content: str) -> float:
        """评估关系丰富度"""
        # 查找相关概念部分
        relation_section = re.search(r'## 相关概念\s*\n(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
        
        if not relation_section:
            # 尝试查找所有链接
            wiki_links = re.findall(r'\[\[(.+?)\]\]', content)
            if wiki_links:
                unique_links = set(wiki_links)
                score = min(100.0, len(unique_links) * 10)
                return score
            return 30.0
        
        relation_content = relation_section.group(1)
        
        # 计算链接数量
        wiki_links = re.findall(r'\[\[(.+?)\]\]', relation_content)
        
        score = 30.0  # 基础分
        
        if wiki_links:
            unique_links = set(wiki_links)
            
            # 数量评分
            if len(unique_links) >= 3:
                score += 40
            
            if len(unique_links) >= 5:
                score += 30
        
        return min(100.0, score)
    
    def assess_case_richness(self, content: str) -> float:
