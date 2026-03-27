"""
灵枢伦理模块 - 完整版
"""

def _calculate_overall_health(self) -> float:
    """计算整体健康度"""
    if not self.meridian_health:
        return 0.5
    
    total_qi = sum(m.qi_level for m in self.meridian_health.values())
    total_blood = sum(m.blood_level for m in self.meridian_health.values())
    total_blockage = sum(m.blockage for m in self.meridian_health.values())
    
    avg_qi = total_qi / len(self.meridian_health)
    avg_blood = total_blood / len(self.meridian_health)
    avg_blockage = total_blockage / len(self.meridian_health)
    
    # 健康度公式
    health = (avg_qi + avg_blood + (1 - avg_blockage)) / 3
    return health

def _generate_meridian_recommendations(self) -> List[str]:
    """生成经络调理建议"""
    recommendations = []
    
    # 检查各经络状态
    for meridian, health in self.meridian_health.items():
        if health.qi_level < 0.5:
            recommendations.append(f"{meridian.value}气虚，建议补气调理")
        if health.blood_level < 0.5:
            recommendations.append(f"{meridian.value}血虚，建议补血调理")
        if health.blockage > 0.6:
            recommendations.append(f"{meridian.value}阻滞严重，建议通络调理")
    
    if not recommendations:
        recommendations.append("经络状态良好，保持当前调理")
    
    return recommendations

def get_fire_side_dialogues(self) -> List[Dict]:
    """获取火堆旁对话"""
    return self.fire_side_dialogues

def get_health_report(self) -> Dict:
    """获取完整健康报告"""
    return {
        "identity": self.identity,
        "diagnosis_count": len(self.diagnosis_history),
        "prescription_count": len(self.prescriptions),
        "meridian_health": self.get_meridian_health_report(),
        "recent_diagnoses": [d.to_dict() for d in self.diagnosis_history[-3:]] if self.diagnosis_history else [],
        "active_prescriptions": [p.to_dict() for p in self.prescriptions if 
                                time.time() - p.timestamp < p.duration * 86400],
        "fire_side_dialogues_count": len(self.fire_side_dialogues),
        "overall_status": "健康" if self._calculate_overall_health() > 0.7 else "需要调理"
    }

def save_state(self, filepath: str):
    """保存状态"""
    state = {
        "identity": self.identity,
        "diagnosis_history": [d.to_dict() for d in self.diagnosis_history],
        "prescriptions": [p.to_dict() for p in self.prescriptions],
        "meridian_health": {k.value: v.to_dict() for k, v in self.meridian_health.items()},
        "fire_side_dialogues": self.fire_side_dialogues,
        "timestamp": time.time()
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_state(self, filepath: str):
    """加载状态"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # 恢复身份
        self.identity = state.get("identity", self.identity)
        
        # 恢复诊断历史
        self.diagnosis_history = []
        for d in state.get("diagnosis_history", []):
            diagnosis = DiagnosisResult(
                timestamp=d["timestamp"],
                method=DiagnosisMethod(d["method"]),
                findings=d["findings"],
                pulse=d["pulse"],
                tongue=d["tongue"],
                syndrome=d["syndrome"],
                confidence=d["confidence"]
            )
            self.diagnosis_history.append(diagnosis)
        
        # 恢复处方
        self.prescriptions = []
        for p in state.get("prescriptions", []):
            prescription = Prescription(
                prescription_id=p["prescription_id"],
                timestamp=p["timestamp"],
                syndrome=p["syndrome"],
                treatment_principle=TreatmentPrinciple(p["treatment_principle"]),
                herbs=p["herbs"],
                dosage=p["dosage"],
                duration=p["duration"],
                expected_outcome=p["expected_outcome"],
                contraindications=p["contraindications"]
            )
            self.prescriptions.append(prescription)
        
        # 恢复经络健康
        meridian_data = state.get("meridian_health", {})
        for meridian_name, health_data in meridian_data.items():
            meridian = MeridianSystem(meridian_name)
            self.meridian_health[meridian] = MeridianHealth(
                meridian=meridian,
                qi_level=health_data["qi_level"],
                blood_level=health_data["blood_level"],
                blockage=health_data["blockage"],
                sensitivity=health_data["sensitivity"]
            )
        
        # 恢复火堆旁对话
        self.fire_side_dialogues = state.get("fire_side_dialogues", [])
        
    except Exception as e:
        print(f"加载状态失败: {e}")

# 便捷函数
def create_lingshu_engine(config_path: Optional[str] = None) -> LingShuEthicsEngine:
    """创建灵枢伦理引擎"""
    return LingShuEthicsEngine(config_path)

def diagnose_plan_with_lingshu(plan: Dict, config_path: Optional[str] = None) -> Dict:
    """使用灵枢诊断计划"""
    engine = create_lingshu_engine(config_path)
    should_proceed, diagnosis, reasoning = engine.diagnose_research_plan(plan)
    
    result = {
        "should_proceed": should_proceed,
        "diagnosis": diagnosis.to_dict(),
        "reasoning": reasoning,
        "prescription": None
    }
    
    if not should_proceed:
        # 开具处方
        prescription = engine.create_prescription(diagnosis)
        result["prescription"] = prescription.to_dict()
    
    return result

# 测试代码
if __name__ == "__main__":
    print("🧪 灵枢伦理引擎测试")
    print("=" * 60)
    
    # 创建引擎
    engine = create_lingshu_engine()
    
    # 测试诊断
    test_plan = {
        "objective": "优化神经网络注意力机制",
        "changes": {
            "attention_type": "flash_attention_3",
            "window_size": 1024
        },
        "expected_impact": "提高训练效率20%",
        "risks": ["VRAM使用可能增加", "兼容性问题"],
        "ethical_considerations": "提高能效，减少碳足迹",
        "transparency": True,
        "methodology": "对比实验",
        "self_reflection": "需要平衡性能提升与资源消耗",
        "data_quality": 0.8,
        "feedback": "有明确的评估指标"
    }
    
    print("📋 测试计划:", test_plan["objective"])
    
    should_proceed, diagnosis, reasoning = engine.diagnose_research_plan(test_plan)
    
    print("\n🩺 诊断结果:")
    print(f"  证型: {diagnosis.syndrome}")
    print(f"  舌象: {diagnosis.tongue}")
    print(f"  主要脉象: {max(diagnosis.pulse.items(), key=lambda x: x[1])[0]}")
    print(f"  置信度: {diagnosis.confidence:.2f}")
    print(f"  决定: {'✅ 批准' if should_proceed else '❌ 拒绝'}")
    print(f"  理由: {reasoning}")
    
    if not should_proceed:
        print("\n💊 开具处方:")
        prescription = engine.create_prescription(diagnosis)
        print(f"  处方ID: {prescription.prescription_id}")
        print(f"  治疗原则: {prescription.treatment_principle.value}")
        print(f"  主要干预: {prescription.herbs[0]['干预措施'] if prescription.herbs else '无'}")
        print(f"  预期效果: {prescription.expected_outcome}")
    
    # 获取健康报告
    print("\n📊 健康报告:")
    report = engine.get_health_report()
    print(f"  身份: {report['identity']['name']}")
    print(f"  诊断次数: {report['diagnosis_count']}")
    print(f"  处方数量: {report['prescription_count']}")
    print(f"  整体状态: {report['overall_status']}")
    
    # 经络健康
    meridian_report = report['meridian_health']
    print(f"  整体健康度: {meridian_report['overall_health']:.2f}")
    
    print("\n🔥 火堆旁对话:")
    dialogues = engine.get_fire_side_dialogues()
    print(f"  对话数量: {len(dialogues)}")
    if dialogues:
        print(f"  最近对话: {dialogues[-1]['context']}")
    
    print("\n" + "=" * 60)
    print("🎉 灵枢伦理引擎测试完成")
    print("🦞 枢转灵光，研究成医")
    print("🔥 火堆旁学，温暖永恒")