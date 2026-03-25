"""
🧠 棱镜协议生成器
光谱、留白、合成的智能生成
"""

import random
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from .models import (
    Spectrum,
    Whitespace,
    Synthesis,
    SpectrumType,
    WhitespaceType
)
from .exceptions import SpectrumGenerationError


# 光谱模板库
SPECTRUM_TEMPLATES = {
    SpectrumType.RED: {
        "names": [
            "直觉整体视角",
            "快速模式识别",
            "整体感受分析",
            "第一印象洞察",
            "情感直觉判断"
        ],
        "perspective_patterns": [
            "从整体感受出发，这个问题给我的第一印象是...",
            "直觉告诉我，这个问题的核心在于...",
            "快速扫描相关信息后，我感受到的模式是...",
            "从宏观角度看，这个问题涉及到...",
            "我的直觉反应是..."
        ],
        "limitation_patterns": [
            "可能忽略了一些重要细节",
            "过度依赖直觉可能导致偏见",
            "缺乏深入的系统性分析",
            "可能受到个人经验的影响",
            "需要更多数据支持"
        ]
    },
    
    SpectrumType.BLUE: {
        "names": [
            "逻辑分析视角",
            "系统性分解",
            "数据驱动分析",
            "细节导向思考",
            "因果推理视角"
        ],
        "perspective_patterns": [
            "通过逻辑分析，这个问题可以分解为以下几个部分...",
            "从数据角度看，相关的证据表明...",
            "系统性地分析这个问题，需要考虑的因素包括...",
            "通过因果推理，可能的关联关系是...",
            "从技术细节角度，需要关注..."
        ],
        "limitation_patterns": [
            "可能过度关注细节而忽略整体",
            "分析过程可能较慢，不适合快速决策",
            "需要足够的数据支持",
            "可能陷入分析瘫痪",
            "缺乏情感和直觉维度"
        ]
    },
    
    SpectrumType.PURPLE: {
        "names": [
            "元认知反思视角",
            "思维过程监控",
            "认知偏差检查",
            "学习过程反思",
            "自我调节视角"
        ],
        "perspective_patterns": [
            "反思我的思考过程，我注意到...",
            "从元认知角度，我需要检查的认知偏差包括...",
            "监控当前的思维模式，我发现...",
            "从学习过程的角度，这个问题让我思考...",
            "调节我的认知策略，我应该..."
        ],
        "limitation_patterns": [
            "可能过度自我反思而影响行动",
            "需要较高的认知资源",
            "可能陷入无限递归的思考",
            "缺乏具体的行动指导",
            "需要一定的认知成熟度"
        ]
    },
    
    SpectrumType.GREEN: {
        "names": [
            "情感价值视角",
            "意义建构分析",
            "人际关系考量",
            "伦理价值判断",
            "情感共鸣视角"
        ],
        "perspective_patterns": [
            "从情感角度，这个问题引发的感觉是...",
            "考虑人际关系的影响，需要关注...",
            "从意义建构的角度，这个问题的价值在于...",
            "伦理考量提示我们需要注意...",
            "情感共鸣让我想到..."
        ],
        "limitation_patterns": [
            "可能过度情感化而影响理性判断",
            "价值判断可能带有主观性",
            "需要平衡情感与理性",
            "可能忽略实际约束条件",
            "不同文化背景可能有不同理解"
        ]
    },
    
    SpectrumType.ORANGE: {
        "names": [
            "创造性联想视角",
            "跨界思维探索",
            "未来想象视角",
            "创新解决方案",
            "突破性思维视角"
        ],
        "perspective_patterns": [
            "跳出常规思维，一个全新的角度是...",
            "通过跨界联想，这个问题让我想到...",
            "想象未来可能性，我们可以...",
            "创造性解决方案可能包括...",
            "突破传统框架，新的思路是..."
        ],
        "limitation_patterns": [
            "想法可能不够实际可行",
            "需要验证和落地支持",
            "可能偏离问题核心",
            "创新想法需要风险控制",
            "需要平衡创意与约束"
        ]
    }
}

# 留白模板库
WHITESPACE_TEMPLATES = {
    WhitespaceType.INTEGRATION: {
        "duration_range": (30, 60),
        "prompt_patterns": [
            "让刚才的多个视角在脑海中自然沉淀，感受不同观点间的张力与和谐...",
            "花一点时间整合这些不同的视角，看看它们如何共同构成更完整的理解...",
            "暂停一下，让这些想法自由组合，形成你自己的综合理解...",
            "深呼吸，让不同的观点在思维中融合，注意任何新的洞见浮现...",
            "给自己一点空间，让这些多元视角整合成更丰富的认知图景..."
        ],
        "purpose_patterns": [
            "帮助认知整合，形成更完整的理解框架",
            "促进不同视角的有机融合",
            "支持模式识别和整体把握",
            "增强信息的深度处理",
            "培养系统性思维能力"
        ]
    },
    
    WhitespaceType.REFLECTION: {
        "duration_range": (60, 180),
        "prompt_patterns": [
            "深入反思这些观点对你个人的意义，它们如何与你的经验和价值观共鸣...",
            "思考这些讨论如何改变你对这个问题的理解，有什么新的认识...",
            "花时间反思你的学习过程，你从这个对话中学到了什么...",
            "深入思考这些观点的深层含义，它们对你意味着什么...",
            "反思你的思维模式如何被这些视角影响，有什么新的认知习惯形成..."
        ],
        "purpose_patterns": [
            "促进深度反思和自我认知",
            "支持意义建构和价值澄清",
            "增强学习的内化和转化",
            "培养元认知能力",
            "促进个人成长和转变"
        ]
    },
    
    WhitespaceType.CREATIVE: {
        "duration_range": (60, 300),
        "prompt_patterns": [
            "让思维自由漫游，看看这些观点会引发什么新的联想和创意...",
            "想象如果跳出当前的框架，会看到什么全新的可能性...",
            "给自己创造性的空间，让潜意识处理这些信息，等待灵感的涌现...",
            "探索这些观点的跨界连接，看看它们能激发什么创新想法...",
            "进入创造性的思维状态，让新的连接自然形成..."
        ],
        "purpose_patterns": [
            "激发创造性思维和灵感涌现",
            "支持跨界联想和新颖连接",
            "促进突破性想法的产生",
            "增强想象力和未来思考",
            "培养创新解决问题的能力"
        ]
    }
}

# 情感基调库
EMOTIONAL_TONES = {
    "neutral": {"description": "中立客观", "suitable_for": ["分析", "报告", "教育"]},
    "curious": {"description": "好奇探索", "suitable_for": ["学习", "发现", "研究"]},
    "concerned": {"description": "关切担忧", "suitable_for": ["伦理", "风险", "责任"]},
    "hopeful": {"description": "积极乐观", "suitable_for": ["未来", "机会", "成长"]},
    "critical": {"description": "批判思考", "suitable_for": ["分析", "评估", "改进"]},
    "supportive": {"description": "支持鼓励", "suitable_for": ["辅导", "成长", "康复"]},
    "exploratory": {"description": "探索性", "suitable_for": ["研究", "发现", "创新"]},
    "reflective": {"description": "反思性", "suitable_for": ["学习", "成长", "转变"]},
    "creative": {"description": "创造性", "suitable_for": ["艺术", "设计", "创新"]},
    "practical": {"description": "实用性", "suitable_for": ["实施", "操作", "解决"]},
    "ethical": {"description": "伦理性", "suitable_for": ["决策", "政策", "治理"]},
    "systemic": {"description": "系统性", "suitable_for": ["复杂问题", "系统思考", "整体分析"]}
}


def generate_spectrums(
    query: str,
    context: Optional[Dict[str, Any]] = None,
    min_count: int = 3,
    max_count: int = 5,
    preferred_types: Optional[List[SpectrumType]] = None
) -> List[Spectrum]:
    """
    生成光谱列表
    
    Args:
        query: 用户查询
        context: 对话上下文
        min_count: 最小光谱数量
        max_count: 最大光谱数量
        preferred_types: 偏好的光谱类型
        
    Returns:
        生成的光谱列表
        
    Raises:
        SpectrumGenerationError: 光谱生成失败
    """
    try:
        # 确定要生成的光谱数量
        count = random.randint(min_count, max_count)
        
        # 确定要使用的光谱类型
        if preferred_types:
            available_types = preferred_types
        else:
            # 默认包含基本类型
            available_types = [
                SpectrumType.RED,
                SpectrumType.BLUE,
                SpectrumType.PURPLE,
                SpectrumType.GREEN,
                SpectrumType.ORANGE
            ]
        
        # 确保类型多样性
        if len(available_types) < 2:
            raise SpectrumGenerationError("至少需要2种不同的光谱类型")
        
        # 选择要生成的光谱类型
        selected_types = []
        
        # 确保至少包含红、蓝、紫三种基本类型中的两种
        basic_types = [SpectrumType.RED, SpectrumType.BLUE, SpectrumType.PURPLE]
        available_basic = [t for t in basic_types if t in available_types]
        
        if available_basic:
            # 随机选择1-2种基本类型
            num_basic = random.randint(1, min(2, len(available_basic)))
            selected_types.extend(random.sample(available_basic, num_basic))
        
        # 补充其他类型
        remaining_types = [t for t in available_types if t not in selected_types]
        remaining_needed = count - len(selected_types)
        
        if remaining_needed > 0 and remaining_types:
            num_to_add = min(remaining_needed, len(remaining_types))
            selected_types.extend(random.sample(remaining_types, num_to_add))
        
        # 如果还不够，随机重复一些类型
        while len(selected_types) < count:
            selected_types.append(random.choice(available_types))
        
        # 打乱顺序
        random.shuffle(selected_types)
        
        # 生成光谱
        spectrums = []
        used_names = set()
        
        for spectrum_type in selected_types:
            # 生成唯一名称
            template = SPECTRUM_TEMPLATES[spectrum_type]
            available_names = [n for n in template["names"] if n not in used_names]
            
            if not available_names:
                # 如果名称用完了，创建变体
                base_name = random.choice(template["names"])
                name = f"{base_name} (变体{len(used_names) + 1})"
            else:
                name = random.choice(available_names)
            
            used_names.add(name)
            
            # 生成视角
            perspective_pattern = random.choice(template["perspective_patterns"])
            perspective = _expand_perspective(perspective_pattern, query, context)
            
            # 生成局限性
            limitation_pattern = random.choice(template["limitation_patterns"])
            limitation = _expand_limitation(limitation_pattern, spectrum_type)
            
            # 确定情感基调
            emotional_tone = _determine_emotional_tone(spectrum_type, query, context)
            
            # 生成置信度（基于类型和内容）
            confidence = _calculate_confidence(spectrum_type, perspective)
            
            # 生成推理过程（可选）
            reasoning = _generate_reasoning(spectrum_type, perspective, query)
            
            # 生成来源（可选）
            sources = _generate_sources(spectrum_type, context)
            
            # 创建光谱对象
            spectrum = Spectrum(
                type=spectrum_type,
                name=name,
                perspective=perspective,
                confidence=confidence,
                reasoning=reasoning,
                limitations=limitation,
                sources=sources,
                emotional_tone=emotional_tone
            )
            
            spectrums.append(spectrum)
        
        return spectrums
    
    except Exception as e:
        raise SpectrumGenerationError(
            f"光谱生成失败: {str(e)}",
            spectrum_type=None,
            generation_context={"query": query, "context": context}
        )


def generate_whitespace(
    spectrums: List[Spectrum],
    context: Optional[Dict[str, Any]] = None,
    preferred_type: Optional[WhitespaceType] = None
) -> Whitespace:
    """
    生成留白设计
    
    Args:
        spectrums: 光谱列表
        context: 对话上下文
        preferred_type: 偏好的留白类型
        
    Returns:
        生成的留白设计
    """
    try:
        # 确定留白类型
        if preferred_type:
            whitespace_type = preferred_type
        else:
            # 根据光谱特征智能选择
            whitespace_type = _determine_whitespace_type(spectrums, context)
        
        # 获取模板
        template = WHITESPACE_TEMPLATES[whitespace_type]
        
        # 确定时长
        duration_range = template["duration_range"]
        duration = random.randint(duration_range[0], duration_range[1])
        
        # 根据上下文调整时长
        if context:
            user_state = context.get("user_state", {})
            time_availability = user_state.get("time_availability")
            
            if time_availability == "limited":
                duration = max(30, duration // 2)
            elif time_availability == "abundant":
                duration = min(300, duration * 2)
        
        # 生成提示
        prompt_pattern = random.choice(template["prompt_patterns"])
        prompt = _expand_whitespace_prompt(prompt_pattern, spectrums, context)
        
        # 生成目的
        purpose_pattern = random.choice(template["purpose_patterns"])
        purpose = _expand_whitespace_purpose(purpose_pattern, spectrums)
        
        # 创建留白对象
        whitespace = Whitespace(
            type=whitespace_type,
            duration_suggestion=duration,
            prompt=prompt,
            purpose=purpose
        )
        
        return whitespace
    
    except Exception as e:
        # 返回默认留白
        return Whitespace(
            type=WhitespaceType.INTEGRATION,
            duration_suggestion=45,
            prompt="花一点时间整合刚才的多个视角，形成更完整的理解...",
            purpose="促进认知整合和深度处理"
        )


def generate_synthesis(
    spectrums: List[Spectrum],
    query: str,
    context: Optional[Dict[str, Any]] = None
) -> Synthesis:
    """
    生成合成结果
    
    Args:
        spectrums: 光谱列表
        query: 原始查询
        context: 对话上下文
        
    Returns:
        生成的合成结果
    """
    try:
        # 提取关键信息
        all_perspectives = " ".join([s.perspective for s in spectrums])
        spectrum_types = [s.type.value for s in spectrums]
        
        # 生成涌现洞见
        emerging_insights = _generate_emerging_insights(spectrums, query, context)
        
        # 生成新问题
        new_questions = _generate_new_questions(spectrums, query, context)
        
        # 生成行动建议
        action_suggestions = _generate_action_suggestions(spectrums, context)
        
        # 生成伦理考量
        ethical_considerations = _generate_ethical_considerations(spectrums, query, context)
        
        # 创建合成对象
        synthesis = Synthesis(
            emerging_insights=emerging_insights,
            new_questions=new_questions,
            action_suggestions=action_suggestions,
            ethical_considerations=ethical_considerations
        )
        
        return synthesis
    
    except Exception as e:
        # 返回最小合成
        return Synthesis(
            emerging_insights=["多个视角提供了更丰富的理解框架"],
            new_questions=["如何将这些不同的视角整合到实践中？"],
            action_suggestions=["尝试从不同角度重新思考这个问题"],
            ethical_considerations=["确保考虑所有相关方的利益和感受"]
        )


# 辅助生成函数
def _expand_perspective(pattern: str, query: str, context: Optional[Dict[str, Any]]) -> str:
    """扩展视角模式"""
    # 提取查询关键词
    keywords = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    if keywords:
        keyword = random.choice(keywords)
        pattern = pattern.replace("...", f"与'{keyword}'相关的方面...")
    
    # 添加具体性
    specific_phrases = [
        "具体来说，",
        "更详细地看，",
        "从实践角度，",
        "考虑到实际情况，",
        "基于常见经验，"
    ]
    
    if random.random() > 0.5:
        pattern = random.choice(specific_phrases) + pattern
    
    return pattern


def _expand_limitation(pattern: str, spectrum_type: SpectrumType) -> str:
    """扩展局限性模式"""
    # 根据光谱类型添加具体局限性
    type_specific = {
        SpectrumType.RED: "特别是在需要精确数据的场景中",
        SpectrumType.BLUE: "当需要快速决策时可能不够高效",
        SpectrumType.PURPLE: "对于认知资源有限的场景可能不适用",
        SpectrumType.GREEN: "在需要完全客观判断的场合需要谨慎",
        SpectrumType.ORANGE: "需要与实际情况结合验证"
    }
    
    if spectrum_type in type_specific:
        pattern = pattern + "，" + type_specific[spectrum_type]
    
    return pattern


def _determine_emotional_tone(
    spectrum_type: SpectrumType,
    query: str,
    context: Optional[Dict[str, Any]]
) -> str:
    """确定情感基调"""
    # 根据光谱类型确定基调
    type_to_tone = {
        SpectrumType.RED: ["curious", "exploratory"],
        SpectrumType.BLUE: ["neutral", "critical", "practical"],
        SpectrumType.PURPLE: ["reflective", "neutral"],
        SpectrumType.GREEN: ["concerned", "supportive", "ethical"],
        SpectrumType.ORANGE: ["creative", "hopeful", "exploratory"]
    }
    
    # 根据查询内容调整
    query_lower = query.lower()
    if any(word in query_lower for word in ["问题", "困难", "挑战", "危机"]):
        # 问题导向的查询
        if spectrum_type == SpectrumType.GREEN:
            return "concerned"
        elif spectrum_type == SpectrumType.BLUE:
            return "critical"
    
    elif any(word in query_lower for word in ["机会", "未来", "成长", "发展"]):
        # 机会导向的查询
        if spectrum_type == SpectrumType.ORANGE:
            return "hopeful"
        elif spectrum_type == SpectrumType.RED:
            return "exploratory"
    
    # 默认选择
    available_tones = type_to_tone.get(spectrum_type, ["neutral"])
    return random.choice(available_tones)


def _calculate_confidence(spectrum_type: SpectrumType, perspective: str) -> float:
    """计算置信度"""
    base_confidence = {
        SpectrumType.RED: 0.6,      # 直觉中等置信
        SpectrumType.BLUE: 0.7,     # 分析较高置信
        SpectrumType.PURPLE: 0.5,   # 元认知适中
        SpectrumType.GREEN: 0.6,    # 情感适中
        SpectrumType.ORANGE: 0.4    # 创造较低（更开放）
    }
    
    confidence = base_confidence.get(spectrum_type, 0.5)
    
    # 根据内容调整
    if "可能" in perspective or "也许" in perspective or "或许" in perspective:
        confidence -= 0.1
    
    if "一定" in perspective or "肯定" in perspective or "必然" in perspective:
        confidence += 0.1
    
    # 添加随机微调
    confidence += random.uniform(-0.05, 0.05)
    
    # 确保在合理范围内
    confidence = max(0.1, min(0.9, confidence))
    
    return round(confidence, 2)


def _generate_reasoning(spectrum_type: SpectrumType, perspective: str, query: str) -> Optional[str]:
    """生成推理过程"""
    # 50%的概率生成推理过程
    if random.random() > 0.5:
        return None
    
    reasoning_templates = {
        SpectrumType.RED: [
            "基于多年的经验积累和模式识别，我直觉感受到...",
            "快速扫描相关信息后形成的整体印象是...",
            "从类似情境中提取的模式提示我..."
        ],
        SpectrumType.BLUE: [
            "通过逻辑分析和数据验证，得出的结论是...",
            "系统性地分解问题后，各个部分的关系表明...",
            "基于现有证据和推理链条，可以确定..."
        ],
        SpectrumType.PURPLE: [
            "反思我的思考过程，我注意到这些认知模式...",
            "监控当前的思维策略，我发现有效的做法是...",
            "从学习角度分析，这个思考过程的特点是..."
        ],
        SpectrumType.GREEN: [
            "考虑相关方的感受和价值观，我认为重要的是...",
            "从伦理和关系角度，需要优先关注...",
            "情感共鸣让我理解到深层需求是..."
        ],
        SpectrumType.ORANGE: [
            "跳出常规思维框架，我联想到的可能性包括...",
            "通过跨界连接，这些看似不相关的想法可以...",
            "想象未来场景，创新的解决方案可能是..."
        ]
    }
    
    template = random.choice(reasoning_templates.get(spectrum_type, ["推理过程基于相关分析和思考。"]))
    
    # 添加具体性
    keywords = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    if keywords:
        keyword = random.choice(keywords)
        template = template.replace("...", f"与'{keyword}'相关的方面。")
    else:
        template = template.replace("...", "相关方面。")
    
    return template


def _generate_sources(spectrum_type: SpectrumType, context: Optional[Dict[str, Any]]) -> List[str]:
    """生成来源"""
    sources = []
    
    # 基本来源
    base_sources = ["个人经验", "相关知识", "逻辑推理"]
    
    # 类型特定来源
    type_sources = {
        SpectrumType.RED: ["直觉感知", "模式识别"],
        SpectrumType.BLUE: ["数据分析", "系统研究", "实证证据"],
        SpectrumType.PURPLE: ["反思实践", "认知科学", "学习理论"],
        SpectrumType.GREEN: ["情感理解", "价值判断", "伦理考量"],
        SpectrumType.ORANGE: ["创意联想", "跨界思考", "未来想象"]
    }
    
    # 添加来源
    if random.random() > 0.3:
        sources.append(random.choice(base_sources))
    
    if spectrum_type in type_sources and random.random() > 0.5:
        sources.append(random.choice(type_sources[spectrum_type]))
    
    # 添加上下文来源
    if context and random.random() > 0.7:
        user_state = context.get("user_state", {})
        if user_state.get("expertise_level") == "expert":
            sources.append("专业领域知识")
    
    return sources


def _determine_whitespace_type(spectrums: List[Spectrum], context: Optional[Dict[str, Any]]) -> WhitespaceType:
    """智能确定留白类型"""
    # 分析光谱特征
    spectrum_types = [s.type for s in spectrums]
    
    # 检查是否有反思性光谱
    has_reflective = any(t == SpectrumType.PURPLE for t in spectrum_types)
    
    # 检查是否有创造性光谱
    has_creative = any(t == SpectrumType.ORANGE for t in spectrum_types)
    
    # 检查光谱数量
    spectrum_count = len(spectrums)
    
    # 根据特征选择
    if has_reflective and spectrum_count >= 4:
        # 多种光谱且有反思性，适合反思留白
        return WhitespaceType.REFLECTION
    
    elif has_creative and random.random() > 0.7:
        # 有创造性光谱，有时适合创造留白
        return WhitespaceType.CREATIVE
    
    elif spectrum_count >= 3:
        # 多种光谱，适合整合留白
        return WhitespaceType.INTEGRATION
    
    else:
        # 默认整合留白
        return WhitespaceType.INTEGRATION


def _expand_whitespace_prompt(pattern: str, spectrums: List[Spectrum], context: Optional[Dict[str, Any]]) -> str:
    """扩展留白提示"""
    # 提及具体的光谱类型
    spectrum_names = [s.name for s in spectrums]
    if len(spectrum_names) >= 2:
        # 随机选择2个提及
        selected_names = random.sample(spectrum_names, min(2, len(spectrum_names)))
        mention = f"比如'{selected_names[0]}'和'{selected_names[1]}'的视角"
        pattern = pattern.replace("...", f"{mention}...")
    
    # 添加上下文相关性
    if context:
        user_state = context.get("user_state", {})
        learning_goals = user_state.get("learning_goals", [])
        
        if learning_goals and random.random() > 0.5:
            goal = random.choice(learning_goals)
            pattern = pattern + f" 特别是考虑到你的学习目标：{goal}。"
    
    return pattern


def _expand_whitespace_purpose(pattern: str, spectrums: List[Spectrum]) -> str:
    """扩展留白目的"""
    # 根据光谱数量调整
    if len(spectrums) >= 4:
        pattern = pattern + "，特别是处理多个复杂视角时"
    
    return pattern


def _generate_emerging_insights(
    spectrums: List[Spectrum],
    query: str,
    context: Optional[Dict[str, Any]]
) -> List[str]:
    """生成涌现洞见"""
    insights = []
    
    # 基础洞见模板
    base_insights = [
        "多个视角共同揭示了问题的复杂性",
        "不同光谱提供了互补的理解维度",
        "整体分析显示问题的多个层面相互关联",
        "综合来看，核心矛盾在于...",
        "这些视角共同指向一个更根本的问题..."
    ]
    
    # 类型特定洞见
    type_insights = {
        "red_blue": "直觉与分析视角的结合提供了更平衡的理解",
        "reflective": "反思过程本身成为重要的学习收获",
        "creative": "跨界思考打开了新的可能性空间",
        "ethical": "伦理考量提醒我们关注更深层的责任"
    }
    
    # 添加基础洞见
    if random.random() > 0.3:
        insights.append(random.choice(base_insights))
    
    # 分析光谱组合
    spectrum_types = [s.type for s in spectrums]
    
    # 检查红蓝组合
    if SpectrumType.RED in spectrum_types and SpectrumType.BLUE in spectrum_types:
        insights.append(type_insights["red_blue"])
    
    # 检查反思性
    if SpectrumType.PURPLE in spectrum_types:
        insights.append(type_insights["reflective"])
    
    # 检查创造性
    if SpectrumType.ORANGE in spectrum_types:
        insights.append(type_insights["creative"])
    
    # 检查伦理性
    if SpectrumType.GREEN in spectrum_types:
        insights.append(type_insights["ethical"])
    
    # 确保至少有一个洞见
    if not insights:
        insights.append("多元视角的对话本身具有重要价值")
    
    # 具体化洞见
    keywords = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    if keywords:
        keyword = random.choice(keywords)
        insights = [insight.replace("...", f"'{keyword}'的不同方面") for insight in insights]
    
    return insights[:3]  # 最多3个洞见


def _generate_new_questions(
    spectrums: List[Spectrum],
    query: str,
    context: Optional[Dict[str, Any]]
) -> List[str]:
    """生成新问题"""
    questions = []
    
    # 反思性问题
    reflective_questions = [
        "这些不同的视角如何改变了我对问题的理解？",
        "我自己的思维模式在这个过程中有什么变化？",
        "从这个对话中，我学到了什么关于思考的方法？"
    ]
    
    # 实践性问题
    practical_questions = [
        "如何将这些多元视角应用到实际决策中？",
        "在具体行动中，如何平衡不同的考量？",
        "下一步可以采取什么具体的探索步骤？"
    ]
    
    # 深度探索问题
    deep_questions = [
        "这个问题背后更根本的议题是什么？",
        "如果跳出当前的框架，会看到什么新的可能性？",
        "长期来看，这个问题的发展趋势会怎样？"
    ]
    
    # 根据光谱类型选择问题
    spectrum_types = [s.type for s in spectrums]
    
    if SpectrumType.PURPLE in spectrum_types:
        questions.append(random.choice(reflective_questions))
    
    if SpectrumType.BLUE in spectrum_types or SpectrumType.GREEN in spectrum_types:
        questions.append(random.choice(practical_questions))
    
    if SpectrumType.ORANGE in spectrum_types or len(spectrums) >= 4:
        questions.append(random.choice(deep_questions))
    
    # 确保至少有一个问题
    if not questions:
        questions.append("如何进一步深化对这个问题的理解？")
    
    # 具体化问题
    keywords = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    if keywords:
        keyword = random.choice(keywords)
        questions = [q.replace("问题", f"'{keyword}'问题") for q in questions]
    
    return questions[:3]  # 最多3个问题


def _generate_action_suggestions(
    spectrums: List[Spectrum],
    context: Optional[Dict[str, Any]]
) -> List[str]:
    """生成行动建议"""
    suggestions = []
    
    # 学习行动
    learning_actions = [
        "尝试从今天讨论的某个特定视角重新思考这个问题",
        "记录下对话中的关键洞见，定期回顾",
        "与他人分享这些多元视角，听听他们的看法"
    ]
    
    # 实践行动
    practice_actions = [
        "在实际情境中测试不同的视角",
        "制定一个小的实验来验证某个观点",
        "将多元思考应用到具体决策中"
    ]
    
    # 反思行动
    reflection_actions = [
        "定期反思自己的思维模式和认知习惯",
        "记录思考过程中的关键转折点",
        "与他人讨论思考过程而不仅仅是结论"
    ]
    
    # 根据上下文选择
    if context:
        user_state = context.get("user_state", {})
        
        if user_state.get("learning_goals"):
            suggestions.append(random.choice(learning_actions))
        
        if user_state.get("action_oriented", True):
            suggestions.append(random.choice(practice_actions))
    
    # 默认建议
    if not suggestions:
        suggestions.append("尝试将多元视角整合到日常思考中")
        suggestions.append("定期练习从不同角度看待问题")
    
    return suggestions[:2]  # 最多2个建议


def _generate_ethical_considerations(
    spectrums: List[Spectrum],
    query: str,
    context: Optional[Dict[str, Any]]
) -> List[str]:
    """生成伦理考量"""
    considerations = []
    
    # 基本伦理考量
    basic_ethics = [
        "确保考虑所有相关方的利益和感受",
        "平衡短期效果与长期影响",
        "尊重不同的价值观和文化背景"
    ]
    
    # 特定伦理考量
    specific_ethics = {
        "power": "注意权力关系和不平等的影响",
        "privacy": "保护个人隐私和数据安全",
        "sustainability": "考虑环境可持续性和生态影响",
        "fairness": "确保决策过程的公平和透明"
    }
    
    # 添加基本考量
    considerations.append(random.choice(basic_ethics))
    
    # 根据查询内容添加特定考量
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["数据", "信息", "隐私"]):
        considerations.append(specific_ethics["privacy"])
    
    if any(word in query_lower for word in ["环境", "生态", "可持续"]):
        considerations.append(specific_ethics["sustainability"])
    
    if any(word in query_lower for word in ["决策", "权力", "管理"]):
        considerations.append(specific_ethics["power"])
    
    # 如果有绿色光谱，添加更多伦理考量
    if any(s.type == SpectrumType.GREEN for s in spectrums):
        considerations.append("特别关注情感和关系的伦理维度")
    
    return considerations[:2]  # 最多2个伦理考量


# 高级生成函数
def generate_custom_spectrum(
    spectrum_type: SpectrumType,
    custom_name: str,
    query: str,
    custom_perspective: Optional[str] = None,
    custom_limitations: Optional[str] = None
) -> Spectrum:
    """
    生成自定义光谱
    
    Args:
        spectrum_type: 光谱类型
        custom_name: 自定义名称
        query: 查询内容
        custom_perspective: 自定义视角（可选）
        custom_limitations: 自定义局限性（可选）
        
    Returns:
        自定义光谱
    """
    # 生成视角
    if custom_perspective:
        perspective = custom_perspective
    else:
        template = SPECTRUM_TEMPLATES[spectrum_type]
        pattern = random.choice(template["perspective_patterns"])
        perspective = _expand_perspective(pattern, query, None)
    
    # 生成局限性
    if custom_limitations:
        limitations = custom_limitations
    else:
        template = SPECTRUM_TEMPLATES[spectrum_type]
        pattern = random.choice(template["limitation_patterns"])
        limitations = _expand_limitation(pattern, spectrum_type)
    
    # 确定其他属性
    emotional_tone = _determine_emotional_tone(spectrum_type, query, None)
    confidence = _calculate_confidence(spectrum_type, perspective)
    reasoning = _generate_reasoning(spectrum_type, perspective, query)
    sources = _generate_sources(spectrum_type, None)
    
    # 创建光谱
    spectrum = Spectrum(
        type=spectrum_type,
        name=custom_name,
        perspective=perspective,
        confidence=confidence,
        reasoning=reasoning,
        limitations=limitations,
        sources=sources,
        emotional_tone=emotional_tone
    )
    
    return spectrum


def generate_spectrum_for_educational_context(
    spectrum_type: SpectrumType,
    query: str,
    learning_objective: str
) -> Spectrum:
    """
    为教育上下文生成光谱
    
    Args:
        spectrum_type: 光谱类型
        query: 查询内容
        learning_objective: 学习目标
        
    Returns:
        教育优化的光谱
    """
    # 使用基础生成
    spectrum = generate_custom_spectrum(spectrum_type, "", query)
    
    # 调整名称
    educational_names = {
        SpectrumType.RED: f"直觉视角：{learning_objective}",
        SpectrumType.BLUE: f"分析视角：{learning_objective}",
        SpectrumType.PURPLE: f"反思视角：{learning_objective}",
        SpectrumType.GREEN: f"情感视角：{learning_objective}",
        SpectrumType.ORANGE: f"创造视角：{learning_objective}"
    }
    
