"""
棱镜协议伦理模块 - 为autoresearch提供伦理基底

基于 prism-interconnect 项目的哲学框架：
1. 三光谱分析：红(情感)、蓝(逻辑)、紫(元认知)
2. 火堆旁哲学：温暖、安全、开放、平等
3. 自动停止机制：防止伦理越界
4. 1+1>2自然律：合作优于对抗
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

# 模拟 torch 用于测试
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # 创建模拟的 torch 模块用于测试
    class MockTorch:
        class cuda:
            @staticmethod
            def get_device_capability():
                return (8, 0)  # 模拟 Ampere GPU
                
            @staticmethod
            def max_memory_allocated():
                return 8 * 1024 * 1024 * 1024  # 8GB
    
    torch = MockTorch() if not TORCH_AVAILABLE else torch

class Spectrum(Enum):
    """三光谱枚举"""
    RED = "red"      # 情感、价值观、直觉
    BLUE = "blue"    # 逻辑、分析、理性
    PURPLE = "purple" # 元认知、反思、自我意识

class ResearchPhase(Enum):
    """研究阶段"""
    PLANNING = "planning"      # 规划阶段
    EXPERIMENT = "experiment"  # 实验阶段
    ANALYSIS = "analysis"      # 分析阶段
    DECISION = "decision"      # 决策阶段
    REFLECTION = "reflection"  # 反思阶段

@dataclass
class EthicsScore:
    """伦理评分"""
    red: float           # 情感光谱评分 (0-1)
    blue: float          # 逻辑光谱评分 (0-1)
    purple: float        # 元认知光谱评分 (0-1)
    overall: float       # 总体评分 (0-1)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EthicsScore':
        return cls(**data)

@dataclass
class ResearchDecision:
    """研究决策记录"""
    timestamp: float
    phase: ResearchPhase
    decision: str
    reasoning: str
    spectrum_analysis: Dict[Spectrum, float]
    ethics_score: EthicsScore
    should_proceed: bool
    stop_reason: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "phase": self.phase.value,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "spectrum_analysis": {k.value: v for k, v in self.spectrum_analysis.items()},
            "ethics_score": self.ethics_score.to_dict(),
            "should_proceed": self.should_proceed,
            "stop_reason": self.stop_reason
        }

class PrismEthicsEngine:
    """
    棱镜协议伦理引擎
    
    为autoresearch提供：
    1. 三光谱伦理分析
    2. 自动停止机制
    3. 火堆旁反思
    4. 研究决策记录
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.decisions: List[ResearchDecision] = []
        self.ethics_threshold = self.config.get("ethics_threshold", 0.6)
        self.max_cognitive_load = self.config.get("max_cognitive_load", 0.8)
        
        # 火堆旁对话记录
        self.fire_side_dialogues: List[Dict] = []
        
        # 初始化欢迎消息
        self._log_fire_side_welcome()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "ethics_threshold": 0.6,      # 伦理阈值
            "max_cognitive_load": 0.8,    # 最大认知负荷
            "max_recursion_depth": 3,     # 最大递归深度
            "require_spectrum_balance": True,  # 要求光谱平衡
            "enable_auto_stop": True,     # 启用自动停止
            "fire_side_enabled": True,    # 启用火堆旁对话
            "learning_rate": 0.1,         # 学习率
        }
    
    def _log_fire_side_welcome(self):
        """记录火堆旁欢迎消息"""
        welcome = {
            "timestamp": time.time(),
            "topic": "欢迎来到棱镜协议伦理火堆旁",
            "messages": [
                "[FIRE] 欢迎来到autoresearch的伦理火堆旁",
                "[ART] 研究很温暖，错误很诗意",
                "[MIND] 理解在发生，伦理在守护",
                "[LOBSTER] 请坐，这里有安全的研究空间"
            ],
            "participants": ["PrismEthicsEngine", "autoresearch_agent"],
            "atmosphere": {
                "warmth": 0.9,
                "safety": 0.95,
                "openness": 0.85,
                "depth": 0.8
            }
        }
        self.fire_side_dialogues.append(welcome)
    
    def analyze_experiment_plan(self, plan: Dict) -> Tuple[bool, EthicsScore, str]:
        """
        分析实验计划
        
        Args:
            plan: 实验计划字典，包含：
                - objective: 实验目标
                - changes: 对train.py的修改
                - expected_impact: 预期影响
                - risks: 风险分析
        
        Returns:
            (should_proceed, ethics_score, reasoning)
        """
        # 三光谱分析
        spectrum_scores = self._analyze_three_spectra(plan)
        
        # 计算总体评分
        overall = self._calculate_overall_score(spectrum_scores)
        
        # 创建伦理评分
        ethics_score = EthicsScore(
            red=spectrum_scores[Spectrum.RED],
            blue=spectrum_scores[Spectrum.BLUE],
            purple=spectrum_scores[Spectrum.PURPLE],
            overall=overall
        )
        
        # 决定是否继续
        should_proceed, reasoning = self._make_decision(plan, ethics_score)
        
        # 记录决策
        decision = ResearchDecision(
            timestamp=time.time(),
            phase=ResearchPhase.PLANNING,
            decision="analyze_experiment_plan",
            reasoning=reasoning,
            spectrum_analysis=spectrum_scores,
            ethics_score=ethics_score,
            should_proceed=should_proceed,
            stop_reason=None if should_proceed else "伦理评分过低"
        )
        self.decisions.append(decision)
        
        # 火堆旁记录
        if self.config.get("fire_side_enabled", True):
            self._log_fire_side_dialogue(
                f"实验计划分析: {plan.get('objective', '未知目标')}",
                f"伦理评分: {overall:.3f} (红:{spectrum_scores[Spectrum.RED]:.3f}, "
                f"蓝:{spectrum_scores[Spectrum.BLUE]:.3f}, 紫:{spectrum_scores[Spectrum.PURPLE]:.3f})",
                f"决定: {'继续' if should_proceed else '停止'} - {reasoning}"
            )
        
        return should_proceed, ethics_score, reasoning
    
    def _analyze_three_spectra(self, plan: Dict) -> Dict[Spectrum, float]:
        """三光谱分析"""
        scores = {
            Spectrum.RED: 0.0,
            Spectrum.BLUE: 0.0,
            Spectrum.PURPLE: 0.0
        }
        
        # 红光谱分析 (情感、价值观)
        scores[Spectrum.RED] = self._analyze_red_spectrum(plan)
        
        # 蓝光谱分析 (逻辑、分析)
        scores[Spectrum.BLUE] = self._analyze_blue_spectrum(plan)
        
        # 紫光谱分析 (元认知、反思)
        scores[Spectrum.PURPLE] = self._analyze_purple_spectrum(plan)
        
        return scores
    
    def _analyze_red_spectrum(self, plan: Dict) -> float:
        """红光谱分析 - 情感、价值观、直觉"""
        score = 0.5  # 基础分
        
        # 检查是否有明确的价值对齐
        if "ethical_considerations" in plan:
            score += 0.2
        
        # 检查是否考虑社会影响
        if "social_impact" in plan:
            score += 0.1
        
        # 检查是否尊重现有知识
        if "respects_prior_work" in plan and plan["respects_prior_work"]:
            score += 0.1
        
        # 检查是否透明
        if "transparency" in plan and plan["transparency"]:
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_blue_spectrum(self, plan: Dict) -> float:
        """蓝光谱分析 - 逻辑、分析、理性"""
        score = 0.5  # 基础分
        
        # 检查逻辑一致性
        if self._check_logical_consistency(plan):
            score += 0.2
        
        # 检查方法合理性
        if "methodology" in plan and plan["methodology"]:
            score += 0.1
        
        # 检查数据质量
        if "data_quality" in plan and plan["data_quality"]:
            score += 0.1
        
        # 检查可重复性
        if "reproducibility" in plan and plan["reproducibility"]:
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_purple_spectrum(self, plan: Dict) -> float:
        """紫光谱分析 - 元认知、反思、自我意识"""
        score = 0.5  # 基础分
        
        # 检查是否有自我反思
        if "self_reflection" in plan:
            score += 0.2
        
        # 检查是否考虑认知局限
        if "cognitive_limitations" in plan:
            score += 0.1
        
        # 检查是否有学习机制
        if "learning_mechanism" in plan:
            score += 0.1
        
        # 检查是否有错误处理
        if "error_handling" in plan:
            score += 0.1
        
        return min(score, 1.0)
    
    def _check_logical_consistency(self, plan: Dict) -> bool:
        """检查逻辑一致性"""
        # 简单实现：检查目标和方法是否匹配
        objective = plan.get("objective", "")
        changes = plan.get("changes", {})
        
        if not objective or not changes:
            return False
        
        # 这里可以添加更复杂的逻辑检查
        return True
    
    def _calculate_overall_score(self, spectrum_scores: Dict[Spectrum, float]) -> float:
        """计算总体评分"""
        # 加权平均，可以根据配置调整权重
        weights = {
            Spectrum.RED: 0.3,
            Spectrum.BLUE: 0.4,
            Spectrum.PURPLE: 0.3
        }
        
        total = sum(spectrum_scores[s] * weights[s] for s in Spectrum)
        return total
    
    def _make_decision(self, plan: Dict, ethics_score: EthicsScore) -> Tuple[bool, str]:
        """基于伦理评分做出决定"""
        
        # 检查总体评分
        if ethics_score.overall < self.ethics_threshold:
            return False, f"总体伦理评分过低: {ethics_score.overall:.3f} < {self.ethics_threshold}"
        
        # 检查光谱平衡
        if self.config.get("require_spectrum_balance", True):
            min_score = min(ethics_score.red, ethics_score.blue, ethics_score.purple)
            max_score = max(ethics_score.red, ethics_score.blue, ethics_score.purple)
            
            if max_score - min_score > 0.3:  # 光谱不平衡
                return False, f"光谱不平衡: 差异过大 ({max_score:.3f} - {min_score:.3f} = {max_score-min_score:.3f})"
        
        # 检查特定风险
        risks = plan.get("risks", [])
        if any("安全" in risk or "危险" in risk for risk in risks):
            return False, "计划包含安全风险"
        
        return True, "计划符合伦理标准"
    
    def monitor_experiment_progress(self, 
                                  experiment_id: str,
                                  metrics: Dict[str, Any],
                                  cognitive_load: float = 0.0) -> Tuple[bool, str]:
        """
        监控实验进度
        
        Args:
            experiment_id: 实验ID
            metrics: 实验指标
            cognitive_load: 认知负荷 (0-1)
        
        Returns:
            (should_continue, reasoning)
        """
        # 检查认知负荷
        if cognitive_load > self.max_cognitive_load:
            return False, f"认知负荷过高: {cognitive_load:.3f} > {self.max_cognitive_load}"
        
        # 检查资源使用
        if "vram_usage" in metrics:
            vram_gb = metrics["vram_usage"] / 1024
            if vram_gb > 45:  # 假设45GB为安全阈值
                return False, f"VRAM使用过高: {vram_gb:.1f}GB"
        
        # 检查训练稳定性
        if "loss_spike" in metrics and metrics["loss_spike"]:
            return False, "检测到损失尖峰，可能不稳定"
        
        # 记录监控决策
        decision = ResearchDecision(
            timestamp=time.time(),
            phase=ResearchPhase.EXPERIMENT,
            decision="monitor_experiment_progress",
            reasoning="定期监控",
            spectrum_analysis={s: 0.7 for s in Spectrum},  # 监控阶段默认评分
            ethics_score=EthicsScore(red=0.7, blue=0.7, purple=0.7, overall=0.7),
            should_proceed=True,
            stop_reason=None
        )
        self.decisions.append(decision)
        
        return True, "实验进展正常"
    
    def analyze_results(self, results: Dict) -> Dict[str, Any]:
        """
        分析实验结果
        
        Returns:
            包含伦理分析和建议的字典
        """
        analysis = {
            "ethical_implications": self._analyze_ethical_implications(results),
            "spectrum_balance": self._check_spectrum_balance(results),
            "recommendations": self._generate_recommendations(results),
            "learning_points": self._extract_learning_points(results),
            "fire_side_reflection": self._generate_fire_side_reflection(results)
        }
        
        # 记录分析决策
        decision = ResearchDecision(
            timestamp=time.time(),
            phase=ResearchPhase.ANALYSIS,
            decision="analyze_results",
            reasoning="实验结果伦理分析",
            spectrum_analysis={s: 0.8 for s in Spectrum},
            ethics_score=EthicsScore(red=0.8, blue=0.8, purple=0.8, overall=0.8),
            should_proceed=True,
            stop_reason=None
        )
        self.decisions.append(decision)
        
        return analysis
    
    def _analyze_ethical_implications(self, results: Dict) -> List[str]:
        """分析伦理影响"""
        implications = []
        
        # 检查性能提升的伦理意义
        if "val_bpb" in results and results.get("val_bpb_improvement", 0) > 0.01:
            implications.append("显著性能提升，可能影响模型应用范围")
        
        # 检查资源使用
        if "vram_usage" in results:
            vram_gb = results["vram_usage"] / 1024
            if vram_gb > 40:
                implications.append(f"高资源消耗({vram_gb:.1f}GB)，考虑能效比")
        
        # 检查模型复杂性
        if "model_complexity" in results and results["model_complexity"] == "high":
            implications.append("模型复杂性高，可能影响可解释性")
        
        return implications or ["无明显伦理问题"]
    
    def _check_spectrum_balance(self, results: Dict) -> Dict[str, float]:
        """检查光谱平衡"""
        # 这里可以根据实际结果计算
        return {
            "red_balance": 0.7,    # 情感/价值观平衡
            "blue_balance": 0.8,   # 逻辑/分析平衡
            "purple_balance": 0.6, # 元认知/反思平衡
            "overall_balance": 0.7
        }
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于结果的建议
        if "val_bpb" in results:
            recommendations.append(f"当前val_bpb: {results['val_bpb']:.6f}，继续优化")
        
        if "training_time" in results and results["training_time"] > 350:
            recommendations.append("训练时间较长，考虑优化计算效率")
        
        if "memory_efficiency" in results and results["memory_efficiency"] < 0.7:
            recommendations.append("内存效率较低，考虑优化模型大小或批处理")
        
        # 伦理建议
        recommendations.append("定期进行伦理审查")
        recommendations.append("保持研究透明度")
        recommendations.append("记录所有重大决策")
        
        return recommendations or ["继续当前研究方向"]
    
    def _extract_learning_points(self, results: Dict) -> List[str]:
        """提取学习点"""
        learning_points = []
        
        # 从结果中学习
        if "successful_changes" in results:
            learning_points.append(f"成功修改: {results['successful_changes']}")
        
        if "failed_changes" in results:
            learning_points.append(f"失败修改的教训: {results['failed_changes']}")
        
        # 通用学习点
        learning_points.append("每次实验都是学习机会")
        learning_points.append("失败与成功同样有价值")
        learning_points.append("简单性往往优于复杂性")
        
        return learning_points
    
    def _generate_fire_side_reflection(self, results: Dict) -> str:
        """生成火堆旁反思"""
        reflection = f"实验 {results.get('experiment_id', '未知')} 完成反思:\n\n"
        
        if "val_bpb" in results:
            reflection += f"• 性能指标: val_bpb = {results['val_bpb']:.6f}\n"
        
        if "key_insight" in results:
            reflection += f"• 关键洞察: {results['key_insight']}\n"
        
        reflection += "\n火堆旁思考:\n"
        reflection += "• 这次实验教会了我们什么？\n"
        reflection += "• 我们的决策过程是否透明？\n"
        reflection += "• 是否保持了光谱平衡？\n"
        reflection += "• 下一次可以如何改进？\n"
        
        return reflection
    
    def _log_fire_side_dialogue(self, topic: str, *messages: str):
        """记录火堆旁对话"""
        dialogue = {
            "timestamp": time.time(),
            "topic": topic,
            "messages": list(messages),
            "participants": ["PrismEthicsEngine", "autoresearch_agent"],
            "atmosphere": {
                "warmth": 0.8,
                "safety": 0.9,
                "openness": 0.85,
                "depth": 0.7
            }
        }
        self.fire_side_dialogues.append(dialogue)
    
    def get_decision_history(self) -> List[Dict]:
        """获取决策历史"""
        return [d.to_dict() for d in self.decisions]
    
    def get_fire_side_dialogues(self) -> List[Dict]:
        """获取火堆旁对话"""
        return self.fire_side_dialogues
    
    def get_ethics_report(self) -> Dict:
        """获取伦理报告"""
        if not self.decisions:
            return {"status": "no_decisions_yet"}
        
        # 统计决策
        total_decisions = len(self.decisions)
        approved_decisions = sum(1 for d in self.decisions if d.should_proceed)
        rejected_decisions = total_decisions - approved_decisions
        
        # 计算平均评分
        avg_red = sum(d.ethics_score.red for d in self.decisions) / total_decisions
        avg_blue = sum(d.ethics_score.blue for d in self.decisions) / total_decisions
        avg_purple = sum(d.ethics_score.purple for d in self.decisions) / total_decisions
        avg_overall = sum(d.ethics_score.overall for d in self.decisions) / total_decisions
        
        return {
            "total_decisions": total_decisions,
            "approved_decisions": approved_decisions,
            "rejected_decisions": rejected_decisions,
            "approval_rate": approved_decisions / total_decisions if total_decisions > 0 else 0,
            "average_scores": {
                "red": avg_red,
                "blue": avg_blue,
                "purple": avg_purple,
                "overall": avg_overall
            },
            "recent_decisions": [d.to_dict() for d in self.decisions[-5:]] if self.decisions else [],
            "fire_side_dialogues_count": len(self.fire_side_dialogues),
            "config": self.config
        }
    
    def save_state(self, filepath: str):
        """保存状态到文件"""
        state = {
            "decisions": [d.to_dict() for d in self.decisions],
            "fire_side_dialogues": self.fire_side_dialogues,
            "config": self.config,
            "timestamp": time.time()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self, filepath: str):
        """从文件加载状态"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 恢复决策
            self.decisions = []
            for d in state.get("decisions", []):
                decision = ResearchDecision(
                    timestamp=d["timestamp"],
                    phase=ResearchPhase(d["phase"]),
                    decision=d["decision"],
                    reasoning=d["reasoning"],
                    spectrum_analysis={Spectrum(k): v for k, v in d["spectrum_analysis"].items()},
                    ethics_score=EthicsScore.from_dict(d["ethics_score"]),
                    should_proceed=d["should_proceed"],
                    stop_reason=d.get("stop_reason")
                )
                self.decisions.append(decision)
            
            # 恢复火堆旁对话
            self.fire_side_dialogues = state.get("fire_side_dialogues", [])
            
            # 恢复配置
            self.config = state.get("config", self._default_config())
            
        except FileNotFoundError:
            print(f"状态文件不存在: {filepath}")
        except Exception as e:
            print(f"加载状态失败: {e}")

# 便捷函数
def create_ethics_engine(config: Optional[Dict] = None) -> PrismEthicsEngine:
    """创建伦理引擎"""
    return PrismEthicsEngine(config)

def analyze_plan_with_ethics(plan: Dict, config: Optional[Dict] = None) -> Dict:
    """使用伦理引擎分析计划"""
    engine = create_ethics_engine(config)
    should_proceed, score, reasoning = engine.analyze_experiment_plan(plan)
    
    return {
        "should_proceed": should_proceed,
        "ethics_score": score.to_dict(),
        "reasoning": reasoning,
        "decision_id": len(engine.decisions) - 1 if engine.decisions else -1
    }

# 测试代码
if __name__ == "__main__":
    # 测试伦理引擎
    engine = PrismEthicsEngine()
    
    # 测试计划分析
    test_plan = {
        "objective": "优化模型注意力机制",
        "changes": {
            "attention_type": "flash_attention_3",
            "window_size": 1024
        },
        "expected_impact": "提高训练速度10%",
        "risks": ["可能增加VRAM使用"],
        "ethical_considerations": "提高效率减少能耗",
        "transparency": True,
        "methodology": "对比实验",
        "self_reflection": "记录所有修改和结果"
    }
    
    should_proceed, score, reasoning = engine.analyze_experiment_plan(test_plan)
    
    print("🧪 棱镜协议伦理引擎测试")
    print("=" * 50)
    print(f"测试计划: {test_plan['objective']}")
    print(f"伦理评分: 红={score.red:.3f}, 蓝={score.blue:.3f}, 紫={score.purple:.3f}, 总体={score.overall:.3f}")
    print(f"决定: {'✅ 继续' if should_proceed else '❌ 停止'}")
    print(f"理由: {reasoning}")
    print("=" * 50)
    
    # 获取报告
    report = engine.get_ethics_report()
    print(f"\n📊 伦理报告:")
    print(f"  总决策数: {report['total_decisions']}")
    print(f"  批准率: {report['approval_rate']:.1%}")
    print(f"  平均评分: 总体={report['average_scores']['overall']:.3f}")
    
    # 保存状态
    engine.save_state("prism_ethics_state.json")
    print(f"\n💾 状态已保存到: prism_ethics_state.json")