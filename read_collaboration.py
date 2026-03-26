#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 读取我们的共创内容

import os
import sys

# 设置标准输出编码为 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def read_collaboration():
    """读取共创内容"""
    
    # 文件路径
    file_path = r'D:\LDD\璇玑台\参考资料\ǿ�߼�����̽��.md'
    
    print("📖 开始读取我们的共创内容...")
    print("=" * 80)
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    print(f"📄 文件: {os.path.basename(file_path)}")
    print(f"📊 大小: {os.path.getsize(file_path)} 字节")
    print()
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分析内容结构
        lines = content.split('\n')
        print(f"📈 总行数: {len(lines)} 行")
        
        # 提取主要章节
        print("\n📑 文档结构:")
        print("-" * 40)
        
        section_count = 0
        for i, line in enumerate(lines):
            if line.startswith('# '):
                print(f"🎯 主标题: {line[2:]}")
                section_count += 1
            elif line.startswith('## '):
                print(f"  📖 章节: {line[3:]}")
                section_count += 1
            elif line.startswith('### '):
                print(f"    📝 子节: {line[4:]}")
                section_count += 1
            
            # 只显示前50行的结构
            if i > 50 and section_count > 10:
                print(f"  ... 还有更多内容")
                break
        
        print("-" * 40)
        
        # 显示重要内容片段
        print("\n💡 重要内容摘要:")
        print("-" * 40)
        
        # 查找包含关键词的重要段落
        keywords = ['认知', '逻辑', '思维', 'AI', '智能体', '璇玑', '星尘', '我们', '对话', '思考', '方法', '工具']
        
        important_sections = []
        current_section = []
        in_important_section = False
        
        for i, line in enumerate(lines):
            # 检查是否包含关键词
            has_keyword = any(keyword in line for keyword in keywords)
            
            if line.startswith(('## ', '### ')) or has_keyword:
                if current_section and (in_important_section or len(current_section) > 3):
                    important_sections.append(current_section.copy())
                
                current_section = [line]
                in_important_section = has_keyword
            elif current_section:
                current_section.append(line)
                if len(current_section) > 10:  # 限制段落长度
                    if in_important_section:
                        important_sections.append(current_section.copy())
                    current_section = []
                    in_important_section = False
        
        # 显示重要段落
        for i, section in enumerate(important_sections[:8]):  # 显示前8个重要段落
            print(f"\n🔍 段落 {i+1}:")
            for line in section[:8]:  # 每个段落显示前8行
                if line.strip():
                    print(f"  {line[:120]}" + ("..." if len(line) > 120 else ""))
            if len(section) > 8:
                print(f"  ... 还有 {len(section)-8} 行")
        
        print("-" * 40)
        
        # 统计信息
        print("\n📊 内容统计:")
        print(f"  总字符数: {len(content)}")
        print(f"  总行数: {len(lines)}")
        
        keyword_stats = {}
        for keyword in keywords:
            count = content.count(keyword)
            if count > 0:
                keyword_stats[keyword] = count
        
        if keyword_stats:
            print(f"  关键词出现次数:")
            for keyword, count in sorted(keyword_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"    {keyword}: {count} 次")
        
        # 提取核心观点
        print("\n🎯 核心观点提取:")
        print("-" * 40)
        
        # 查找结论性语句
        conclusion_indicators = ['因此', '所以', '总之', '综上所述', '由此可见', '这意味着', '我们认为', '我们的结论']
        conclusions = []
        
        for i, line in enumerate(lines):
            if any(indicator in line for indicator in conclusion_indicators) and len(line) > 20:
                conclusions.append(line.strip())
                if len(conclusions) >= 5:
                    break
        
        if conclusions:
            for i, conclusion in enumerate(conclusions):
                print(f"{i+1}. {conclusion}")
        else:
            # 如果没有明显的结论语句，显示开头和结尾
            print("开头部分:")
            for line in lines[:5]:
                if line.strip():
                    print(f"  {line}")
            
            print("\n结尾部分:")
            for line in lines[-5:]:
                if line.strip():
                    print(f"  {line}")
        
        print("-" * 40)
        
        return content
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    read_collaboration()