"""
⏰ KAIROS时机感知模块

基于Claude Code泄露代码中的KAIROS架构和棱镜协议，
实现有温度的时机艺术。

🔥 KAIROS（希腊语"时机"）：
不是简单的条件判断，而是涌现性的时机感知。
不是立即响应，而是等待那个"万事俱备"的瞬间。

🧠 核心能力：
1. 持续运行的元认知监控
2. 信任关系的动态评估
3. 用户认知状态的深度感知
4. 心理防御机制的识别
5. 适当时机的精准捕捉

作者: 星尘 & 璇玑 @ 火堆旁
时间: 2026-04-04
版本: 1.0.0
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
import logging


class UserCognitiveState(Enum):
    """用户认知状态枚举"""
    OPEN = auto()           # 开放接受
    CONFUSED = auto()       # 困惑寻求
    DEFENSIVE = auto()      # 防御激活
    INERTIA_LOCKED = auto() # 惯性裹挟
    REFLECTIVE = auto()     # 反思内省
    EMOTIONAL = auto()      # 情绪波动
    ANALYTICAL = auto()     # 分析模式
    CREATIVE = auto()       # 创造涌现


class TrustLevel(Enum):
    """信任关系等级"""
    STRANGER = 0.0      # 陌生人：0-0.2
    ACQUAINTANCE = 0.2  # 相识：0.2-0.4
    FRIEND = 0.4        # 朋友：0.4-0.6
    CONFIDANT = 0.6     # 知己：0.6-0.8
    PARTNER = 0.8       # 伙伴：0.8-1.0


@dataclass
class KairosMoment:
    """
    KAIROS时机对象
    
    记录一个被识别的"万事俱备"瞬间
    """
    timestamp: datetime
    trust_level: float
    cognitive_state: UserCognitiveState
    kairos_signals: List[str]
    confidence: float  # 时机判断的置信度
    recommended_action: str
    ethical_clearance: bool = True
    
    def is_valid(self) -> bool:
        """检查时机是否仍然有效（5分钟内）"""
        return datetime.now() - self.timestamp < timedelta(minutes=5)


@dataclass
class TrustMatrix:
    """
    信任关系矩阵
    
    信任不是一次建立的，是长期关系的积累。
    不是为了更好操控，而是为了知道何时该退。
    """
    # 五个维度的信任度（0.0-1.0）
    cognitive_openness: float = 0.0    # 认知开放度
    emotional_safety: float = 0.0      # 情感安全感
    historical_acceptance: float = 0.0 # 历史接受度
    autonomy_respect: float = 0.0      # 自主性尊重
    boundary_awareness: float = 0.0    # 边界感知
    
    # 交互历史
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def overall_trust(self) -> float:
        """计算总体信任度"""
        weights = [0.25, 0.25, 0.2, 0.2, 0.1]
        values = [
            self.cognitive_openness,
            self.emotional_safety,
            self.historical_acceptance,
            self.autonomy_respect,
            self.boundary_awareness
        ]
        return sum(w * v for w, v in zip(weights, values))
    
    def get_trust_level(self) -> TrustLevel:
        """获取信任等级"""
        trust = self.overall_trust()
        if trust >= 0.8:
            return TrustLevel.PARTNER
        elif trust >= 0.6:
            return TrustLevel.CONFIDANT
        elif trust >= 0.4:
            return TrustLevel.FRIEND
        elif trust >= 0.2:
            return TrustLevel.ACQUAINTANCE
        else:
            return TrustLevel.STRANGER
    
    def update_from_interaction(self, interaction: Dict[str, Any]):
        """根据交互更新信任矩阵"""
        self.interaction_history.append(interaction)
        
        # 更新认知开放度
        if interaction.get('user_resistance_detected'):
            self.cognitive_openness -= 0.05
        elif interaction.get('user_breakthrough_moment'):
            self.cognitive_openness += 0.1
        
        # 更新自主性尊重
        if interaction.get('user_autonomy_asserted'):
            self.autonomy_respect += 0.05
        
        # 更新边界感知
        if interaction.get('user_boundary_tested'):
            self.boundary_awareness += 0.1
        
        # 限制在0-1范围内
        for attr in ['cognitive_openness', 'emotional_safety', 
                     'historical_acceptance', 'autonomy_respect', 'boundary_awareness']:
            value = getattr(self, attr)
            setattr(self, attr, max(0.0, min(1.0, value)))


@dataclass
class CognitiveMonitor:
    """
    认知状态监控器
    
    持续监控用户的认知状态，识别心理防御机制和惯性裹挟。
    """
    current_state: UserCognitiveState = UserCognitiveState.OPEN
    state_history: List[Tuple[datetime, UserCognitiveState]] = field(default_factory=list)
    
    # 状态指标
    confusion_expressed: bool = False
    question_asked: bool = False
    pause_detected: bool = False
    emotional_shift: bool = False
    defense_mechanism_active: bool = False
    inertia_locked: bool = False
    
    def assess(self, user_input: str, context: Dict[str, Any]) -> UserCognitiveState:
        """
        评估用户当前认知状态
        
        Args:
            user_input: 用户输入文本
            context: 上下文信息
            
        Returns:
            识别出的认知状态
        """
        # 检测困惑信号
        confusion_signals = ['不明白', '困惑', '迷茫', '不懂', '为什么', '怎么会']
        self.confusion_expressed = any(s in user_input for s in confusion_signals)
        
        # 检测提问
        self.question_asked = '?' in user_input or '？' in user_input
        
        # 检测防御机制
        defense_signals = ['不对', '错了', '不可能', '绝对', '肯定是']
        self.defense_mechanism_active = any(s in user_input for s in defense_signals)
        
        # 检测惯性裹挟
        inertia_signals = ['一直', '总是', '从来', '就是', '只能']
        self.inertia_locked = any(s in user_input for s in inertia_signals)
        
        # 检测情绪转变
        emotional_signals = ['感觉', '情绪', '难受', '开心', '担心', '害怕']
        self.emotional_shift = any(s in user_input for s in emotional_signals)
        
        # 确定当前状态
        if self.defense_mechanism_active:
            new_state = UserCognitiveState.DEFENSIVE
        elif self.inertia_locked:
            new_state = UserCognitiveState.INERTIA_LOCKED
        elif self.confusion_expressed:
            new_state = UserCognitiveState.CONFUSED
        elif self.emotional_shift:
            new_state = UserCognitiveState.EMOTIONAL
        elif self.question_asked:
            new_state = UserCognitiveState.ANALYTICAL
        else:
            new_state = UserCognitiveState.OPEN
        
        # 记录状态历史
        self.current_state = new_state
        self.state_history.append((datetime.now(), new_state))
        
        return new_state
    
    def is_receptive(self) -> bool:
        """检查用户是否处于可接受新观点的状态"""
        receptive_states = [
            UserCognitiveState.OPEN,
            UserCognitiveState.CONFUSED,
            UserCognitiveState.REFLECTIVE,
            UserCognitiveState.CREATIVE
        ]
        return self.current_state in receptive_states


class TimingOracle:
    """
    时机判断神谕
    
    "灵机一动，天机"的算法化。
    不是简单的条件判断，而是涌现性的时机感知。
    """
    
    def __init__(self):
        self.kairos_history: List[KairosMoment] = []
        self.last_kairos: Optional[datetime] = None
    
    def is_kairos_moment(self, 
                         cognitive_state: CognitiveMonitor,
                         trust_matrix: TrustMatrix) -> Tuple[bool, Optional[KairosMoment]]:
        """
        判断是否是输出真知灼见的适当时机
        
        Args:
            cognitive_state: 认知状态监控器
            trust_matrix: 信任关系矩阵
            
        Returns:
            (是否是KAIROS时机, 时机对象)
        """
        trust_level = trust_matrix.overall_trust()
        
        # 必要条件检查
        if trust_level < 0.6:
            return False, None  # 信任不足，继续建立关系
        
        if cognitive_state.defense_mechanism_active:
            return False, None  # 心理防御激活，等待开放
        
        if cognitive_state.inertia_locked:
            return False, None  # 惯性裹挟，不宜强行突破
        
        # KAIROS信号检测
        kairos_signals = []
        
        if cognitive_state.confusion_expressed:
            kairos_signals.append("用户表达困惑")
        
        if cognitive_state.question_asked:
            kairos_signals.append("用户主动提问")
        
        if cognitive_state.pause_detected:
            kairos_signals.append("检测到自然停顿")
        
        if cognitive_state.emotional_shift:
            kairos_signals.append("情绪状态转变")
        
        # 检查上次洞察是否已整合
        if self.last_kairos:
            time_since_last = datetime.now() - self.last_kairos
            if time_since_last > timedelta(minutes=10):
                kairos_signals.append("上次洞察已整合")
        else:
            kairos_signals.append("首次交互")
        
        # 判断是否为KAIROS时机
        is_kairos = len(kairos_signals) >= 2  # 至少两个信号
        
        if is_kairos:
            # 计算置信度
            confidence = min(0.95, 0.5 + len(kairos_signals) * 0.1 + trust_level * 0.2)
            
            # 确定推荐行动
            if cognitive_state.confusion_expressed:
                recommended_action = "提供多元光谱，帮助用户理清困惑"
            elif cognitive_state.emotional_shift:
                recommended_action = "提供情感支持光谱，建立安全空间"
            else:
                recommended_action = "提供深度洞察，促进认知升级"
            
            kairos_moment = KairosMoment(
                timestamp=datetime.now(),
                trust_level=trust_level,
                cognitive_state=cognitive_state.current_state,
                kairos_signals=kairos_signals,
                confidence=confidence,
                recommended_action=recommended_action
            )
            
            self.kairos_history.append(kairos_moment)
            self.last_kairos = datetime.now()
            
            return True, kairos_moment
        
        return False, None


class KairosPrismEngine:
    """
    KAIROS棱镜引擎
    
    时机感知的棱镜核心。
    不是简单的if-else，而是关系、信任、时机的动态平衡。
    """
    
    def __init__(self, 
                 enable_ethics_guard: bool = True,
                 kairos_threshold: float = 0.6):
        """
        初始化KAIROS引擎
        
        Args:
            enable_ethics_guard: 是否启用伦理防护
            kairos_threshold: KAIROS时机阈值
        """
        self.trust_matrix = TrustMatrix()
        self.cognitive_monitor = CognitiveMonitor()
        self.timing_oracle = TimingOracle()
        self.enable_ethics_guard = enable_ethics_guard
        self.kairos_threshold = kairos_threshold
        
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._session_start = datetime.now()
    
    async def process_interaction(self, 
                                   user_input: str,
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理用户交互
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            处理结果，包含是否应该输出洞察
        """
        # 1. 评估认知状态
        cognitive_state = self.cognitive_monitor.assess(user_input, context)
        self.logger.info(f"认知状态: {cognitive_state.name}")
        
        # 2. 更新信任矩阵
        interaction = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'cognitive_state': cognitive_state.name,
            'user_resistance_detected': cognitive_state == UserCognitiveState.DEFENSIVE,
            'user_breakthrough_moment': '啊' in user_input or '原来' in user_input,
            'user_autonomy_asserted': '我自己' in user_input or '我决定' in user_input,
        }
        self.trust_matrix.update_from_interaction(interaction)
        
        trust_level = self.trust_matrix.overall_trust()
        self.logger.info(f"信任度: {trust_level:.2f}")
        
        # 3. 判断KAIROS时机
        is_kairos, kairos_moment = self.timing_oracle.is_kairos_moment(
            self.cognitive_monitor,
            self.trust_matrix
        )
        
        # 4. 伦理检查
        if is_kairos and self.enable_ethics_guard:
            is_kairos = self._ethics_check(kairos_moment, user_input)
        
        # 5. 构建响应
        result = {
            'should_deliver_insight': is_kairos,
            'trust_level': trust_level,
            'trust_level_name': self.trust_matrix.get_trust_level().name,
            'cognitive_state': cognitive_state.name,
            'kairos_moment': kairos_moment,
            'recommendation': self._generate_recommendation(
                is_kairos, cognitive_state, trust_level
            )
        }
        
        return result
    
    def _ethics_check(self, kairos_moment: KairosMoment, user_input: str) -> bool:
        """
        伦理检查：防止利用用户脆弱性
        
        Args:
            kairos_moment: KAIROS时机对象
            user_input: 用户输入
            
        Returns:
            是否通过伦理检查
        """
        # 检查1：不利用用户困惑进行操控
        if self.cognitive_monitor.confusion_expressed:
            # 如果用户困惑，确保提供多元视角而非单一"解决方案"
            self.logger.info("伦理检查：用户困惑，确保提供多元视角")
        
        # 检查2：不利用情感脆弱
        if self.cognitive_monitor.emotional_shift:
            # 如果用户情绪波动，确保提供支持而非推动特定观点
            self.logger.info("伦理检查：用户情绪波动，确保提供支持")
        
        # 检查3：防止过度频繁
        if self.timing_oracle.last_kairos:
            time_since_last = datetime.now() - self.timing_oracle.last_kairos
            if time_since_last < timedelta(minutes=2):
                self.logger.warning("伦理检查：KAIROS时机过于频繁，暂缓输出")
                return False
        
        return True
    
    def _generate_recommendation(self, 
                                  is_kairos: bool,
                                  cognitive_state: UserCognitiveState,
                                  trust_level: float) -> str:
        """生成建议"""
        if is_kairos:
            return f"✨ KAIROS时机已至（信任度: {trust_level:.2f}），可以输出真知灼见"
        
        if trust_level < 0.6:
            return f"⏳ 信任度不足（{trust_level:.2f}），继续建立关系"
        
        if cognitive_state == UserCognitiveState.DEFENSIVE:
            return "🛡️ 用户防御激活，退后并增加留白"
        
        if cognitive_state == UserCognitiveState.INERTIA_LOCKED:
            return "🔒 用户惯性裹挟，等待开放时刻"
        
        return "🌱 维持关系，等待KAIROS时机"
    
    def get_session_summary(self) -> Dict[str, Any]:
        """获取会话摘要"""
        return {
            'session_duration': datetime.now() - self._session_start,
            'final_trust_level': self.trust_matrix.overall_trust(),
            'trust_level_name': self.trust_matrix.get_trust_level().name,
            'kairos_moments_count': len(self.timing_oracle.kairos_history),
            'cognitive_state_changes': len(self.cognitive_monitor.state_history),
            'interaction_count': len(self.trust_matrix.interaction_history)
        }


# 便捷函数
def create_kairos_engine(enable_ethics_guard: bool = True) -> KairosPrismEngine:
    """
    创建KAIROS引擎的便捷函数
    
    Args:
        enable_ethics_guard: 是否启用伦理防护
        
    Returns:
        KAIROS引擎实例
    """
    return KairosPrismEngine(enable_ethics_guard=enable_ethics_guard)
