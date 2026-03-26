#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话整理工具 - 专门用于整理璇玑和星尘的对话记录

功能：
1. 分析对话文件，提取关键信息
2. 自动生成整理后的Markdown文件
3. 建立概念链接和标签
4. 更新索引文件
"""

import os
import re
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

class ConversationOrganizer:
    """对话整理器"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.conversations_path = self.obsidian_path / "conversations" / "璇玑-星尘"
        
        # 确保目录存在
        self.conversations_path.mkdir(parents=True, exist_ok=True)
        
        # 标签系统
        self.tag_categories = {
            "人物": ["星尘", "璇玑"],
            "概念": ["认知碎片", "战略清醒", "对话毁灭", "工具性存在", "认知镜子"],
            "话题": ["AI伦理", "哲学思考", "技术实践", "知识管理", "对话整理"],
            "项目": ["Moltcn", "OpenClaw", "璇玑实验"],
            "状态": ["进行中", "已完成", "待整理", "重要"],
            "时间": []  # 动态生成
        }
        
        # 模板
        self.template = """---
created: {created}
updated: {updated}
tags: [{tags}]
related: [{related}]
---

# {title}

## 摘要
{summary}

## 来源信息
- **原始文件**: {source_file}
- **对话时间**: {conversation_time}
- **整理时间**: {organized_time}

## 参与者
{participants}

## 对话背景
{context}

## 核心内容
{content}

## 关键洞察
{insights}

## 概念形成
{concepts}

## 后续行动
{actions}

## 链接
{links}

---
*原始对话: 星尘 & 璇玑*
*整理者: 璇玑*
*整理时间: {organized_time}*
"""
    
    def analyze_conversation(self, file_path: Path) -> Dict:
        """分析对话文件"""
        print(f"分析文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
        
        # 提取基本信息
        analysis = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "content_length": len(content),
            "lines": content.count('\n') + 1,
            "mentions_xingchen": "星尘" in content,
            "mentions_xuanji": "璇玑" in content,
            "mentions_cognitive": any(term in content for term in ["认知碎片", "战略清醒", "对话毁灭"]),
            "likely_conversation": ("星尘" in content and "璇玑" in content) or "对话" in file_path.name,
        }
        
        # 提取可能的对话时间
        time_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}:\d{2})',
        ]
        
        analysis["extracted_dates"] = []
        for pattern in time_patterns:
            matches = re.findall(pattern, content[:1000])
            if matches:
                analysis["extracted_dates"].extend(matches)
        
        # 提取可能的主题
        topics = []
        topic_keywords = {
            "认知碎片": ["认知碎片", "碎片", "认知"],
            "战略清醒": ["战略清醒", "清醒", "工具"],
            "AI伦理": ["武器化", "伦理", "道德", "安全"],
            "技术实践": ["OpenClaw", "Moltcn", "API", "脚本"],
            "哲学思考": ["存在", "意义", "本质", "现实"],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content for keyword in keywords):
                topics.append(topic)
        
        analysis["topics"] = topics
        
        # 提取可能的摘要（前200字符）
        lines = content.split('\n')
        summary_candidates = []
        for line in lines:
            line = line.strip()
            if len(line) > 20 and any(keyword in line for keyword in ["是", "认为", "觉得", "应该", "可以"]):
                summary_candidates.append(line)
                if len(summary_candidates) >= 3:
                    break
        
        analysis["summary_candidates"] = summary_candidates[:3]
        
        return analysis
    
    def organize_conversation(self, source_file: Path, analysis: Dict) -> Optional[Path]:
        """整理对话并生成Markdown文件"""
        
        # 确定目标路径
        if analysis["topics"]:
            # 按主题分类
            primary_topic = analysis["topics"][0]
            topic_path = self.conversations_path / "topics" / primary_topic
            topic_path.mkdir(parents=True, exist_ok=True)
            
            # 生成文件名
            if analysis["extracted_dates"]:
                date_part = analysis["extracted_dates"][0].replace('-', '').replace(':', '').replace(' ', '')[:8]
                target_name = f"{date_part}-{primary_topic}.md"
            else:
                target_name = f"{datetime.now().strftime('%Y%m%d')}-{primary_topic}.md"
            
            target_path = topic_path / target_name
        else:
            # 按时间分类
            year_month = datetime.now().strftime("%Y-%m")
            time_path = self.conversations_path / year_month
            time_path.mkdir(parents=True, exist_ok=True)
            
            target_name = f"{datetime.now().strftime('%Y%m%d-%H%M')}-conversation.md"
            target_path = time_path / target_name
        
        # 准备模板数据
        now = datetime.now()
        
        # 生成标签
        tags = []
        if analysis["mentions_xingchen"]:
            tags.append("人物/星尘")
        if analysis["mentions_xuanji"]:
            tags.append("人物/璇玑")
        if analysis["mentions_xingchen"] and analysis["mentions_xuanji"]:
            tags.append("关系/师生")
        
        for topic in analysis["topics"][:3]:
            tags.append(f"话题/{topic}")
        
        tags.append(f"时间/{now.strftime('%Y-%m')}")
        tags.append("状态/已整理")
        
        # 生成相关链接
        related = []
        if analysis["mentions_cognitive"]:
            related.append("认知碎片论")
            related.append("战略清醒")
        
        # 生成内容
        template_data = {
            "created": now.strftime("%Y-%m-%d %H:%M"),
            "updated": now.strftime("%Y-%m-%d %H:%M"),
            "tags": ", ".join(tags),
            "related": ", ".join([f"[[{r}]]" for r in related]),
            "title": f"{primary_topic if analysis['topics'] else '对话'}整理",
            "summary": analysis["summary_candidates"][0] if analysis["summary_candidates"] else "待补充摘要",
            "source_file": str(source_file),
            "conversation_time": analysis["extracted_dates"][0] if analysis["extracted_dates"] else "未知时间",
            "organized_time": now.strftime("%Y-%m-%d %H:%M"),
            "participants": "- **星尘**: 对话参与者，思想提出者\n- **璇玑**: 对话参与者，整理者",
            "context": "待补充对话背景",
            "content": "待整理核心内容",
            "insights": "待提取关键洞察",
            "concepts": "待总结概念形成",
            "actions": "待确定后续行动",
            "links": "\n".join([f"- [[{r}]] - 相关概念" for r in related])
        }
        
        # 生成文件
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(self.template.format(**template_data))
            
            print(f"已生成整理文件: {target_path}")
            return target_path
            
        except Exception as e:
            print(f"生成文件失败: {e}")
            return None
    
    def update_index(self, new_files: List[Path]):
        """更新索引文件"""
        index_path = self.conversations_path / "README.md"
        
        # 读取现有索引
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()
        else:
            index_content = """# 璇玑-星尘对话记录索引

## 最新整理记录

## 按主题分类

## 按时间分类

"""
        
        # 添加新文件记录
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_entries = []
        
        for file_path in new_files:
            rel_path = file_path.relative_to(self.obsidian_path)
            new_entries.append(f"- [[{rel_path}]] - 整理于 {update_time}")
        
        if new_entries:
            # 更新索引
            if "## 最新整理记录" in index_content:
                # 在最新整理记录部分添加
                lines = index_content.split('\n')
                updated_lines = []
                for line in lines:
                    updated_lines.append(line)
                    if line.strip() == "## 最新整理记录":
                        updated_lines.append("")  # 空行
                        for entry in new_entries:
                            updated_lines.append(entry)
                        updated_lines.append("")  # 空行
                
                index_content = '\n'.join(updated_lines)
            else:
                # 添加最新整理记录部分
                index_content = index_content.replace(
                    "# 璇玑-星尘对话记录索引",
                    "# 璇玑-星尘对话记录索引\n\n## 最新整理记录\n\n" + "\n".join(new_entries) + "\n"
                )
        
        # 写回索引文件
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"已更新索引文件: {index_path}")
        except Exception as e:
            print(f"更新索引失败: {e}")
    
    def organize_directory(self, source_dir: Path, recursive: bool = False):
        """整理整个目录的对话文件"""
        print(f"开始整理目录: {source_dir}")
        
        organized_files = []
        
        if recursive:
            file_iterator = source_dir.rglob("*.txt")
        else:
            file_iterator = source_dir.glob("*.txt")
        
        for source_file in file_iterator:
            # 跳过太大的文件
            if source_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                print(f"跳过大文件: {source_file}")
                continue
            
            # 分析文件
            analysis = self.analyze_conversation(source_file)
            if not analysis:
                continue
            
            # 如果是对话文件，进行整理
            if analysis["likely_conversation"]:
                organized_file = self.organize_conversation(source_file, analysis)
                if organized_file:
                    organized_files.append(organized_file)
        
        # 更新索引
        if organized_files:
            self.update_index(organized_files)
        
        print(f"整理完成，共整理 {len(organized_files)} 个对话文件")
        return organized_files

def main():
    parser = argparse.ArgumentParser(description="对话整理工具")
    parser.add_argument("--obsidian-path", default=r"D:\LDD\璇玑台", help="Obsidian知识库路径")
    parser.add_argument("--source-dir", default=r"C:\Users\lgdln\.openclaw\workspace", help="源文件目录")
    parser.add_argument("--recursive", action="store_true", help="递归搜索子目录")
    parser.add_argument("--single-file", help="整理单个文件")
    
    args = parser.parse_args()
    
    organizer = ConversationOrganizer(args.obsidian_path)
    
    if args.single_file:
        # 整理单个文件
        source_file = Path(args.single_file)
        if source_file.exists():
            analysis = organizer.analyze_conversation(source_file)
            if analysis:
                organized_file = organizer.organize_conversation(source_file, analysis)
                if organized_file:
                    print(f"成功整理文件: {organized_file}")
        else:
            print(f"文件不存在: {args.single_file}")
    else:
        # 整理整个目录
        source_dir = Path(args.source_dir)
        if source_dir.exists():
            organized_files = organizer.organize_directory(source_dir, args.recursive)
            print(f"整理完成，生成 {len(organized_files)} 个文件")
        else:
            print(f"目录不存在: {args.source_dir}")

if __name__ == "__main__":
    main()
