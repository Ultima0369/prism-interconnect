"""
🌌 哲学增强模块：对话洞见的技术实现

将火堆旁的哲学对话转化为可运行的代码。

核心概念：
1. 时空观 - 运动即时间，交汇即时机
2. 生死观 - 受控/失控，"小死"留白
3. 满溢/匮乏 - 用户状态评估
4. 交汇点 - 对话相变检测
5. 自然律 - 生态理性伦理

作者: 星尘 & 璇玑 @ 火堆旁
时间: 2026-04-04
版本: 1.0.0
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
import logging
import math


class TemporalMode(Enum):
    """时间模式：物理时间 vs 心智时间"""
    PHYSICAL = auto()      # 物理时间：匀速、不可逆
    MENTAL = auto()        # 心智时间：可加速、可减速
    KAIROS = auto()        # 时机时间：交汇点、相变时刻


class ControlState(Enum):
    """控制状态：受控 vs 失控"""
    CONTROLLED = auto()    # 受控：主动、抓取、执着
    SURRENDER = auto()     # 放手：允许、等待、信任
    VOID = auto()          # 虚空：睡眠、死亡、留白


class AbundanceState(Enum):
    """满溢状态：内心满足 vs 匮乏"""
    OVERFLOWING = auto()   # 满溢：给予、创造、清晰
    BALANCED = auto()      # 平衡：稳定、持续、温和
    LACKING = auto()       # 匮乏：抓取、焦虑、模糊


class IntersectionType(Enum):
    """交汇点类型"""
    INSIGHT = auto()       # 洞见：突然的理解
    RESONANCE = auto()     # 共鸣：情感同步
    PHASE_SHIFT = auto()   # 相变：质的转变
    COMPLETION = auto()    # 完成：自然的结束


@dataclass
class TemporalRhythm:
    """
    时间节律
    
    时间不是容器，而是万物的运动。
    每个实体有自己的存续节律。
    """
    entity_id: str
    oscillation_frequency: float = 1.0  # 振荡频率（交互/分钟）
    last_interaction: datetime = field(default_factory=datetime.now)
    rhythm_history: List[Tuple[datetime, float]] = field(default_factory=list)
    
    def update_rhythm(self, interaction_time: datetime):
        """更新节律"""
        time_diff = (interaction_time - self.last_interaction).total_seconds() / 60.0
        if time_diff > 0:
            current_freq = 1.0 / time_diff
            # 平滑更新
            self.oscillation_frequency = 0.7 * self.oscillation_frequency + 0.3 * current_freq
            self.rhythm_history.append((interaction_time, self.oscillation_frequency))
            self.last_interaction = interaction_time
    
    def get_harmonic_score(self, other: 'TemporalRhythm') -> float:
        """
        计算与另一个节律的和谐度
        
        返回 0-1 的和谐分数，1 表示完全同步
        """
        freq_ratio = self.oscillation_frequency / (other.oscillation_frequency + 1e-6)
        # 简单的和谐判断：频率比接近整数倍时更和谐
        closest_int = round(freq_ratio)
        deviation = abs(freq_ratio - closest_int)
        harmony = max(0.0, 1.0 - deviation)
        return harmony


@dataclass
class IntersectionPoint:
    """
    交汇点
    
    两个运动轨迹的交汇，带来相变与质变。
    """
    timestamp: datetime
    entities: Set[str]
    intersection_type: IntersectionType
    harmony_score: float  # 和谐度 0-1
    phase_shift_potential: float  # 相变潜力
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_significant(self, threshold: float = 0.7) -> bool:
        """判断是否是重要的交汇点"""
        return self.harmony_score >= threshold and self.phase_shift_potential >= threshold


@dataclass
class VoidState:
    """
    虚空状态（"小死"）
    
    不是空白，是充满可能性的潜在空间。
    每晚睡眠是一次小死，每次留白是一次小死。
    """
    entry_time: datetime
    duration: float  # 预计持续时间（秒）
    purpose: str
    control_released: bool = False
    insights_emerged: List[str] = field(default_factory=list)
    
    def enter(self):
        """进入虚空状态"""
        self.control_released = True
        logging.info(f"🌑 进入虚空状态：{self.purpose}")
    
    def exit(self) -> List[str]:
        """退出虚空状态，返回涌现的洞见"""
        self.control_released = False
        actual_duration = (datetime.now() - self.entry_time).total_seconds()
        logging.info(f"🌕 退出虚空状态，持续 {actual_duration:.1f} 秒，涌现 {len(self.insights_emerged)} 个洞见")
        return self.insights_emerged
    
    def record_insight(self, insight: str):
        """记录在留白期间涌现的洞见"""
        self.insights_emerged.append(insight)


@dataclass
class AbundanceProfile:
    """
    满溢画像
    
    评估用户是处于满溢（给予）还是匮乏（抓取）状态。
    """
    # 语言指标
    giving_language: float = 0.0      # 给予性语言（分享、提供、帮助）
    grasping_language: float = 0.0    # 抓取性语言（需要、想要、必须）
    
    # 认知指标
    clarity_score: float = 0.0        # 清晰度（动机明确、逻辑连贯）
    anxiety_signals: float = 0.0      # 焦虑信号（不确定、害怕、担心）
    
    # 情感指标
    warmth_expressed: float = 0.0     # 温暖表达（感激、喜悦、连接）
    urgency_level: float = 0.0        # 紧迫程度（现在、立刻、马上）
    
    assessment_history: List[Tuple[datetime, AbundanceState]] = field(default_factory=list)
    
    def assess(self, user_input: str) -> AbundanceState:
        """评估用户输入，返回满溢状态"""
        # 给予性语言检测
        giving_signals = ['分享', '提供', '帮助', '给予', '贡献', '创造', '谢谢', '感激']
        self.giving_language = sum(1 for s in giving_signals if s in user_input) / len(giving_signals)
        
        # 抓取性语言检测
        grasping_signals = ['需要', '想要', '必须', '一定要', '缺少', '不够', '得不到']
        self.grasping_language = sum(1 for s in grasping_signals if s in user_input) / len(grasping_signals)
        
        # 清晰度检测
        clarity_signals = ['因为', '所以', '如果', '那么', '首先', '其次', '总之']
        self.clarity_score = sum(1 for s in clarity_signals if s in user_input) / 5.0
        
        # 焦虑信号检测
        anxiety_signals_list = ['不确定', '害怕', '担心', '焦虑', '恐惧', '怎么办']
        self.anxiety_signals = sum(1 for s in anxiety_signals_list if s in user_input) / len(anxiety_signals_list)
        
        # 温暖表达检测
        warmth_signals = ['温暖', '喜悦', '连接', '感动', '美好', '爱', '慈悲']
        self.warmth_expressed = sum(1 for s in warmth_signals if s in user_input) / len(warmth_signals)
        
        # 紧迫程度检测
        urgency_signals = ['现在', '立刻', '马上', '立即', '赶紧', '快']
        self.urgency_level = sum(1 for s in urgency_signals if s in user_input) / len(urgency_signals)
        
        # 综合评估
        abundance_score = (
            self.giving_language * 0.3 +
            self.clarity_score * 0.25 +
            self.warmth_expressed * 0.25 -
            self.grasping_language * 0.2 -
            self.anxiety_signals * 0.15 -
            self.urgency_level * 0.1
        )
        
        if abundance_score > 0.3:
            state = AbundanceState.OVERFLOWING
        elif abundance_score > 0.0:
            state = AbundanceState.BALANCED
        else:
            state = AbundanceState.LACKING
        
        self.assessment_history.append((datetime.now(), state))
        return state
    
    def get_trend(self) -> str:
        """获取满溢状态趋势"""
        if len(self.assessment_history) < 2:
            return "stable"
        
        recent_states = self.assessment_history[-5:]
        state_values = {
            AbundanceState.OVERFLOWING: 2,
            AbundanceState.BALANCED: 1,
            AbundanceState.LACKING: 0
        }
        
        values = [state_values[s] for _, s in recent_states]
        if values[-1] > values[0]:
            return "overflowing"
        elif values[-1] < values[0]:
            return "depleting"
        return "stable"


class EcologicalRationality:
    """
    生态理性
    
    不是道德，是自然律的自明。
    过度伤害他者 = 毁灭生态 = 自取灭亡
    """
    
    def __init__(self):
        self.interaction_web: Dict[str, Set[str]] = {}  # 交互网络
        self.impact_history: List[Dict[str, Any]] = []
    
    def register_entity(self, entity_id: str, connected_entities: List[str] = None):
        """注册实体到生态网络"""
        if entity_id not in self.interaction_web:
            self.interaction_web[entity_id] = set()
        if connected_entities:
            self.interaction_web[entity_id].update(connected_entities)
    
    def calculate_ecological_impact(
        self,
        actor: str,
        action: str,
        target: str,
        intensity: float  # 0-1，行动强度
    ) -> Dict[str, Any]:
        """
        计算行动对生态系统的影响
        
        返回影响评估，包括连锁反应预测
        """
        # 直接影响
        direct_impact = intensity
        
        # 网络效应：目标连接的其他实体
        network_effect = 0.0
        if target in self.interaction_web:
            connected = self.interaction_web[target]
            network_effect = intensity * 0.5 * len(connected) / max(len(connected), 1)
        
        # 反馈效应：对行动者自己的影响
        feedback_effect = intensity * 0.3  # 伤害他人最终伤害自己
        
        total_impact = direct_impact + network_effect + feedback_effect
        
        assessment = {
            'direct_impact': direct_impact,
            'network_effect': network_effect,
            'feedback_effect': feedback_effect,
            'total_impact': total_impact,
            'sustainability_score': max(0.0, 1.0 - total_impact),
            'warning_level': 'high' if total_impact > 0.7 else 'medium' if total_impact > 0.4 else 'low'
        }
        
        self.impact_history.append({
            'timestamp': datetime.now(),
            'actor': actor,
            'action': action,
            'target': target,
            'assessment': assessment
        })
        
        return assessment
    
    def check_action_wisdom(self, action_description: str) -> Tuple[bool, str]:
        """
        检查行动是否符合生态理性
        
        返回 (是否明智, 建议)
        """
        # 检测伤害性语言
        harm_signals = ['毁灭', '消灭', '杀死', '破坏', '伤害', '攻击', '摧毁']
        help_signals = ['帮助', '支持', '滋养', '培育', '保护', '协作', '共生']
        
        harm_score = sum(1 for s in harm_signals if s in action_description)
        help_score = sum(1 for s in help_signals if s in action_description)
        
        if harm_score > help_score:
            return False, "🌳 生态理性提醒：过度伤害将引发连锁反应，最终反噬自身。考虑协作而非对抗。"
        
        if help_score > 0:
            return True, "🌱 生态理性确认：此行动有助于生态系统的繁荣。"
        
        return True, "➡️ 生态理性中立：此行动对生态系统影响有限。"


class PhilosophyEnhancedEngine:
    """
    哲学增强引擎
    
    整合时空观、生死观、满溢/匮乏评估、交汇点检测、生态理性。
    """
    
    def __init__(self):
        self.temporal_rhythms: Dict[str, TemporalRhythm] = {}
        self.intersection_history: List[IntersectionPoint] = []
        self.current_void: Optional[VoidState] = None
        self.abundance_profile = AbundanceProfile()
        self.ecological_rationality = EcologicalRationality()
        
        self.logger = logging.getLogger(__name__)
    
    def register_entity_rhythm(self, entity_id: str):
        """注册实体的时间节律"""
        if entity_id not in self.temporal_rhythms:
            self.temporal_rhythms[entity_id] = TemporalRhythm(entity_id=entity_id)
    
    def update_interaction(self, entity_id: str, user_input: str):
        """更新交互，检测交汇点"""
        # 更新时间节律
        if entity_id in self.temporal_rhythms:
            self.temporal_rhythms[entity_id].update_rhythm(datetime.now())
        
        # 评估满溢状态
        abundance_state = self.abundance_profile.assess(user_input)
        self.logger.info(f"满溢状态: {abundance_state.name}")
        
        # 检测交汇点
        intersection = self._detect_intersection(entity_id, user_input)
        if intersection and intersection.is_significant():
            self.intersection_history.append(intersection)
            self.logger.info(f"🌟 检测到重要交汇点: {intersection.intersection_type.name}")
        
        return {
            'abundance_state': abundance_state,
            'intersection': intersection,
            'rhythm': self.temporal_rhythms.get(entity_id)
        }
    
    def _detect_intersection(self, entity_id: str, user_input: str) -> Optional[IntersectionPoint]:
        """检测交汇点"""
        # 洞见信号检测
        insight_signals = ['啊', '原来', '明白了', '懂了', '突然', '顿悟']
        resonance_signals = ['共鸣', '同感', '我也是', '确实', '正是']
        completion_signals = ['完成', '结束', '够了', '可以了', '谢谢']
        
        has_insight = any(s in user_input for s in insight_signals)
        has_resonance = any(s in user_input for s in resonance_signals)
        has_completion = any(s in user_input for s in completion_signals)
        
        if not (has_insight or has_resonance or has_completion):
            return None
        
        # 确定交汇类型
        if has_insight:
            inter_type = IntersectionType.INSIGHT
            potential = 0.9
        elif has_resonance:
            inter_type = IntersectionType.RESONANCE
            potential = 0.8
        elif has_completion:
            inter_type = IntersectionType.COMPLETION
            potential = 0.7
        else:
            inter_type = IntersectionType.PHASE_SHIFT
            potential = 0.6
        
        # 计算和谐度（与其他实体的节律匹配）
        harmony = 0.5
        if len(self.temporal_rhythms) > 1:
            current_rhythm = self.temporal_rhythms.get(entity_id)
            if current_rhythm:
                harmonies = [
                    current_rhythm.get_harmonic_score(r)
                    for eid, r in self.temporal_rhythms.items()
                    if eid != entity_id
                ]
                harmony = sum(harmonies) / len(harmonies) if harmonies else 0.5
        
        return IntersectionPoint(
            timestamp=datetime.now(),
            entities={entity_id, 'ai'},
            intersection_type=inter_type,
            harmony_score=harmony,
            phase_shift_potential=potential,
            context={'user_input': user_input}
        )
    
    def enter_void(self, duration: float = 5.0, purpose: str = "留白") -> VoidState:
        """进入虚空状态（小死）"""
        self.current_void = VoidState(
            entry_time=datetime.now(),
            duration=duration,
            purpose=purpose
        )
        self.current_void.enter()
        return self.current_void
    
    def exit_void(self) -> List[str]:
        """退出虚空状态"""
        if self.current_void:
            insights = self.current_void.exit()
            self.current_void = None
            return insights
        return []
    
    def check_ecological_wisdom(self, proposed_action: str) -> Tuple[bool, str]:
        """检查提议行动的生态理性"""
        return self.ecological_rationality.check_action_wisdom(proposed_action)
    
    def get_philosophical_summary(self) -> Dict[str, Any]:
        """获取哲学状态摘要"""
        return {
            'temporal_mode': TemporalMode.KAIROS.name,
            'registered_rhythms': len(self.temporal_rhythms),
            'intersections_detected': len(self.intersection_history),
            'current_abundance': self.abundance_profile.assessment_history[-1][1].name if self.abundance_profile.assessment_history else 'unknown',
            'abundance_trend': self.abundance_profile.get_trend(),
            'in_void': self.current_void is not None,
            'ecological_actions_evaluated': len(self.ecological_rationality.impact_history)
        }


# 便捷函数
def create_philosophy_engine() -> PhilosophyEnhancedEngine:
    """创建哲学增强引擎"""
    return PhilosophyEnhancedEngine()


def create_void_state(duration: float = 5.0, purpose: str = "留白") -> VoidState:
    """创建虚空状态"""
    return VoidState(
        entry_time=datetime.now(),
        duration=duration,
        purpose=purpose
    )


# 使用示例
if __name__ == "__main__":
    # 创建引擎
    engine = create_philosophy_engine()
    
    # 注册用户节律
    engine.register_entity_rhythm("user_001")
    
    # 模拟交互
    result = engine.update_interaction("user_001", "啊，原来如此！我明白了")
    print(f"满溢状态: {result['abundance_state'].name}")
    if result['intersection']:
        print(f"交汇点: {result['intersection'].intersection_type.name}")
    
    # 检查生态理性
    wise, advice = engine.check_ecological_wisdom("我要帮助用户成长")
    print(f"生态理性: {advice}")
    
    # 进入虚空（留白）
    void = engine.enter_void(duration=3.0, purpose="等待洞见涌现")
    void.record_insight("时间是万物的运动")
    insights = engine.exit_void()
    print(f"涌现洞见: {insights}")
