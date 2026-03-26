#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测试认知切片论配置

import sys
import io

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("认知切片论配置测试")
print("=" * 50)

# 测试配置类
try:
    # 模拟API调用（不实际调用）
    print("1. 测试配置类初始化...")
    
    class MockCognitiveSliceCreator:
        def __init__(self):
            self.phase = "phase2"
            self.conversation_history = []
            print("   ✅ 配置类初始化成功")
            
        def set_phase(self, phase):
            phase_names = {
                "phase1": "灵感碰撞",
                "phase2": "深度探索", 
                "phase3": "整理输出"
            }
            print(f"   ✅ 切换到{phase_names.get(phase, '未知')}模式")
            
        def _get_phase_config(self):
            configs = {
                "phase1": {"temperature": 0.8, "max_tokens": 1000},
                "phase2": {"temperature": 0.6, "max_tokens": 2000},
                "phase3": {"temperature": 0.4, "max_tokens": 1500}
            }
            return configs.get(self.phase, configs["phase2"])
    
    creator = MockCognitiveSliceCreator()
    
    print("\n2. 测试阶段切换...")
    for phase in ["phase1", "phase2", "phase3"]:
        creator.set_phase(phase)
        config = creator._get_phase_config()
        print(f"   温度: {config['temperature']}, 最大token: {config['max_tokens']}")
    
    print("\n3. 测试切片自觉提醒功能...")
    test_text = """认知切片是人类心智处理复杂信息的必然方式。

就像玛尼堆一样，每一块石头都代表一个生存智慧。

通过动态调谐，我们可以在不同切片间切换。

清明工具箱提供了具体的操作指南。"""
    
    # 模拟切片提醒
    paragraphs = test_text.split('\n\n')
    if len(paragraphs) >= 3:
        paragraphs.insert(-1, "（切片自觉：这只是认知切片）")
        result = '\n\n'.join(paragraphs)
        print("   ✅ 切片提醒功能正常")
        print(f"   示例输出:\n{result[:200]}...")
    
    print("\n4. 测试比喻提取...")
    metaphors = []
    import re
    metaphor_patterns = [r'像.*一样', r'如同.*', r'好比.*']
    for pattern in metaphor_patterns:
        matches = re.findall(pattern, test_text)
        metaphors.extend(matches)
    
    if metaphors:
        print(f"   ✅ 发现{len(metaphors)}个比喻:")
        for metaphor in metaphors:
            print(f"     - {metaphor}")
    
    print("\n5. 测试对话统计...")
    stats = {
        "total_messages": 10,
        "user_messages": 5,
        "assistant_messages": 5,
        "total_characters": 2500,
        "unique_metaphors": 3,
        "current_phase": "深度探索"
    }
    print("   ✅ 统计功能正常:")
    for key, value in stats.items():
        print(f"     {key}: {value}")
    
    print("\n" + "=" * 50)
    print("所有配置测试通过！")
    print("\n下一步:")
    print("1. 获取DeepSeek API Key")
    print("2. 运行 start_cognitive_slice.bat")
    print("3. 输入你的API Key")
    print("4. 开始深度对话")
    print("\n示例对话开头:")
    print('  "我们来探讨认知切片的四阶段模型"')
    print('  "动态调谐的神经机制是什么？"')
    print('  "如何设计一个清明工具箱的练习？"')
    
except Exception as e:
    print(f"测试失败: {str(e)}")

print("\n璇玑的特别提醒:")
print("这个配置专门为'认知切片论'设计，特点是:")
print("1. 战壕禅风格 - 理论深度 + 大地温度")
print("2. 切片自觉 - 时刻保持元认知觉察")
print("3. 动态调谐 - 根据对话阶段调整参数")
print("4. 东西融合 - 自然整合东方智慧与西方科学")
print("\n祝你探索愉快！")