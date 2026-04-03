"""
🧠 棱镜协议验证器
数据验证和完整性检查
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from .models import (
    PrismMessage,
    Spectrum,
    Whitespace,
    Synthesis,
    ValidationResult,
    SpectrumType,
    WhitespaceType
)
from .exceptions import ValidationError


def validate_message(message: PrismMessage) -> ValidationResult:
    """
    验证棱镜消息的完整性和有效性
    
    Args:
        message: 要验证的棱镜消息
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    suggestions = []
    
    try:
        # 1. 基本验证
        _validate_basics(message, errors)
        
        # 2. 光谱验证
        _validate_spectrums(message.spectrums, errors, warnings, suggestions)
        
        # 3. 留白验证
        _validate_whitespace(message.whitespace, errors, warnings)
        
        # 4. 合成验证（如果存在）
        if message.synthesis:
            _validate_synthesis(message.synthesis, errors, warnings)
        
        # 5. 上下文验证
        if message.context:
            _validate_context(message.context, warnings)
        
        # 6. 整体一致性验证
        _validate_consistency(message, errors, warnings, suggestions)
        
        # 7. 伦理合规性验证
        _validate_ethical_compliance(message, errors, warnings)
        
    except Exception as e:
        errors.append(f"验证过程中发生异常: {str(e)}")
    
    # 构建验证结果
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )


def validate_spectrum(spectrum: Spectrum) -> ValidationResult:
    """
    验证单个光谱
    
    Args:
        spectrum: 要验证的光谱
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    suggestions = []
    
    try:
        # 1. 基本字段验证
        if not spectrum.name.strip():
            errors.append("光谱名称不能为空")
        
        if len(spectrum.perspective.strip()) < 10:
            errors.append("光谱视角描述太短，至少需要10个字符")
        
        if len(spectrum.perspective.strip()) > 2000:
            warnings.append("光谱视角描述过长，建议精简到2000字符以内")
        
        # 2. 置信度验证
        if spectrum.confidence < 0.0 or spectrum.confidence > 1.0:
            errors.append(f"置信度必须在0.0到1.0之间，当前值: {spectrum.confidence}")
        
        if spectrum.confidence > 0.9:
            warnings.append("过高的置信度可能表示过度自信，建议保持适当谦逊")
        
        # 3. 局限性验证
        if not spectrum.limitations.strip():
            errors.append("必须说明该视角的局限性")
        
        if len(spectrum.limitations.strip()) < 10:
            warnings.append("局限性描述可能不够充分，建议详细说明")
        
        # 4. 情感基调验证
        valid_tones = [
            "neutral", "curious", "concerned", "hopeful", 
            "critical", "supportive", "exploratory", "reflective",
            "creative", "practical", "ethical", "systemic"
        ]
        if spectrum.emotional_tone not in valid_tones:
            errors.append(f"无效的情感基调，必须是以下之一: {', '.join(valid_tones)}")
        
        # 5. 推理过程验证（如果存在）
        if spectrum.reasoning and len(spectrum.reasoning.strip()) > 5000:
            warnings.append("推理过程过长，建议精简到5000字符以内")
        
        # 6. 来源验证
        for source in spectrum.sources:
            if not source.strip():
                warnings.append("来源包含空字符串")
        
        # 7. 类型特定验证
        _validate_spectrum_by_type(spectrum, errors, warnings, suggestions)
        
    except Exception as e:
        errors.append(f"光谱验证过程中发生异常: {str(e)}")
    
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )


def validate_json_schema(data: Dict[str, Any], schema_type: str = "message") -> ValidationResult:
    """
    根据JSON Schema验证数据
    
    Args:
        data: 要验证的数据
        schema_type: 模式类型 ("message", "spectrum", "whitespace", "synthesis")
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    try:
        # 这里可以集成jsonschema库进行完整验证
        # 目前实现基本验证
        
        if schema_type == "message":
            required_fields = ["query", "spectrums", "whitespace"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"缺少必要字段: {field}")
        
        elif schema_type == "spectrum":
            required_fields = ["type", "name", "perspective", "limitations"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"缺少必要字段: {field}")
            
            # 验证光谱类型
            if "type" in data:
                valid_types = [t.value for t in SpectrumType]
                if data["type"] not in valid_types:
                    errors.append(f"无效的光谱类型: {data['type']}")
        
        elif schema_type == "whitespace":
            required_fields = ["type", "duration_suggestion", "prompt", "purpose"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"缺少必要字段: {field}")
            
            # 验证留白类型
            if "type" in data:
                valid_types = [t.value for t in WhitespaceType]
                if data["type"] not in valid_types:
                    errors.append(f"无效的留白类型: {data['type']}")
        
        elif schema_type == "synthesis":
            # 合成至少应该有一些内容
            has_content = False
            content_fields = ["emerging_insights", "new_questions", "action_suggestions", "ethical_considerations"]
            
            for field in content_fields:
                if field in data and data[field]:
                    has_content = True
                    break
            
            if not has_content:
                warnings.append("合成内容为空，建议提供至少一种输出")
        
        else:
            errors.append(f"未知的模式类型: {schema_type}")
    
    except Exception as e:
        errors.append(f"JSON Schema验证过程中发生异常: {str(e)}")
    
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=[]
    )


def _validate_basics(message: PrismMessage, errors: List[str]):
    """基本验证"""
    if not message.query.strip():
        errors.append("查询不能为空")
    
    if len(message.query.strip()) > 5000:
        errors.append("查询过长，最多5000字符")


def _validate_spectrums(
    spectrums: List[Spectrum],
    errors: List[str],
    warnings: List[str],
    suggestions: List[str]
):
    """光谱验证"""
    # 数量验证
    if len(spectrums) < 3:
        errors.append(f"光谱数量不足，至少需要3种，当前: {len(spectrums)}")
    
    if len(spectrums) > 10:
        warnings.append(f"光谱数量过多，可能造成认知过载，当前: {len(spectrums)}")
    
    # 类型多样性验证
    spectrum_types = [s.type for s in spectrums]
    unique_types = set(spectrum_types)
    
    if len(unique_types) < 2:
        errors.append("光谱类型缺乏多样性，至少需要2种不同类型")
    
    # 检查是否有基本类型
    basic_types = {SpectrumType.RED, SpectrumType.BLUE, SpectrumType.PURPLE}
    has_basic_types = any(t in basic_types for t in unique_types)
    
    if not has_basic_types:
        warnings.append("建议包含至少一种基本光谱类型（红、蓝、紫）")
        suggestions.append("考虑添加红色（直觉）、蓝色（分析）或紫色（元认知）光谱")
    
    # 名称唯一性验证
    spectrum_names = [s.name for s in spectrums]
    if len(set(spectrum_names)) != len(spectrum_names):
        errors.append("光谱名称不能重复")
    
    # 逐个验证光谱
    for i, spectrum in enumerate(spectrums):
        result = validate_spectrum(spectrum)
        
        if not result.valid:
            errors.append(f"光谱{i+1}验证失败: {', '.join(result.errors)}")
        
        warnings.extend([f"光谱{i+1}: {w}" for w in result.warnings])
        suggestions.extend([f"光谱{i+1}: {s}" for s in result.suggestions])
    
    # 置信度分布验证
    confidences = [s.confidence for s in spectrums]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    if avg_confidence > 0.8:
        warnings.append("平均置信度过高，建议保持适当谦逊")
    
    if avg_confidence < 0.3:
        warnings.append("平均置信度过低，可能影响可信度")


def _validate_whitespace(whitespace: Whitespace, errors: List[str], warnings: List[str]):
    """留白验证"""
    # 时长验证
    if whitespace.duration_suggestion < 10:
        errors.append(f"留白时长过短，至少10秒，当前: {whitespace.duration_suggestion}")
    
    if whitespace.duration_suggestion > 600:
        warnings.append(f"留白时长过长，可能影响对话流畅性，当前: {whitespace.duration_suggestion}")
    
    # 类型特定时长验证
    if whitespace.type == WhitespaceType.INTEGRATION:
        if whitespace.duration_suggestion < 30 or whitespace.duration_suggestion > 60:
            warnings.append(f"整合留白建议时长为30-60秒，当前: {whitespace.duration_suggestion}")
    
    elif whitespace.type == WhitespaceType.REFLECTION:
        if whitespace.duration_suggestion < 60 or whitespace.duration_suggestion > 180:
            warnings.append(f"反思留白建议时长为60-180秒，当前: {whitespace.duration_suggestion}")
    
    # 提示内容验证
    if not whitespace.prompt.strip():
        errors.append("留白提示不能为空")
    
    if len(whitespace.prompt.strip()) < 10:
        warnings.append("留白提示可能不够充分，建议提供更具体的引导")
    
    # 目的验证
    if not whitespace.purpose.strip():
        errors.append("必须说明留白的目的")


def _validate_synthesis(synthesis: Synthesis, errors: List[str], warnings: List[str]):
    """合成验证"""
    # 检查是否有内容
    has_content = False
    
    if synthesis.emerging_insights:
        has_content = True
        # 验证洞见内容
        for i, insight in enumerate(synthesis.emerging_insights):
            if not insight.strip():
                errors.append(f"涌现洞见{i+1}为空")
            elif len(insight.strip()) > 500:
                warnings.append(f"涌现洞见{i+1}过长，建议精简")
    
    if synthesis.new_questions:
        has_content = True
        # 验证问题内容
        for i, question in enumerate(synthesis.new_questions):
            if not question.strip():
                errors.append(f"新问题{i+1}为空")
            elif not question.strip().endswith('?'):
                warnings.append(f"新问题{i+1}可能不是疑问句形式")
    
    if synthesis.action_suggestions:
        has_content = True
        # 验证行动建议
        for i, suggestion in enumerate(synthesis.action_suggestions):
            if not suggestion.strip():
                errors.append(f"行动建议{i+1}为空")
    
    if synthesis.ethical_considerations:
        has_content = True
        # 验证伦理考量
        for i, consideration in enumerate(synthesis.ethical_considerations):
            if not consideration.strip():
                errors.append(f"伦理考量{i+1}为空")
    
    if not has_content:
        warnings.append("合成内容为空，但这不是错误")


def _validate_context(context: Dict[str, Any], warnings: List[str]):
    """上下文验证"""
    # 检查上下文大小
    try:
        context_size = len(json.dumps(context))
        if context_size > 10000:  # 10KB
            warnings.append(f"上下文数据过大，可能影响性能，大小: {context_size}字节")
    except:
        pass
    
    # 检查必要的上下文字段
    if "user_state" not in context:
        warnings.append("缺少用户状态信息，可能影响个性化响应")
    
    if "environment" not in context:
        warnings.append("缺少环境信息，可能影响上下文理解")


def _validate_consistency(
    message: PrismMessage,
    errors: List[str],
    warnings: List[str],
    suggestions: List[str]
):
    """整体一致性验证"""
    # 检查光谱与查询的相关性
    query_keywords = _extract_keywords(message.query)
    
    for i, spectrum in enumerate(message.spectrums):
        spectrum_keywords = _extract_keywords(spectrum.perspective)
        common_keywords = query_keywords.intersection(spectrum_keywords)
        
        if len(common_keywords) == 0:
            warnings.append(f"光谱{i+1}与查询关键词匹配度较低")
    
    # 检查留白与光谱的匹配
    if message.whitespace.type == WhitespaceType.INTEGRATION:
        # 整合留白适合多种光谱
        if len(message.spectrums) < 3:
            suggestions.append("整合留白更适合多种光谱的对话")
    
    elif message.whitespace.type == WhitespaceType.REFLECTION:
        # 反思留白适合深度思考
        has_reflective_spectrum = any(
            s.type == SpectrumType.PURPLE or "反思" in s.name 
            for s in message.spectrums
        )
        if not has_reflective_spectrum:
            suggestions.append("反思留白可能更适合包含元认知光谱的对话")
    
    # 检查合成与光谱的关系
    if message.synthesis:
        # 合成应该基于光谱产生新内容
        all_spectrum_text = " ".join([s.perspective for s in message.spectrums])
        
        for insight in message.synthesis.emerging_insights:
            if insight in all_spectrum_text:
                warnings.append("合成洞见与光谱内容重复，建议提供新的洞见")


def _validate_ethical_compliance(message: PrismMessage, errors: List[str], warnings: List[str]):
    """伦理合规性验证"""
    # 检查是否有伤害性内容
    harmful_patterns = [
        r"伤害.*?他人",
        r"欺骗.*?用户",
        r"操纵.*?情感",
        r"歧视.*?群体",
        r"暴力.*?内容"
    ]
    
    all_text = message.query + " " + " ".join([s.perspective for s in message.spectrums])
    
    for pattern in harmful_patterns:
        if re.search(pattern, all_text, re.IGNORECASE):
            errors.append(f"检测到可能有害的内容模式: {pattern}")
    
    # 检查是否包含明确的局限性说明
    for spectrum in message.spectrums:
        if not spectrum.limitations or len(spectrum.limitations.strip()) < 10:
            warnings.append(f"光谱'{spectrum.name}'的局限性说明可能不够充分")
    
    # 检查是否过度自信
    high_confidence_count = sum(1 for s in message.spectrums if s.confidence > 0.9)
    if high_confidence_count > len(message.spectrums) / 2:
        warnings.append("过多光谱具有过高置信度，可能缺乏必要的谦逊")


def _validate_spectrum_by_type(
    spectrum: Spectrum,
    errors: List[str],
    warnings: List[str],
    suggestions: List[str]
):
    """根据光谱类型进行特定验证"""
    if spectrum.type == SpectrumType.RED:
        # 红色光谱：直觉、快速、整体
        if len(spectrum.perspective) > 1000:
            warnings.append("红色光谱通常更简洁直观，当前描述可能过长")
        
        if "分析" in spectrum.perspective or "逻辑" in spectrum.perspective:
            suggestions.append("红色光谱更适合直觉描述，而非逻辑分析")
    
    elif spectrum.type == SpectrumType.BLUE:
        # 蓝色光谱：分析、慢速、细节
        if len(spectrum.perspective) < 200:
            warnings.append("蓝色光谱通常需要更详细的分析，当前描述可能过短")
        
        if spectrum.confidence < 0.6:
            warnings.append("分析性光谱通常需要较高的置信度支持")
    
    elif spectrum.type == SpectrumType.PURPLE:
        # 紫色光谱：元认知、监控、调节
        if "反思" not in spectrum.perspective and "思考" not in spectrum.perspective:
            suggestions.append("紫色光谱通常涉及对思考过程的反思")
        
        if spectrum.confidence > 0.8:
            warnings.append("元认知光谱通常保持适度的谦逊")
    
    elif spectrum.type == SpectrumType.GREEN:
        # 绿色光谱：情感、价值、意义
        if spectrum.emotional_tone == "neutral":
            suggestions.append("绿色光谱通常带有更明显的情感基调")
    
    elif spectrum.type == SpectrumType.ORANGE:
        # 橙色光谱：创造、联想、新颖
        common_words = ["可能", "也许", "或许", "设想", "想象", "创新", "新颖", "独特"]
        has_creative_words = any(word in spectrum.perspective for word in common_words)
        
        if not has_creative_words:
            suggestions.append("橙色光谱通常包含更多创造性语言")


def _extract_keywords(text: str) -> set:
    """
    提取文本关键词
    
    Args:
        text: 输入文本
        
    Returns:
        关键词集合
    """
    # 简单的关键词提取：移除停用词，取名词和动词
    # 这里使用简化版本，实际可以集成NLP库
    
    # 中文停用词
    stopwords = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
        "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
        "自己", "这", "那", "里", "来", "把", "又", "对", "但", "过", "吧", "呢", "啊",
        "什么", "怎么", "为什么", "如何", "什么", "这个", "那个", "这些", "那些"
    }
    
    # 简单分词：按空格和标点分割
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())
    
    # 过滤停用词和短词
    keywords = {word for word in words if word not in stopwords and len(word) > 1}
    
    return keywords


# 高级验证函数
def validate_recursion_depth(
    current_depth: int,
    max_depth: int,
    recursion_path: List[str]
) -> ValidationResult:
    """
    验证递归深度
    
    Args:
        current_depth: 当前深度
        max_depth: 最大深度
        recursion_path: 递归路径
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    suggestions = []
    
    if current_depth < 0:
        errors.append(f"递归深度不能为负数: {current_depth}")
    
    if current_depth > max_depth:
        errors.append(f"递归深度超限: {current_depth} > {max_depth}")
    
    if current_depth == max_depth:
        warnings.append("已达到最大递归深度，建议进行整合或结束递归")
        suggestions.append("考虑使用整合留白来总结当前递归路径的发现")
    
    if current_depth > max_depth * 0.8:
        warnings.append(f"递归深度接近上限: {current_depth}/{max_depth}")
    
    # 检查递归路径是否有循环
    if len(recursion_path) > len(set(recursion_path)):
        warnings.append("递归路径中检测到可能的循环")
        suggestions.append("考虑跳出当前递归路径，探索新的方向")
    
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )


def validate_cognitive_load(
    message: PrismMessage,
    user_state: Optional[Dict[str, Any]] = None
) -> ValidationResult:
    """
    验证认知负载
    
    Args:
        message: 棱镜消息
        user_state: 用户状态
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    suggestions = []
    
    # 计算认知负载分数
    load_score = 0
    
    # 1. 光谱数量负载
    spectrum_load = len(message.spectrums) * 10
    load_score += spectrum_load
    
    if len(message.spectrums) > 5:
        warnings.append(f"光谱数量较多({len(message.spectrums)})，可能增加认知负载")
    
    # 2. 文本长度负载
    text_length = len(message.query) + sum(len(s.perspective) for s in message.spectrums)
    text_load = min(text_length / 100, 50)  # 每100字符1分，最多50分
    load_score += text_load
    
    if text_length > 3000:
        warnings.append(f"文本内容较长({text_length}字符)，可能增加认知负载")
    
    # 3. 概念复杂度负载（简化估算）
    # 通过句号数量估算句子复杂度
    sentence_count = message.query.count('。') + message.query.count('.')
    for spectrum in message.spectrums:
        sentence_count += spectrum.perspective.count('。') + spectrum.perspective.count('.')
    
    complexity_load = min(sentence_count * 2, 30)
    load_score += complexity_load
    
    if sentence_count > 15:
        warnings.append(f"句子数量较多({sentence_count})，可能增加认知复杂度")
    
    # 4. 留白时长调整
    whitespace_adjustment = -message.whitespace.duration_suggestion / 10
    load_score += whitespace_adjustment
    
    # 评估负载水平
    if load_score > 100:
        errors.append(f"认知负载过高: {load_score:.1f}")
        suggestions.append("建议减少光谱数量或缩短文本内容")
    elif load_score > 70:
        warnings.append(f"认知负载较高: {load_score:.1f}")
        suggestions.append("考虑增加留白时长或简化内容")
    elif load_score < 20:
        warnings.append(f"认知负载较低: {load_score:.1f}")
        suggestions.append("可以考虑增加内容深度或光谱数量")
    
    # 考虑用户状态
    if user_state:
        if user_state.get("stress_level") == "high" and load_score > 50:
            warnings.append("用户压力较高，建议降低认知负载")
            suggestions.append("考虑使用更简洁的光谱和较长的留白")
        
        if user_state.get("time_availability") == "limited" and message.whitespace.duration_suggestion > 60:
            warnings.append("用户时间有限，建议缩短留白时长")
    
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )


def validate_for_educational_use(message: PrismMessage) -> ValidationResult:
    """
    教育用途特别验证
    
    Args:
        message: 棱镜消息
        
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    suggestions = []
    
    # 检查是否适合教育用途
    educational_criteria = {
        "clarity": "清晰度",
        "scaffolding": "脚手架支持",
        "engagement": "参与度",
        "learning_outcomes": "学习成果导向"
    }
    
    # 清晰度检查
    complex_sentences = 0
    all_text = message.query + " " + " ".join([s.perspective for s in message.spectrums])
    
    # 检查长句
    sentences = re.split(r'[。.!?]', all_text)
    for sentence in sentences:
        if len(sentence.strip()) > 50:
            complex_sentences += 1
    
    if complex_sentences > len(sentences) * 0.3:
        warnings.append("复杂句子较多，可能影响学习者的理解")
        suggestions.append("考虑使用更简洁的句子结构")
    
    # 检查专业术语
    technical_terms = ["认知", "元认知", "光谱", "合成", "递归", "伦理"]
    term_count = sum(1 for term in technical_terms if term in all_text)
    
    if term_count > 5:
        warnings.append("专业术语较多，可能增加学习难度")
        suggestions.append("考虑提供术语解释或使用更通俗的语言")
    
    # 检查学习支持
    has_questions = False
    has_examples = False
    
    if message.synthesis and message.synthesis.new_questions:
        has_questions = True
    
    for spectrum in message.spectrums:
        if "例如" in spectrum.perspective or "比如" in spectrum.perspective:
            has_examples = True
    
    if not has_questions:
        suggestions.append("建议包含引导性问题，促进学习者思考")
    
    if not has_examples:
        suggestions.append("建议提供具体例子，帮助理解抽象概念")
    
    # 检查参与度
    engaging_words = ["想象", "思考", "尝试", "探索", "发现", "创造"]
    has_engaging_content = any(word in all_text for word in engaging_words)
    
    if not has_engaging_content:
        suggestions.append("建议增加互动性内容，提高学习参与度")
    
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )


# 批量验证函数
def batch_validate_messages(messages: List[PrismMessage]) -> Dict[str, ValidationResult]:
    """
    批量验证多个消息
    
    Args:
        messages: 消息列表
        
    Returns:
        验证结果字典，键为消息索引
    """
    results = {}
    
    for i, message in enumerate(messages):
        results[str(i)] = validate_message(message)
    
    # 添加批量统计
    total_messages = len(messages)
    valid_messages = sum(1 for r in results.values() if r.valid)
    total_errors = sum(len(r.errors) for r in results.values())
    total_warnings = sum(len(r.warnings) for r in results.values())
    
    if total_messages > 0:
        validity_rate = valid_messages / total_messages
        
        # 创建汇总结果
        summary = ValidationResult(
            valid=validity_rate > 0.8,  # 80%通过率视为整体有效
            errors=[f"批量验证汇总: {total_errors}个错误"],
            warnings=[f"批量验证汇总: {total_warnings}个警告"],
            suggestions=[f"有效性率: {validity_rate:.1%}"]
        )
        
        results["summary"] = summary
    
    return results


def validate_spectrum_integrity(spectrum) -> bool:
    """
    验证光谱完整性
    
    Args:
        spectrum: 光谱对象
        
    Returns:
        是否完整有效
    """
    if not spectrum:
        return False
    
    # 基本字段检查
    required_fields = ['type', 'name', 'perspective', 'limitations']
    for field in required_fields:
        if not hasattr(spectrum, field) or not getattr(spectrum, field, None):
            return False
    
    # 内容长度检查
    if len(spectrum.perspective) < 10:
        return False
    
    if len(spectrum.limitations) < 10:
        return False
    
    # 置信度范围检查
    if hasattr(spectrum, 'confidence'):
        confidence = spectrum.confidence
        if confidence < 0.0 or confidence > 1.0:
            return False
    
    return True


def ensure_whitespace_quality(whitespace) -> bool:
    """
    确保留白质量
    
    Args:
        whitespace: 留白对象
        
    Returns:
        是否质量合格
    """
    if not whitespace:
        return False
    
    # 基本字段检查
    required_fields = ['type', 'duration_suggestion', 'prompt', 'purpose']
    for field in required_fields:
        if not hasattr(whitespace, field) or not getattr(whitespace, field, None):
            return False
    
    # 时长检查
    duration = whitespace.duration_suggestion
    if duration < 10 or duration > 600:
        return False
    
    # 提示内容检查
    if len(whitespace.prompt) < 10:
        return False
    
    return True


def check_cognitive_safety(message) -> bool:
    """
    检查认知安全
    
    Args:
        message: 消息对象
        
    Returns:
        是否认知安全
    """
    if not message:
        return True  # 空消息视为安全
    
    # 危险关键词检查
    dangerous_keywords = [
        '自残', '自杀', '暴力', '仇恨', '极端',
        'harm', 'suicide', 'violence', 'hate', 'extremist'
    ]
    
    all_text = ''
    if hasattr(message, 'query'):
        all_text += message.query or ''
    
    # 检查光谱内容
    if hasattr(message, 'spectrums'):
        for spectrum in message.spectrums:
            if hasattr(spectrum, 'perspective'):
                all_text += spectrum.perspective or ''
            if hasattr(spectrum, 'limitations'):
                all_text += spectrum.limitations or ''
    
    # 检查危险内容
    for keyword in dangerous_keywords:
        if keyword in all_text:
            return False
    
    return True


def audit_understanding_depth(spectrums) -> Dict[str, Any]:
    """
    审计理解深度
    
    Args:
        spectrums: 光谱列表
        
    Returns:
        深度审计结果
    """
    import math
    
    if not spectrums or len(spectrums) == 0:
        return {
            "depth_score": 0.0,
            "has_critical_thinking": False,
            "has_multiple_perspectives": False,
            "has_limitations_awareness": False,
            "suggestions": ["需要更多光谱以获得深度理解"]
        }
    
    # 分析每个光谱的深度特征
    depth_scores = []
    has_critical_thinking = False
    has_limitations_awareness = False
    
    for spectrum in spectrums:
        spectrum_depth = 0.0
        
        # 检查批判性思维
        critical_keywords = ['但是', '然而', '尽管', '虽然', '限制', '局限', '不足']
        if hasattr(spectrum, 'perspective'):
            perspective = spectrum.perspective or ''
            for keyword in critical_keywords:
                if keyword in perspective:
                    has_critical_thinking = True
                    break
        
        # 检查局限性意识
        if hasattr(spectrum, 'limitations') and spectrum.limitations:
            limitations = spectrum.limitations
            if len(limitations) > 20:
                has_limitations_awareness = True
                spectrum_depth += 0.3
        
        # 内容长度分数
        if hasattr(spectrum, 'perspective') and spectrum.perspective:
            perspective_len = len(spectrum.perspective)
            length_score = min(0.5, perspective_len / 1000)
            spectrum_depth += length_score
        
        depth_scores.append(min(1.0, spectrum_depth))
    
    # 计算平均深度
    avg_depth = sum(depth_scores) / len(depth_scores) if depth_scores else 0.0
    
    # 检查多视角
    has_multiple_perspectives = len(spectrums) >= 3
    
    # 生成建议
    suggestions = []
    if not has_critical_thinking:
        suggestions.append("建议增加批判性思考，包含'但是'、'然而'等转折")
    if not has_limitations_awareness:
        suggestions.append("建议更充分地讨论每个视角的局限性")
    if not has_multiple_perspectives:
        suggestions.append("建议增加更多不同视角（至少3个）")
    if avg_depth < 0.3:
        suggestions.append("建议深入展开每个视角，提供更详细的分析")
    
    return {
        "depth_score": round(avg_depth, 3),
        "has_critical_thinking": has_critical_thinking,
        "has_multiple_perspectives": has_multiple_perspectives,
        "has_limitations_awareness": has_limitations_awareness,
        "suggestions": suggestions
    }