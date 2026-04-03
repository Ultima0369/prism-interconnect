"""
🎭 艺术化处理模块

处理棱镜协议的艺术化表现，包括初始化、显示、输出格式化等。

🔥 艺术设计原则:
1. 温度感: 代码有温度，错误有诗意
2. 节奏感: 响应有节奏，留白有时机
3. 可视化: 抽象可感知，数据可欣赏
4. 人格化: 系统有性格，交互有情感

🌈 设计目标:
- 让技术实现具有美学品质
- 让错误处理具有教育价值
- 让用户体验具有情感共鸣
- 让系统交互具有人文温度
"""

import time
import random
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from dataclasses import dataclass

from .models import PrismResponse, Spectrum


@dataclass
class ArtisticDisplay:
    """艺术化显示配置"""
    
    enable_spectrum_art: bool = True
    output_channel: Callable[[str], None] = print
    warmth_level: float = 0.7
    response_art_form: str = "haiku"
    
    def show_initialization(self, client_name: str = "棱镜客户端"):
        """显示初始化艺术化信息"""
        if not self.enable_spectrum_art:
            return
        
        output = self.output_channel
        output("🎭 棱镜客户端初始化中...")
        time.sleep(0.3)
        
        warmth_desc = {
            0.9: "🔥 非常温暖",
            0.7: "🔥 舒适温暖",
            0.5: "🔥 温和温暖", 
            0.3: "🔥 需要添柴"
        }
        
        closest = min(warmth_desc.keys(), 
                     key=lambda x: abs(x - self.warmth_level))
        
        output(f"🦞 温暖度: {self.warmth_level:.1f} ({warmth_desc[closest]})")
        output(f"{'='*40}")
    
    def show_refraction_start(self, message: str, spectrum_count: int):
        """显示折射开始的艺术化信息"""
        if not self.enable_spectrum_art:
            return
        
        output = self.output_channel
        output(f"\n🌈 开始折射消息...")
        output(f"💭 消息: {message[:50]}{'...' if len(message) > 50 else ''}")
        output(f"🎯 目标光谱数: {spectrum_count}")
        output(f"⏳ 思考中..." + ("." * random.randint(1, 3)))
        time.sleep(0.5)
    
    def show_refraction_result(self, response: PrismResponse):
        """显示折射结果的艺术化信息"""
        if not self.enable_spectrum_art:
            return
        
        output = self.output_channel
        output(f"\n✅ 折射完成!")
        output(f"📊 生成光谱数: {len(response.spectrums)}")
        output(f"🧠 理解深度: {response.metadata.understanding_depth:.2f}")
        output(f"⏱️  耗时: {response.metadata.processing_time_ms}ms")
        
        if response.whitespace_recommendation:
            output(f"🧘 留白建议: {response.whitespace_recommendation.guidance}")
        
        output(f"{'='*40}")
    
    def generate_artistic_metadata(self, response: PrismResponse) -> Dict[str, Any]:
        """生成艺术化元数据"""
        metadata = {
            "refraction_timestamp": datetime.now().isoformat(),
            "spectrum_count": len(response.spectrums),
            "understanding_depth": response.metadata.understanding_depth,
            "processing_time_ms": response.metadata.processing_time_ms,
            "art_form": self._select_art_form(response),
            "philosophical_notes": self._select_philosophical_notes(response)
        }
        
        # 计算伦理得分
        ethics_score = self._calculate_ethics_score(response)
        metadata["ethics_score"] = ethics_score
        metadata["ethics_level"] = self._describe_ethics_level(ethics_score)
        
        # 添加光谱统计
        spectrum_stats = {}
        for spectrum in response.spectrums:
            spectrum_type = spectrum.type.value
            if spectrum_type not in spectrum_stats:
                spectrum_stats[spectrum_type] = 0
            spectrum_stats[spectrum_type] += 1
        
        metadata["spectrum_distribution"] = spectrum_stats
        metadata["cognitive_balance"] = self._calculate_cognitive_balance(spectrum_stats)
        
        return metadata
    
    def _select_art_form(self, response: PrismResponse) -> str:
        """选择艺术形式"""
        art_forms = ["haiku", "free_verse", "visual"]
        
        # 根据理解深度选择艺术形式
        depth = response.metadata.understanding_depth
        
        if depth > 0.8:
            return "visual"  # 深度理解用视觉艺术
        elif depth > 0.6:
            return "free_verse"  # 中等理解用自由诗
        else:
            return "haiku"  # 基础理解用俳句
    
    def _select_philosophical_notes(self, response: PrismResponse) -> List[str]:
        """选择哲学注释"""
        notes = [
            "E=mc² 告诉我们改变世界的可能，但真正的改变来自理解。",
            "1+1>2 是生命的合作法则，也是认知的乘法原理。",
            "留白不是空白，是思考的空间，是理解的深度。",
            "多元视角不是混乱，是认知的丰富，是智慧的层次。",
            "桃树伦理提醒我们：强大能力的背后是更大责任。",
            "认知镜子让我们看见自己看不见的思考模式。",
            "火堆旁的温度来自真诚对话，不是技术炫耀。",
            "代码可以冷，但理解必须暖。技术可以快，但对话必须慢。",
            "存在升级不是目标，是过程；不是终点，是起点。",
            "棱镜折射的不是光，是认知；不是答案，是可能性。"
        ]
        
        # 桃树伦理相关的注释 (前7个)
        peach_tree_notes = notes[:7]
        regular_notes = notes[7:]
        
        # 根据伦理得分调整权重
        ethics_score = self._calculate_ethics_score(response)
        weights = [0.7] * len(peach_tree_notes) + [0.3] * len(regular_notes)
        
        # 根据伦理得分调整权重
        if ethics_score > 0.8:
            weights = [0.3] * len(peach_tree_notes) + [0.7] * len(regular_notes)
        elif ethics_score < 0.5:
            weights = [0.9] * len(peach_tree_notes) + [0.1] * len(regular_notes)
        
        all_notes = peach_tree_notes + regular_notes
        selected = random.choices(all_notes, weights=weights, k=min(3, len(all_notes)))
        
        return selected
    
    def _calculate_ethics_score(self, response: PrismResponse) -> int:
        """计算伦理得分"""
        score = 0
        
        # 基于光谱多样性
        spectrum_types = set(s.type.value for s in response.spectrums)
        diversity_bonus = len(spectrum_types) * 10
        score += min(diversity_bonus, 30)  # 最多30分
        
        # 基于理解深度
        depth = response.metadata.understanding_depth
        depth_bonus = int(depth * 40)
        score += depth_bonus  # 最多40分
        
        # 基于留白建议
        if response.whitespace_recommendation:
            if response.whitespace_recommendation.duration_seconds >= 30:
                score += 20  # 充分留白
            else:
                score += 10  # 基础留白
        
        # 基于认知平衡
        spectrum_counts = {}
        for spectrum in response.spectrums:
            spectrum_type = spectrum.type.value
            if spectrum_type not in spectrum_counts:
                spectrum_counts[spectrum_type] = 0
            spectrum_counts[spectrum_type] += 1
        
        if len(spectrum_counts) >= 3:
            score += 10  # 良好的认知多样性
        
        return min(score, 100)  # 满分100分
    
    def _describe_ethics_level(self, score: int) -> str:
        """描述伦理水平"""
        if score >= 90:
            return "🔥 卓越伦理意识"
        elif score >= 80:
            return "🌟 优秀伦理实践"
        elif score >= 70:
            return "✅ 良好伦理基础"
        elif score >= 60:
            return "⚠️  基本伦理合规"
        else:
            return "🔴 需要伦理关注"
    
    def _calculate_cognitive_balance(self, spectrum_stats: Dict[str, int]) -> str:
        """计算认知平衡"""
        if not spectrum_stats:
            return "无数据"
        
        total = sum(spectrum_stats.values())
        if total == 0:
            return "无光谱"
        
        # 检查分布是否均衡
        max_count = max(spectrum_stats.values())
        min_count = min(spectrum_stats.values())
        
        if max_count - min_count <= 1:
            return "均衡分布"
        elif max_count > total * 0.6:
            dominant_type = [k for k, v in spectrum_stats.items() if v == max_count][0]
            return f"{dominant_type}主导"
        else:
            return "多样分布"
    
    def get_cognitive_report(self, 
                           response: PrismResponse,
                           cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """获取认知报告"""
        artistic_metadata = self.generate_artistic_metadata(response)
        
        report = {
            "refraction_summary": {
                "total_refractions": cognitive_state.get("refractions_count", 0),
                "total_whitespace_seconds": cognitive_state.get("total_whitespace_seconds", 0),
                "understanding_trend": cognitive_state.get("understanding_depth_trend", [])
            },
            "artistic_evaluation": artistic_metadata,
            "spectrum_analysis": self._analyze_spectrums(response.spectrums),
            "whitespace_evaluation": self._evaluate_whitespace(response.whitespace_recommendation),
            "ethical_audit": {
                "score": artistic_metadata["ethics_score"],
                "level": artistic_metadata["ethics_level"],
                "recommendations": self._generate_ethical_recommendations(artistic_metadata)
            }
        }
        
        return report
    
    def _analyze_spectrums(self, spectrums: List[Spectrum]) -> Dict[str, Any]:
        """分析光谱"""
        if not spectrums:
            return {"status": "无光谱数据"}
        
        analysis = {
            "total_count": len(spectrums),
            "type_distribution": {},
            "confidence_stats": {
                "average": 0.0,
                "min": 1.0,
                "max": 0.0
            },
            "emotional_tone_distribution": {}
        }
        
        total_confidence = 0
        for spectrum in spectrums:
            # 类型分布
            spectrum_type = spectrum.type.value
            if spectrum_type not in analysis["type_distribution"]:
                analysis["type_distribution"][spectrum_type] = 0
            analysis["type_distribution"][spectrum_type] += 1
            
            # 置信度统计
            confidence = spectrum.confidence
            total_confidence += confidence
            analysis["confidence_stats"]["min"] = min(analysis["confidence_stats"]["min"], confidence)
            analysis["confidence_stats"]["max"] = max(analysis["confidence_stats"]["max"], confidence)
            
            # 情感基调分布
            tone = spectrum.emotional_tone
            if tone not in analysis["emotional_tone_distribution"]:
                analysis["emotional_tone_distribution"][tone] = 0
            analysis["emotional_tone_distribution"][tone] += 1
        
        if len(spectrums) > 0:
            analysis["confidence_stats"]["average"] = total_confidence / len(spectrums)
        
        return analysis
    
    def _evaluate_whitespace(self, whitespace_recommendation: Any) -> Dict[str, Any]:
        """评估留白建议"""
        if not whitespace_recommendation:
            return {"status": "无留白建议", "recommendation": "考虑添加认知暂停"}
        
        evaluation = {
            "type": whitespace_recommendation.type.value if hasattr(whitespace_recommendation.type, 'value') else str(whitespace_recommendation.type),
            "duration_seconds": getattr(whitespace_recommendation, 'duration_seconds', 0),
            "guidance": getattr(whitespace_recommendation, 'guidance', ''),
            "quality": "优质" if getattr(whitespace_recommendation, 'duration_seconds', 0) >= 30 else "基础"
        }
        
        return evaluation
    
    def _generate_ethical_recommendations(self, artistic_metadata: Dict[str, Any]) -> List[str]:
        """生成伦理建议"""
        recommendations = []
        ethics_score = artistic_metadata.get("ethics_score", 0)
        
        if ethics_score < 60:
            recommendations.append("建议增加光谱多样性")
            recommendations.append("考虑延长留白时间")
            recommendations.append("关注认知平衡性")
        elif ethics_score < 80:
            recommendations.append("保持当前伦理实践水平")
            recommendations.append("考虑增加哲学反思")
            recommendations.append("监控认知趋势变化")
        else:
            recommendations.append("优秀伦理实践，继续保持")
            recommendations.append("考虑分享最佳实践")
            recommendations.append("探索更深层伦理维度")
        
        # 基于认知平衡的建议
        cognitive_balance = artistic_metadata.get("cognitive_balance", "")
        if "主导" in cognitive_balance:
            recommendations.append(f"注意{cognitive_balance}可能导致的认知偏见")
        
        return recommendations
    
    def format_error_poetically(self, 
                              error_type: str, 
                              error_message: str,
                              context: Dict[str, Any]) -> str:
        """诗意化格式化错误"""
        error_templates = [
            f"🔥 火堆旁提醒: {error_type}\n   在{context.get('location', '未知位置')}，{error_message}\n   这不是失败，是学习的机会。",
            f"🎭 艺术化错误: {error_type}\n   {error_message}\n   代码有温度，错误有诗意。",
            f"🧠 认知提醒: {error_type}\n   {error_message}\n   理解在发生，即使在错误中。",
            f"🌈 棱镜折射: 遇到{error_type}\n   {error_message}\n   每个错误都是一面认知镜子。"
        ]
        
        return random.choice(error_templates)