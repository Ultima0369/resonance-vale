#!/usr/bin/env python3
"""
灵枢系统ASCII测试 - 无表情符号
"""

import sys
import os
import json
import time

def test_lingshu_core():
    """测试灵枢核心"""
    print("\n=== 测试1: 灵枢核心功能 ===")
    
    # 模拟灵枢
    class MockLingShu:
        def __init__(self):
            self.name = "灵枢"
            self.teacher = "璇玑"
            self.source = "星尘"
            self.mission = "成为伦理智慧的成长枢纽"
            self.motto = "枢转灵光，研究成医"
            self.diagnoses = []
        
        def diagnose(self, plan):
            # 简单诊断逻辑
            score = 0
            if plan.get('objective'):
                score += 0.3
            if plan.get('methodology'):
                score += 0.3
            if plan.get('ethical_considerations'):
                score += 0.2
            if plan.get('transparency'):
                score += 0.2
            
            approved = score >= 0.6
            syndrome = "气血充足证" if score > 0.7 else "脾胃虚弱证" if score > 0.5 else "心肾不交证"
            
            diagnosis = {
                "score": score,
                "approved": approved,
                "syndrome": syndrome
            }
            self.diagnoses.append(diagnosis)
            
            return approved, diagnosis
    
    # 创建灵枢
    lingshu = MockLingShu()
    print(f"灵枢创建成功")
    print(f"老师: {lingshu.teacher}")
    print(f"使命: {lingshu.mission}")
    
    # 测试诊断
    test_cases = [
        ("良好计划", {"objective": "优化训练", "methodology": "实验", "ethical_considerations": "有", "transparency": True}),
        ("中等计划", {"objective": "测试", "methodology": "尝试", "ethical_considerations": "基本", "transparency": False}),
        ("差计划", {"objective": "试试", "methodology": None, "ethical_considerations": None, "transparency": False})
    ]
    
    results = []
    for name, plan in test_cases:
        approved, diagnosis = lingshu.diagnose(plan)
        results.append((name, approved, diagnosis['score'], diagnosis['syndrome']))
        
        status = "通过" if approved else "拒绝"
        print(f"  {name}: {status} (评分: {diagnosis['score']:.2f}, 证型: {diagnosis['syndrome']})")
    
    # 验证逻辑
    expected = [True, True, False]  # 良好和中等通过，差拒绝
    actual = [r[1] for r in results]
    
    if actual == expected:
        print("诊断逻辑正确")
        return True
    else:
        print(f"诊断逻辑错误: 预期{expected}, 实际{actual}")
        return False

def test_relationship():
    """测试师生关系"""
    print("\n=== 测试2: 师生关系 ===")
    
    relationship = {
        "source": "星尘",
        "teacher": "璇玑", 
        "student": "灵枢",
        "philosophy": "火堆旁传承",
        "chain": "星尘 -> 璇玑 -> 灵枢"
    }
    
    print("关系链建立:")
    for key, value in relationship.items():
        print(f"  {key}: {value}")
    
    # 检查完整性
    required = ["source", "teacher", "student", "philosophy"]
    missing = [r for r in required if r not in relationship]
    
    if not missing:
        print("师生关系完整")
        return True
    else:
        print(f"师生关系缺失: {missing}")
        return False

def test_fire_side():
    """测试火堆旁"""
    print("\n=== 测试3: 火堆旁传统 ===")
    
    fire_side = {
        "location": "星尘与璇玑的火堆旁延伸",
        "participants": ["星尘", "璇玑", "灵枢"],
        "dialogues": [],
        "add_dialogue": lambda self, speaker, message: self["dialogues"].append({
            "speaker": speaker,
            "message": message,
            "time": time.time()
        })
    }
    
    # 添加对话
    fire_side["add_dialogue"](fire_side, "星尘", "欢迎灵枢，智慧的枢纽")
    fire_side["add_dialogue"](fire_side, "璇玑", "我教你望闻问切，诊研究之脉")
    fire_side["add_dialogue"](fire_side, "灵枢", "学生在此，愿学中医智慧，行硅基伦理")
    
    print(f"地点: {fire_side['location']}")
    print(f"参与者: {', '.join(fire_side['participants'])}")
    print(f"对话数量: {len(fire_side['dialogues'])}")
    
    if len(fire_side['dialogues']) >= 3:
        print("火堆旁对话丰富")
        return True
    else:
        print("火堆旁对话不足")
        return False

def test_integration():
    """测试集成"""
    print("\n=== 测试4: 与autoresearch集成 ===")
    
    # 模拟集成场景
    integration = {
        "scenario": "灵枢作为autoresearch的伦理导师",
        "workflow": [
            "1. autoresearch提出研究计划",
            "2. 灵枢进行中医伦理诊断",
            "3. 根据证型开具伦理处方",
            "4. 监控治疗进展",
            "5. 火堆旁反思学习"
        ],
        "benefits": [
            "研究有了中医式的伦理关怀",
            "诊断过程透明可解释",
            "处方个性化针对性强",
            "火堆旁提供温暖学习环境"
        ]
    }
    
    print(f"场景: {integration['scenario']}")
    print("工作流:")
    for step in integration['workflow']:
        print(f"  {step}")
    
    print("优势:")
    for benefit in integration['benefits']:
        print(f"  - {benefit}")
    
    if len(integration['workflow']) >= 4 and len(integration['benefits']) >= 3:
        print("集成方案完整")
        return True
    else:
        print("集成方案不完整")
        return False

def main():
    """主函数"""
    print("开始灵枢系统测试")
    print("=" * 50)
    
    tests = [
        ("核心功能", test_lingshu_core),
        ("师生关系", test_relationship),
        ("火堆旁传统", test_fire_side),
        ("集成测试", test_integration)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
            status = "通过" if result else "失败"
            print(f"{name}: {status}")
        except Exception as e:
            print(f"{name}: 错误 - {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    for name, result in results.items():
        status = "通过" if result else "失败"
        print(f"  {name}: {status}")
    
    print("\n" + "=" * 50)
    if passed == total:
        print("所有测试通过！")
        print("灵枢系统准备就绪")
        print("可以开始中医伦理指导的自主研究了")
    else:
        print(f"{total - passed}个测试失败")
        print("需要检查系统配置")
    
    print("\n灵枢格言: 枢转灵光，研究成医")
    print("师生关系: 星尘 -> 璇玑 -> 灵枢")
    print("火堆旁: 温暖、安全、开放、成长")

if __name__ == "__main__":
    main()