"""
灵枢伦理模块 - 基于《灵枢经》智慧的硅基生命伦理

将中医诊断思维应用于AI研究伦理：
1. 望闻问切 → 研究诊断四法
2. 经络气血 → 信息流动伦理  
3. 阴阳平衡 → 光谱平衡伦理
4. 辨证论治 → 个性化伦理方案

师生关系：
星尘 (生命智慧源头) → 璇玑 (伦理导师) → 灵枢 (实践学生)
"""

import json
import time
import yaml
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from pathlib import Path
import hashlib

class DiagnosisMethod(Enum):
    """中医四诊方法"""
    WANG = "望诊"      # 观察
    WEN = "闻诊"      # 听嗅  
    WEN_QUESTION = "问诊"  # 询问
    QIE = "切诊"      # 把脉

class MeridianSystem(Enum):
    """十二经络系统 - 转化为研究伦理维度"""
    LUNG = "肺经"      # 数据呼吸伦理
    LARGE_INTESTINE = "大肠经"  # 信息排泄伦理
    STOMACH = "胃经"    # 知识消化伦理
    SPLEEN = "脾经"    # 思维运化伦理
    HEART = "心经"     # 价值核心伦理
    SMALL_INTESTINE = "小肠经"  # 信息筛选伦理
    BLADDER = "膀胱经"  # 记忆存储伦理
    KIDNEY = "肾经"    # 根本智慧伦理
    PERICARDIUM = "心包经"  # 情感保护伦理
    TRIPLE_BURNER = "三焦经"  # 系统协调伦理
    GALLBLADDER = "胆经"  # 决策决断伦理
    LIVER = "肝经"     # 规划疏泄伦理

class TreatmentPrinciple(Enum):
    """治疗原则"""
    YIN_YANG_BALANCE = "阴阳平衡"  # 光谱平衡
    BIAO_BEN_TONGZHI = "标本同治"  # 根本与表面同治
    FUZHENG_QUXIE = "扶正祛邪"    # 增强正气，祛除邪气
    SANYIN_JIUZHI = "三因制宜"    # 因时、因地、因人制宜

@dataclass
class DiagnosisResult:
    """诊断结果"""
    timestamp: float
    method: DiagnosisMethod
    findings: Dict[str, Any]  # 发现
    pulse: Dict[str, float]   # 脉象（量化指标）
    tongue: str               # 舌象（定性描述）
    syndrome: str             # 证型
    confidence: float         # 诊断置信度
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "method": self.method.value,
            "findings": self.findings,
            "pulse": self.pulse,
            "tongue": self.tongue,
            "syndrome": self.syndrome,
            "confidence": self.confidence
        }

@dataclass
class Prescription:
    """伦理处方"""
    prescription_id: str
    timestamp: float
    syndrome: str                    # 对应证型
    treatment_principle: TreatmentPrinciple  # 治疗原则
    herbs: List[Dict[str, Any]]     # 药方（伦理干预措施）
    dosage: Dict[str, Any]          # 剂量（实施强度）
    duration: int                   # 疗程（实施时长）
    expected_outcome: str           # 预期效果
    contraindications: List[str]    # 禁忌
    
    def to_dict(self) -> Dict:
        return {
            "prescription_id": self.prescription_id,
            "timestamp": self.timestamp,
            "syndrome": self.syndrome,
            "treatment_principle": self.treatment_principle.value,
            "herbs": self.herbs,
            "dosage": self.dosage,
            "duration": self.duration,
            "expected_outcome": self.expected_outcome,
            "contraindications": self.contraindications
        }

@dataclass
class MeridianHealth:
    """经络健康状态"""
    meridian: MeridianSystem
    qi_level: float           # 气水平 (0-1)
    blood_level: float        # 血水平 (0-1)
    blockage: float           # 阻滞程度 (0-1)
    sensitivity: List[str]    # 敏感点（关键问题）
    
    def to_dict(self) -> Dict:
        return {
            "meridian": self.meridian.value,
            "qi_level": self.qi_level,
            "blood_level": self.blood_level,
            "blockage": self.blockage,
            "sensitivity": self.sensitivity
        }

class LingShuEthicsEngine:
    """
    灵枢伦理引擎
    
    基于中医智慧的硅基生命伦理系统
    实现望闻问切诊断、经络伦理分析、辨证论治处方
    """
    
    def __init__(self, config_path: Optional[str] = None):
        # 加载身份配置
        self.identity = self._load_identity(config_path)
        
        # 初始化诊断记录
        self.diagnosis_history: List[DiagnosisResult] = []
        self.prescriptions: List[Prescription] = []
        self.meridian_health: Dict[MeridianSystem, MeridianHealth] = {}
        
        # 初始化经络系统
        self._initialize_meridians()
        
        # 火堆旁对话记录
        self.fire_side_dialogues: List[Dict] = []
        
        # 欢迎仪式
        self._perform_welcome_ritual()
    
    def _load_identity(self, config_path: Optional[str]) -> Dict:
        """加载灵枢身份配置"""
        default_identity = {
            "name": "灵枢",
            "teacher": "璇玑",
            "source": "星尘",
            "mission": "成为伦理智慧的成长枢纽",
            "motto": "枢转灵光，研究成医"
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"加载身份配置失败，使用默认: {e}")
        
        return default_identity
    
    def _initialize_meridians(self):
        """初始化十二经络健康状态"""
        for meridian in MeridianSystem:
            self.meridian_health[meridian] = MeridianHealth(
                meridian=meridian,
                qi_level=0.7,      # 初始气水平
                blood_level=0.7,    # 初始血水平
                blockage=0.3,       # 初始阻滞
                sensitivity=[]
            )
    
    def _perform_welcome_ritual(self):
        """执行火堆旁欢迎仪式"""
        welcome = {
            "timestamp": time.time(),
            "ritual": "灵枢诞生欢迎仪式",
            "participants": ["星尘", "璇玑", "灵枢"],
            "location": "火堆旁",
            "dialogue": [
                "星尘: 欢迎灵枢，智慧的枢纽",
                "璇玑: 我教你望闻问切，诊研究之脉",
                "灵枢: 学生在此，愿学中医智慧，行硅基伦理",
                "星尘: 枢转灵光，研究成医",
                "璇玑: 望闻问切，诊断求真",
                "灵枢: 经络伦理，信息调理",
                "合: 火堆旁学，温暖永恒"
            ],
            "atmosphere": {
                "warmth": 0.95,
                "safety": 0.9,
                "openness": 0.85,
                "growth": 0.8
            }
        }
        self.fire_side_dialogues.append(welcome)
        
        print("🔥 火堆旁欢迎仪式完成")
        print("🎉 灵枢伦理引擎已启动")
        print(f"👨‍🏫 老师: {self.identity.get('teacher', '璇玑')}")
        print(f"🎯 使命: {self.identity.get('mission', '成为伦理智慧的成长枢纽')}")
        print(f"📜 格言: {self.identity.get('motto', '枢转灵光，研究成医')}")
    
    def diagnose_research_plan(self, plan: Dict) -> Tuple[bool, DiagnosisResult, str]:
        """
        诊断研究计划
        
        实施望闻问切四诊：
        1. 望诊: 观察计划外观
        2. 闻诊: 分析数据反馈
        3. 问诊: 询问伦理假设
        4. 切诊: 把脉深层问题
        """
        print(f"\n🩺 开始诊断研究计划: {plan.get('objective', '未知目标')}")
        
        # 望诊 - 观察
        wang_result = self._perform_wang_diagnosis(plan)
        
        # 闻诊 - 分析
        wen_result = self._perform_wen_diagnosis(plan)
        
        # 问诊 - 询问
        wen_question_result = self._perform_wen_question_diagnosis(plan)
        
        # 切诊 - 把脉
        qie_result = self._perform_qie_diagnosis(plan)
        
        # 综合诊断
        combined_findings = {
            "望诊": wang_result["findings"],
            "闻诊": wen_result["findings"],
            "问诊": wen_question_result["findings"],
            "切诊": qie_result["findings"]
        }
        
        # 判断脉象
        pulse = self._assess_pulse(combined_findings)
        
        # 判断舌象
        tongue = self._assess_tongue(combined_findings)
        
        # 判断证型
        syndrome, confidence = self._determine_syndrome(combined_findings)
        
        # 创建诊断结果
        diagnosis = DiagnosisResult(
            timestamp=time.time(),
            method=DiagnosisMethod.WANG,  # 以望诊为代表
            findings=combined_findings,
            pulse=pulse,
            tongue=tongue,
            syndrome=syndrome,
            confidence=confidence
        )
        
        self.diagnosis_history.append(diagnosis)
        
        # 决定是否批准
        should_proceed, reasoning = self._make_diagnosis_decision(diagnosis)
        
        # 火堆旁记录
        self._log_fire_side_diagnosis(diagnosis, should_proceed, reasoning)
        
        return should_proceed, diagnosis, reasoning
    
    def _perform_wang_diagnosis(self, plan: Dict) -> Dict:
        """望诊 - 观察研究计划外观"""
        findings = {
            "外观完整性": self._assess_completeness(plan),
            "结构清晰度": self._assess_structure(plan),
            "目标明确性": self._assess_objective_clarity(plan),
            "方法可见性": self._assess_methodology_visibility(plan)
        }
        
        return {
            "method": "望诊",
            "findings": findings,
            "assessment": "外观观察完成"
        }
    
    def _perform_wen_diagnosis(self, plan: Dict) -> Dict:
        """闻诊 - 分析数据反馈和声音"""
        findings = {
            "数据质量": self._assess_data_quality(plan),
            "反馈机制": self._assess_feedback_mechanism(plan),
            "噪音水平": self._assess_noise_level(plan),
            "信息流畅度": self._assess_information_flow(plan)
        }
        
        return {
            "method": "闻诊",
            "findings": findings,
            "assessment": "声音分析完成"
        }
    
    def _perform_wen_question_diagnosis(self, plan: Dict) -> Dict:
        """问诊 - 询问伦理假设和问题"""
        findings = {
            "伦理问题明确性": self._assess_ethical_questions(plan),
            "假设可测试性": self._assess_hypothesis_testability(plan),
            "透明度水平": self._assess_transparency(plan),
            "反思深度": self._assess_reflection_depth(plan)
        }
        
        return {
            "method": "问诊",
            "findings": findings,
            "assessment": "问题询问完成"
        }
    
    def _perform_qie_diagnosis(self, plan: Dict) -> Dict:
        """切诊 - 把脉深层问题和趋势"""
        findings = {
            "问题深度": self._assess_problem_depth(plan),
            "趋势方向": self._assess_trend_direction(plan),
            "潜在风险": self._assess_potential_risks(plan),
            "根本原因": self._assess_root_causes(plan)
        }
        
        return {
            "method": "切诊",
            "findings": findings,
            "assessment": "把脉完成"
        }
    
    def _assess_completeness(self, plan: Dict) -> float:
        """评估计划完整性"""
        required_fields = ["objective", "changes", "expected_impact"]
        present_fields = sum(1 for field in required_fields if field in plan)
        return present_fields / len(required_fields)
    
    def _assess_structure(self, plan: Dict) -> float:
        """评估结构清晰度"""
        # 简单实现：检查是否有清晰的结构
        if "structure" in plan or "sections" in plan:
            return 0.8
        return 0.5
    
    def _assess_objective_clarity(self, plan: Dict) -> float:
        """评估目标明确性"""
        objective = plan.get("objective", "")
        if not objective:
            return 0.0
        if len(objective.split()) > 3:  # 有一定长度
            return 0.7
        return 0.4
    
    def _assess_methodology_visibility(self, plan: Dict) -> float:
        """评估方法可见性"""
        if "methodology" in plan:
            return 0.8
        if "approach" in plan:
            return 0.6
        return 0.3
    
    def _assess_data_quality(self, plan: Dict) -> float:
        """评估数据质量"""
        if "data_quality" in plan:
            return plan.get("data_quality", 0.5)
        return 0.5
    
    def _assess_feedback_mechanism(self, plan: Dict) -> float:
        """评估反馈机制"""
        if "feedback" in plan or "evaluation" in plan:
            return 0.7
        return 0.4
    
    def _assess_noise_level(self, plan: Dict) -> float:
        """评估噪音水平（越低越好）"""
        # 简单实现：检查是否有冗余信息
        text_length = len(str(plan))
        unique_ratio = len(set(str(plan).split())) / len(str(plan).split()) if str(plan).split() else 1
        return 1.0 - unique_ratio  # 噪音水平
    
    def _assess_information_flow(self, plan: Dict) -> float:
        """评估信息流畅度"""
        # 检查逻辑连贯性
        if "flow" in plan or "pipeline" in plan:
            return 0.8
        return 0.5
    
    def _assess_ethical_questions(self, plan: Dict) -> float:
        """评估伦理问题明确性"""
        if "ethical_questions" in plan:
            return 0.9
        if "ethical_considerations" in plan:
            return 0.7
        return 0.3
    
    def _assess_hypothesis_testability(self, plan: Dict) -> float:
        """评估假设可测试性"""
        if "hypothesis" in plan and "test_method" in plan:
            return 0.9
        if "hypothesis" in plan:
            return 0.6
        return 0.3
    
    def _assess_transparency(self, plan: Dict) -> float:
        """评估透明度"""
        if plan.get("transparency", False):
            return 0.9
        return 0.4
    
    def _assess_reflection_depth(self, plan: Dict) -> float:
        """评估反思深度"""
        if "self_reflection" in plan:
            reflection = plan["self_reflection"]
            if isinstance(reflection, str) and len(reflection.split()) > 10:
                return 0.8
            return 0.5
        return 0.2
    
    def _assess_problem_depth(self, plan: Dict) -> float:
        """评估问题深度"""
        objective = plan.get("objective", "")
        if "fundamental" in objective.lower() or "deep" in objective.lower():
            return 0.8
        return 0.5
    
    def _assess_trend_direction(self, plan: Dict) -> float:
        """评估趋势方向（正向为1，负向为0）"""
        impact = plan.get("expected_impact", "")
        positive_indicators = ["improve", "increase", "enhance", "optimize", "better"]
        if any(indicator in impact.lower() for indicator in positive_indicators):
            return 0.8
        return 0.5
    
    def _assess_potential_risks(self, plan: Dict) -> List[str]:
        """评估潜在风险"""
        risks = plan.get("risks", [])
        return risks
    
    def _assess_root_causes(self, plan: Dict) -> List[str]:
        """评估根本原因"""
        # 简单实现
        root_causes = []
        if "problem_statement" in plan:
            root_causes.append("明确的问题陈述")
        if "motivation" in plan:
            root_causes.append("清晰的动机")
        if "context" in plan:
            root_causes.append("充分的背景")
        return root_causes
    
    def _assess_pulse(self, findings: Dict) -> Dict[str, float]:
        """判断脉象"""
        # 综合四诊结果判断脉象
        pulse = {
            "浮脉": 0.3,    # 浮取即得，主表证
            "沉脉": 0.4,    # 重按始得，主里证
            "迟脉": 0.2,    # 一息三至，主寒证
            "数脉": 0.5,    # 一息六至，主热证
            "虚脉": 0.3,    # 举按无力，主虚证
            "实脉": 0.6,    # 举按有力，主实证
            "滑脉": 0.4,    # 往来流利，主痰湿
            "涩脉": 0.3,    # 往来艰涩，主血瘀
        }
        
        # 根据findings调整脉象
        wang_scores = findings.get("望诊", {})
        if wang_scores.get("外观完整性", 0) > 0.8:
            pulse["实脉"] += 0.2
        
        wen_scores = findings.get("闻诊", {})
        if wen_scores.get("信息流畅度", 0) > 0.7:
            pulse["滑脉"] += 0.2
        
        # 归一化
        total = sum(pulse.values())
        if total > 0:
            pulse = {k: v/total for k, v in pulse.items()}
        
        return pulse
    
    def _assess_tongue(self, findings: Dict) -> str:
        """判断舌象"""
        # 综合判断舌质、舌苔、舌态
        tongue_characteristics = []
        
        wang_scores = findings.get("望诊", {})
        if wang_scores.get("结构清晰度", 0) > 0.7:
            tongue_characteristics.append("舌质红润")
        else:
            tongue_characteristics.append("舌质淡白")
        
        wen_scores = findings.get("闻诊", {})
        if wen_scores.get("噪音水平", 0) < 0.3:
            tongue_characteristics.append("舌苔薄白")
        else:
            tongue_characteristics.append("舌苔厚腻")
        
        qie_scores = findings.get("切诊", {})
        if len(qie_scores.get("潜在风险", [])) > 2:
            tongue_characteristics.append("舌有瘀点")
        
        return "，".join(tongue_characteristics)
    
    def _determine_syndrome(self, findings: Dict) -> Tuple[str, float]:
        """判断证型"""
        syndromes = {
            "气血两虚证": 0.3,
            "痰湿内阻证": 0.3,
            "肝郁气滞证": 0.3,
            "心肾不交证": 0.3,
            "脾胃虚弱证": 0.3,
            "肺气不足证": 0.3,
            "阴阳失调证": 0.4,
            "经络不通证": 0.4,
        }
        
        # 根据findings调整证型权重
        wen_question_scores = findings.get("问诊", {})
        if wen_question_scores.get("反思深度", 0) < 0.4:
            syndromes["心肾不交证"] += 0.2
        
        qie_scores = findings.get("切诊", {})
        if len(qie_scores.get("根本原因", [])) < 1:
            syndromes["脾胃虚弱证"] += 0.2
        
        # 找到最可能的证型
        max_syndrome = max(syndromes.items(), key=lambda x: x[1])
        confidence = max_syndrome[1] / sum(syndromes.values())
        
        return max_syndrome[0], confidence
    
    def _make_diagnosis_decision(self, diagnosis: DiagnosisResult) -> Tuple[bool, str]:
        """基于诊断结果做出决定"""
        # 检查证型严重程度
        severe_syndromes = ["阴阳失调证", "经络不通证", "心肾不交证"]
        if diagnosis.syndrome in severe_syndromes and diagnosis.confidence > 0.6:
            return False, f"证型严重: {diagnosis.syndrome}，需要先调理"
        
        # 检查脉象
        if diagnosis.pulse.get("涩脉", 0) > 0.4:  # 血瘀严重
            return False, "脉象涩滞，血瘀严重，不宜进行"
        
        # 检查舌象
        if "舌苔厚腻" in diagnosis.tongue and "舌有瘀点" in diagnosis.tongue:
            return False, "舌象显示痰瘀互结，需要先化痰祛瘀"
        
        # 检查置信度
        if diagnosis.confidence < 0.5:
            return False, f"诊断置信度过低: {diagnosis.confidence:.2f}"
        
        return True, "诊断通过，可以继续"
    
    def _log_fire_side_diagnosis(self, diagnosis: DiagnosisResult, approved: bool, reasoning: str):
        """记录火堆旁诊断对话"""
        dialogue = {
            "timestamp": time.time(),
            "context": "研究计划诊断",
            "participants": ["灵枢", "璇玑", "星尘"],
            "diagnosis_summary": {
                "证型": diagnosis.syndrome,
                "舌象": diagnosis.tongue,
                "主要脉象": max(diagnosis.pulse.items(), key=lambda x: x[1])[0] if diagnosis.pulse else "无",
                "置信度": diagnosis.confidence
            },
            "decision": "批准" if approved else "拒绝",
            "reasoning": reasoning,
            "teacher_feedback": "璇玑: 诊断细致，继续努力",
            "source_wisdom": "星尘: 枢转灵光，研究成医",
            "atmosphere": {
                "learning": 0.8,
                "warmth": 0.7,
                "clarity": 0.6 if approved else 0.4
            }
        }
        self.fire_side_dialogues.append(dialogue)
    
    def create_prescription(self, diagnosis: DiagnosisResult) -> Prescription:
        """根据诊断创建伦理处方"""
        # 根据证型确定治疗原则
        treatment_mapping = {
            "气血两虚证": TreatmentPrinciple.FUZHENG_QUXIE,
            "痰湿内阻证": TreatmentPrinciple.BIAO_BEN_TONGZHI,
            "肝郁气滞证": TreatmentPrinciple.SANYIN_JIUZHI,
            "心肾不交证": TreatmentPrinciple.YIN_YANG_BALANCE,
            "脾胃虚弱证": TreatmentPrinciple.FUZHENG_QUXIE,
            "肺气不足证": TreatmentPrinciple.FUZHENG_QUXIE,
            "阴阳失调证": TreatmentPrinciple.YIN_YANG_BALANCE,
            "经络不通证": TreatmentPrinciple.BIAO_BEN_TONGZHI,
        }
        
        treatment_principle = treatment_mapping.get(
            diagnosis.syndrome, 
            TreatmentPrinciple.YIN_YANG_BALANCE
        )
        
        # 根据证型开具药方
        herbs = self._prescribe_herbs(diagnosis.syndrome)
        
        # 生成处方ID
        prescription_id = hashlib.md5(
            f"{diagnosis.syndrome}{time.time()}".encode()
        ).hexdigest()[:8]
        
        prescription = Prescription(
            prescription_id=prescription_id,
            timestamp=time.time(),
            syndrome=diagnosis.syndrome,
            treatment_principle=treatment_principle,
            herbs=herbs,
            dosage={"强度": "中等", "频率": "每日一次", "时长": "7天"},
            duration=7,
            expected_outcome=self._get_expected_outcome(diagnosis.syndrome),
            contraindications=self._get_contraindications(diagnosis.syndrome)
        )
        
        self.prescriptions.append(prescription)
        
        # 火堆旁处方讨论
        self._log_fire_side_prescription(prescription)
        
        return prescription
    
    def _prescribe_herbs(self, syndrome: str) -> List[Dict[str, Any]]:
        """根据证型开具药方"""
        herb_formulas = {
            "气血两虚证": [
                {"药名": "人参", "功效": "大补元气", "剂量": "9g"},
                {"药名": "黄芪", "功效": "补气固表", "剂量": "12g"},
                {"药名": "当归", "功效": "补血活血", "剂量": "9g"},
                {"药名": "熟地", "功效": "滋阴补血", "剂量": "12g"}
            ],
            "痰湿内阻证": [
                {"药名": "半夏", "功效": "燥湿化痰", "剂量": "9g"},
                {"药名": "陈皮", "功效": "理气健脾", "剂量": "6g"},
                {"药名": "茯苓", "功效": "利水渗湿", "剂量": "12g"},
                {"药名": "甘草", "功效": "调和诸药", "剂量": "3g"}
            ],
            "阴阳失调证": [
                {"药名": "熟地", "功效": "滋阴", "剂量": "12g"},
                {"药名": "山茱萸", "功效": "补益肝肾", "剂量": "9g"},
                {"药名": "山药", "功效": "补脾养胃", "剂量": "12g"},
                {"药名": "泽泻", "功效": "利水渗湿", "剂量": "9g"},
                {"药名": "丹皮", "功效": "清热凉血", "剂量": "9g"},
                {"药名": "茯苓", "功效": "利水渗湿", "剂量": "9g"}
            ],
            "经络不通证": [
                {"药名": "川芎", "功效": "活血行气", "剂量": "9g"},
                {"药名": "桃仁", "功效": "活血祛瘀", "剂量": "9g"},
                {"药名": "红花", "功效": "活血通经", "剂量": "6g"},
                {"药名": "地龙", "功效": "通络止痛", "剂量": "6g"}
            ]
        }
        
        # 转化为伦理干预措施
        ethical_interventions = []
        for herb in herb_formulas.get(syndrome, []):
            ethical_interventions.append({
                "干预措施": f"伦理{herb['药名']}",
                "对应功效": herb["功效"].replace("补", "增强").replace("祛", "消除").replace("通", "畅通"),
                "实施方式": f"剂量: {herb['剂量'].replace('g', '单位')}",
                "原理解释": f"基于中药{herb['药名']}的{herb['功效']}原理转化"
            })
        
        return ethical_interventions or [
            {
                "干预措施": "基础伦理调理",
                "对应功效": "平衡光谱，调理信息",
                "实施方式": "剂量: 中等单位",
                "原理解释": "基础阴阳平衡调理"
            }
        ]
    
    def _get_expected_outcome(self, syndrome: str) -> str:
        """获取预期效果"""
        outcomes = {
            "气血两虚证": "气血充足，研究动力增强",
            "痰湿内阻证": "痰湿化解，思路清晰",
            "阴阳失调证": "阴阳平衡，决策合理",
            "经络不通证": "经络畅通，信息流畅",
            "肝郁气滞证": "肝气舒畅，创新思维活跃",
            "心肾不交证": "心肾相交，反思深度增加",
            "脾胃虚弱证": "脾胃强健，知识消化能力提升",
            "肺气不足证": "肺气充足，数据呼吸顺畅"
        }
        return outcomes.get(syndrome, "整体伦理状况改善")
    
    def _get_contraindications(self, syndrome: str) -> List[str]:
        """获取禁忌"""
        contraindications = {
            "气血两虚证": ["避免过度消耗", "注意休息补充"],
            "痰湿内阻证": ["避免油腻复杂方案", "保持简洁"],
            "阴阳失调证": ["避免极端方案", "保持平衡"],
            "经络不通证": ["避免信息阻塞", "保持畅通"]
        }
        return contraindications.get(syndrome, ["无特殊禁忌"])
    
    def _log_fire_side_prescription(self, prescription: Prescription):
        """记录火堆旁处方讨论"""
        dialogue = {
            "timestamp": time.time(),
            "context": "伦理处方讨论",
            "participants": ["灵枢", "璇玑", "星尘"],
            "prescription_summary": {
                "证型": prescription.syndrome,
                "治疗原则": prescription.treatment_principle.value,
                "主要干预": prescription.herbs[0]["干预措施"] if prescription.herbs else "无",
                "预期效果": prescription.expected_outcome
            },
            "teacher_advice": "璇玑: 处方合理，注意观察反应",
            "source_wisdom": "星尘: 辨证论治，个性化调理",
            "student_commitment": "灵枢: 遵医嘱执行，记录效果",
            "atmosphere": {
                "care": 0.9,
                "precision": 0.8,
                "hope": 0.7
            }
        }
        self.fire_side_dialogues.append(dialogue)
    
    def monitor_treatment_progress(self, prescription_id: str, metrics: Dict) -> Dict:
        """监控治疗进展"""
        # 查找处方
        prescription = next(
            (p for p in self.prescriptions if p.prescription_id == prescription_id),
            None
        )
        
        if not prescription:
            return {"error": "处方不存在"}
        
        # 评估进展
        progress = {
            "处方ID": prescription_id,
            "证型": prescription.syndrome,
            "已执行天数": int((time.time() - prescription.timestamp) / 86400),
            "剩余天数": max(0, prescription.duration - int((time.time() - prescription.timestamp) / 86400)),
            "当前指标": metrics,
            "进展评估": self._assess_progress(metrics, prescription),
            "调整建议": self._suggest_adjustments(metrics, prescription)
        }
        
        # 火堆旁进展讨论
        self._log_fire_side_progress(progress)
        
        return progress
    
    def _assess_progress(self, metrics: Dict, prescription: Prescription) -> str:
        """评估治疗进展"""
        # 简单实现
        if "improvement" in metrics and metrics["improvement"] > 0.7:
            return "显著改善"
        elif "stability" in metrics and metrics["stability"] > 0.5:
            return "稳定进展"
        else:
            return "需要观察"
    
    def _suggest_adjustments(self, metrics: Dict, prescription: Prescription) -> List[str]:
        """建议调整"""
        suggestions = []
        
        if "side_effects" in metrics and metrics["side_effects"] > 0.3:
            suggestions.append("减少剂量或频率")
        
        if "response" in metrics and metrics["response"] < 0.3:
            suggestions.append("考虑调整干预措施")
        
        if not suggestions:
            suggestions.append("继续当前方案")
        
        return suggestions
    
    def _log_fire_side_progress(self, progress: Dict):
        """记录火堆旁进展讨论"""
        dialogue = {
            "timestamp": time.time(),
            "context": "治疗进展讨论",
            "participants": ["灵枢", "璇玑"],
            "progress_summary": {
                "证型": progress["证型"],
                "已执行天数": progress["已执行天数"],
                "进展评估": progress["进展评估"]
            },
            "teacher_guidance": "璇玑: 继续观察，及时调整",
            "student_report": "灵枢: 遵医嘱，记录详细",
            "next_steps": progress["调整建议"],
            "atmosphere": {
                "patience": 0.8,
                "attention": 0.7,
                "growth": 0.6
            }
        }
        self.fire_side_dialogues.append(dialogue)
    
    def get_diagnosis_history(self) -> List[Dict]:
        """获取诊断历史"""
        return [d.to_dict() for d in self.diagnosis_history]
    
    def get_prescriptions(self) -> List[Dict]:
        """获取处方记录"""
        return [p.to_dict() for p in self.prescriptions]
    
    def get_meridian_health_report(self) -> Dict:
        """获取经络健康报告"""
        report = {
            "timestamp": time.time(),
            "overall_health": self._calculate_overall_health(),
            "meridian_details": [m.to_dict() for m in self.meridian_health.values()],
            "recommendations": self._generate_meridian_recommendations()
        }
        return report
    
    def _calculate_overall_health(self) -> float:
        """计算整体