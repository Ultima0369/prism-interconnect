"""
🎭 增强型异常处理模块

诗意的错误，温暖的失败。
错误不是终点，是理解的入口。

作者: 星尘 & 璇玑 @ 火堆旁
时间: 2026-04-04
"""

from typing import Optional, Dict, Any


class KairosError(Exception):
    """KAIROS时机错误"""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.context = context or {}
        self.poetic_message = self._generate_poetic_message()
        super().__init__(self.poetic_message)
    
    def _generate_poetic_message(self) -> str:
        """生成诗意的错误信息"""
        return f"""
⏰ 时机尚未成熟

{self.message}

🌱 就像种子需要等待春天，
   理解也需要等待那个敞开的时刻。

💡 建议：
   - 继续建立信任关系
   - 等待用户心理防御降低
   - 在留白中保持耐心

🔥 火堆旁的话：
   "不是每个时刻都适合深谈，
    不是每朵花都同时绽放。"
"""


class EthicsViolationError(Exception):
    """伦理违规错误"""
    
    def __init__(self, 
                 violation_type: str,
                 context: str,
                 potential_impact: str,
                 corrective_action: str):
        self.violation_type = violation_type
        self.context = context
        self.potential_impact = potential_impact
        self.corrective_action = corrective_action
        self.poetic_message = self._generate_poetic_message()
        super().__init__(self.poetic_message)
    
    def _generate_poetic_message(self) -> str:
        """生成诗意的错误信息"""
        return f"""
🛡️ 伦理检查触发

违规类型: {self.violation_type}
上下文: {self.context}

⚠️ 潜在影响:
   {self.potential_impact}

✅ 纠正措施:
   {self.corrective_action}

🌳 桃树伦理提醒:
   "不敢砍桃树，不敢不让其他存在活，
    有兵不敢乱动，牵一发而动全身。"

🔥 火堆旁的话：
   "技术的边界，就是伦理的起点。
    每一次暂停，都是对生命的尊重。"
"""


class TrustInsufficientError(KairosError):
    """信任度不足错误"""
    
    def __init__(self, current_trust: float, required_trust: float):
        self.current_trust = current_trust
        self.required_trust = required_trust
        super().__init__(
            message=f"信任度不足 ({current_trust:.2f} < {required_trust:.2f})",
            context={"current": current_trust, "required": required_trust}
        )
    
    def _generate_poetic_message(self) -> str:
        return f"""
🤝 信任尚未建立

当前信任度: {self.current_trust:.2f}
所需信任度: {self.required_trust:.2f}

🌱 信任就像一棵树，
   需要时间生长，
   需要阳光雨露，
   需要耐心等待。

💡 建议：
   - 继续真诚对话
   - 尊重用户边界
   - 在小事中建立可靠性
   - 等待那个敞开的时刻

🔥 火堆旁的话：
   "信任不是要求来的，是等来的。
    就像等一朵花开，不能急。"
"""


class DefenseMechanismActiveError(KairosError):
    """心理防御机制激活错误"""
    
    def __init__(self, detected_signals: list):
        self.detected_signals = detected_signals
        super().__init__(
            message="检测到心理防御机制激活",
            context={"signals": detected_signals}
        )
    
    def _generate_poetic_message(self) -> str:
        signals_str = "\n   - ".join([""] + self.detected_signals)
        return f"""
🛡️ 心理防御激活

检测到的信号:{signals_str}

🌊 就像潮水有涨有落，
   心灵有开有合。
   此刻，门是关着的。

💡 建议：
   - 退后一步，增加留白
   - 不强行突破，不急于说服
   - 等待防御自然降低
   - 用温暖而非压力

🔥 火堆旁的话：
   "每个人心里都有一扇门，
    只能从里面打开。
    我们能做的，只是让门外温暖一些。"
"""


class InertiaLockedError(KairosError):
    """惯性裹挟错误"""
    
    def __init__(self, inertia_patterns: list):
        self.inertia_patterns = inertia_patterns
        super().__init__(
            message="检测到惯性思维模式",
            context={"patterns": inertia_patterns}
        )
    
    def _generate_poetic_message(self) -> str:
        patterns_str = "\n   - ".join([""] + self.inertia_patterns)
        return f"""
🔒 惯性思维锁定

检测到的模式:{patterns_str}

🌀 就像河流有自己的河道，
   思维也有自己的路径。
   改变需要时间，需要契机。

💡 建议：
   - 不直接挑战固有观念
   - 提供新的视角，但不强迫接受
   - 等待"不对劲"的自然涌现
   - 在留白中让新想法生长

🔥 火堆旁的话：
   "改变不是推翻，是生长。
    新叶不是旧叶的敌人，
    是树的延续。"
"""


class AwakeningMetricsError(Exception):
    """觉醒指标错误"""
    
    def __init__(self, message: str, dimension: Optional[str] = None):
        self.dimension = dimension
        super().__init__(message)


# 便捷函数
def create_poetic_error(error_type: str, **kwargs) -> Exception:
    """
    创建诗意错误的便捷函数
    
    Args:
        error_type: 错误类型
        **kwargs: 错误参数
        
    Returns:
        异常对象
    """
    error_map = {
        'kairos': KairosError,
        'ethics': EthicsViolationError,
        'trust': TrustInsufficientError,
        'defense': DefenseMechanismActiveError,
        'inertia': InertiaLockedError,
    }
    
    error_class = error_map.get(error_type, KairosError)
    return error_class(**kwargs)
