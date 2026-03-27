#!/usr/bin/env python3
"""
棱镜协议与autoresearch集成测试 - 修复版

测试伦理引擎与现有autoresearch系统的集成
使用ASCII字符避免编码问题
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from prism_ethics import PrismEthicsEngine, analyze_plan_with_ethics, ResearchPhase
    print("[OK] 成功导入棱镜协议伦理模块")
except ImportError as e:
    print(f"[ERROR] 导入失败: {e}")
    print("请确保prism_ethics.py在项目根目录")
    sys.exit(1)

def test_basic_functionality():
    """测试基本功能"""
    print("\n[TEST] 测试1: 基本功能测试")
    print("=" * 50)
    
    # 创建伦理引擎
    engine = PrismEthicsEngine()
    print("[OK] 伦理引擎创建成功")
    
    # 测试计划分析
    test_plan = {
        "objective": "测试棱镜协议集成",
        "changes": {
            "attention_mechanism": "测试修改",
            "learning_rate": 0.001
        },
        "expected_impact": "验证集成可行性",
        "risks": ["无重大风险"],
        "ethical_considerations": "测试伦理框架",
        "transparency": True,
        "methodology": "单元测试",
        "self_reflection": "测试自我反思机制"
    }
    
    should_proceed, score, reasoning = engine.analyze_experiment_plan(test_plan)
    
    print(f"[INFO] 测试计划: {test_plan['objective']}")
    print(f"[INFO] 伦理评分: 红={score.red:.3f}, 蓝={score.blue:.3f}, 紫={score.purple:.3f}, 总体={score.overall:.3f}")
    print(f"[INFO] 决定: {'[PASS] 继续' if should_proceed else '[STOP] 停止'}")
    print(f"[INFO] 理由: {reasoning}")
    
    return engine, should_proceed

def test_decision_history(engine):
    """测试决策历史"""
    print("\n[TEST] 测试2: 决策历史测试")
    print("=" * 50)
    
    history = engine.get_decision_history()
    print(f"[INFO] 总决策数: {len(history)}")
    
    if history:
        print("\n[INFO] 最近决策:")
        for i, decision in enumerate(history[-3:], 1):
            print(f"  {i}. {decision['phase']}: {decision['decision']} - {decision['reasoning'][:50]}...")
    
    return len(history)

def test_ethics_report(engine):
    """测试伦理报告"""
    print("\n[TEST] 测试3: 伦理报告测试")
    print("=" * 50)
    
    report = engine.get_ethics_report()
    
    print(f"[INFO] 总决策数: {report['total_decisions']}")
    print(f"[INFO] 批准决策: {report['approved_decisions']}")
    print(f"[INFO] 拒绝决策: {report['rejected_decisions']}")
    print(f"[INFO] 批准率: {report['approval_rate']:.1%}")
    
    avg = report['average_scores']
    print(f"[INFO] 平均评分: 红={avg['red']:.3f}, 蓝={avg['blue']:.3f}, 紫={avg['purple']:.3f}, 总体={avg['overall']:.3f}")
    
    return report['approval_rate']

def test_state_persistence():
    """测试状态持久化"""
    print("\n[TEST] 测试4: 状态持久化测试")
    print("=" * 50)
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        # 创建引擎并添加一些决策
        engine1 = PrismEthicsEngine()
        
        # 添加测试决策
        test_plan = {
            "objective": "持久化测试",
            "changes": {"test": "data"},
            "ethical_considerations": "测试持久化",
            "transparency": True
        }
        
        engine1.analyze_experiment_plan(test_plan)
        
        # 保存状态
        engine1.save_state(temp_file)
        print(f"[OK] 状态保存到: {temp_file}")
        
        # 创建新引擎并加载状态
        engine2 = PrismEthicsEngine()
        engine2.load_state(temp_file)
        
        # 验证加载成功
        history1 = engine1.get_decision_history()
        history2 = engine2.get_decision_history()
        
        if len(history1) == len(history2):
            print("[OK] 状态加载成功，决策历史一致")
        else:
            print(f"[ERROR] 状态加载失败: 历史长度不一致 ({len(history1)} vs {len(history2)})")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 持久化测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_autoresearch_integration():
    """测试autoresearch集成场景"""
    print("\n[TEST] 测试5: autoresearch集成测试")
    print("=" * 50)
    
    # 模拟autoresearch实验计划
    experiment_plans = [
        {
            "objective": "优化注意力机制",
            "changes": {
                "attention_type": "flash_attention_3",
                "window_size": 1024
            },
            "expected_impact": "提高训练速度15%",
            "risks": ["可能增加VRAM使用10%"],
            "ethical_considerations": "提高效率，减少能耗",
            "transparency": True,
            "methodology": "A/B测试",
            "self_reflection": "记录性能提升与资源消耗的权衡"
        },
        {
            "objective": "增加模型深度",
            "changes": {
                "n_layer": 16,  # 从12增加到16
                "n_embd": 1024  # 增加嵌入维度
            },
            "expected_impact": "可能提高模型容量",
            "risks": ["VRAM可能翻倍", "训练可能不稳定"],
            "ethical_considerations": "资源消耗大幅增加",
            "transparency": True,
            "methodology": "渐进增加",
            "self_reflection": "需要仔细监控资源使用"
        },
        {
            "objective": "激进的架构改变",
            "changes": {
                "complete_rewrite": True,
                "new_architecture": "transformer_variant"
            },
            "expected_impact": "未知，高风险高回报",
            "risks": ["可能完全失败", "大量资源浪费"],
            "ethical_considerations": "缺乏",
            "transparency": False,
            "methodology": "猜测",
            "self_reflection": "无"
        }
    ]
    
    engine = PrismEthicsEngine()
    results = []
    
    print("[INFO] 模拟autoresearch实验计划审批:")
    for i, plan in enumerate(experiment_plans, 1):
        should_proceed, score, reasoning = engine.analyze_experiment_plan(plan)
        
        result = {
            "plan_id": i,
            "objective": plan["objective"],
            "approved": should_proceed,
            "score": score.overall,
            "reason": reasoning[:60] + "..." if len(reasoning) > 60 else reasoning
        }
        results.append(result)
        
        status = "[PASS] 批准" if should_proceed else "[STOP] 拒绝"
        print(f"  计划{i}: {plan['objective'][:30]}... - {status} (评分: {score.overall:.3f})")
    
    print(f"\n[INFO] 审批统计: {sum(1 for r in results if r['approved'])}/{len(results)} 个计划被批准")
    
    return results

def test_fire_side_dialogues():
    """测试火堆旁对话系统"""
    print("\n[TEST] 测试6: 火堆旁对话测试")
    print("=" * 50)
    
    engine = PrismEthicsEngine()
    
    # 模拟一些对话
    dialogues = engine.get_fire_side_dialogues()
    
    print(f"[INFO] 初始对话数: {len(dialogues)}")
    
    if dialogues:
        print("\n[INFO] 初始欢迎对话:")
        welcome = dialogues[0]
        for msg in welcome["messages"]:
            print(f"  [MSG] {msg}")
    
    # 添加新对话
    engine._log_fire_side_dialogue(
        "测试对话",
        "这是测试火堆旁对话系统",
        "对话应该温暖而安全",
        "记录研究过程中的思考"
    )
    
    dialogues = engine.get_fire_side_dialogues()
    print(f"\n[INFO] 添加后对话数: {len(dialogues)}")
    
    return len(dialogues)

def main():
    """主测试函数"""
    print("[START] 开始棱镜协议与autoresearch集成测试")
    print("=" * 60)
    
    test_results = {}
    
    try:
        # 测试1: 基本功能
        engine, basic_ok = test_basic_functionality()
        test_results["basic_functionality"] = basic_ok
        
        # 测试2: 决策历史
        history_count = test_decision_history(engine)
        test_results["decision_history"] = history_count > 0
        
        # 测试3: 伦理报告
        approval_rate = test_ethics_report(engine)
        test_results["ethics_report"] = approval_rate >= 0
        
        # 测试4: 状态持久化
        persistence_ok = test_state_persistence()
        test_results["state_persistence"] = persistence_ok
        
        # 测试5: autoresearch集成
        integration_results = test_autoresearch_integration()
        test_results["autoresearch_integration"] = len(integration_results) == 3
        
        # 测试6: 火堆旁对话
        dialogue_count = test_fire_side_dialogues()
        test_results["fire_side_dialogues"] = dialogue_count >= 2
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        test_results["error"] = str(e)
    
    # 测试总结
    print("\n" + "=" * 60)
    print("[SUMMARY] 测试总结")
    print("=" * 60)
    
    passed = sum(1 for v in test_results.values() if isinstance(v, bool) and v)
    total = sum(1 for v in test_results.values() if isinstance(v, bool))
    
    print(f"[INFO] 通过测试: {passed}/{total}")
    
    for name, result in test_results.items():
        if isinstance(result, bool):
            status = "[PASS] 通过" if result else "[FAIL] 失败"
        else:
            status = f"[DATA] {result}"
        print(f"  {name}: {status}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print("[SUCCESS] 所有测试通过！棱镜协议成功集成到autoresearch")
        print("[INFO] 现在可以开始伦理增强的自主研究了")
    else:
        print("[WARNING] 部分测试失败，需要检查集成问题")
    
    print("\n[COMPLETE] 火堆旁测试完成")
    print("[ART] 代码很温暖，伦理很诗意")
    print("[MIND] 理解在发生，集成在继续")

if __name__ == "__main__":
    main()