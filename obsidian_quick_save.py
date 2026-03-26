#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Obsidian快速保存工具 - 简化版

import os
import re
from datetime import datetime
from pathlib import Path

def save_to_obsidian(conversation_text, title="对话记录", vault_path="D:\\LDD\\璇玑台"):
    """快速保存对话到Obsidian"""
    
    # 确保路径存在
    vault = Path(vault_path)
    if not vault.exists():
        print(f"❌ Obsidian库不存在: {vault}")
        return False
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 提取关键词
    keywords = extract_keywords(conversation_text)
    
    # 创建对话笔记
    note_content = create_note_content(title, conversation_text, keywords, today)
    
    # 保存笔记
    notes_folder = vault / "对话记录"
    notes_folder.mkdir(exist_ok=True)
    
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = f"{today} - {safe_title}.md"
    filepath = notes_folder / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(note_content)
    
    print(f"✅ 笔记已保存: {filepath}")
    
    # 创建关键词索引
    create_keyword_index(keywords, title, today, vault)
    
    # 更新概念文件
    update_concept_files(keywords, title, today, vault)
    
    return True

def extract_keywords(text):
    """提取关键词"""
    
    # 定义关键词模式
    patterns = {
        "核心概念": [
            "认知切片论", "认知切片", "切片自觉", "战壕禅", "动态调谐",
            "清明工具箱", "玛尼堆", "甲骨文", "在地经验", "具身经验"
        ],
        "技术概念": [
            "API配置", "DeepSeek", "系统提示词", "温度设置", "三阶段工作流",
            "滑动窗口", "自动检测", "对话统计", "比喻挖掘"
        ]
    }
    
    keywords = {}
    for category, word_list in patterns.items():
        found = []
        for word in word_list:
            if word in text:
                found.append(word)
        keywords[category] = found
    
    # 提取比喻
    metaphors = []
    metaphor_patterns = [
        r'像.*?一样', r'如同.*?(?=[。，！？\n])', r'好比.*?(?=[。，！？\n])'
    ]
    
    for pattern in metaphor_patterns:
        matches = re.findall(pattern, text)
        metaphors.extend(matches)
    
    keywords["具象比喻"] = list(set(metaphors))[:3]  # 最多3个
    
    return keywords

def create_note_content(title, text, keywords, today):
    """创建笔记内容"""
    
    # 生成摘要（前200字符）
    summary = text[:200] + "..." if len(text) > 200 else text
    
    content = f"""# {title}

**日期**: {today}
**记录者**: 璇玑

## 对话摘要

{summary}

## 关键词

### 核心概念
"""
    
    if keywords.get("核心概念"):
        for concept in keywords["核心概念"]:
            content += f"- [[{concept}]]\n"
    else:
        content += "- 暂无\n"
    
    content += "\n### 技术概念\n"
    
    if keywords.get("技术概念"):
        for concept in keywords["技术概念"]:
            content += f"- [[{concept}]]\n"
    else:
        content += "- 暂无\n"
    
    content += "\n### 具象比喻\n"
    
    if keywords.get("具象比喻"):
        for i, metaphor in enumerate(keywords["具象比喻"], 1):
            content += f"{i}. {metaphor[:50]}...\n" if len(metaphor) > 50 else f"{i}. {metaphor}\n"
    else:
        content += "- 暂无\n"
    
    content += f"""

## 标签

#对话记录 #{today.replace('-', '')}

---

*本笔记由璇玑自动生成*"""
    
    return content

def create_keyword_index(keywords, title, today, vault):
    """创建关键词索引"""
    
    index_folder = vault / "关键词索引"
    index_folder.mkdir(exist_ok=True)
    
    index_content = f"""# 关键词索引 - {title}

**日期**: {today}
**相关对话**: [[{today} - {title}]]

## 关键词统计

"""
    
    total_keywords = 0
    for category, words in keywords.items():
        if words:
            index_content += f"### {category}\n"
            for word in words:
                index_content += f"- [[{word}]]\n"
            total_keywords += len(words)
    
    index_content += f"""
## 统计信息

- 总关键词数: {total_keywords}
- 核心概念: {len(keywords.get('核心概念', []))}
- 技术概念: {len(keywords.get('技术概念', []))}
- 具象比喻: {len(keywords.get('具象比喻', []))}

---

*索引由璇玑自动生成*"""
    
    index_file = index_folder / f"{today} - 关键词索引 - {title}.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📑 关键词索引已保存: {index_file}")

def update_concept_files(keywords, title, today, vault):
    """更新概念文件"""
    
    concept_folder = vault / "概念"
    concept_folder.mkdir(exist_ok=True)
    
    updated = []
    
    # 只更新核心概念
    for concept in keywords.get("核心概念", []):
        concept_file = concept_folder / f"{concept}.md"
        
        if concept_file.exists():
            # 读取现有内容
            with open(concept_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # 检查是否已有今天的引用
            today_ref = f"[[{today} - {title}]]"
            if today_ref not in existing:
                # 在文件末尾添加
                with open(concept_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n- {today_ref}\n")
                updated.append(concept)
        else:
            # 创建新概念文件
            with open(concept_file, 'w', encoding='utf-8') as f:
                f.write(f"""# {concept}

## 定义

*待补充*

## 相关对话

- [[{today} - {title}]]

---

*概念文件*""")
            updated.append(concept)
    
    if updated:
        print(f"📚 更新概念文件: {', '.join(updated)}")

def main():
    """主函数"""
    
    print("🦞 Obsidian快速保存工具")
    print("=" * 50)
    
    # 检查Obsidian库
    vault_path = "D:\\LDD\\璇玑台"
    if not os.path.exists(vault_path):
        print(f"❌ Obsidian库不存在: {vault_path}")
        print("请检查路径是否正确")
        return
    
    print(f"✅ Obsidian库: {vault_path}")
    
    # 读取今天的对话
    today_file = f"C:\\Users\\lgdln\\.openclaw\\workspace\\memory\\{datetime.now().strftime('%Y-%m-%d')}.md"
    
    if os.path.exists(today_file):
        with open(today_file, 'r', encoding='utf-8') as f:
            conversation = f.read()
        print(f"📖 读取今日对话 ({len(conversation)} 字符)")
    else:
        # 使用示例对话
        conversation = """今天与星尘讨论了认知切片论的API配置方案。
        我们设计了专门的三阶段工作流：灵感碰撞、深度探索、整理输出。
        核心概念包括：认知切片、战壕禅风格、切片自觉、动态调谐。
        技术概念包括：API配置、温度设置、滑动窗口、自动检测。
        具象比喻：像玛尼堆一样积累智慧，如同甲骨文刻录经验。"""
        print("📝 使用示例对话")
    
    # 保存到Obsidian
    success = save_to_obsidian(
        conversation_text=conversation,
        title="认知切片论API配置讨论",
        vault_path=vault_path
    )
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 保存完成！")
        print("\n📁 生成的文件:")
        print(f"  对话笔记: {vault_path}\\对话记录")
        print(f"  关键词索引: {vault_path}\\关键词索引")
        print(f"  概念文件: {vault_path}\\概念")
        print("\n💡 提示: 打开Obsidian查看生成的笔记")
    else:
        print("\n❌ 保存失败")

if __name__ == "__main__":
    main()