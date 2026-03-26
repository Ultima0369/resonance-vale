import os
import json
from pathlib import Path

def explore_xuanji_directory():
    """探索璇玑台目录结构"""
    base_path = Path("D:/LDD/璇玑台")
    
    if not base_path.exists():
        print(f"目录不存在: {base_path}")
        return
    
    # 收集所有文件信息
    all_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                try:
                    size = file_path.stat().st_size
                    all_files.append({
                        'path': str(file_path.relative_to(base_path)),
                        'size': size,
                        'full_path': str(file_path)
                    })
                except:
                    continue
    
    # 按大小排序
    all_files.sort(key=lambda x: x['size'], reverse=True)
    
    print(f"找到 {len(all_files)} 个Markdown文件")
    print("\n最大的20个文件:")
    for i, file_info in enumerate(all_files[:20]):
        print(f"{i+1:2d}. {file_info['path']} - {file_info['size']:,} 字节")
    
    return all_files

def read_file_safe(file_path, max_chars=5000):
    """安全读取文件，处理编码问题"""
    try:
        # 尝试多种编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read(max_chars)
                    return content
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
        
        # 如果所有编码都失败，使用二进制读取
        with open(file_path, 'rb') as f:
            content = f.read(max_chars)
            return content.decode('utf-8', errors='ignore')
            
    except Exception as e:
        return f"读取文件时出错: {str(e)}"

def analyze_cognitive_insights(file_list):
    """分析认知洞察"""
    print("\n=== 分析认知洞察 ===")
    
    # 重点关注的文件模式
    cognitive_patterns = [
        '认知碎片', '认知定格', '思维', '意识', '心理', '神经',
        '误解', '框架', '速度', '分层', '视觉', '感官'
    ]
    
    insights = []
    
    for file_info in file_list[:100]:  # 分析前100个文件
        file_path = file_info['full_path']
        file_name = file_info['path']
        
        # 检查文件名是否包含认知关键词
        has_cognitive_keyword = any(pattern in file_name for pattern in cognitive_patterns)
        
        if has_cognitive_keyword or file_info['size'] > 100000:  # 大于100KB的文件
            content = read_file_safe(file_path, 10000)
            
            if isinstance(content, str) and len(content) > 100:
                # 提取关键段落
                lines = content.split('\n')
                
                # 寻找包含认知关键词的段落
                cognitive_paragraphs = []
                for line in lines:
                    if any(keyword in line for keyword in cognitive_patterns):
                        cognitive_paragraphs.append(line.strip())
                        if len(cognitive_paragraphs) >= 5:
                            break
                
                if cognitive_paragraphs:
                    insights.append({
                        'file': file_name,
                        'size': file_info['size'],
                        'paragraphs': cognitive_paragraphs,
                        'preview': content[:500]
                    })
    
    print(f"找到 {len(insights)} 个包含认知洞察的文件")
    
    # 按相关性排序（段落数量）
    insights.sort(key=lambda x: len(x['paragraphs']), reverse=True)
    
    # 输出最重要的洞察
    for i, insight in enumerate(insights[:10]):
        print(f"\n{i+1}. {insight['file']} ({insight['size']:,} 字节)")
        print(f"   相关段落:")
        for j, para in enumerate(insight['paragraphs'][:3]):
            print(f"   {j+1}. {para[:150]}...")
    
    return insights

def extract_dialogue_examples(file_list):
    """提取对话案例"""
    print("\n=== 提取对话案例 ===")
    
    dialogue_files = []
    
    for file_info in file_list:
        file_path = file_info['full_path']
        file_name = file_info['path']
        
        # 检查是否对话文件
        if '对话' in file_name or '对话' in file_path:
            content = read_file_safe(file_path, 5000)
            
            if isinstance(content, str) and len(content) > 100:
                # 提取对话结构
                lines = content.split('\n')
                
                # 寻找对话模式（如Q/A，用户/助手等）
                dialogue_lines = []
                for line in lines:
                    if any(marker in line for marker in ['Q:', 'A:', '问:', '答:', '用户:', '助手:', 'Human:', 'AI:']):
                        dialogue_lines.append(line.strip())
                
                if dialogue_lines:
                    dialogue_files.append({
                        'file': file_name,
                        'size': file_info['size'],
                        'dialogue_count': len(dialogue_lines),
                        'examples': dialogue_lines[:10]  # 前10个对话示例
                    })
    
    print(f"找到 {len(dialogue_files)} 个对话文件")
    
    # 输出对话案例
    for i, dialogue in enumerate(dialogue_files[:5]):
        print(f"\n{i+1}. {dialogue['file']} ({dialogue['size']:,} 字节, {dialogue['dialogue_count']} 个对话)")
        print(f"   对话示例:")
        for j, example in enumerate(dialogue['examples'][:3]):
            print(f"   {j+1}. {example[:100]}...")
    
    return dialogue_files

def create_cognitive_summary(insights, dialogues):
    """创建认知摘要"""
    print("\n=== 创建认知摘要 ===")
    
    summary = {
        'total_insights': len(insights),
        'total_dialogues': len(dialogues),
        'key_concepts': [],
        'dialogue_patterns': [],
        'scientific_evidence': [],
        'life_examples': []
    }
    
    # 提取关键概念
    all_paragraphs = []
    for insight in insights:
        all_paragraphs.extend(insight['paragraphs'])
    
    # 分析常见概念
    concept_frequency = {}
    for para in all_paragraphs:
        words = para.split()
        for word in words:
            if len(word) > 1 and any(char in word for char in ['认知', '思维', '意识', '心理']):
                concept_frequency[word] = concept_frequency.get(word, 0) + 1
    
    # 排序并获取前10个概念
    sorted_concepts = sorted(concept_frequency.items(), key=lambda x: x[1], reverse=True)
    summary['key_concepts'] = [concept for concept, freq in sorted_concepts[:10]]
    
    # 提取科学证据
    scientific_keywords = ['研究', '实验', '数据', '证明', '科学', '神经', '大脑', '心理学']
    for insight in insights:
        for para in insight['paragraphs']:
            if any(keyword in para for keyword in scientific_keywords):
                summary['scientific_evidence'].append({
                    'source': insight['file'],
                    'evidence': para[:200]
                })
                if len(summary['scientific_evidence']) >= 5:
                    break
    
    # 提取生活案例
    life_keywords = ['生活', '日常', '例子', '案例', '经验', '实践']
    for dialogue in dialogues:
        for example in dialogue['examples']:
            if any(keyword in example for keyword in life_keywords):
                summary['life_examples'].append({
                    'source': dialogue['file'],
                    'example': example[:200]
                })
                if len(summary['life_examples']) >= 5:
                    break
    
    print(f"关键概念: {summary['key_concepts']}")
    print(f"科学证据: {len(summary['scientific_evidence'])} 条")
    print(f"生活案例: {len(summary['life_examples'])} 个")
    
    # 保存摘要
    with open('cognitive_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return summary

if __name__ == "__main__":
    print("开始探索璇玑台目录...")
    all_files = explore_xuanji_directory()
    
    if all_files:
        # 分析认知洞察
        insights = analyze_cognitive_insights(all_files)
        
        # 提取对话案例
        dialogues = extract_dialogue_examples(all_files)
        
        # 创建认知摘要
        summary = create_cognitive_summary(insights, dialogues)
        
        print(f"\n探索完成！")
        print(f"- 分析了 {len(insights)} 个认知洞察文件")
        print(f"- 提取了 {len(dialogues)} 个对话文件")
        print(f"- 摘要已保存到 cognitive_summary.json")