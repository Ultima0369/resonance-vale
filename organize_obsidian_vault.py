#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Obsidian 仓库整理脚本

import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ObsidianVaultOrganizer:
    """Obsidian 仓库整理器"""
    
    def __init__(self, vault_path="D:\\LDD\\璇玑台"):
        self.vault_path = Path(vault_path)
        self.backup_path = self.vault_path.parent / f"{self.vault_path.name}_备份_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 分类规则
        self.classification_rules = {
            # 索引文件
            "索引": [
                r"主页", r"索引", r"导航", r"目录", r"图谱",
                r"时间线", r"标签", r"分类", r"地图"
            ],
            
            # 日记文件
            "日记": [
                r"\d{4}-\d{2}-\d{2}",  # 日期格式
                r"日记", r"日志", r"日更", r"周记", r"月报",
                r"总结", r"回顾", r"计划", r"日程"
            ],
            
            # 项目文件
            "项目": [
                r"项目", r"任务", r"TODO", r"待办", r"计划",
                r"进度", r"里程碑", r"目标", r"规划"
            ],
            
            # 知识文件
            "知识": [
                r"概念", r"定义", r"术语", r"理论", r"原理",
                r"方法", r"技巧", r"策略", r"框架", r"模型",
                r"工具", r"技术", r"算法", r"系统"
            ],
            
            # 对话文件
            "对话": [
                r"对话", r"聊天", r"讨论", r"交流", r"访谈",
                r"会议", r"对谈", r"问答", r"咨询", r"璇玑",
                r"星尘", r"AI", r"助手"
            ],
            
            # 创作文件
            "创作": [
                r"文章", r"论文", r"报告", r"笔记", r"随笔",
                r"诗歌", r"小说", r"故事", r"剧本", r"研究",
                r"分析", r"评论", r"读后感", r"观后感"
            ],
            
            # 资源文件
            "资源": [
                r"书籍", r"文章", r"论文", r"视频", r"课程",
                r"教程", r"指南", r"手册", r"文档", r"资料",
                r"参考", r"素材", r"模板", r"示例"
            ],
            
            # 人物文件
            "人物": [
                r"人物", r"作者", r"专家", r"学者", r"联系人",
                r"朋友", r"同事", r"合作伙伴", r"导师"
            ],
            
            # 模板文件
            "模板": [
                r"模板", r"格式", r"样式", r"范例", r"示例",
                r"空白", r"标准", r"规范"
            ]
        }
        
        # 建议的文件夹结构
        self.suggested_structure = {
            "00-索引": {
                "description": "导航和索引文件",
                "subfolders": ["主页索引", "标签索引", "时间线索引", "图谱索引"]
            },
            "01-日记": {
                "description": "个人日记和时间记录",
                "subfolders": ["每日记录", "周记", "月总结", "年度回顾"]
            },
            "02-项目": {
                "description": "项目和任务管理",
                "subfolders": ["进行中", "已完成", "归档", "计划中"]
            },
            "03-知识": {
                "description": "知识库和概念定义",
                "subfolders": ["概念", "理论", "方法", "工具", "案例"]
            },
            "04-对话": {
                "description": "对话记录和交流",
                "subfolders": ["璇玑对话", "外部对话", "会议记录", "思考对话"]
            },
            "05-创作": {
                "description": "创作内容和作品",
                "subfolders": ["文章", "诗歌", "故事", "研究", "分析"]
            },
            "06-资源": {
                "description": "参考资料和素材",
                "subfolders": ["书籍", "文章", "视频", "课程", "工具"]
            },
            "07-人物": {
                "description": "人物档案和联系",
                "subfolders": ["联系人", "专家", "作者", "合作伙伴"]
            },
            "08-模板": {
                "description": "模板和格式文件",
                "subfolders": ["笔记模板", "项目模板", "会议模板", "日记模板"]
            },
            "99-归档": {
                "description": "归档和旧文件",
                "subfolders": ["旧文件", "临时文件", "备份", "废弃文件"]
            }
        }
        
        # 统计信息
        self.stats = {
            "total_files": 0,
            "moved_files": 0,
            "skipped_files": 0,
            "failed_files": 0,
            "updated_links": 0,
            "created_folders": 0,
            "classification": {}
        }
    
    def backup_vault(self):
        """备份整个仓库"""
        print(f"创建备份: {self.backup_path}")
        
        if self.backup_path.exists():
            print(f"警告: 备份目录已存在，跳过备份")
            return False
        
        try:
            # 复制整个仓库
            shutil.copytree(self.vault_path, self.backup_path)
            print(f"备份完成: {self.backup_path}")
            return True
        except Exception as e:
            print(f"备份失败: {e}")
            return False
    
    def create_folder_structure(self):
        """创建新的文件夹结构"""
        print("\n创建文件夹结构...")
        
        for folder_name, folder_info in self.suggested_structure.items():
            folder_path = self.vault_path / folder_name
            
            # 创建主文件夹
            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)
                self.stats["created_folders"] += 1
                print(f"  创建: {folder_name}")
            
            # 创建子文件夹
            for subfolder in folder_info["subfolders"]:
                subfolder_path = folder_path / subfolder
                if not subfolder_path.exists():
                    subfolder_path.mkdir(exist_ok=True)
                    self.stats["created_folders"] += 1
                    print(f"    └── 创建: {subfolder}")
        
        print(f"创建了 {self.stats['created_folders']} 个文件夹")
    
    def classify_file(self, filename: str, content: str = "") -> Tuple[str, str]:
        """分类文件"""
        
        # 检查文件名匹配
        for category, patterns in self.classification_rules.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    return category, "文件名匹配"
        
        # 检查内容匹配（如果提供了内容）
        if content:
            content_lower = content.lower()
            for category, patterns in self.classification_rules.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower, re.IGNORECASE):
                        return category, "内容匹配"
        
        # 默认分类
        return "归档", "未分类"
    
    def get_destination_path(self, category: str, filename: str) -> Path:
        """获取目标路径"""
        
        # 映射分类到文件夹
        category_mapping = {
            "索引": "00-索引",
            "日记": "01-日记",
            "项目": "02-项目", 
            "知识": "03-知识",
            "对话": "04-对话",
            "创作": "05-创作",
            "资源": "06-资源",
            "人物": "07-人物",
            "模板": "08-模板",
            "归档": "99-归档"
        }
        
        # 获取主文件夹
        main_folder = category_mapping.get(category, "99-归档")
        main_path = self.vault_path / main_folder
        
        # 根据文件名进一步分类到子文件夹
        filename_lower = filename.lower()
        
        # 日记文件按日期分类
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
        if date_match and category == "日记":
            year = date_match.group(1)
            month = date_match.group(2)
            return main_path / "每日记录" / f"{year}-{month}" / filename
        
        # 对话文件分类
        if category == "对话":
            if "璇玑" in filename or "AI" in filename or "助手" in filename:
                return main_path / "璇玑对话" / filename
            elif "会议" in filename:
                return main_path / "会议记录" / filename
            else:
                return main_path / "外部对话" / filename
        
        # 知识文件分类
        if category == "知识":
            if "概念" in filename or "定义" in filename:
                return main_path / "概念" / filename
            elif "理论" in filename or "原理" in filename:
                return main_path / "理论" / filename
            elif "方法" in filename or "技巧" in filename:
                return main_path / "方法" / filename
            elif "工具" in filename or "技术" in filename:
                return main_path / "工具" / filename
            else:
                return main_path / "案例" / filename
        
        # 默认返回主文件夹
        return main_path / filename
    
    def update_links_in_file(self, file_path: Path, moved_files: Dict[str, str]):
        """更新文件中的内部链接"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated = False
            
            # 查找所有内部链接
            link_pattern = r'\[\[([^\]]+)\]\]'
            links = re.findall(link_pattern, content)
            
            for link in links:
                # 清理链接（移除可能的锚点）
                clean_link = link.split('|')[0].split('#')[0].strip()
                
                # 检查这个链接是否被移动了
                if clean_link in moved_files:
                    new_path = moved_files[clean_link]
                    old_link = f"[[{link}]]"
                    new_link = f"[[{new_path}]]"
                    
                    # 替换链接
                    content = content.replace(old_link, new_link)
                    updated = True
                    self.stats["updated_links"] += 1
            
            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
        except Exception as e:
            print(f"更新链接失败 {file_path}: {e}")
        
        return False
    
    def organize_files(self, dry_run: bool = True):
        """整理文件"""
        
        print(f"\n开始整理文件 (dry_run={dry_run})...")
        
        # 收集所有 Markdown 文件
        all_files = list(self.vault_path.rglob("*.md"))
        self.stats["total_files"] = len(all_files)
        
        # 记录移动的文件（用于更新链接）
        moved_files = {}  # 旧路径 -> 新路径
        
        # 跳过新创建的文件夹
        skip_folders = [folder for folder in self.suggested_structure.keys()]
        
        for file_path in all_files:
            # 跳过新文件夹中的文件
            if any(str(file_path).startswith(str(self.vault_path / folder)) for folder in skip_folders):
                continue
            
            relative_path = file_path.relative_to(self.vault_path)
            filename = file_path.name
            
            # 读取文件内容（用于分类）
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)  # 只读取前5000字符用于分类
            except:
                content = ""
            
            # 分类文件
            category, reason = self.classify_file(filename, content)
            
            # 统计分类
            if category not in self.stats["classification"]:
                self.stats["classification"][category] = 0
            self.stats["classification"][category] += 1
            
            # 获取目标路径
            dest_path = self.get_destination_path(category, filename)
            
            # 确保目标目录存在
            dest_path.parent.mkdir(exist_ok=True, parents=True)
            
            # 记录移动
            moved_files[str(relative_path)] = str(dest_path.relative_to(self.vault_path))
            
            if dry_run:
                print(f"  {relative_path}")
                print(f"    -> {dest_path.relative_to(self.vault_path)} ({category} - {reason})")
            else:
                try:
                    # 移动文件
                    shutil.move(str(file_path), str(dest_path))
                    self.stats["moved_files"] += 1
                    print(f"  移动: {relative_path} -> {dest_path.relative_to(self.vault_path)}")
                except Exception as e:
                    print(f"  移动失败: {relative_path} - {e}")
                    self.stats["failed_files"] += 1
        
        # 更新所有文件中的链接
        if not dry_run and moved_files:
            print(f"\n更新内部链接...")
            for file_path in self.vault_path.rglob("*.md"):
                self.update_links_in_file(file_path, moved_files)
        
        return moved_files
    
    def create_index_pages(self):
        """创建索引页面"""
        print("\n创建索引页面...")
        
        # 1. 主页索引
        homepage_content = """# 璇玑台 - 主页

欢迎来到璇玑台，这是星尘的知识管理和创作空间。

## 快速导航

### 核心区域
- [[00-索引/标签索引|标签索引]] - 按标签浏览所有内容
- [[00-索引/时间线索引|时间线索引]] - 按时间顺序查看
- [[00-索引/图谱索引|知识图谱]] - 可视化概念关系

### 主要内容
- [[01-日记/每日记录|每日记录]] - 日常思考和记录
- [[03-知识/概念|概念库]] - 核心概念和定义
- [[04-对话/璇玑对话|璇玑对话]] - 与AI助手的深度对话
- [[05-创作/文章|创作文章]] - 原创内容和研究

### 实用工具
- [[08-模板/笔记模板|笔记模板]] - 各种笔记模板
- [[06-资源/工具|工具资源]] - 实用工具和资源

## 统计信息

**最后更新**: {{date:YYYY-MM-DD HH:mm}}

- **总笔记数**: {{allNotesCount}}
- **最近7天**: {{recentNotesCount}}
- **热门标签**: {{topTags}}

## 搜索提示

1. 使用 `#标签` 进行标签搜索
2. 使用 `[[链接]]` 查看相关笔记
3. 使用 `path:文件夹` 限制搜索范围

## 快速开始

### 新笔记
- [[08-模板/笔记模板/快速笔记|快速笔记模板]]
- [[08-模板/笔记模板/读书笔记|读书笔记模板]]
- [[08-模板/笔记模板/会议记录|会议记录模板]]

### 常用操作
- [[00-索引/标签索引|浏览所有标签]]
- [[03-知识/概念|查看概念库]]
- [[04-对话/璇玑对话|查看最新对话]]

---

*本页面由璇玑自动生成和维护*"""
        
        homepage_path = self.vault_path / "00-索引" / "主页索引.md"
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(homepage_content)
        print(f"  创建: 主页索引.md")
        
        # 2. 标签索引
        tags_index_content = """# 标签索引

## 标签分类

### 状态标签
- #进行中 - 正在进行的项目或任务
- #已完成 - 已完成的工作
- #待处理 - 需要处理的事项
- #归档 - 已归档的内容

### 内容类型
- #概念 - 核心概念和定义
- #方法 - 方法和技巧
- #工具 - 工具和技术
- #案例 - 实际案例和分析
- #思考 - 个人思考和反思

### 领域标签
- #哲学 - 哲学相关讨论
- #科学 - 科学和技术
- #艺术 - 艺术和创作
- #生活 - 日常生活和感悟
- #技术 - 技术和工具

### 项目标签
- #璇玑台 - 璇玑台项目相关
- #认知切片 - 认知切片论项目
- #AI助手 - AI助手相关
- #个人成长 - 个人成长和发展

### 时间标签
- #2026 - 2026年的内容
- #2025 - 2025年的内容
- #月度 - 月度总结
- #周度 - 周度记录
- #每日 - 每日记录

## 热门标签

{{tags}}

## 标签使用统计

{{tagCounts}}

## 标签管理建议

1. **保持简洁**: 每个笔记使用3-5个核心标签
2. **层级结构**: 使用父子标签如 `#项目/璇玑台`
3. **一致性**: 相同概念使用相同标签
4. **定期清理**: 定期合并相似标签

## 快速链接

- [[00-索引/主页索引|返回主页]]
- [[00-索引/时间线索引|时间线索引]]
- [[00-索引/图谱索引|知识图谱]]

---

*本