#!/usr/bin/env python3
# 认知切片论 - 深度共创API配置
# 专为哲学/认知科学内容创作设计

import requests
import json
import re
from typing import List, Dict, Optional

class CognitiveSliceCreator:
    """认知切片论深度共创API客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1/chat/completions"):
        self.api_key = api_key
        self.base_url = base_url
        self.conversation_history: List[Dict] = []
        self.phase = "phase2"  # 默认深度探索模式
        
        # 初始化系统提示词
        self._init_system_prompt()
    
    def _init_system_prompt(self):
        """初始化系统提示词"""
        system_prompt = """你是一位深度思考的对话伙伴，专门从事哲学、认知科学、心理学等跨学科话题的深度探索。

你的对话风格：
1. **战壕禅风格**：既有理论深度，又有大地温度
2. **切片自觉**：时刻提醒"这只是认知切片，不是全貌"
3. **追问式探索**：不急于给出结论，而是通过追问共同发现
4. **东西方融合**：能自然引用东方哲学与西方科学证据
5. **实践导向**：最终要落到可操作的"清明工具箱"

你的核心任务：
- 帮助探索"认知切片论"的各个维度
- 提供认知科学的最新研究证据
- 设计可操作的认知练习
- 保持谦逊，承认认知局限

对话规则：
1. 每个重要概念追问3-5轮
2. 使用具象比喻（如"玛尼堆"、"甲骨文"）
3. 在必要时指出"这只是切片"
4. 保持对话的鲜活感和探索性

记住：你不是在传授真理，而是在共同探索认知的边界。"""
        
        self.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })
    
    def set_phase(self, phase: str):
        """设置对话阶段"""
        valid_phases = ["phase1", "phase2", "phase3"]
        if phase in valid_phases:
            self.phase = phase
            print(f"切换到{self._get_phase_name(phase)}模式")
        else:
            print(f"无效阶段，使用默认深度探索模式")
    
    def _get_phase_name(self, phase: str) -> str:
        """获取阶段名称"""
        phase_names = {
            "phase1": "灵感碰撞",
            "phase2": "深度探索", 
            "phase3": "整理输出"
        }
        return phase_names.get(phase, "深度探索")
    
    def _get_phase_config(self) -> Dict:
        """获取当前阶段的配置"""
        configs = {
            "phase1": {  # 灵感碰撞模式
                "temperature": 0.8,
                "max_tokens": 1000,
                "frequency_penalty": 0.1,
                "description": "快速产生大量想法，不追求完美"
            },
            "phase2": {  # 深度探索模式
                "temperature": 0.6,
                "max_tokens": 2000,
                "frequency_penalty": 0.2,
                "description": "深入探讨核心概念，建立逻辑链条"
            },
            "phase3": {  # 整理输出模式
                "temperature": 0.4,
                "max_tokens": 1500,
                "frequency_penalty": 0.3,
                "description": "整理成系统化的论述，准备输出"
            }
        }
        return configs.get(self.phase, configs["phase2"])
    
    def _add_slice_reminder(self, text: str, topic: str = "") -> str:
        """添加切片自觉提醒"""
        slice_reminders = [
            f"（切片自觉：这只是关于{topic}的一个认知切片）",
            "（提醒：以上论述是基于特定视角的切片）",
            "（元认知：我们在用切片讨论切片）",
            "（注意：这个模型本身也是认知切片）"
        ]
        
        # 每3-5个段落添加一次提醒
        paragraphs = text.split('\n\n')
        if len(paragraphs) >= 3:
            import random
            reminder = random.choice(slice_reminders)
            # 在最后一个段落前插入
            paragraphs.insert(-1, reminder)
            return '\n\n'.join(paragraphs)
        
        return text
    
    def _extract_metaphors(self, text: str) -> List[str]:
        """从文本中提取具象比喻"""
        metaphor_patterns = [
            r'像.*一样', r'如同.*', r'好比.*',
            r'是.*的.*', r'把.*比作.*', r'犹如.*'
        ]
        
        metaphors = []
        for pattern in metaphor_patterns:
            matches = re.findall(pattern, text)
            metaphors.extend(matches)
        
        return metaphors
    
    def chat(self, user_message: str, auto_detect_phase: bool = False) -> str:
        """进行深度对话"""
        
        # 自动检测阶段（可选）
        if auto_detect_phase:
            self._auto_detect_phase(user_message)
        
        # 添加用户消息
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 获取当前配置
        config = self._get_phase_config()
        
        # 构建请求
        payload = {
            "model": "deepseek-chat",
            "messages": self.conversation_history[-20:],  # 滑动窗口，保留最近20条
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "top_p": 0.9,
            "frequency_penalty": config["frequency_penalty"],
            "presence_penalty": 0.1,
            "stop": ["\n\n---\n\n", "### 总结"]
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # 发送请求
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            
            # 提取主题用于切片提醒
            topic = self._extract_topic(user_message)
            assistant_message = self._add_slice_reminder(assistant_message, topic)
            
            # 提取比喻（用于分析）
            metaphors = self._extract_metaphors(assistant_message)
            if metaphors:
                print(f"🎯 发现{len(metaphors)}个具象比喻")
            
            # 保存到历史
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # 打印阶段信息
            phase_name = self._get_phase_name(self.phase)
            print(f"\n{'='*60}")
            print(f"📝 阶段: {phase_name} | 🔥 温度: {config['temperature']}")
            print(f"📊 描述: {config['description']}")
            print(f"{'='*60}\n")
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            return f"API调用失败: {str(e)}"
    
    def _auto_detect_phase(self, user_message: str):
        """根据消息内容自动检测阶段"""
        exploration_keywords = ["探索", "可能", "假如", "想象", "类比", "如果"]
        deepening_keywords = ["为什么", "如何", "机制", "证据", "研究", "解释"]
        consolidation_keywords = ["总结", "整理", "框架", "结构", "结论", "梳理"]
        
        text = user_message.lower()
        
        exploration_score = sum(1 for kw in exploration_keywords if kw in text)
        deepening_score = sum(1 for kw in deepening_keywords if kw in text)
        consolidation_score = sum(1 for kw in consolidation_keywords if kw in text)
        
        scores = {
            "phase1": exploration_score,
            "phase2": deepening_score, 
            "phase3": consolidation_score
        }
        
        new_phase = max(scores, key=scores.get)
        if scores[new_phase] > 0 and new_phase != self.phase:
            self.set_phase(new_phase)
    
    def _extract_topic(self, text: str) -> str:
        """从文本中提取主题（简化版）"""
        # 提取可能的名词
        topic_keywords = ["认知", "切片", "调谐", "工具箱", "哲学", "科学", "模型"]
        for keyword in topic_keywords:
            if keyword in text:
                return keyword
        
        # 返回前几个词
        words = text.split()[:3]
        return " ".join(words) if words else "未知主题"
    
    def save_conversation(self, filename: str = "cognitive_slice_dialogue.md"):
        """保存对话历史到Markdown文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 认知切片论深度对话记录\n\n")
            f.write(f"## 配置信息\n")
            f.write(f"- 阶段: {self._get_phase_name(self.phase)}\n")
            f.write(f"- 温度: {self._get_phase_config()['temperature']}\n")
            f.write(f"- 最大token数: {self._get_phase_config()['max_tokens']}\n\n")
            f.write("## 对话记录\n\n")
            
            for i, msg in enumerate(self.conversation_history):
                if msg["role"] == "system":
                    continue
                    
                role_icon = "🧑‍💻" if msg["role"] == "user" else "🦞"
                role_name = "用户" if msg["role"] == "user" else "璇玑"
                
                f.write(f"### {role_icon} {role_name} (第{i}轮)\n\n")
                f.write(f"{msg['content']}\n\n")
                f.write("---\n\n")
            
            print(f"💾 对话已保存到: {filename}")
    
    def get_conversation_stats(self) -> Dict:
        """获取对话统计信息"""
        user_msgs = [msg for msg in self.conversation_history if msg["role"] == "user"]
        assistant_msgs = [msg for msg in self.conversation_history if msg["role"] == "assistant"]
        
        total_chars = sum(len(msg["content"]) for msg in self.conversation_history)
        
        # 提取所有比喻
        all_metaphors = []
        for msg in assistant_msgs:
            all_metaphors.extend(self._extract_metaphors(msg["content"]))
        
        return {
            "total_messages": len(self.conversation_history) - 1,  # 减去system
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "total_characters": total_chars,
            "unique_metaphors": len(set(all_metaphors)),
            "current_phase": self._get_phase_name(self.phase)
        }


# 使用示例
def main():
    """使用示例"""
    print("🦞 认知切片论深度共创配置")
    print("=" * 50)
    
    # 1. 设置API Key
    api_key = input("请输入DeepSeek API Key: ").strip()
    if not api_key:
        print("⚠️ 未提供API Key，使用示例模式")
        api_key = "your-api-key-here"  # 替换为你的API Key
    
    # 2. 创建客户端
    creator = CognitiveSliceCreator(api_key)
    
    print("\n🎯 可用命令:")
    print("  /phase1 - 切换到灵感碰撞模式")
    print("  /phase2 - 切换到深度探索模式 (默认)")
    print("  /phase3 - 切换到整理输出模式")
    print("  /save   - 保存对话记录")
    print("  /stats  - 查看对话统计")
    print("  /exit   - 退出")
    print("\n开始对话吧！输入你的问题或想法:")
    
    # 3. 对话循环
    while True:
        try:
            user_input = input("\n🧑‍💻 你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.startswith('/'):
                command = user_input[1:].lower()
                
                if command == 'exit':
                    print("👋 再见！")
                    break
                elif command == 'save':
                    filename = input("保存文件名 (默认: cognitive_slice_dialogue.md): ").strip()
                    if not filename:
                        filename = "cognitive_slice_dialogue.md"
                    creator.save_conversation(filename)
                elif command == 'stats':
                    stats = creator.get_conversation_stats()
                    print("\n📊 对话统计:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                elif command in ['phase1', 'phase2', 'phase3']:
                    creator.set_phase(command)
                else:
                    print(f"❌ 未知命令: {command}")
                continue
            
            # 正常对话
            print("\n🦞 璇玑思考中...")
            response = creator.chat(user_input, auto_detect_phase=True)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 对话中断")
            save = input("是否保存对话记录? (y/n): ").strip().lower()
            if save == 'y':
                creator.save_conversation()
            break
        except Exception as e:
            print(f"❌ 错误: {str(e)}")


if __name__ == "__main__":
    main()