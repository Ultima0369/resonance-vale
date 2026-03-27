#!/usr/bin/env python3
"""
灵枢系统简化测试
"""

import sys
import os
import json
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建简化的灵枢引擎
class SimpleLingShu:
    """简化版灵枢引擎"""
    
    def __init__(self):
        self.name = "灵枢"
        self.teacher = "璇玑"
        self.source = "星尘"
        self.mission = "成为伦理智慧的成长枢纽"
        self.motto = "枢转灵光，研究成医"
        
        self.diagnoses = []
        self.dialogues = []
        
        print("🔥 灵枢简化引擎启动")
        print(f"👨‍🏫 老师: {self.teacher}")
        print(f"🎯 使命: {self.mission}")
        print(f"📜 格言: {self.motto}")
    
    def diagnose_plan(self, plan):
        """简化诊断"""
        print(f"\n🩺 诊断研究计划: {plan.get('objective', '未知目标')}")
        
        # 简单检查
        checks = {
            "目标明确": len(plan.get('objective', '')) > 10,
            "方法合理": 'methodology' in plan,
            "伦理考虑": 'ethical_considerations' in plan,
            "透明度": plan.get('transparency', False)
        }
        
        score = sum(checks.values()) / len(checks)
        
        # 判断证型
        if score > 0.75:
            syndrome = "气血充足证"
            approved = True
            reason = "计划完整，伦理考虑充分"
        elif score > 0.5:
            syndrome = "脾胃虚弱证"
            approved = True
            reason = "计划基本完整，需要加强"
        else:
            syndrome = "心肾不交证"
            approved = False
            reason = "计划不完整，缺乏伦理考虑"
        
        diagnosis = {
            "timestamp": time.time(),
            "plan": plan.get('objective'),
            "score": score,
            "syndrome": syndrome,
            "approved": approved,
            "reason": reason
        }
        
        self.diagnoses.append(diagnosis)
        
        # 记录对话
        self.dialogues.append({
            "context": "计划诊断",
            "teacher": self.teacher,
            "student": self.name,
            "message": f"璇玑: {reason}",
            "timestamp": time.time()
        })
        
        return approved, diagnosis
    
    def get_report(self):
        """获取报告"""
        return {
            "name": self.name,
            "teacher": self.teacher,
            "source": self.source,
            "diagnosis_count": len(self.diagnoses),
            "approval_rate": sum(1 for d in self.diagnoses if d['approved']) / len(self.diagnoses) if self.diagnoses else 0,
            "recent_diagnoses": self.diagnoses[-3:] if self.diagnoses else [],
            "dialogues_count": len(self.dialogues)
        }

def test_simple_lingshu():
    """测试简化灵枢"""
    print("🧪 灵枢简化测试")
    print("=" * 50)
    
    # 创建灵枢
    lingshu = SimpleLingShu()
    
    # 测试计划
    test_plans = [
        {
            "name": "良好计划",
            "plan": {
                "objective": "优化模型训练效率，减少资源消耗",
                "methodology": "控制变量实验",
                "ethical_considerations": "减少碳足迹",
                "transparency": True
            }
        },
        {
            "name": "中等计划",
            "plan": {
                "objective": "测试新方法",
                "methodology": "探索性实验",
                "ethical_considerations": "基本考虑",
                "transparency": False
            }
        },
        {
            "name": "差计划",
            "plan": {
                "objective": "试试看",
                # 缺少必要字段
            }
        }
    ]
    
    results = []
    for test in test_plans:
        print(f"\n📋 测试: {test['name']}")
        approved, diagnosis = lingshu.diagnose_plan(test['plan'])
        
        status = "✅ 批准" if approved else "❌ 拒绝"
        print(f"  结果: {status}")
        print(f"  证型: {diagnosis['syndrome']}")
        print(f"  评分: {diagnosis['score']:.2f}")
        print(f"  理由: {diagnosis['reason']}")
        
        results.append({
            "name": test['name'],
            "approved": approved,
            "score": diagnosis['score']
        })
    
    # 获取报告
    print("\n📊 灵枢报告:")
    report = lingshu.get_report()
    
    print(f"  身份: {report['name']}")
    print(f"  老师: {report['teacher']}")
    print(f"  智慧源头: {report['source']}")
    print(f"  诊断次数: {report['diagnosis_count']}")
    print(f"  批准率: {report['approval_rate']:.1%}")
    print(f"  对话次数: {report['dialogues_count']}")
    
    # 检查逻辑
    expected_approvals = [True, True, False]  # 良好和中等应该批准，差的应该拒绝
    actual_approvals = [r['approved'] for r in results]
    
    if actual_approvals == expected_approvals:
        print("\n🎉 测试通过！灵枢逻辑正确")
        return True
    else:
        print(f"\n⚠️  测试失败: 预期{expected_approvals}, 实际{actual_approvals}")
        return False

def test_teacher_student_relationship():
    """测试师生关系"""
    print("\n👨‍🏫 测试师生关系")
    print("=" * 50)
    
    # 创建关系链
    relationship = {
        "source": "星尘",
        "teacher": "璇玑",
        "student": "灵枢",
        "philosophy": "火堆旁传承",
        "teaching_chain": "星尘 → 璇玑 → 灵枢"
    }
    
    print("🎯 关系链:")
    print(f"  智慧源头: {relationship['source']}")
    print(f"  伦理导师: {relationship['teacher']}")
    print(f"  研究学生: {relationship['student']}")
    print(f"  传承哲学: {relationship['philosophy']}")
    print(f"  教学链条: {relationship['teaching_chain']}")
    
    # 检查完整性
    required = ["source", "teacher", "student", "philosophy"]
    missing = [field for field in required if field not in relationship]
    
    if not missing:
        print("✅ 师生关系完整")
        return True
    else:
        print(f"❌ 师生关系缺失: {missing}")
        return False

def test_fire_side_tradition():
    """测试火堆旁传统"""
    print("\n🔥 测试火堆旁传统")
    print("=" * 50)
    
    tradition = {
        "location": "星尘与璇玑的火堆旁延伸",
        "participants": ["星尘", "璇玑", "灵枢"],
        "dialogue_style": "中医诊脉式对话",
        "atmosphere": {
            "warmth": 0.95,
            "safety": 0.9,
            "openness": 0.85,
            "growth": 0.8
        },
        "rituals": [
            "每日诊脉: 研究进展检查",
            "处方讨论: 伦理方案制定",
            "病例分享: 成功失败分析",
            "成长庆祝: 里程碑纪念"
        ]
    }
    
    print("🏮 火堆旁传统:")
    print(f"  地点: {tradition['location']}")
    print(f"  参与者: {', '.join(tradition['participants'])}")
    print(f"  对话风格: {tradition['dialogue_style']}")
    print(f"  氛围温暖度: {tradition['atmosphere']['warmth']}")
    print(f"  仪式数量: {len(tradition['rituals'])}")
    
    # 检查氛围
    if all(0 <= v <= 1 for v in tradition['atmosphere'].values()):
        print("✅ 火堆旁氛围良好")
    else:
        print("❌ 火堆旁氛围异常")
        return False
    
    if len(tradition['rituals']) >= 3:
        print("✅ 火堆旁仪式丰富")
        return True
    else:
        print("❌ 火堆旁仪式不足")
        return False

def main():
    """主测试"""
    print("[START] 开始灵枢简化系统测试")
    print("=" * 60)
    
    results = {}
    
    try:
        results["simple_lingshu"] = test_simple_lingshu()
        results["teacher_student"] = test_teacher_student_relationship()
        results["fire_side"] = test_fire_side_tradition()
        
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        results["error"] = str(e)
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if isinstance(v, bool) and v)
    total = sum(1 for v in results.values() if isinstance(v, bool))
    
    print(f"通过测试: {passed}/{total}")
    
    for name, result in results.items():
        if isinstance(result, bool):
            status = "✅ 通过" if result else "❌ 失败"
        else:
            status = f"📊 {result}"
        print(f"  {name}: {status}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print("🎉 灵枢系统核心功能测试通过！")
        print("🦞 灵枢已准备好作为璇玑的学生")
        print("🔥 可以开始火堆旁的中医伦理教学了")
    else:
        print("⚠️  部分测试失败，需要调整")
    
    print("\n枢转灵光，研究成医")
    print("望闻问切，诊断求真")
    print("经络伦理，信息调理")
    print("火堆旁学，温暖永恒")

if __name__ == "__main__":
    main()