#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识发现工具 - 帮助探索璇玑台知识库中的概念和关系
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class KnowledgeDiscovery:
    """知识发现工具"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.graph = nx.DiGraph()  # 有向图
        self.concepts = {}
        self.relationships = []
        
    def load_concepts(self):
        """加载概念文件"""
        print("加载概念文件...")
        
        concepts_dir = self.obsidian_path / "concepts"
        if not concepts_dir.exists():
            print("concepts目录不存在")
            return
        
        # 加载所有概念文件
        for concept_file in concepts_dir.glob("*.md"):
            if concept_file.name == "README.md":
                continue
            
            try:
                with open(concept_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取概念信息
                concept_name = concept_file.stem
                
                # 提取标题
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else concept_name
                
                # 提取定义
                definition_match = re.search(r'## 定义\s*\n(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
                definition = definition_match.group(1).strip() if definition_match else ""
                
                # 提取标签
                tags_match = re.search(r'tags:\s*\[(.+?)\]', content)
                tags = [tag.strip() for tag in tags_match.group(1).split(',')] if tags_match else []
                
                # 提取相关概念
                related_match = re.search(r'related:\s*\[(.+?)\]', content)
                related = []
                if related_match:
                    related_text = related_match.group(1)
                    # 提取[[概念名]]格式
                    related_concepts = re.findall(r'\[\[(.+?)\]\]', related_text)
                    related = [concept.strip() for concept in related_concepts]
                
                # 存储概念信息
                self.concepts[concept_name] = {
                    "title": title,
                    "definition": definition[:200] + "..." if len(definition) > 200 else definition,
                    "tags": tags,
                    "related": related,
                    "file_path": str(concept_file.relative_to(self.obsidian_path))
                }
                
                # 添加到图
                self.graph.add_node(concept_name, 
                                   title=title,
                                   definition=definition[:100],
                                   tags=tags)
                
                # 添加关系
                for related_concept in related:
                    if related_concept in self.concepts:
                        self.graph.add_edge(concept_name, related_concept, type="related")
                        self.relationships.append({
                            "from": concept_name,
                            "to": related_concept,
                            "type": "related"
                        })
                
            except Exception as e:
                print(f"加载概念文件 {concept_file.name} 失败: {e}")
        
        print(f"加载完成: {len(self.concepts)} 个概念，{len(self.relationships)} 个关系")
    
    def find_concept(self, keyword: str) -> List[Dict]:
        """查找概念"""
        results = []
        keyword_lower = keyword.lower()
        
        for concept_name, info in self.concepts.items():
            # 在概念名中查找
            if keyword_lower in concept_name.lower():
                results.append({
                    "concept": concept_name,
                    "match_type": "name",
                    "info": info
                })
                continue
            
            # 在标题中查找
            if keyword_lower in info["title"].lower():
                results.append({
                    "concept": concept_name,
                    "match_type": "title",
                    "info": info
                })
                continue
            
            # 在定义中查找
            if keyword_lower in info["definition"].lower():
                results.append({
                    "concept": concept_name,
                    "match_type": "definition",
                    "info": info
                })
                continue
        
        return results
    
    def explore_relationships(self, concept_name: str, depth: int = 2) -> Dict:
        """探索概念关系"""
        if concept_name not in self.graph:
            return {"error": f"概念 '{concept_name}' 不存在"}
        
        result = {
            "concept": concept_name,
            "title": self.concepts.get(concept_name, {}).get("title", concept_name),
            "definition": self.concepts.get(concept_name, {}).get("definition", ""),
            "related_concepts": [],
            "incoming": [],
            "outgoing": []
        }
        
        # 查找相关概念
        if concept_name in self.concepts:
            related = self.concepts[concept_name].get("related", [])
            for related_concept in related:
                if related_concept in self.concepts:
                    result["related_concepts"].append({
                        "concept": related_concept,
                        "title": self.concepts[related_concept]["title"],
                        "relation": "explicit"
                    })
        
        # 查找入边（指向该概念的概念）
        for predecessor in self.graph.predecessors(concept_name):
            result["incoming"].append({
                "concept": predecessor,
                "title": self.concepts.get(predecessor, {}).get("title", predecessor),
                "relation": "references"
            })
        
        # 查找出边（该概念指向的概念）
        for successor in self.graph.successors(concept_name):
            result["outgoing"].append({
                "concept": successor,
                "title": self.concepts.get(successor, {}).get("title", successor),
                "relation": "references"
            })
        
        return result
    
    def find_connections(self, concept1: str, concept2: str) -> List[List[str]]:
        """查找两个概念之间的连接路径"""
        if concept1 not in self.graph or concept2 not in self.graph:
            return []
        
        try:
            paths = list(nx.all_simple_paths(self.graph, concept1, concept2, cutoff=3))
            return paths
        except:
            return []
    
    def discover_clusters(self) -> List[Dict]:
        """发现概念集群"""
        # 使用社区检测算法
        try:
            # 转换为无向图进行社区检测
            undirected_graph = self.graph.to_undirected()
            
            # 使用Louvain算法检测社区
            import community as community_louvain
            partition = community_louvain.best_partition(undirected_graph)
            
            # 组织结果
            clusters = defaultdict(list)
            for node, community_id in partition.items():
                clusters[community_id].append(node)
            
            # 转换为列表格式
            result = []
            for community_id, nodes in clusters.items():
                if len(nodes) >= 3:  # 只包含至少3个概念的集群
                    result.append({
                        "cluster_id": community_id,
                        "size": len(nodes),
                        "concepts": nodes[:10],  # 只显示前10个
                        "sample_concepts": [self.concepts.get(n, {}).get("title", n) for n in nodes[:3]]
                    })
            
            return sorted(result, key=lambda x: x["size"], reverse=True)
            
        except ImportError:
            print("请安装python-louvain包: pip install python-louvain")
            return []
        except Exception as e:
            print(f"社区检测失败: {e}")
            return []
    
    def generate_report(self) -> str:
        """生成知识发现报告"""
        report = []
        report.append("# 知识发现报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"概念总数: {len(self.concepts)}")
        report.append(f"关系总数: {len(self.relationships)}")
        report.append("")
        
        # 核心概念
        report.append("## 核心概念")
        core_concepts = []
        for concept_name, info in self.concepts.items():
            # 根据连接数判断重要性
            degree = self.graph.degree(concept_name)
            if degree >= 3:  # 连接数至少3个
                core_concepts.append((concept_name, degree, info["title"]))
        
        core_concepts.sort(key=lambda x: x[1], reverse=True)
        
        for concept_name, degree, title in core_concepts[:10]:
            report.append(f"- **{title}** ({concept_name}) - 连接数: {degree}")
        
        report.append("")
        
        # 概念集群
        clusters = self.discover_clusters()
        if clusters:
            report.append("## 概念集群")
            for cluster in clusters[:5]:  # 只显示前5个集群
                report.append(f"### 集群 {cluster['cluster_id']} (大小: {cluster['size']})")
                report.append(f"示例概念: {', '.join(cluster['sample_concepts'])}")
                report.append("")
        
        # 发现建议
        report.append("## 发现建议")
        report.append("### 1. 深入探索")
        for concept_name, degree, title in core_concepts[:3]:
            report.append(f"- 深入研究 **{title}** 及其相关概念")
        
        report.append("")
        report.append("### 2. 连接建立")
        # 查找可能缺失的连接
        high_degree_nodes = [n for n, d in self.graph.degree() if d >= 3]
        if len(high_degree_nodes) >= 2:
            report.append(f"- 探索 **{self.concepts[high_degree_nodes[0]]['title']}** 和 **{self.concepts[high_degree_nodes[1]]['title']}** 之间的潜在关系")
        
        report.append("")
        report.append("### 3. 新概念建议")
        # 根据集群发现可能的缺失概念
        if clusters:
            largest_cluster = clusters[0]
            report.append(f"- 在最大的概念集群中（{largest_cluster['size']}个概念），可能存在尚未定义的核心概念")
        
        return "\n".join(report)
    
    def run_discovery(self, keyword: str = None):
        """运行知识发现"""
        print("🚀 开始知识发现")
        print("=" * 60)
        
        # 加载概念
        self.load_concepts()
        
        if not self.concepts:
            print("未找到概念文件")
            return
        
        print()
        
        # 如果有关键词，进行搜索
        if keyword:
            print(f"🔍 搜索关键词: {keyword}")
            results = self.find_concept(keyword)
            
            if results:
                print(f"找到 {len(results)} 个相关概念:")
                for result in results[:5]:  # 只显示前5个
                    info = result["info"]
                    print(f"\n📚 {info['title']} ({result['concept']})")
                    print(f"   匹配类型: {result['match_type']}")
                    print(f"   定义: {info['definition'][:100]}...")
                    print(f"   标签: {', '.join(info['tags'][:3])}")
                    print(f"   相关概念: {', '.join(info['related'][:3])}")
            else:
                print("未找到相关概念")
        
        print()
        
        # 生成报告
        print("📊 知识发现报告")
        print("=" * 60)
        
        report = self.generate_report()
        print(report)
        
        # 保存报告
        report_path = self.obsidian_path / "system" / "discovery" / f"知识发现报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print()
        print(f"📄 报告已保存: {report_path}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="知识发现工具")
    parser.add_argument("--obsidian-path", default=r"D:\LDD\璇玑台", help="Obsidian知识库路径")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--explore", help="探索特定概念的关系")
    parser.add_argument("--connect", nargs=2, help="查找两个概念之间的连接")
    
    args = parser.parse_args()
    
    # 创建发现工具
    discovery = KnowledgeDiscovery(args.obsidian_path)
    
    if args.explore:
        # 探索特定概念
        discovery.load_concepts()
        result = discovery.explore_relationships(args.explore)
        
        print(f"🔗 探索概念: {args.explore}")
        print("=" * 60)
        
        if "error" in result:
            print(result["error"])
        else:
            print(f"概念: {result['title']}")
            print(f"定义: {result['definition'][:200]}...")
            print()
            
            print("📥 入边（引用此概念的概念）:")
            for item in result["incoming"][:5]:
                print(f"  • {item['title']} ({item['relation']})")
            
            print()
            print("📤 出边（此概念引用的概念）:")
            for item in result["outgoing"][:5]:
                print(f"  • {item['title']} ({item['relation']})")
            
            print()
            print("🔗 显式相关概念:")
            for item in result["related_concepts"][:5]:
                print(f"  • {item['title']} ({item['relation']})")
    
    elif args.connect:
        # 查找连接
        discovery.load_concepts()
        paths = discovery.find_connections(args.connect[0], args.connect[1])
        
        print(f"🔗 查找连接: {args.connect[0]} → {args.connect[1]}")
        print("=" * 60)
        
        if paths:
            print(f"找到 {len(paths)} 条连接路径:")
            for i, path in enumerate(paths[:3], 1):  # 只显示前3条
                print(f"\n路径 {i}:")
                for j, concept in enumerate(path):
                    concept_info = discovery.concepts.get(concept, {})
                    title = concept_info.get("title", concept)
                    print(f"  {j+1}. {title} ({concept})")
        else:
            print("未找到直接连接路径")
    
    else:
        # 运行完整发现
        discovery.run_discovery(args.keyword)

if __name__ == "__main__":
    main()
