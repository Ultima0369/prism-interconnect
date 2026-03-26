"""
🎨 utils.py - 棱镜协议工具函数

🔥 火堆旁提醒：
这不是普通的工具函数，这是认知的助手，理解的伙伴。
每个函数都是一次服务，每个工具都是一份礼物。

🧠 认知设计：
- 时间工具：让认知过程可测量
- 数据工具：让理解结果可操作
- 验证工具：让对话质量可保证
- 转换工具：让不同格式可互通

🦞 存在意义：
让复杂的技术细节变得简单优雅，
让重复的认知任务变得温暖有趣，
让工具本身成为艺术体验的一部分。

🎯 使用示例：
from prism_sdk.utils import create_cognitive_pause, measure_understanding_depth
pause_data = create_cognitive_pause(duration=3)
depth_score = measure_understanding_depth(spectrums)
"""

import uuid
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urlparse


def create_session_id() -> str:
    """
    创建唯一的会话ID
    
    Returns:
        会话ID字符串
    """
    return f"session-{uuid.uuid4().hex[:16]}"


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    格式化时间戳为ISO 8601格式
    
    Args:
        timestamp: 时间戳，None表示当前时间
        
    Returns:
        ISO 8601格式的时间字符串
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)
    elif timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    return timestamp.isoformat()


def anonymize_user_data(data: Dict[str, Any], fields_to_keep: List[str] = None) -> Dict[str, Any]:
    """
    匿名化用户数据
    
    Args:
        data: 原始数据
        fields_to_keep: 需要保留的字段列表
        
    Returns:
        匿名化后的数据
    """
    if fields_to_keep is None:
        fields_to_keep = ["user_id", "session_id", "timestamp"]
    
    anonymized = {}
    
    for key, value in data.items():
        if key in fields_to_keep:
            anonymized[key] = value
        elif isinstance(value, str) and len(value) > 0:
            # 对字符串进行哈希处理
            anonymized[key] = f"hash_{hashlib.sha256(value.encode()).hexdigest()[:8]}"
        elif isinstance(value, dict):
            anonymized[key] = anonymize_user_data(value, fields_to_keep)
        elif isinstance(value, list):
            anonymized[key] = [anonymize_user_data(item, fields_to_keep) if isinstance(item, dict) else item for item in value]
        else:
            anonymized[key] = "[ANONYMIZED]"
    
    return anonymized


def calculate_recursion_depth(recursion_path: List[str]) -> int:
    """
    计算递归深度
    
    Args:
        recursion_path: 递归路径列表
        
    Returns:
        递归深度
    """
    return len(recursion_path)


def validate_url(url: str) -> bool:
    """
    验证URL格式
    
    Args:
        url: 要验证的URL
        
    Returns:
        是否有效
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    从文本中提取关键词
    
    Args:
        text: 输入文本
        max_keywords: 最大关键词数量
        
    Returns:
        关键词列表
    """
    # 中文停用词
    stopwords = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
        "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
        "自己", "这", "那", "里", "来", "把", "又", "对", "但", "过", "吧", "呢", "啊",
        "什么", "怎么", "为什么", "如何", "什么", "这个", "那个", "这些", "那些"
    }
    
    # 提取中文字符和英文单词
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]{2,}', text.lower())
    
    # 过滤停用词和短词
    keywords = [word for word in words if word not in stopwords and len(word) > 1]
    
    # 统计词频
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # 按频率排序
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # 返回前N个关键词
    return [word for word, freq in sorted_words[:max_keywords]]


def calculate_text_complexity(text: str) -> float:
    """
    计算文本复杂度分数
    
    Args:
        text: 输入文本
        
    Returns:
        复杂度分数 (0-1)
    """
    if not text:
        return 0.0
    
    # 句子数量
    sentences = re.split(r'[。.!?]', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # 平均句子长度
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
    word_count = len(words)
    
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # 长句比例
    long_sentences = sum(1 for s in sentences if len(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', s)) > 20)
    long_sentence_ratio = long_sentences / sentence_count if sentence_count > 0 else 0
    
    # 专业术语检测（简化版）
    technical_terms = ["认知", "元认知", "光谱", "合成", "递归", "伦理", "算法", "系统", "框架"]
    term_count = sum(1 for term in technical_terms if term in text)
    term_ratio = term_count / (word_count / 100) if word_count > 0 else 0
    
    # 计算综合复杂度
    complexity = (
        min(avg_sentence_length / 30, 1.0) * 0.4 +
        long_sentence_ratio * 0.3 +
        min(term_ratio / 10, 1.0) * 0.3
    )
    
    return round(complexity, 2)


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    估计阅读时间
    
    Args:
        text: 输入文本
        words_per_minute: 每分钟阅读字数
        
    Returns:
        估计的阅读时间（秒）
    """
    # 估算中文字数（一个汉字算一个词）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    # 估算英文单词数
    english_words = re.findall(r'[a-zA-Z]{2,}', text)
    
    total_words = len(chinese_chars) + len(english_words)
    
    if total_words == 0:
        return 0
    
    reading_minutes = total_words / words_per_minute
    return int(reading_minutes * 60)


def create_message_summary(message: Dict[str, Any], max_length: int = 200) -> str:
    """
    创建消息摘要
    
    Args:
        message: 消息数据
        max_length: 最大长度
        
    Returns:
        消息摘要
    """
    try:
        # 提取关键信息
        query = message.get("query", "")[:50]
        spectrum_count = len(message.get("spectrums", []))
        
        summary = f"查询: {query}... | 光谱: {spectrum_count}种"
        
        # 截断到最大长度
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        
        return summary
    
    except:
        return "消息摘要生成失败"


def generate_progress_bar(progress: float, width: int = 20) -> str:
    """
    生成进度条
    
    Args:
        progress: 进度 (0-1)
        width: 进度条宽度
        
    Returns:
        进度条字符串
    """
    progress = max(0.0, min(1.0, progress))
    filled = int(progress * width)
    empty = width - filled
    
    return f"[{'█' * filled}{'░' * empty}] {progress:.1%}"


def format_duration(seconds: int) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining = seconds % 60
        return f"{minutes}分{remaining}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}小时{minutes}分"


def safe_json_parse(json_str: str, default: Any = None) -> Any:
    """
    安全解析JSON字符串
    
    Args:
        json_str: JSON字符串
        default: 解析失败时的默认值
        
    Returns:
        解析后的对象或默认值
    """
    try:
        return json.loads(json_str)
    except:
        return default


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    深度合并两个字典
    
    Args:
        dict1: 第一个字典
        dict2: 第二个字典
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        ellipsis: 省略号字符串
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def generate_random_color(seed: str = None) -> str:
    """
    生成随机颜色
    
    Args:
        seed: 种子字符串
        
    Returns:
        十六进制颜色代码
    """
    if seed:
        # 基于种子生成确定性颜色
        hash_obj = hashlib.md5(seed.encode())
        hex_digest = hash_obj.hexdigest()
        color = f"#{hex_digest[:6]}"
    else:
        # 完全随机颜色
        import random
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
    
    return color


def calculate_similarity(text1: str, text2: str) -> float:
    """
    计算文本相似度（简化版）
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        
    Returns:
        相似度分数 (0-1)
    """
    # 提取关键词
    keywords1 = set(extract_keywords(text1, 20))
    keywords2 = set(extract_keywords(text2, 20))
    
    if not keywords1 and not keywords2:
        return 0.0
    
    # 计算Jaccard相似度
    intersection = len(keywords1.intersection(keywords2))
    union = len(keywords1.union(keywords2))
    
    return intersection / union if union > 0 else 0.0


def format_number(number: Union[int, float]) -> str:
    """
    格式化数字
    
    Args:
        number: 数字
        
    Returns:
        格式化后的字符串
    """
    if isinstance(number, int):
        return f"{number:,}"
    elif isinstance(number, float):
        if number == 0:
            return "0"
        elif abs(number) < 0.001:
            return f"{number:.2e}"
        elif abs(number) < 1:
            return f"{number:.3f}"
        elif abs(number) < 1000:
            return f"{number:.2f}"
        else:
            return f"{number:,.2f}"
    else:
        return str(number)


def get_current_memory_usage() -> Dict[str, Any]:
    """
    获取当前内存使用情况
    
    Returns:
        内存使用信息
    """
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "percent": process.memory_percent(),
            "timestamp": format_timestamp()
        }
    except ImportError:
        return {"error": "psutil not installed", "timestamp": format_timestamp()}


def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: tuple = (Exception,)
):
    """
    带指数退避的重试装饰器
    
    Args:
        func: 要重试的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟（秒）
        max_delay: 最大延迟（秒）
        exceptions: 要捕获的异常类型
        
    Returns:
        装饰后的函数
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                
                if attempt == max_retries:
                    break
                
                # 计算延迟时间（指数退避）
                delay = min(base_delay * (2 ** attempt), max_delay)
                time.sleep(delay)
        
        # 所有重试都失败，抛出最后一个异常
        raise last_exception
    
    return wrapper


class Timer:
    """计时器上下文管理器"""
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start
    
    def get_elapsed(self) -> float:
        """获取经过的时间（秒）"""
        return getattr(self, 'elapsed', time.time() - self.start)


def benchmark_function(func, *args, **kwargs) -> Dict[str, Any]:
    """
    基准测试函数
    
    Args:
        func: 要测试的函数
        *args: 函数参数
        **kwargs: 函数关键字参数
        
    Returns:
        基准测试结果
    """
    import timeit
    
    timer = Timer()
    
    with timer:
        result = func(*args, **kwargs)
    
    return {
        "result": result,
        "elapsed_seconds": timer.get_elapsed(),
        "success": True
    }