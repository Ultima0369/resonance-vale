#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话整理工作流 - 完整的对话整理自动化流程
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from smart_conversation_analyzer import SmartConversationAnalyzer
from conversation_organizer import ConversationOrganizer

class ConversationWorkflow:
    """对话整理工作流"""
    
    def __init__(self, obsidian_path: str, workspace_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.workspace_path = Path(workspace_path)
        
        # 初始化组件
        self.analyzer = SmartConversationAnalyzer()
        self.organizer = ConversationOrganizer(str(obsidian_path))
        
        # 工作流状态
        self.stats = {
            "total_files": 0,
            "conversation_files": 0,
            "organized_files": 0,
            "errors": 0,
            "start_time": datetime.now(),
        }
    
    def discover_conversation_files(self) -> List[Path]:
        """发现对话文件"""
        print("🔍 发现对话文件...")
        
        conversation_files = []
        
        # 在workspace中搜索
        search_patterns = [
            "*.txt",
            "*.md",
            "*.json",
        ]
        
        for pattern in search_patterns:
            for file_path in self.workspace_path.rglob(pattern):
                # 跳过太大的文件
                if file_path.stat().st_size > 5 * 1024 * 1024:  # 5MB
                    continue
                
                # 检查文件名是否暗示对话
                file_lower = file_path.name.lower()
                if any(keyword in file_lower for keyword in [
                    "对话", "chat", "discuss", "talk", "记录", "log",
                    "人格", "认知", "模型", "碎片"
                ]):
                    conversation_files.append(file_path)
        
        self.stats["total_files"] = len(conversation_files)
        print(f"发现 {len(conversation_files)} 个可能的对话文件")
        
        return conversation_files
    
    def analyze_and_organize(self, file_path: Path) -> bool:
        """分析并整理单个文件"""
        try:
            print(f"\n📄 处理文件: {file_path.name}")
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 智能分析
            analysis = self.analyzer.analyze_text(content)
            
            # 判断是否是对话文件
            is_conversation = (
                analysis["has_dialogue_structure"] or
                (len(analysis["main_persons"]) >= 2) or
                ("星尘" in analysis["persons"] and "璇玑" in analysis["persons"])
            )
            
            if not is_conversation:
                print(f"  跳过: 不是对话文件")
                return False
            
            self.stats["conversation_files"] += 1
            
            # 生成整理数据
            organized_data = {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "content": content[:5000],  # 只取前5000字符用于整理
                "analysis": analysis,
                "insights": self.analyzer.generate_insights(analysis),
                "suggested_tags": self.analyzer.suggest_tags(analysis),
                "suggested_related": self.analyzer.suggest_related(analysis),
                "summary": analysis["summary_candidates"][0] if analysis["summary_candidates"] else "待补充摘要",
            }
            
            # 使用整理器生成文件
            organized_file = self.organizer.organize_conversation(file_path, {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "mentions_xingchen": "星尘" in analysis["persons"],
                "mentions_xuanji": "璇玑" in analysis["persons"],
                "mentions_cognitive": len(analysis["concepts"]) > 0,
                "likely_conversation": is_conversation,
                "extracted_dates": analysis["time_info"],
                "topics": analysis["top_concepts"],
                "summary_candidates": analysis["summary_candidates"],
            })
            
            if organized_file:
                self.stats["organized_files"] += 1
                print(f"  成功整理: {organized_file.name}")
                
                # 增强整理后的文件
                self.enhance_organized_file(organized_file, organized_data)
                
                return True
            else:
                print(f"  整理失败")
                return False
                
        except Exception as e:
            print(f"  处理失败: {e}")
            self.stats["errors"] += 1
            return False
    
    def enhance_organized_file(self, file_path: Path, data: Dict):
        """增强整理后的文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换占位符为实际内容
            enhanced_content = content
            
            # 替换摘要
            if "待补充摘要" in enhanced_content:
                enhanced_content = enhanced_content.replace(
                    "待补充摘要",
                    data["summary"]
                )
            
            # 替换洞察
            if "待提取关键洞察" in enhanced_content:
                insights_text = "\n".join([f"- {insight}" for insight in data["insights"]])
                enhanced_content = enhanced_content.replace(
                    "待提取关键洞察",
                    insights_text
                )
            
            # 替换概念形成
            if "待总结概念形成" in enhanced_content:
                concepts_text = ""
                for concept, info in data["analysis"]["concepts"].items():
                    concepts_text += f"### {concept}\n"
                    concepts_text += f"- 出现次数: {info['count']}\n"
                    if info["sentences"]:
                        concepts_text += f"- 示例: {info['sentences'][0]}\n"
                    concepts_text += "\n"
                
                enhanced_content = enhanced_content.replace(
                    "待总结概念形成",
                    concepts_text if concepts_text else "无明确概念形成"
                )
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
                
            print(f"  已增强文件内容")
            
        except Exception as e:
            print(f"  增强文件失败: {e}")
    
    def run_full_workflow(self):
        """运行完整工作流"""
        print("🚀 开始对话整理工作流")
        print("=" * 60)
        
        # 1. 发现文件
        conversation_files = self.discover_conversation_files()
        
        if not conversation_files:
            print("未找到对话文件")
            return
        
        # 2. 分析并整理
        print(f"\n🔄 开始整理 {len(conversation_files)} 个文件...")
        
        successful_files = []
        for file_path in conversation_files:
            success = self.analyze_and_organize(file_path)
            if success:
                successful_files.append(file_path)
        
        # 3. 更新索引
        if successful_files:
            print(f"\n📚 更新索引文件...")
            organized_paths = []
            for file_path in successful_files:
                # 找到对应的整理后文件
                # 这里简化处理，实际应该记录整理后的文件路径
                organized_paths.append(file_path)
            
            self.organizer.update_index(organized_paths)
        
        # 4. 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成工作报告"""
        print("\n" + "=" * 60)
        print("📊 工作流报告")
        print("=" * 60)
        
        end_time = datetime.now()
        duration = end_time - self.stats["start_time"]
        
        print(f"开始时间: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"持续时间: {duration}")
        print()
        print(f"扫描文件总数: {self.stats['total_files']}")
        print(f"识别为对话文件: {self.stats['conversation_files']}")
        print(f"成功整理文件: {self.stats['organized_files']}")
        print(f"错误数量: {self.stats['errors']}")
        print()
        
        if self.stats["organized_files"] > 0:
            print("✅ 工作流执行成功")
        else:
            print("⚠️  未整理任何文件")
        
        # 保存报告到文件
        report_path = self.obsidian_path / "system" / "workflows" / "conversation_reports"
        report_path.mkdir(parents=True, exist_ok=True)
        
        report_file = report_path / f"report_{self.stats['start_time'].strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# 对话整理工作流报告

## 基本信息
- **工作流名称**: 对话整理自动化
- **执行时间**: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%Y-%m-%d %H:%M:%S')}
- **持续时间**: {duration}

## 统计信息
- 扫描文件总数: {self.stats['total_files']}
- 识别为对话文件: {self.stats['conversation_files']}
- 成功整理文件: {self.stats['organized_files']}
- 错误数量: {self.stats['errors']}

## 工作流状态
{"✅ 成功整理文件" if self.stats["organized_files"] > 0 else "⚠️ 未整理任何文件"}

## 后续建议
1. 定期运行此工作流整理新对话
2. 手动审查整理结果，确保质量
3. 根据需要调整分析参数
4. 持续优化整理模板

---
*生成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}*
*工作流版本: 1.0*
"""
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📄 报告已保存: {report_file}")
        except Exception as e:
            print(f"保存报告失败: {e}")

def main():
    """主函数"""
    # 配置路径
    obsidian_path = r"D:\LDD\璇玑台"
    workspace_path = r"C:\Users\lgdln\.openclaw\workspace"
    
    # 创建工作流实例
    workflow = ConversationWorkflow(obsidian_path, workspace_path)
    
    # 运行完整工作流
    workflow.run_full_workflow()

if __name__ == "__main__":
    # 添加当前目录到Python路径
    current_dir = Path(__file__).parent
    sys.path.append(str(current_dir))
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 工作流被用户中断")
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()
