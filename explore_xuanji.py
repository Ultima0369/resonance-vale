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
    
    # 保存文件列表
    with open('xuanji_files.json', 'w', encoding='utf-8') as f:
        json.dump(all_files[:100], f, ensure_ascii=False, indent=2)
    
    return all_files

def read_large_files(file_list, max_files=10):
    """读取最大的几个文件"""
    results = []
    
    for i, file_info in enumerate(file_list[:max_files]):
        try:
            with open(file_info['full_path'], 'r', encoding='utf-8') as f:
                content = f.read(5000)  # 只读取前5000字符
                
            # 提取关键信息
            lines = content.split('\n')
            title = lines[0] if lines else "无标题"
            
            results.append({
                'index': i+1,
                'path': file_info['path'],
                'size': file_info['size'],
                'title': title[:100],
                'preview': content[:500]
            })
            
            print(f"\n=== 文件 {i+1}: {file_info['path']} ===")
            print(f"大小: {file_info['size']:,} 字节")
            print(f"标题: {title[:100]}")
            print(f"预览: {content[:500]}...")
            
        except Exception as e:
            print(f"读取文件 {file_info['path']} 时出错: {e}")
            continue
    
    return results

def search_cognitive_content(file_list):
    """搜索认知相关的内容"""
    cognitive_keywords = ['认知', '思维', '意识', '心理', '神经', '大脑', '思考', '理解', '误解', '框架', '定格']
    
    cognitive_files = []
    
    for file_info in file_list[:50]:  # 只检查前50个文件
        try:
            with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000)  # 读取前10000字符
                
            # 检查是否包含认知关键词
            keyword_hits = []
            for keyword in cognitive_keywords:
                if keyword in content:
                    keyword_hits.append(keyword)
            
            if keyword_hits:
                # 提取包含关键词的段落
                lines = content.split('\n')
                relevant_lines = []
                for line in lines:
                    if any(keyword in line for keyword in cognitive_keywords):
                        relevant_lines.append(line[:200])
                        if len(relevant_lines) >= 3:
                            break
                
                cognitive_files.append({
                    'path': file_info['path'],
                    'size': file_info['size'],
                    'keywords': keyword_hits,
                    'preview': '\n'.join(relevant_lines[:3])
                })
                
        except Exception as e:
            continue
    
    print(f"\n=== 找到 {len(cognitive_files)} 个认知相关文件 ===")
    for i, cf in enumerate(cognitive_files[:10]):
        print(f"\n{i+1}. {cf['path']}")
        print(f"   关键词: {cf['keywords']}")
        print(f"   预览: {cf['preview'][:300]}...")
    
    return cognitive_files

if __name__ == "__main__":
    print("开始探索璇玑台目录...")
    all_files = explore_xuanji_directory()
    
    if all_files:
        print("\n=== 读取大文件内容 ===")
        large_files = read_large_files(all_files, max_files=5)
        
        print("\n=== 搜索认知相关内容 ===")
        cognitive_files = search_cognitive_content(all_files)
        
        # 保存结果
        with open('cognitive_insights.json', 'w', encoding='utf-8') as f:
            json.dump({
                'large_files': large_files,
                'cognitive_files': cognitive_files
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n探索完成！结果已保存到 cognitive_insights.json")