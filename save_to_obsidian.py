#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 将对话关键词保存到Obsidian笔记

import os
import json
import re
from datetime import datetime
from pathlib import Path

class ObsidianNoteSaver:
    """Obsidian笔记保存器"""
    
    def __init__(self, vault_path="D:\\LDD\\璇玑台"):
        self.vault_path = Path(vault_path)
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # 确保库目录存在
        if not self.vault_path.exists():
            print(f"❌ Obsidian库不存在: {self.vault_path}")
            raise FileNotFoundError(f"Obsidian库不存在: {self.vault_path}")
        
        print(f"✅ Obsidian库: {self.vault_path}")
    
    def extract_keywords_from_conversation(self, conversation_text):
        """从对话文本中提取关键词"""
        
        # 核心概念关键词
        core_concepts = [
            "认知切片论", "认知切片", "切片自觉",
            "战壕禅", "动态调谐", "清明工具箱",
            "玛尼堆", "甲骨文", "在地经验",
            "具身经验", "元认知", "认知跃迁"
        ]
        
        # 技术概念关键词
        tech_concepts = [
            "API配置", "DeepSeek", "系统提示词",
            "温度设置", "三阶段工作流", "滑动窗口",
            "自动检测", "对话统计", "比喻挖掘"
        ]
        
        # 对话特征关键词
        dialogue_features = [
            "深度追问", "东西融合", "实践导向",
            "谦逊探索", "鲜活对话", "共创内容"
        ]
        
        # 查找关键词
        found_keywords = {
            "核心概念": [],
            "技术概念": [],
            "对话特征": [],
            "具象比喻": []
        }
        
        # 检查核心概念
        for concept in core_concepts:
            if concept in conversation_text:
                found_keywords["核心概念"].append(concept)
        
        # 检查技术概念
        for concept in tech_concepts:
            if concept in conversation_text:
                found_keywords["技术概念"].append(concept)
        
        # 检查对话特征
        for feature in dialogue_features:
            if feature in conversation_text:
                found_keywords["对话特征"].append(feature)
        
        # 提取具象比喻（使用正则表达式）
        metaphor_patterns = [
            r'像.*一样', r'如同.*', r'好比.*',
            r'是.*的.*', r'把.*比作.*', r'犹如.*',
            r'仿佛.*', r'宛若.*'
        ]
        
        metaphors = []
        for pattern in metaphor_patterns:
            matches = re.findall(pattern, conversation_text)
            metaphors.extend(matches)
        
        found_keywords["具象比喻"] = list(set(metaphors))[:5]  # 最多5个
        
        return found_keywords
    
    def create_obsidian_note(self, title, content, tags=None, folder="对话记录"):
        """创建Obsidian笔记"""
        
        # 创建文件夹（如果不存在）
        folder_path = self.vault_path / folder
        folder_path.mkdir(exist_ok=True)
        
        # 生成文件名（避免特殊字符）
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = f"{self.today} - {safe_title}.md"
        filepath = folder_path / filename
        
        # 构建笔记内容
        note_content = f"""# {title}

**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**记录者**: 璇玑

## 📝 对话摘要

{content}

## 🏷️ 标签

"""
        
        # 添加标签
        if tags:
            tag_lines = []
            for tag in tags:
                if tag:  # 确保标签不为空
                    tag_lines.append(f"#{tag}")
            
            if tag_lines:
                note_content += " ".join(tag_lines) + "\n\n"
        
        note_content += "---\n\n"
        note_content += "*本笔记由璇玑自动生成，记录与星尘的深度对话内容*"
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(note_content)
        
        print(f"✅ 笔记已保存: {filepath}")
        return filepath
    
    def create_keyword_index(self, keywords, conversation_title):
        """创建关键词索引笔记"""
        
        # 生成索引内容
        index_content = f"""# 对话关键词索引 - {conversation_title}

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**相关对话**: [[{self.today} - {conversation_title}]]

## 🔑 关键词分类

### 核心概念
"""
        
        # 核心概念
        if keywords["核心概念"]:
            for concept in keywords["核心概念"]:
                index_content += f"- [[{concept}]]\n"
        else:
            index_content += "- 暂无\n"
        
        index_content += "\n### 技术概念\n"
        
        # 技术概念
        if keywords["技术概念"]:
            for concept in keywords["技术概念"]:
                index_content += f"- [[{concept}]]\n"
        else:
            index_content += "- 暂无\n"
        
        index_content += "\n### 对话特征\n"
        
        # 对话特征
        if keywords["对话特征"]:
            for feature in keywords["对话特征"]:
                index_content += f"- [[{feature}]]\n"
        else:
            index_content += "- 暂无\n"
        
        index_content += "\n### 具象比喻\n"
        
        # 具象比喻
        if keywords["具象比喻"]:
            for i, metaphor in enumerate(keywords["具象比喻"], 1):
                # 清理比喻文本
                clean_metaphor = metaphor[:50] + "..." if len(metaphor) > 50 else metaphor
                index_content += f"{i}. {clean_metaphor}\n"
        else:
            index_content += "- 暂无\n"
        
        index_content += f"""

## 📊 统计信息

- 核心概念数: {len(keywords['核心概念'])}
- 技术概念数: {len(keywords['技术概念'])}
- 对话特征数: {len(keywords['对话特征'])}
- 具象比喻数: {len(keywords['具象比喻'])}

## 🔗 相关链接

- [[对话索引]]
- [[认知切片论]]
- [[API配置]]

---

*本索引由璇玑自动生成，用于快速检索对话中的关键概念*"""
        
        # 保存索引笔记
        index_title = f"关键词索引 - {conversation_title}"
        index_file = self.create_obsidian_note(
            title=index_title,
            content=index_content,
            tags=["关键词索引", "对话分析", "概念提取"],
            folder="关键词索引"
        )
        
        return index_file
    
    def update_concept_files(self, keywords):
        """更新概念文件（如果存在）"""
        
        concept_folder = self.vault_path / "概念"
        concept_folder.mkdir(exist_ok=True)
        
        updated_files = []
        
        # 更新核心概念文件
        for concept in keywords["核心概念"]:
            concept_file = concept_folder / f"{concept}.md"
            
            if concept_file.exists():
                # 读取现有内容
                with open(concept_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否已有今天的引用
                today_ref = f"[[{self.today} - 认知切片论API配置]]"
                if today_ref not in content:
                    # 添加新引用
                    new_content = content.rstrip() + f"\n\n## 相关对话\n- {today_ref}\n"
                    with open(concept_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files.append(concept)
                    print(f"📝 更新概念文件: {concept}")
            else:
                # 创建新概念文件
                concept_content = f"""# {concept}

## 定义


## 相关对话
- [[{self.today} - 认知切片论API配置]]

## 参考资料


---

*概念文件 - 由璇玑维护*"""
                
                with open(concept_file, 'w', encoding='utf-8') as f:
                    f.write(concept_content)
                updated_files.append(concept)
                print(f"📄 创建概念文件: {concept}")
        
        return updated_files

def main():
    """主函数"""
    
    print("🦞 Obsidian笔记保存工具")
    print("=" * 50)
    
    try:
        # 1. 初始化Obsidian保存器
        saver = ObsidianNoteSaver()
        
        # 2. 读取今天的对话内容
        conversation_file = "C:\\Users\\lgdln\\.openclaw\\workspace\\memory\\2026-03-23.md"
        
        if not os.path.exists(conversation_file):
            print(f"❌ 对话文件不存在: {conversation_file}")
            # 使用示例对话内容
            conversation_text = """认知切片论API配置对话
            我们讨论了认知切片论的深度共创API配置方案。
            核心概念包括：认知切片、战壕禅风格、切片自觉、动态调谐、清明工具箱。
            技术概念包括：API配置、三阶段工作流、自动检测、对话统计。
            具象比喻包括：像玛尼堆一样积累智慧、如同甲骨文刻录生存经验。"""
        else:
            with open(conversation_file, 'r', encoding='utf-8') as f:
                conversation_text = f.read()
        
        print(f"📖 读取对话内容 ({len(conversation_text)} 字符)")
        
        # 3. 提取关键词
        keywords = saver.extract_keywords_from_conversation(conversation_text)
        
        print("\n🔍 提取的关键词:")
        for category, words in keywords.items():
            if words:
                print(f"  {category}: {', '.join(words[:3])}{'...' if len(words) > 3 else ''}")
        
        # 4. 创建对话笔记
        conversation_title = "认知切片论API配置"
        conversation_summary = """今天与星尘讨论了认知切片论的深度共创API配置方案。

## 主要内容
1. 分析了《认知切片论2.md》文件的特点
2. 设计了专门的API配置方案（三阶段工作流）
3. 创建了完整的工具链（Python脚本 + 配置文档）
4. 强调了"战壕禅风格"和"切片自觉"

## 核心价值
- 为深度哲学/认知科学内容创作提供可操作的技术方案
- 体现了理论深度与大地温度的平衡
- 创建了支持长期深度对话的工具生态系统"""
        
        note_file = saver.create_obsidian_note(
            title=conversation_title,
            content=conversation_summary,
            tags=["认知切片论", "API配置", "深度对话", "技术实现"],
            folder="对话记录"
        )
        
        print(f"\n📓 对话笔记: {note_file.name}")
        
        # 5. 创建关键词索引
        index_file = saver.create_keyword_index(keywords, conversation_title)
        print(f"📑 关键词索引: {index_file.name}")
        
        # 6. 更新概念文件
        updated_concepts = saver.update_concept_files(keywords)
        if updated_concepts:
            print(f"📚 更新概念文件: {', '.join(updated_concepts)}")
        
        # 7. 生成报告
        print("\n" + "=" * 50)
        print("🎉 Obsidian笔记保存完成！")
        print("\n📊 成果统计:")
        print(f"  - 对话笔记: 1 个")
        print(f"  - 关键词索引: 1 个")
        print(f"  - 核心概念: {len(keywords['核心概念'])} 个")
        print(f"  - 技术概念: {len(keywords['技术概念'])} 个")
        print(f"  - 对话特征: {len(keywords['对话特征'])} 个")
        print(f"  - 具象比喻: {len(keywords['具象比喻'])} 个")
        print(f"  - 更新概念: {len(updated_concepts)} 个")
        
        print("\n📁 保存位置:")
        print(f"  Obsidian库: {saver.vault_path}")
        print(f"  对话记录: {saver.vault_path / '对话记录'}")
        print(f"  关键词索引: {saver.vault_path / '关键词索引'}")
        print(f"  概念文件: {saver.vault_path / '概念'}")
        
        print("\n🔗 下一步:")
        print("  1. 在Obsidian中打开笔记库查看")
        print("  2. 使用关键词索引快速检索概念")
        print("  3. 继续完善概念文件的定义和引用")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()