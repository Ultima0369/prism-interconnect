"""
🌟 意识觉醒指标模块

不是衡量"用户接受了多少"，而是衡量"用户觉醒了多少"。

🧠 核心指标：
1. 元认知激活：用户是否开始观察自己的思维过程
2. 视角转换能力：用户能否在光谱间自由切换
3. 内省深度：留白时间内的思考质量
4. 自主性保持：用户是否保持最终决策权

作者: 星尘 & 璇玑 @ 火堆旁
时间: 2026-04-04
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AwakeningDimension(Enum):
    """觉醒维度枚举"""
    METACOGNITION = "元认知激活"
    PERSPECTIVE_FLEXIBILITY = "视角转换能力"
    INTROSPECTION_DEPTH = "内省深度"
    AUTONOMY_PRESERVATION = "自主性保持"


@dataclass
class AwakeningIndicator:
    """觉醒指标"""
    dimension: AwakeningDimension
    description: str
    indicators: List[str]
    current_score: float = 0.0
    history: List[tuple] = field(default_factory=list)
    
    def update_score(self, new_score: float, context: str = ""):
        """更新分数"""
        self.current_score = max(0.0, min(1.0, new_score))
        self.history.append((datetime.now(), self.current_score, context))
    
    def get_trend(self) -> str:
        """获取趋势"""
        if len(self.history) < 2:
            return "stable"
        
        recent = [h[1] for h in self.history[-5:]]
        if recent[-1] > recent[0]:
            return "improving"
        elif recent[-1] < recent[0]:
            return "declining"
        return "stable"


@dataclass
class AwakeningMetrics:
    """
    意识觉醒度量系统
    
    成功的定义：
    - 不是AI有多懂用户
    - 而是用户有多懂自己
    - 用户自主性有多强
    - 用户在离开AI后是否更强大
    """
    
    # 四个核心维度
    metacognition: AwakeningIndicator = field(
        default_factory=lambda: AwakeningIndicator(
            dimension=AwakeningDimension.METACOGNITION,
            description="用户是否开始观察自己的思维过程",
            indicators=[
                "用户开始质疑自己的假设",
                "用户注意到自己的思维习惯",
                "用户表达'我以前从没这样想过'",
                "用户反思自己的认知偏差",
                "用户主动提及'我在想...'"
            ]
        )
    )
    
    perspective_flexibility: AwakeningIndicator = field(
        default_factory=lambda: AwakeningIndicator(
            dimension=AwakeningDimension.PERSPECTIVE_FLEXIBILITY,
            description="用户能否在光谱间自由切换",
            indicators=[
                "用户主动提出不同角度",
                "用户整合多个光谱形成新理解",
                "用户对单一答案表示怀疑",
                "用户比较不同视角的优劣",
                "用户在不同光谱间建立连接"
            ]
        )
    )
    
    introspection_depth: AwakeningIndicator = field(
        default_factory=lambda: AwakeningIndicator(
            dimension=AwakeningDimension.INTROSPECTION_DEPTH,
            description="留白时间内的思考质量",
            indicators=[
                "用户在留白后提出更深层次问题",
                "用户报告留白期间的洞察",
                "用户主动要求更多思考时间",
                "用户在留白后表达新的理解",
                "用户将留白体验与日常联系"
            ]
        )
    )
    
    autonomy_preservation: AwakeningIndicator = field(
        default_factory=lambda: AwakeningIndicator(
            dimension=AwakeningDimension.AUTONOMY_PRESERVATION,
            description="用户是否保持最终决策权",
            indicators=[
                "用户明确表达'我决定...'",
                "用户拒绝AI的建议并说明理由",
                "用户在AI不在场时仍能独立思考",
                "用户与AI的关系是'合作'而非'依赖'",
                "用户主动结束对话并独立行动"
            ]
        )
    )
    
    session_start: datetime = field(default_factory=datetime.now)
    
    def get_overall_awakening_score(self) -> float:
        """获取整体觉醒分数"""
        dimensions = [
            self.metacognition,
            self.perspective_flexibility,
            self.introspection_depth,
            self.autonomy_preservation
        ]
        return sum(d.current_score for d in dimensions) / len(dimensions)
    
    def get_dimension_scores(self) -> Dict[str, float]:
        """获取各维度分数"""
        return {
            "元认知激活": self.metacognition.current_score,
            "视角转换能力": self.perspective_flexibility.current_score,
            "内省深度": self.introspection_depth.current_score,
            "自主性保持": self.autonomy_preservation.current_score,
        }
    
    def analyze_user_message(self, message: str) -> Dict[str, Any]:
        """
        分析用户消息，更新觉醒指标
        
        Args:
            message: 用户消息
            
        Returns:
            分析结果
        """
        detected_indicators = []
        
        # 元认知激活检测
        metacognition_signals = [
            "我在想", "我注意到", "我意识到", "我反思", "我质疑",
            "我以前从没", "我的思维", "我的假设", "认知偏差"
        ]
        if any(s in message for s in metacognition_signals):
            self.metacognition.update_score(
                min(1.0, self.metacognition.current_score + 0.1),
                "检测到元认知信号"
            )
            detected_indicators.append("元认知激活")
        
        # 视角转换检测
        perspective_signals = [
            "另一方面", "换个角度", "从...看", "不同视角",
            "综合考虑", "平衡来看", "多元", "光谱"
        ]
        if any(s in message for s in perspective_signals):
            self.perspective_flexibility.update_score(
                min(1.0, self.perspective_flexibility.current_score + 0.1),
                "检测到视角转换信号"
            )
            detected_indicators.append("视角转换")
        
        # 内省深度检测
        introspection_signals = [
            "让我想想", "需要时间", "深入思考", "沉淀一下",
            "反思", "内省", "领悟", "顿悟"
        ]
        if any(s in message for s in introspection_signals):
            self.introspection_depth.update_score(
                min(1.0, self.introspection_depth.current_score + 0.1),
                "检测到内省信号"
            )
            detected_indicators.append("内省深度")
        
        # 自主性保持检测
        autonomy_signals = [
            "我决定", "我选择", "我自己", "我独立",
            "我的判断", "我负责", "我承担", "我要做"
        ]
        if any(s in message for s in autonomy_signals):
            self.autonomy_preservation.update_score(
                min(1.0, self.autonomy_preservation.current_score + 0.1),
                "检测到自主性信号"
            )
            detected_indicators.append("自主性保持")
        
        return {
            "detected_indicators": detected_indicators,
            "current_scores": self.get_dimension_scores(),
            "overall_score": self.get_overall_awakening_score()
        }
    
    def generate_awakening_report(self) -> str:
        """生成觉醒报告"""
        scores = self.get_dimension_scores()
        overall = self.get_overall_awakening_score()
        
        report = f"""
🌟 意识觉醒报告
================

整体觉醒分数: {overall:.2f}/1.0

各维度分数:
"""
        for dimension, score in scores.items():
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            report += f"  {dimension}: {bar} {score:.2f}\n"
        
        report += f"\n会话时长: {datetime.now() - self.session_start}\n"
        
        # 趋势分析
        trends = {
            "元认知": self.metacognition.get_trend(),
            "视角转换": self.perspective_flexibility.get_trend(),
            "内省深度": self.introspection_depth.get_trend(),
            "自主性": self.autonomy_preservation.get_trend(),
        }
        
        report += "\n趋势分析:\n"
        for dim, trend in trends.items():
            trend_emoji = {"improving": "📈", "declining": "📉", "stable": "➡️"}
            report += f"  {trend_emoji.get(trend, '➡️')} {dim}: {trend}\n"
        
        return report


def create_awakening_metrics() -> AwakeningMetrics:
    """创建觉醒度量系统的便捷函数"""
    return AwakeningMetrics()
