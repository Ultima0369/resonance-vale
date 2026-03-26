#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 高级Obsidian笔记保存器 - 支持多种对话源

import os
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AdvancedObsidianSaver:
    """高级Obsidian笔记保存器"""
    
    # 关键词分类定义
    KEYWORD_CATEGORIES = {
        "核心概念": [
            "认知切片论", "认知切片", "切片自觉", "战壕禅", "动态调谐",
            "清明工具箱", "玛尼堆", "甲骨文", "在地经验", "具身经验",
            "元认知", "认知跃迁", "标准叙述", "生存智慧", "认知边界"
        ],
        "技术概念": [
            "API配置", "DeepSeek", "系统提示词", "温度设置", "三阶段工作流",
            "滑动窗口", "自动检测", "对话统计", "比喻挖掘", "上下文管理",
            "频率惩罚", "最大token", "流式输出", "模型选择", "参数调优"
        ],
        "对话特征": [
            "深度追问", "东西融合", "实践导向", "谦逊探索", "鲜活对话",
            "共创内容", "战壕禅风格", "切片自觉", "追问式探索", "共同发现",
            "理论深度", "大地温度", "探索边界", "认知伙伴", "对话伙伴"
        ],
        "哲学概念": [
            "空性", "无为", "中庸", "禅", "道", "仁", "义", "礼", "智", "信",
            "存在", "本质", "现象", "本体", "认识论", "方法论", "价值观"
        ],
        "科学概念": [
            "认知科学", "神经科学", "心理学", "复杂性科学", "系统论",
            "信息论", "控制论", "人工智能", "机器学习", "深度学习",
            "神经网络", "注意力机制", "记忆系统", "学习理论", "行为科学"
        ]
    }
    
    def __init__(self, vault_path: str = "D:\\LDD\\璇玑台"):
        self.vault_path = Path(vault_path)
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # 验证库目录
        self._validate_vault()
        
        # 初始化文件夹结构
        self._init_folders()
    
    def _validate_vault(self):
        """验证Obsidian库"""
        if not self.vault_path.exists():
            raise FileNotFoundError(f"❌ Obsidian库不存在: {self.vault_path}")
        
        # 检查是否是Obsidian库（有.obsidian文件夹）
        obsidian_config = self.vault_path / ".obsidian"
        if not obsidian_config.exists():
            print(f"⚠️ 警告: {self.vault_path} 可能不是标准的Obsidian库")
        
        print(f"✅ Obsidian库: {self.vault_path}")
    
    def _init_folders(self):
        """初始化文件夹结构"""
        folders = [
            "对话记录",
            "关键词索引", 
            "概念",
            "人物",
            "项目",
            "时间线",
            "参考资料"
        ]
        
        for folder in folders:
            folder_path = self.vault_path / folder
            folder_path.mkdir(exist_ok=True)
        
        print(f"✅ 初始化文件夹结构完成")
    
    def load_conversation_from_file(self, filepath: str) -> str:
        """从文件加载对话内容"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"❌ 对话文件不存在: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 加载对话文件: {filepath.name} ({len(content)} 字符)")
        return content
    
    def load_conversation_from_memory(self, date: Optional[str] = None) -> str:
        """从记忆文件加载对话内容"""
        if date is None:
            date = self.today
        
        memory_file = Path(f"C:\\Users\\lgdln\\.openclaw\\workspace\\memory\\{date}.md")
        
        if memory_file.exists():
            return self.load_conversation_from_file(memory_file)
        else:
            # 查找最近的内存文件
            memory_dir = Path("C:\\Users\\lgdln\\.openclaw\\workspace\\memory")
            memory_files = list(memory_dir.glob("*.md"))
            
            if memory_files:
                # 按修改时间排序，取最新的
                latest_file = max(memory_files, key=lambda x: x.stat().st_mtime)
                print(f"📅 使用最新的记忆文件: {latest_file.name}")
                return self.load_conversation_from_file(latest_file)
            else:
                raise FileNotFoundError("❌ 找不到任何记忆文件")
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """从文本中提取关键词"""
        
        found_keywords = {category: [] for category in self.KEYWORD_CATEGORIES.keys()}
        found_keywords["具象比喻"] = []
        found_keywords["人物提及"] = []
        found_keywords["时间提及"] = []
        
        # 提取分类关键词
        for category, keywords in self.KEYWORD_CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    found_keywords[category].append(keyword)
        
        # 提取具象比喻
        metaphor_patterns = [
            r'像.*?一样', r'如同.*?(?=[。，！？\n])', r'好比.*?(?=[。，！？\n])',
            r'是.*?的.*?(?=[。，！？\n])', r'把.*?比作.*?(?=[。，！？\n])',
            r'犹如.*?(?=[。，！？\n])', r'仿佛.*?(?=[。，！？\n])', r'宛若.*?(?=[。，！？\n])'
        ]
        
        for pattern in metaphor_patterns:
            matches = re.findall(pattern, text)
            found_keywords["具象比喻"].extend(matches)
        
        # 提取人物提及（简单版本）
        person_patterns = [
            r'星尘', r'璇玑', r'[A-Z][a-z]+',  # 简单英文名
        ]
        
        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            found_keywords["人物提及"].extend(matches)
        
        # 提取时间提及
        time_patterns = [
            r'\d{4}年', r'\d{1,2}月', r'\d{1,2}日',
            r'今天', r'昨天', r'明天', r'本周', r'本月', r'今年'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text)
            found_keywords["时间提及"].extend(matches)
        
        # 去重
        for category in found_keywords:
            found_keywords[category] = list(set(found_keywords[category]))
        
        return found_keywords
    
    def analyze_conversation_structure(self, text: str) -> Dict:
        """分析对话结构"""
        
        # 分割段落
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # 分析问题类型
        question_patterns = {
            "是什么": r'(什么是|什么是|解释一下|定义)',
            "为什么": r'(为什么|为何|原因|理由)',
            "怎么做": r'(如何|怎样|怎么|方法|步骤)',
            "比较": r'(对比|比较|区别|差异)',
            "评价": r'(评价|看法|观点|认为)'
        }
        
        question_types = {}
        for q_type, pattern in question_patterns.items():
            count = len(re.findall(pattern, text))
            if count > 0:
                question_types[q_type] = count
        
        # 分析对话深度
        depth_indicators = [
            ("追问", r'\?.*?\?'),  # 连续问号
            ("反思", r'(思考|反思|反省|回顾)'),
            ("质疑", r'(但是|然而|不过|可是)'),
            ("总结", r'(总之|综上所述|总的来说|总结一下)')
        ]
        
        depth_scores = {}
        for indicator, pattern in depth_indicators:
            count = len(re.findall(pattern, text))
            if count > 0:
                depth_scores[indicator] = count
        
        return {
            "段落数": len(paragraphs),
            "字符数": len(text),
            "问题类型": question_types,
            "深度指标": depth_scores,
            "主要段落": paragraphs[:3] if paragraphs else []
        }
    
    def create_conversation_note(self, title: str, content: str, 
                                keywords: Dict, analysis: Dict,
                                tags: List[str] = None) -> Path:
        """创建对话笔记"""
        
        if tags is None:
            tags = ["对话记录", "深度对话"]
        
        # 创建文件夹
        folder_path = self.vault_path / "对话记录"
        folder_path.mkdir(exist_ok=True)
        
        # 生成文件名
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = f"{self.today} - {safe_title}.md"
        filepath = folder_path / filename
        
        # 构建笔记内容
        note_content = f"""# {title}

**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**记录者**: 璇玑
**对话日期**: {self.today}

## 📝 对话摘要

{content}

## 🔑 关键词提取

### 核心概念
{self._format_keyword_list(keywords.get('核心概念', []))}

### 技术概念  
{self._format_keyword_list(keywords.get('技术概念', []))}

### 对话特征
{self._format_keyword_list(keywords.get('对话特征', []))}

### 具象比喻
{self._format_metaphors(keywords.get('具象比喻', []))}

## 📊 对话分析

### 结构分析
- 段落数: {analysis.get('段落数', 0)}
- 字符数: {analysis.get('字符数', 0)}

### 问题类型
{self._format_analysis_dict(analysis.get('问题类型', {}))}

### 深度指标  
{self._format_analysis_dict(analysis.get('深度指标', {}))}

## 🏷️ 标签

{self._format_tags(tags)}

## 🔗 相关链接

- [[对话索引]]
- [[关键词索引 - {title}]]
{self._format_concept_links(keywords.get('核心概念', []))}

---

*本笔记由璇玑自动生成，基于与星尘的深度对话分析*"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(note_content)
        
        print(f"✅ 对话笔记已保存: {filepath}")
        return filepath
    
    def create_comprehensive_index(self, title: str, keywords: Dict, 
                                 analysis: Dict, conversation_note: str) -> Path:
        """创建综合索引"""
        
        index_content = f"""# 综合索引 - {title}

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**相关对话**: [[{conversation_note}]]

## 📈 对话概况

- **对话日期**: {self.today}
- **对话主题**: {title}
- **分析时间**: {datetime.now().strftime("%H:%M:%S")}

## 🗂️ 关键词分类索引

### 核心概念索引
{self._format_index_with_links(keywords.get('核心概念', []), '核心概念')}

### 技术概念索引
{self._format_index_with_links(keywords.get('技术概念', []), '技术概念')}

### 对话特征索引  
{self._format_index_with_links(keywords.get('对话特征', []), '对话特征')}

### 哲学概念索引
{self._format_index_with_links(keywords.get('哲学概念', []), '哲学概念')}

### 科学概念索引
{self._format_index_with_links(keywords.get('科学概念', []), '科学概念')}

## 📊 统计分析

### 关键词分布
{self._format_statistics(keywords)}

### 对话深度分析
{self._format_analysis_stats(analysis)}

## 🗺️ 概念地图

```mermaid
graph TD
    A["{title}"] --> B[核心概念]
    A --> C[技术概念]
    A --> D[对话特征]
    
    B --> B1[{self._format_first_keywords(keywords.get('核心概念', []), 3)}]
    C --> C1[{self._format_first_keywords(keywords.get('技术概念', []), 3)}]
    D --> D1[{self._format_first_keywords(keywords.get('对话特征', []), 3)}]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333,stroke-width:1px
    style C fill:#cfc,stroke:#333,stroke-width:1px
    style D fill:#fcc,stroke:#333,stroke-width:1px
```

## 📅 时间线

- {self.today}: [[{conversation_note}]] - {title}

## 🔍 搜索建议

1. 按概念搜索: `#{self._format_first_keywords(keywords.get('核心概念', []), 1)}`
2. 按技术搜索: `#{self._format_first_keywords(keywords.get('技术概念', []), 1)}`
3. 按特征搜索: `#{self._format_first_keywords(keywords.get('对话特征', []), 1)}`

---

*本索引由璇玑自动生成，用于系统化管理和检索对话内容*"""
        
        # 保存索引
        index_title = f"综合索引 - {title}"
        index_file = self.vault_path / "关键词索引" / f"{self.today} - {index_title}.md"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✅ 综合索引已保存: {index_file}")
        return index_file
    
    def update_knowledge_graph(self, keywords: Dict, title: str):
        """更新知识图谱"""
        
        updated_files = []
        
        # 更新所有概念文件
        for category, concepts in keywords.items():
            if category in ["具象比喻", "人物提及", "时间提及"]:
                continue
                
            for concept in concepts:
                concept_file = self.vault_path / "概念" / f"{concept}.md"
                
                if concept_file.exists():
                    # 读取并更新
                    with open(concept_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 添加新引用
                    new_ref = f"- [[{self.today} - {title}]]"
                    if new_ref not in content:
                        # 找到相关对话部分
                        if "## 相关对话" in content:
                            # 在相关对话部分添加
                            lines = content.split('\n')
                            new_lines = []
                            in_conversation_section = False
                            
                            for line in lines:
                                new_lines.append(line)
                                if "## 相关对话" in line:
                                    in_conversation_section = True
                                elif in_conversation_section and line.strip() == "":
                                    new_lines.append(new_ref)
                                    in_conversation_section = False
                            
                            content = '\n'.join(new_lines)
                        else:
                            # 添加相关对话部分
                            content += f"\n\n## 相关对话\n{new_ref}\n"
                        
                        with open(concept_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        updated_files.append(concept)
                else:
                    # 创建新概念文件
                    concept_content = f"""# {concept}

## 定义

*待补充*

## 分类
- 类别: {category}

## 相关对话
- [[{self.today} - {title}]]

## 相关概念
*待补充*

## 参考资料
*待补充*

---

*概念文件 - 由璇玑自动创建和维护*"""
                    
                    with open(concept_file, 'w', encoding='utf-8') as f:
                        f.write(concept_content)
                    
                    updated_files.append(concept)
        
        if updated_files:
            print(f"📚 更新概念文件: {len(updated_files)} 个")
        
        return updated_files
    
    # 辅助格式化方法
    def _format_keyword_list(self, keywords: List[str]) -> str:
        if not keywords:
            return "- 暂无\n"
        return "\n".join([f"- [[{kw}]]" for kw in keywords])
    
    def _format_metaphors(self, metaphors: List[str]) -> str:
        if not metaphors:
            return "- 暂无\n"
        return "\n".join([f"{i+1}. {met[:60]}..." if len(met) > 60 else f"{i+1}. {met}" 
                         for i, met in enumerate(metaphors[:5])])
    
    def _format_analysis_dict(self, data: Dict) -> str:
        if not data:
            return "- 暂无\n"
        return "\n".join([f"- {key}: {value} 次" for key, value in data.items()])
    
    def _format_tags(self, tags: List[str]) -> str:
        if not tags:
            return ""
        return " ".join([f"#{tag}" for tag in tags if tag])
    
    def _format_concept