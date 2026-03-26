#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 分析 Obsidian 仓库结构

import os
import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter

class ObsidianVaultAnalyzer:
    """Obsidian 仓库分析器"""
    
    def __init__(self, vault_path="D:\\LDD\\璇玑台"):
        self.vault_path = Path(vault_path)
        self.analysis = {
            "total_files": 0,
            "folders": defaultdict(list),
            "file_types": Counter(),
            "file_sizes": defaultdict(list),
            "creation_dates": defaultdict(int),
            "tags": Counter(),
            "links": Counter(),
            "empty_files": [],
            "large_files": [],
            "recent_files": [],
            "old_files": []
        }
        
    def analyze_vault(self):
        """分析整个仓库"""
        print(f"开始分析 Obsidian 仓库: {self.vault_path}")
        print("=" * 60)
        
        # 遍历所有文件
        for file_path in self.vault_path.rglob("*.md"):
            if file_path.is_file():
                self._analyze_file(file_path)
        
        # 生成统计报告
        self._generate_report()
        
        # 生成整理建议
        self._generate_organization_suggestions()
        
        return self.analysis
    
    def _analyze_file(self, file_path: Path):
        """分析单个文件"""
        relative_path = file_path.relative_to(self.vault_path)
        folder = str(relative_path.parent)
        
        # 基础信息
        self.analysis["total_files"] += 1
        self.analysis["folders"][folder].append(str(relative_path))
        
        # 文件大小
        file_size = file_path.stat().st_size
        self.analysis["file_sizes"][folder].append(file_size)
        
        if file_size == 0:
            self.analysis["empty_files"].append(str(relative_path))
        elif file_size > 100000:  # 大于100KB
            self.analysis["large_files"].append((str(relative_path), file_size))
        
        # 修改时间
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m")
        self.analysis["creation_dates"][date_str] += 1
        
        # 判断新旧文件
        days_ago = (datetime.now() - mtime).days
        if days_ago <= 7:
            self.analysis["recent_files"].append(str(relative_path))
        elif days_ago > 180:  # 超过6个月
            self.analysis["old_files"].append(str(relative_path))
        
        # 读取文件内容分析
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 分析标签
                tags = re.findall(r'#([\w\u4e00-\u9fff\-]+)', content)
                for tag in tags:
                    self.analysis["tags"][tag] += 1
                
                # 分析内部链接
                links = re.findall(r'\[\[([^\]]+)\]\]', content)
                for link in links:
                    self.analysis["links"][link] += 1
                    
        except Exception as e:
            print(f"[警告] 无法读取文件 {relative_path}: {e}")
    
    def _generate_report(self):
        """生成分析报告"""
        print("\n[统计] 仓库分析报告")
        print("=" * 60)
        
        print(f"[结构] 总文件数: {self.analysis['total_files']}")
        print(f"[文件夹] 文件夹数: {len(self.analysis['folders'])}")
        
        # 文件夹统计
        print("\n[文件夹] 文件夹分布:")
        for folder, files in sorted(self.analysis["folders"].items(), 
                                   key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"  {folder}: {len(files)} 个文件")
        
        # 文件大小统计
        print("\n[大小] 文件大小分布:")
        size_ranges = {
            "0-1KB": 0,
            "1-10KB": 0,
            "10-100KB": 0,
            "100KB-1MB": 0,
            ">1MB": 0
        }
        
        for folder, sizes in self.analysis["file_sizes"].items():
            for size in sizes:
                if size == 0:
                    size_ranges["0-1KB"] += 1
                elif size < 1024:
                    size_ranges["0-1KB"] += 1
                elif size < 10240:
                    size_ranges["1-10KB"] += 1
                elif size < 102400:
                    size_ranges["10-100KB"] += 1
                elif size < 1048576:
                    size_ranges["100KB-1MB"] += 1
                else:
                    size_ranges[">1MB"] += 1
        
        for range_name, count in size_ranges.items():
            if count > 0:
                percentage = (count / self.analysis["total_files"]) * 100
                print(f"  {range_name}: {count} 个文件 ({percentage:.1f}%)")
        
        # 时间分布
        print("\n[时间] 创建时间分布:")
        for month, count in sorted(self.analysis["creation_dates"].items(), reverse=True)[:12]:
            print(f"  {month}: {count} 个文件")
        
        # 标签统计
        print("\n[标签] 热门标签 (前20):")
        for tag, count in self.analysis["tags"].most_common(20):
            print(f"  #{tag}: {count}")
        
        # 链接统计
        print("\n[链接] 热门链接 (前10):")
        for link, count in self.analysis["links"].most_common(10):
            print(f"  [[{link}]]: {count}")
        
        # 问题文件
        print(f"\n[警告] 空文件: {len(self.analysis['empty_files'])} 个")
        if self.analysis['empty_files']:
            for file in self.analysis['empty_files'][:5]:
                print(f"  - {file}")
        
        print(f"\n[大文件] 大文件 (>100KB): {len(self.analysis['large_files'])} 个")
        for file, size in sorted(self.analysis['large_files'], key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {file} ({size/1024:.1f}KB)")
        
        print(f"\n[新文件] 最近7天修改的文件: {len(self.analysis['recent_files'])} 个")
        print(f"[时间] 超过6个月未修改的文件: {len(self.analysis['old_files'])} 个")
    
    def _generate_organization_suggestions(self):
        """生成整理建议"""
        print("\n[建议] 整理建议")
        print("=" * 60)
        
        # 1. 文件夹结构建议
        print("\n1. [结构] 建议的文件夹结构:")
        suggested_structure = {
            "00-索引": ["主页索引", "标签索引", "时间线索引", "图谱索引"],
            "01-日记": ["每日记录", "周记", "月总结"],
            "02-项目": ["进行中", "已完成", "归档"],
            "03-知识": ["概念", "理论", "方法", "工具"],
            "04-对话": ["璇玑对话", "外部对话", "会议记录"],
            "05-创作": ["文章", "诗歌", "故事", "研究"],
            "06-资源": ["书籍", "文章", "视频", "课程"],
            "07-人物": ["联系人", "专家", "作者"],
            "08-模板": ["笔记模板", "项目模板", "会议模板"],
            "99-归档": ["旧文件", "临时文件", "备份"]
        }
        
        for folder, subfolders in suggested_structure.items():
            print(f"  [文件夹] {folder}/")
            for subfolder in subfolders:
                print(f"    └── {subfolder}/")
        
        # 2. 文件整理建议
        print("\n2. [整理] 文件整理建议:")
        
        # 根据文件名模式分类
        file_patterns = defaultdict(list)
        for folder, files in self.analysis["folders"].items():
            for file in files:
                filename = Path(file).name
                
                # 检测文件名模式
                if re.match(r'\d{4}-\d{2}-\d{2}', filename):
                    file_patterns["日期文件"].append(file)
                elif "对话" in filename or "聊天" in filename:
                    file_patterns["对话文件"].append(file)
                elif "笔记" in filename or "记录" in filename:
                    file_patterns["笔记文件"].append(file)
                elif "项目" in filename or "任务" in filename:
                    file_patterns["项目文件"].append(file)
                elif "概念" in filename or "定义" in filename:
                    file_patterns["概念文件"].append(file)
                else:
                    file_patterns["其他文件"].append(file)
        
        print(f"  发现 {len(file_patterns['日期文件'])} 个日期格式文件")
        print(f"  发现 {len(file_patterns['对话文件'])} 个对话相关文件")
        print(f"  发现 {len(file_patterns['笔记文件'])} 个笔记文件")
        print(f"  发现 {len(file_patterns['项目文件'])} 个项目文件")
        print(f"  发现 {len(file_patterns['概念文件'])} 个概念文件")
        
        # 3. 标签整理建议
        print("\n3. [标签] 标签整理建议:")
        
        # 建议的标签体系
        tag_categories = {
            "状态": ["进行中", "已完成", "待处理", "归档"],
            "类型": ["概念", "方法", "工具", "案例", "思考"],
            "领域": ["哲学", "科学", "技术", "艺术", "生活"],
            "项目": ["璇玑台", "认知切片", "AI助手", "个人成长"],
            "人物": ["星尘", "璇玑", "家人", "朋友", "专家"],
            "时间": ["2026", "2025", "月度", "周度", "每日"]
        }
        
        print("  建议的标签分类体系:")
        for category, tags in tag_categories.items():
            print(f"    #{category}: {', '.join([f'#{tag}' for tag in tags])}")
        
        # 4. 自动化整理建议
        print("\n4. [自动化] 自动化整理建议:")
        print("   a. 创建自动分类脚本")
        print("   b. 设置定期整理任务")
        print("   c. 创建模板系统")
        print("   d. 建立索引页面")
        print("   e. 清理空文件和重复文件")
        
        # 5. 具体行动计划
        print("\n5. [行动] 具体行动计划:")
        print("   第1步: 备份当前仓库")
        print("   第2步: 创建新的文件夹结构")
        print("   第3步: 编写文件分类脚本")
        print("   第4步: 批量移动文件到新结构")
        print("   第5步: 更新所有内部链接")
        print("   第6步: 创建索引页面")
        print("   第7步: 测试和验证")
        
    def save_analysis_report(self, output_path="obsidian_analysis_report.md"):
        """保存分析报告"""
        report_path = Path(output_path)
        
        report_content = f"""# Obsidian 仓库分析报告

**分析时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**仓库路径**: {self.vault_path}
**总文件数**: {self.analysis['total_files']}

## [统计] 统计摘要

### 文件分布
- 总文件数: {self.analysis['total_files']}
- 文件夹数: {len(self.analysis['folders'])}
- 空文件数: {len(self.analysis['empty_files'])}
- 大文件数: {len(self.analysis['large_files'])}
- 最近文件: {len(self.analysis['recent_files'])}
- 旧文件: {len(self.analysis['old_files'])}

### 热门标签
{self._format_tags_for_report()}

### 热门链接
{self._format_links_for_report()}

## [结构] 详细文件列表

### 空文件
{self._format_file_list(self.analysis['empty_files'])}

### 大文件 (>100KB)
{self._format_large_files_for_report()}

### 最近修改的文件
{self._format_file_list(self.analysis['recent_files'][:20])}

## [建议] 整理建议

### 建议的文件夹结构
```
00-索引/
├── 主页索引.md
├── 标签索引.md
├── 时间线索引.md
└── 图谱索引.md

01-日记/
├── 每日记录/
├── 周记/
└── 月总结/

02-项目/
├── 进行中/
├── 已完成/
└── 归档/

03-知识/
├── 概念/
├── 理论/
├── 方法/
└── 工具/

04-对话/
├── 璇玑对话/
├── 外部对话/
└── 会议记录/

05-创作/
├── 文章/
├── 诗歌/
├── 故事/
└── 研究/

06-资源/
├── 书籍/
├── 文章/
├── 视频/
└── 课程/

07-人物/
├── 联系人/
├── 专家/
└── 作者/

08-模板/
├── 笔记模板/
├── 项目模板/
└── 会议模板/

99-归档/
├── 旧文件/
├── 临时文件/
└── 备份/
```

### 行动计划
1. **备份**: 复制整个仓库到安全位置
2. **创建结构**: 按照建议创建文件夹
3. **分类文件**: 根据文件名和内容分类
4. **移动文件**: 批量移动到新位置
5. **更新链接**: 修复所有内部链接
6. **创建索引**: 生成导航页面
7. **测试验证**: 确保一切正常工作

---

*本报告由璇玑自动生成，用于优化 Obsidian 仓库结构*"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n[报告] 分析报告已保存: {report_path}")
        return report_path
    
    def _format_tags_for_report(self):
        """格式化标签用于报告"""
        if not self.analysis['tags']:
            return "暂无标签数据"
        
        lines = []
        for tag, count in self.analysis['tags'].most_common(30):
            lines.append(f"- #{tag}: {count} 次")
        
        return "\n".join(lines)
    
    def _format_links_for_report(self):
        """格式化链接用于报告"""
        if not self.analysis['links']:
            return "暂无链接数据"
        
        lines = []
        for link, count in self.analysis['links'].most_common(20):
            lines.append(f"- [[{link}]]: {count} 次")
        
        return "\n".join(lines)
    
    def _format_file_list(self, files):
        """格式化文件列表"""
        if not files:
            return "无"
        
        lines = []
        for file in files[:50]:  # 最多显示50个
            lines.append(f"- {file}")
        
        if len(files) > 50:
            lines.append(f"... 还有 {len(files) - 50} 个文件")
        
        return "\n".join(lines)
    
    def _format_large_files_for_report(self):
        """格式化大文件列表"""
        if not self.analysis['large_files']:
            return "无"
        
        lines = []
        for file, size in sorted(self.analysis['large_files'], key=lambda x: x[1], reverse=True)[:20]:
            size_kb = size / 1024
            size_mb = size_kb / 1024 if size_kb > 1024 else None
            
            if size_mb:
                lines.append(f"- {file} ({size_mb:.1f}MB)")
            else:
                lines.append(f"- {file} ({size_kb:.1f}KB)")
        
        return "\n".join(lines)

def main():
    """主函数"""
    print("璇玑 - Obsidian 仓库分析工具")
    print("=" * 60)
    
    try:
        # 初始化分析器
        analyzer = ObsidianVaultAnalyzer()
        
        # 分析仓库
        analysis = analyzer.analyze_vault()
        
        # 保存报告
        report_file = analyzer.save_analysis_report()
        
        print("\n" + "=" * 60)
        print("分析完成！")
        print(f"详细报告: {report_file}")
        print("\n下一步:")
        print("  1. 查看分析报告了解当前状况")
        print("  2. 根据建议创建新的文件夹结构")
        print("  3. 运行整理脚本重新组织文件")
        print("  4. 创建索引页面方便导航")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()