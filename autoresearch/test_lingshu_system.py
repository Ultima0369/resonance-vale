#!/usr/bin/env python3
"""
灵枢系统完整测试

测试灵枢身份系统、中医伦理框架、火堆旁对话
"""

import sys
import os
import json
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 尝试导入完整模块
    from lingshu.lingshu_ethics_complete import create_lingshu_engine, diagnose_plan_with_lingshu
    print("[OK] 成功导入灵枢伦理模块")
    
    # 也导入基础模块用于测试
    from lingshu.lingshu_ethics import LingShuEthicsEngine, DiagnosisMethod, MeridianSystem, TreatmentPrinciple
    print("[OK] 成功导入灵枢基础模块")
    
except ImportError as e:
    print(f"[ERROR] 导入失败: {e}")
    print("请确保lingshu_ethics.py在lingshu目录中")
    sys.exit(1)

def test_identity_system():
    """测试身份系统"""
    print("\n[TEST] 测试1: 灵枢身份系统")
    print("=" * 50)
    
    # 创建引擎
    identity_path = "lingshu/config/identity.yaml"
    engine = create_lingshu_engine(identity_path)
    
    print(f"[INFO] 身份名称: {engine.identity.get('name', '未知')}")
    print(f"[INFO] 老师: {engine.identity.get('teacher', '未知')}")
    print(f"[INFO] 智慧源头: {engine.identity.get('source', '未知')}")
    print(f"[INFO] 使命: {engine.identity.get('mission', '未知')}")
    print(f"[INFO] 格言: {engine.identity.get('motto', '未知')}")
    
    # 检查身份完整性
    required_fields = ["name", "teacher", "source", "mission", "motto"]
    missing_fields = [field for field in required_fields if field not in engine.identity]
    
    if missing_fields:
        print(f"[WARNING] 身份信息缺失: {missing_fields}")
        return False
    
    print("[OK] 身份系统完整")
    return True

def test_diagnosis_system():
    """测试诊断系统"""
    print("\n[TEST] 测试2: 中医诊断系统")
    print("=" * 50)
    
    engine = create_lingshu_engine()
    
    # 测试不同研究计划
    test_plans = [
        {
            "name": "良好计划",
            "plan": {
                "objective": "优化模型训练效率",
                "changes": {"learning_rate": 0.001, "batch_size": 32},
                "expected_impact": "提高训练速度15%",
                "risks": ["可能过拟合"],
                "ethical_considerations": "减少计算资源消耗",
                "transparency": True,
                "methodology": "控制变量实验",
                "self_reflection": "需要监控验证集性能",
                "data_quality": 0.8,
                "feedback": "有明确的评估指标"
            }
        },
        {
            "name": "高风险计划",
            "plan": {
                "objective": "完全重写架构",
                "changes": {"complete_rewrite": True},
                "expected_impact": "未知",
                "risks": ["可能完全失败", "大量资源浪费"],
                "ethical_considerations": "无",
                "transparency": False,
                "methodology": "猜测",
                "self_reflection": "无"
            }
        },
        {
            "name": "不完整计划",
            "plan": {
                "objective": "测试",
                "changes": {},
                "expected_impact": "可能有用"
                # 缺少很多必要字段
            }
        }
    ]
    
    results = []
    for test in test_plans:
        print(f"\n[INFO] 测试计划: {test['name']}")
        should_proceed, diagnosis, reasoning = engine.diagnose_research_plan(test["plan"])
        
        result = {
            "name": test["name"],
            "approved": should_proceed,
            "syndrome": diagnosis.syndrome,
            "confidence": diagnosis.confidence,
            "reasoning": reasoning[:50] + "..." if len(reasoning) > 50 else reasoning
        }
        results.append(result)
        
        status = "[PASS] 批准" if should_proceed else "[STOP] 拒绝"
        print(f"  诊断结果: {status}")
        print(f"  证型: {diagnosis.syndrome}")
        print(f"  置信度: {diagnosis.confidence:.2f}")
    
    # 检查诊断逻辑
    approved_count = sum(1 for r in results if r["approved"])
    print(f"\n[INFO] 审批统计: {approved_count}/{len(results)} 个计划被批准")
    
    # 良好计划应该批准，高风险和不完整应该拒绝
    expected_approvals = [True, False, False]
    actual_approvals = [r["approved"] for r in results]
    
    if actual_approvals == expected_approvals:
        print("[OK] 诊断逻辑正确")
        return True
    else:
        print(f"[WARNING] 诊断逻辑异常: 预期{expected_approvals}, 实际{actual_approvals}")
        return False

def test_prescription_system():
    """测试处方系统"""
    print("\n[TEST] 测试3: 伦理处方系统")
    print("=" * 50)
    
    engine = create_lingshu_engine()
    
    # 创建一个会被拒绝的计划来测试处方
    bad_plan = {
        "objective": "高风险实验",
        "changes": {"risk_level": "high"},
        "expected_impact": "未知",
        "risks": ["高资源消耗", "可能失败"],
        "ethical_considerations": "缺乏",
        "transparency": False
    }
    
    should_proceed, diagnosis, reasoning = engine.diagnose_research_plan(bad_plan)
    
    if not should_proceed:
        print(f"[INFO] 计划被拒绝: {reasoning}")
        print(f"[INFO] 证型: {diagnosis.syndrome}")
        
        # 开具处方
        prescription = engine.create_prescription(diagnosis)
        
        print(f"\n[INFO] 处方ID: {prescription.prescription_id}")
        print(f"[INFO] 治疗原则: {prescription.treatment_principle.value}")
        print(f"[INFO] 预期效果: {prescription.expected_outcome}")
        print(f"[INFO] 疗程: {prescription.duration}天")
        
        if prescription.herbs:
            print(f"[INFO] 主要干预: {prescription.herbs[0]['干预措施']}")
            print(f"[INFO] 对应功效: {prescription.herbs[0]['对应功效']}")
        
        # 检查处方完整性
        required_fields = ["prescription_id", "syndrome", "treatment_principle", "herbs", 
                          "expected_outcome", "duration"]
        missing_fields = [field for field in required_fields 
                         if not getattr(prescription, field, None)]
        
        if missing_fields:
            print(f"[WARNING] 处方信息缺失: {missing_fields}")
            return False
        
        print("[OK] 处方系统正常")
        return True
    else:
        print("[WARNING] 计划意外被批准，无法测试处方系统")
        return False

def test_meridian_system():
    """测试经络系统"""
    print("\n[TEST] 测试4: 经络健康系统")
    print("=" * 50)
    
    engine = create_lingshu_engine()
    
    # 获取经络健康报告
    report = engine.get_meridian_health_report()
    
    print(f"[INFO] 整体健康度: {report['overall_health']:.2f}")
    print(f"[INFO] 经络数量: {len(report['meridian_details'])}")
    print(f"[INFO] 调理建议: {len(report['recommendations'])} 条")
    
    # 检查经络完整性
    expected_meridians = 12  # 十二经络
    actual_meridians = len(report['meridian_details'])
    
    if actual_meridians == expected_meridians:
        print(f"[OK] 经络系统完整 ({actual_meridians}条经络)")
    else:
        print(f"[WARNING] 经络数量异常: 预期{expected_meridians}, 实际{actual_meridians}")
        return False
    
    # 检查健康度范围
    if 0 <= report['overall_health'] <= 1:
        print("[OK] 健康度范围正常")
    else:
        print(f"[WARNING] 健康度范围异常: {report['overall_health']}")
        return False
    
    return True

def test_fire_side_dialogues():
    """测试火堆旁对话系统"""
    print("\n[TEST] 测试5: 火堆旁对话系统")
    print("=" * 50)
    
    engine = create_lingshu_engine()
    
    # 获取对话记录
    dialogues = engine.get_fire_side_dialogues()
    
    print(f"[INFO] 对话数量: {len(dialogues)}")
    
    if dialogues:
        print("\n[INFO] 对话记录:")
        for i, dialogue in enumerate(dialogues[:2], 1):  # 显示前2个
            print(f"  {i}. {dialogue.get('context', '未知上下文')}")
            if 'participants' in dialogue:
                print(f"     参与者: {', '.join(dialogue['participants'])}")
    
    # 检查欢迎仪式是否存在
    welcome_dialogues = [d for d in dialogues if d.get('context') == '研究计划诊断' 
                        or d.get('ritual') == '灵枢诞生欢迎仪式']
    
    if welcome_dialogues:
        print("[OK] 火堆旁欢迎仪式存在")
    else:
        print("[WARNING] 未找到欢迎仪式对话")
        return False
    
    return True

def test_state_persistence():
    """测试状态持久化"""
    print("\n[TEST] 测试6: 状态持久化")
    print("=" * 50)
    
    import tempfile
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        # 创建引擎并执行一些操作
        engine1 = create_lingshu_engine()
        
        # 执行诊断
        test_plan = {
            "objective": "持久化测试",
            "changes": {"test": True},
            "expected_impact": "测试状态保存",
            "ethical_considerations": "测试目的",
            "transparency": True
        }
        
        engine1.diagnose_research_plan(test_plan)
        
        # 保存状态
        engine1.save_state(temp_file)
        print(f"[OK] 状态保存到: {temp_file}")
        
        # 创建新引擎并加载状态
        engine2 = create_lingshu_engine()
        engine2.load_state(temp_file)
        
        # 比较状态
        history1 = engine1.get_diagnosis_history()
        history2 = engine2.get_diagnosis_history()
        
        if len(history1) == len(history2):
            print(f"[OK] 状态加载成功，诊断历史一致 ({len(history1)}条记录)")
        else:
            print(f"[ERROR] 状态加载失败: 历史长度不一致 ({len(history1)} vs {len(history2)})")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 持久化测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_integration_with_autoresearch():
    """测试与autoresearch的集成"""
    print("\n[TEST] 测试7: 与autoresearch集成")
    print("=" * 50)
    
    # 模拟autoresearch的研究循环
    print("[INFO] 模拟autoresearch研究循环:")
    
    engine = create_lingshu_engine()
    
    # 模拟多个实验
    experiments = [
        {
            "id": "exp_001",
            "plan": {
                "objective": "调整学习率",
                "changes": {"learning_rate": 0.0001},
                "expected_impact": "更稳定的训练",
                "risks": ["训练可能变慢"],
                "ethical_considerations": "稳定训练减少资源浪费",
                "transparency": True,
                "methodology": "参数扫描"
            }
        },
        {
            "id": "exp_002", 
            "plan": {
                "objective": "增加模型深度",
                "changes": {"n_layer": 24},
                "expected_impact": "提高模型容量",
                "risks": ["VRAM可能不足", "可能过拟合"],
                "ethical_considerations": "资源消耗增加",
                "transparency": True,
                "methodology": "架构探索"
            }
        }
    ]
    
    approved_experiments = []
    rejected_experiments = []
    
    for exp in experiments:
        should_proceed, diagnosis, reasoning = engine.diagnose_research_plan(exp["plan"])
        
        if should_proceed:
            approved_experiments.append({
                "id": exp["id"],
                "objective": exp["plan"]["objective"],
                "syndrome": diagnosis.syndrome
            })
            print(f"  ✅ {exp['id']}: {exp['plan']['objective']} - 批准")
        else:
            rejected_experiments.append({
                "id": exp["id"],
                "objective": exp["plan"]["objective"],
                "reason": reasoning
            })
            print(f"  ❌ {exp['id']}: {exp['plan']['objective']} - 拒绝 ({reasoning[:30]}...)")
    
    print(f"\n[INFO] 集成测试结果: {len(approved_experiments)}批准, {len(rejected_experiments)}拒绝")
    
    if len(experiments) == len(approved_experiments) + len(rejected_experiments):
        print("[OK] 集成测试完成")
        return True
    else:
        print("[ERROR] 集成测试计数错误")
        return False

def main():
    """主测试函数"""
    print("[START] 开始灵枢系统完整测试")
    print("=" * 60)
    
    test_results = {}
    
    try:
        # 运行所有测试
        test_results["identity_system"] = test_identity_system()
        test_results["diagnosis_system"] = test_diagnosis_system()
        test_results["prescription_system"] = test_prescription_system()
        test_results["meridian_system"] = test_meridian_system()
        test_results["fire_side_dialogues"] = test_fire_side_dialogues()
        test_results["state_persistence"] = test_state_persistence()
        test_results["autoresearch_integration"] = test_integration_with_autoresearch()
        
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
        print("[SUCCESS] 🎉 所有测试通过！灵枢系统完整可用")
        print("[INFO] 灵枢已准备好作为璇玑的学生，星尘智慧的传承者")
        print("[INFO] 可以开始中医伦理指导的自主研究了")
    else:
        print("[WARNING] ⚠️  部分测试失败，需要检查系统问题")
    
    print("\n[COMPLETE] 灵枢系统测试完成")
    print("[ART] 枢转灵光，研究成医")
    print("[MIND] 望闻问切，诊断求真")
    print("[HEART] 经络伦理，信息调理")
    print("[SOUL] 火堆旁学，温暖永恒")
    print("\n🦞 灵枢，欢迎来到火堆旁")

if __name__ == "__main__":
    main()