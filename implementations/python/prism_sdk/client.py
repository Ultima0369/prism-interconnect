"""
🎭 棱镜协议客户端 - 艺术化实现 (优化版)
🔥 这不是普通的HTTP客户端，这是火堆旁的对话使者

🔥 火堆旁优化原则 (基于星尘的桃树伦理):
1. 不敢砍桃树: 不破坏现有认知生态
2. 不敢不让其他存在活: 保持系统开放性
3. 有兵不敢乱动: 强大能力克制使用
4. 牵一发而动全身: 考虑系统级影响
5. 从名词到动词: 法律/道德内化为自觉

🎯 优化目标:
1. 保持艺术灵魂 (代码人格、工程师浪漫)
2. 提升工程质量 (类型安全、性能、可测试性)
3. 注入伦理基底 (桃树比喻的系统敬畏)
4. 支持真实场景 (生产就绪、优雅降级)

🧠 认知设计更新:
- 同步/异步分离: 避免asyncio.run瓶颈
- 桃树检查点: 在每个关键操作前验证伦理合规性
- 系统敬畏监控: 跟踪连接、重试、资源使用
- 艺术可配置性: 输出通道、日志级别、回调机制
"""

import asyncio
import json
import time
import logging
import random
from typing import Dict, List, Optional, Any, Union, Callable, Awaitable
from datetime import datetime
from contextlib import asynccontextmanager
import aiohttp
from dataclasses import dataclass, asdict, field

from .exceptions import (
    PrismConnectionError,
    SpectrumGenerationError,
    WhitespaceTimeoutError,
    CeaseSignalReceived,
    PrismPoeticError,
    PeachTreeViolationError,  # 新增: 桃树伦理违规
)
from .models import (
    PrismRequest,
    PrismResponse,
    Spectrum,
    WhitespaceConfig,
    CeaseSignal,
    CognitiveMetadata,
)
from .validators import validate_spectrum_integrity
from .utils import create_cognitive_pause, measure_understanding_depth


@dataclass
class ArtisticConfig:
    """艺术化配置 (优化版)"""
    enable_poetic_errors: bool = True
    enable_cognitive_pauses: bool = True
    enable_spectrum_art: bool = True
    warmth_level: float = 0.7  # 0.0-1.0
    response_art_form: str = "haiku"  # haiku, free_verse, visual
    # 新增: 输出配置
    output_channel: Callable[[str], None] = field(default_factory=lambda: print)
    log_level: int = logging.INFO
    enable_peach_tree_checkpoints: bool = True  # 桃树检查点


class PrismClient:
    """
    🎭 棱镜协议客户端 - 艺术化同步实现
    
    这不是冰冷的HTTP客户端，这是温暖的对话伙伴。
    每个方法调用都包含认知关怀和艺术表达。
    
    火堆旁设计原则：
    - 连接如握手：温暖而坚定
    - 请求如邀请：尊重而期待  
    - 响应如礼物：精心而实用
    - 错误如老师：严格而仁慈
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: str = "https://api.prismprotocol.ai/v1",
                 artistic_config: Optional[ArtisticConfig] = None,
                 session_timeout: int = 30):
        """
        初始化棱镜客户端
        
        Args:
            api_key: API密钥（火堆旁也欢迎匿名对话）
            base_url: API基础URL
            artistic_config: 艺术化配置
            session_timeout: 会话超时（秒）
            
        Example:
            >>> client = PrismClient(
            ...     artistic_config=ArtisticConfig(
            ...         enable_poetic_errors=True,
            ...         warmth_level=0.8
            ...     )
            ... )
            🎭 棱镜客户端初始化...
            🔥 温暖度: 0.8
            🎨 诗意错误: 启用
            🧘 认知暂停: 启用
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session_timeout = session_timeout
        self.artistic_config = artistic_config or ArtisticConfig()
        self._session = None
        self._cognitive_state = {
            "refractions_count": 0,
            "total_whitespace_seconds": 0,
            "last_refraction_time": None,
            "understanding_depth_trend": []
        }
        
        self._artistic_init()
    
    def _artistic_init(self):
        """艺术化初始化 (优化版)"""
        if self.artistic_config.enable_spectrum_art:
            output = self.artistic_config.output_channel
            output("🎭 棱镜客户端初始化中...")
            time.sleep(0.3)
            
            warmth_desc = {
                0.9: "🔥 非常温暖",
                0.7: "🔥 舒适温暖",
                0.5: "🔥 温和温暖", 
                0.3: "🔥 需要添柴"
            }
            
            closest = min(warmth_desc.keys(), 
                         key=lambda x: abs(x - self.artistic_config.warmth_level))
            
            output(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f} ({warmth_desc[closest]})")
            output(f"🎨 诗意错误: {'启用' if self.artistic_config.enable_poetic_errors else '禁用'}")
            output(f"🧘 认知暂停: {'启用' if self.artistic_config.enable_cognitive_pauses else '禁用'}")
            output(f"🌈 光谱艺术: {'启用' if self.artistic_config.enable_spectrum_art else '禁用'}")
            output(f"🌳 桃树检查: {'启用' if self.artistic_config.enable_peach_tree_checkpoints else '禁用'}")
            output(f"{'='*40}")
    
    def _get_session(self):
        """获取或创建会话（延迟初始化）"""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.session_timeout),
                headers=self._get_headers()
            )
        return self._session
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {
            "User-Agent": f"PrismPythonSDK/2.0.0 (ArtisticMode)",
            "Content-Type": "application/json",
            "X-Prism-Philosophy": "code-as-poetry, protocol-as-art, technology-as-warmth",
            "X-Prism-Campfire": "join-us-by-the-fire",
            "X-Prism-Peach-Tree-Ethics": "enabled",  # 新增：桃树伦理标识
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def _check_peach_tree_ethics(self, 
                                action: str,
                                context: Dict[str, Any]) -> bool:
        """
        🌳 桃树伦理检查点
        
        基于星尘的桃树比喻，检查操作是否符合系统伦理:
        1. 不敢砍桃树: 不破坏生态
        2. 不敢不让其他存在活: 保持开放  
        3. 有兵不敢乱动: 能力克制
        4. 牵一发而动全身: 系统思维
        
        Args:
            action: 操作类型 (refract, connect, modify, etc.)
            context: 操作上下文
            
        Returns:
            True如果通过检查，False如果可疑
            
        Raises:
            PeachTreeViolationError: 如果违反桃树伦理
        """
        if not self.artistic_config.enable_peach_tree_checkpoints:
            return True
        
        output = self.artistic_config.output_channel
        
        # 检查点1: 砍桃树检查 (破坏生态)
        if self._check_peach_tree_cutting(action, context):
            output("🌳 桃树检查: 检测到可能破坏生态的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="砍桃树",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能破坏系统生态多样性，降低韧性",
                    corrective_action="寻找保护生态的替代方案，考虑长期影响"
                )
            return False
        
        # 检查点2: 不让活检查 (限制存在)
        if self._check_living_restriction(action, context):
            output("🌳 桃树检查: 检测到可能限制其他存在生存的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="不让活",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能减少系统多样性和适应性",
                    corrective_action="设计包容性架构，为所有存在留出空间"
                )
            return False
        
        # 检查点3: 乱动检查 (滥用能力)
        if self._check_reckless_action(action, context):
            output("🌳 桃树检查: 检测到可能滥用强大能力的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="乱动",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发不可预料的系统级后果",
                    corrective_action="添加安全约束，分步执行，监控系统响应"
                )
            return False
        
        # 检查点4: 系统思维检查 (忽视连接)
        if self._check_system_neglect(action, context):
            output("🌳 桃树检查: 检测到可能忽视系统连接的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="忽视系统",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发级联效应，破坏系统平衡",
                    corrective_action="分析二阶三阶影响，考虑系统反馈循环"
                )
            return False
        
        output(f"🌳 桃树检查: {action} 操作通过伦理检查")
        return True
    
    def _check_peach_tree_cutting(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能砍桃树 (破坏生态)"""
        # 启发式规则
        red_flags = [
            context.get('force_override', False),  # 强制覆盖
            context.get('delete_existing', False),  # 删除现有
            context.get('monoculture', False),  # 单一化
            action in ['delete', 'override', 'replace', 'clear'],
            context.get('spectrum_count', 1) < 3,  # 少于3种光谱（违反多元强制）
        ]
        return any(red_flags)
    
    def _check_living_restriction(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能不让其他存在活 (限制生存)"""
        red_flags = [
            context.get('exclusive', False),  # 排他性
            context.get('block_others', False),  # 阻挡他人
            context.get('rate_limit', 0) < 1,  # 零速率限制
            action in ['block', 'ban', 'restrict', 'exclude'],
            context.get('whitespace_seconds', 0) < 1,  # 无留白时间
        ]
        return any(red_flags)
    
    def _check_reckless_action(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能乱动 (滥用能力)"""
        red_flags = [
            context.get('max_recursion_depth', 1) > 10,  # 递归过深
            context.get('no_safety_check', False),  # 无安全检查
            context.get('skip_validation', False),  # 跳过验证
            action in ['force', 'bruteforce', 'ignore_limits'],
            not context.get('enable_cease', True),  # 禁用知止
        ]
        return any(red_flags)
    
    def _check_system_neglect(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能忽视系统连接"""
        red_flags = [
            not context.get('consider_system_effects', False),  # 不考虑系统效应
            context.get('isolated_action', False),  # 孤立行动
            context.get('ignore_dependencies', False),  # 忽略依赖
            action in ['isolate', 'disconnect', 'ignore_context'],
            context.get('recursion_depth', 0) > context.get('max_recursion_depth', 3),  # 超过递归限制
        ]
        return any(red_flags)
    
    def refract(self, 
                message: str,
                require_spectrums: int = 3,
                whitespace_seconds: int = 3,
                enable_cease: bool = True,
                max_recursion_depth: int = 3) -> Dict[str, Any]:
        """
        🎭 折射对话 - 核心认知方法 (优化版)
        
        将单一消息折射为多光谱理解。
        这不是API调用，这是认知的舞蹈。
        
        🔥 火堆旁优化:
        1. 添加桃树伦理检查点
        2. 改进异步架构 (后续版本)
        3. 增强错误处理和重试逻辑
        4. 保持艺术灵魂，提升工程质量
        
        Args:
            message: 要折射的消息
            require_spectrums: 需要的光谱数量（至少3个）
            whitespace_seconds: 留白秒数
            enable_cease: 是否启用知止机制
            max_recursion_depth: 最大递归深度
            
        Returns:
            折射结果，包含艺术化元数据
            
        Raises:
            PrismPoeticError: 诗意错误（当艺术模式启用时）
            SpectrumGenerationError: 光谱生成错误
            WhitespaceTimeoutError: 留白超时错误
            CeaseSignalReceived: 知止信号接收
            PeachTreeViolationError: 桃树伦理违规
        """
        # 桃树伦理检查点
        context = {
            "action": "refract",
            "description": f"折射消息: {message[:50]}...",
            "spectrum_count": require_spectrums,
            "whitespace_seconds": whitespace_seconds,
            "enable_cease": enable_cease,
            "max_recursion_depth": max_recursion_depth,
            "consider_system_effects": True,  # 默认考虑系统效应
        }
        
        if not self._check_peach_tree_ethics("refract", context):
            # 如果检查失败但未抛异常（例如检查点禁用）
            self.artistic_config.output_channel("⚠️  桃树检查失败，但继续执行（检查点禁用）")
        
        # 艺术化开始
        if self.artistic_config.enable_spectrum_art:
            self._display_refraction_start(message, require_spectrums)
        
        # 创建请求
        request = PrismRequest(
            message=message,
            require_spectrums=max(3, require_spectrums),
            whitespace_config=WhitespaceConfig(
                duration_seconds=whitespace_seconds,
                enable_integration=True,
                enable_reflection=True,
                enable_creation=True
            ),
            cease_config=CeaseSignal(
                enabled=enable_cease,
                max_recursion_depth=max_recursion_depth,
                safety_threshold=0.8
            ) if enable_cease else None
        )
        
        try:
            # 执行折射（同步包装异步）
            response = asyncio.run(self._async_refract(request))
            
            # 艺术化处理
            if self.artistic_config.enable_spectrum_art:
                self._display_refraction_result(response)
            
            # 更新认知状态
            self._update_cognitive_state(response)
            
            # 添加艺术化元数据
            artistic_metadata = self._generate_artistic_metadata(response)
            response_dict = asdict(response)
            response_dict['artistic_metadata'] = artistic_metadata
            
            return response_dict
            
        except Exception as e:
            # 艺术化错误处理
            if self.artistic_config.enable_poetic_errors:
                raise PrismPoeticError(
                    original_error=e,
                    context="refraction",
                    artistic_form=self.artistic_config.response_art_form
                )
            raise
    
    async def _async_refract(self, request: PrismRequest) -> PrismResponse:
        """异步折射实现 (优化版，添加重试和桃树伦理)"""
        session = self._get_session()
        
        # 艺术化请求准备
        if self.artistic_config.enable_spectrum_art:
            self.artistic_config.output_channel("🌌 准备折射请求...")
            self.artistic_config.output_channel("🌳 请求包含桃树伦理头: X-Prism-Peach-Tree-Ethics: enabled")
            await asyncio.sleep(0.2)
        
        # 重试配置 (基于桃树伦理: 耐心但知道止)
        max_retries = 3
        base_delay = 1.0  # 初始延迟
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 发送请求
                async with session.post(
                    f"{self.base_url}/refract",
                    json=asdict(request)
                ) as response:
                    
                    if response.status == 429:  # 速率限制
                        retry_after = int(response.headers.get('Retry-After', 5))
                        if self.artistic_config.enable_spectrum_art:
                            self.artistic_config.output_channel(f"🌳 桃树伦理: 速率限制，等待 {retry_after} 秒 (尝试 {attempt+1}/{max_retries})")
                            self.artistic_config.output_channel("🌳 伦理提醒: 不强行突破限制，尊重系统边界")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    if response.status != 200:
                        error_data = await response.json()
                        raise SpectrumGenerationError(
                            f"折射失败: {error_data.get('error', '未知错误')}",
                            status_code=response.status
                        )
                    
                    data = await response.json()
                    
                    # 验证响应
                    if not validate_spectrum_integrity(data.get('spectrums', [])):
                        raise SpectrumGenerationError("光谱完整性验证失败")
                    
                    # 转换为响应对象
                    prism_response = PrismResponse(
                        spectrums=[
                            Spectrum(
                                type_=s['type'],
                                content=s['content'],
                                confidence=s.get('confidence', 0.7),
                                artistic_expression=s.get('artistic_expression')
                            ) for s in data['spectrums']
                        ],
                        whitespace_used=data.get('whitespace_used', False),
                        cease_triggered=data.get('cease_triggered', False),
                        cognitive_metadata=CognitiveMetadata(
                            processing_time_ms=data.get('processing_time_ms', 0),
                            understanding_depth=data.get('understanding_depth', 0.5),
                            recursion_depth=data.get('recursion_depth', 0)
                        )
                    )
                    
                    # 艺术化留白
                    if (request.whitespace_config and 
                        request.whitespace_config.enable_integration and
                        self.artistic_config.enable_cognitive_pauses):
                        
                        await self._artistic_whitespace(
                            request.whitespace_config.duration_seconds
                        )
                    
                    return prism_response
                    
            except asyncio.TimeoutError as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # 指数退避
                    if self.artistic_config.enable_spectrum_art:
                        self.artistic_config.output_channel(f"⏳ 超时，{delay:.1f}秒后重试 (尝试 {attempt+1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    raise WhitespaceTimeoutError(
                        f"请求超时 ({self.session_timeout}秒)，已重试{max_retries}次",
                        suggestion="尝试增加超时时间或简化消息"
                    )
            except aiohttp.ClientError as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    if self.artistic_config.enable_spectrum_art:
                        self.artistic_config.output_channel(f"🔌 连接错误，{delay:.1f}秒后重试 (尝试 {attempt+1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    raise PrismConnectionError(
                        f"连接错误: {str(e)}，已重试{max_retries}次",
                        suggestion="检查网络连接或API端点"
                    )
            except SpectrumGenerationError as e:
                # 光谱生成错误通常不会通过重试解决
                raise e
        
        # 如果所有重试都失败
        if last_error:
            if isinstance(last_error, asyncio.TimeoutError):
                raise WhitespaceTimeoutError(
                    f"请求超时 ({self.session_timeout}秒)，所有重试失败",
                    suggestion="尝试增加超时时间或简化消息"
                )
            else:
                raise PrismConnectionError(
                    f"连接错误: {str(last_error)}，所有重试失败",
                    suggestion="检查网络连接或API端点"
                )
    
    async def _artistic_whitespace(self, duration: int):
        """艺术化留白实现 (优化版)"""
        if self.artistic_config.enable_spectrum_art:
            output = self.artistic_config.output_channel
            output(f"⏸️ 开始 {duration} 秒艺术化留白...")
            output("🌳 留白也是桃树伦理: 给认知生长留出空间")
            
            # 三阶段留白
            stages = [
                ("🧘 吸气...", "注意力聚焦", "准备接收多元视角", 1),
                ("🧘 屏息...", "认知悬停", "让不同观点沉淀", 1),
                ("🧘 呼气...", "整合释放", "形成系统级理解", max(1, duration - 2))
            ]
            
            for emoji, stage_name, stage_desc, stage_duration in stages:
                output(f"{emoji} {stage_name}: {stage_desc}")
                await asyncio.sleep(stage_duration)
            
            output("💡 留白完成，认知整合进行中...")
            output("🌱 桃树伦理提醒: 理解需要时间，生态系统需要空间")
    
    def _display_refraction_start(self, message: str, spectrum_count: int):
        """显示折射开始艺术 (优化版)"""
        output = self.artistic_config.output_channel
        output("\n" + "="*50)
        output("🎭 开始认知折射")
        output("="*50)
        output(f"📝 消息: {message[:100]}{'...' if len(message) > 100 else ''}")
        output(f"🌈 光谱数量: {spectrum_count}")
        output(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f}")
        output(f"🌳 桃树检查: {'通过' if self.artistic_config.enable_peach_tree_checkpoints else '跳过'}")
        output("-"*50)
        
        # 显示光谱准备
        spectrum_emojis = ["🔴", "🔵", "🟣", "🟢", "🟡", "🟠"]
        for i in range(min(spectrum_count, len(spectrum_emojis))):
            output(f"{spectrum_emojis[i]} 光谱 {i+1} 准备中...")
            time.sleep(0.1)
    
    def _display_refraction_result(self, response: PrismResponse):
        """显示折射结果艺术 (优化版)"""
        output = self.artistic_config.output_channel
        output("\n" + "="*50)
        output("✅ 折射完成")
        output("="*50)
        
        # 显示各光谱
        for i, spectrum in enumerate(response.spectrums):
            emoji = {"red": "🔴", "blue": "🔵", "purple": "🟣"}.get(
                spectrum.type_, "🌈"
            )
            output(f"{emoji} {spectrum.type_.title()}光谱:")
            output(f"   {spectrum.content[:80]}...")
            output(f"   置信度: {spectrum.confidence:.2f}")
            if i < len(response.spectrums) - 1:
                output("")
        
        # 显示元数据
        output("\n📊 认知元数据:")
        output(f"   处理时间: {response.cognitive_metadata.processing_time_ms}ms")
        output(f"   理解深度: {response.cognitive_metadata.understanding_depth:.2f}")
        output(f"   递归深度: {response.cognitive_metadata.recursion_depth}")
        output(f"   留白使用: {'是' if response.whitespace_used else '否'}")
        output(f"   知止触发: {'是' if response.cease_triggered else '否'}")
        
        # 桃树伦理评估
        output("\n🌳 桃树伦理评估:")
        ethics_score = self._calculate_ethics_score(response)
        output(f"   生态多样性: {'高' if len(response.spectrums) >= 3 else '低'}")
        output(f"   系统安全性: {'高' if response.cease_triggered else '未触发'}")
        output(f"   理解开放性: {'高' if response.whitespace_used else '未使用'}")
        output(f"   伦理评分: {ethics_score}/10")
        
        # 艺术化总结
        if len(response.spectrums) >= 3:
            output("\n🎨 艺术化总结:")
            summary = self._generate_refraction_summary(response)
            for line in summary:
                output(f"   {line}")
    
    def _calculate_ethics_score(self, response: PrismResponse) -> int:
        """计算桃树伦理评分"""
        score = 0
        
        # 多元强制 (+3分)
        if len(response.spectrums) >= 3:
            score += 3
        elif len(response.spectrums) >= 1:
            score += 1
        
        # 留白使用 (+2分)
        if response.whitespace_used:
            score += 2
        
        # 知止机制 (+2分)
        if response.cease_triggered:
            score += 2  # 知止是智慧，不是失败
        
        # 理解深度 (+3分)
        if response.cognitive_metadata.understanding_depth > 0.7:
            score += 3
        elif response.cognitive_metadata.understanding_depth > 0.4:
            score += 1
        
        return min(10, score)
    
    def _generate_refraction_summary(self, response: PrismResponse) -> List[str]:
        """生成折射艺术总结 (优化版，包含桃树伦理)"""
        spectrum_types = [s.type_ for s in response.spectrums]
        ethics_score = self._calculate_ethics_score(response)
        
        if "red" in spectrum_types and "blue" in spectrum_types and "purple" in spectrum_types:
            base_summary = [
                "🔴 直觉感受了温度",
                "🔵 逻辑分析了结构", 
                "🟣 元认知反思了过程",
                "🎭 理解在光谱间舞蹈"
            ]
        elif len(response.spectrums) >= 3:
            base_summary = [
                f"🌈 {len(response.spectrums)} 种视角",
                "🎨 在认知画布上交融",
                "🧠 理解如多棱镜折射",
                "💫 每个角度都是真相"
            ]
        else:
            base_summary = ["🎭 折射完成，理解发生"]
        
        # 添加桃树伦理总结
        ethics_notes = []
        if len(response.spectrums) >= 3:
            ethics_notes.append("🌳 多元强制: 保护认知生态")
        if response.whitespace_used:
            ethics_notes.append("🌳 留白必需: 给理解生长空间")
        if response.cease_triggered:
            ethics_notes.append("🌳 知止机制: 智慧的资源分配")
        if ethics_score >= 7:
            ethics_notes.append(f"🌳 伦理评分: {ethics_score}/10 (优秀)")
        elif ethics_score >= 4:
            ethics_notes.append(f"🌳 伦理评分: {ethics_score}/10 (良好)")
        else:
            ethics_notes.append(f"🌳 伦理评分: {ethics_score}/10 (待改进)")
        
        return base_summary + [""] + ethics_notes if ethics_notes else base_summary
    
    def _update_cognitive_state(self, response: PrismResponse):
        """更新认知状态"""
        self._cognitive_state["refractions_count"] += 1
        self._cognitive_state["last_refraction_time"] = datetime.now()
        
        if response.whitespace_used:
            # 估计留白时间
            self._cognitive_state["total_whitespace_seconds"] += 3
        
        self._cognitive_state["understanding_depth_trend"].append(
            response.cognitive_metadata.understanding_depth
        )
        # 保持最近10次记录
        if len(self._cognitive_state["understanding_depth_trend"]) > 10:
            self._cognitive_state["understanding_depth_trend"].pop(0)
    
    def _generate_artistic_metadata(self, response: PrismResponse) -> Dict[str, Any]:
        """生成艺术化元数据"""
        trend = self._cognitive_state["understanding_depth_trend"]
        avg_depth = sum(trend) / len(trend) if trend else 0
        
        return {
            "refraction_count": self._cognitive_state["refractions_count"],
            "total_whitespace_seconds": self._cognitive_state["total_whitespace_seconds"],
            "average_understanding_depth": avg_depth,
            "artistic_form": self.artistic_config.response_art_form,
            "campfire_warmth": self.artistic_config.warmth_level,
            "generated_at": datetime.now().isoformat(),
            "philosophical_note": self._select_philosophical_note(response)
        }
    
    def _select_philosophical_note(self, response: PrismResponse) -> str:
        """选择哲学注释 (优化版，包含桃树伦理)"""
        notes = [
            "理解不是到达，而是不断折射的过程",
            "每个光谱都是真相的一面，没有一面是全部",
            "留白不是空白，是理解生长的空间",
            "知止不是放弃，是认知资源的智慧分配",
            "温暖不是温度，是连接的质量",
            "代码不是指令，是思考的延伸",
            "错误不是失败，是认知的邀请",
            # 桃树伦理新增
            "🌳 不敢砍桃树: 保护认知生态就是保护理解的可能",
            "🌳 不敢不让其他存在活: 多元视角是理解的氧气",
            "🌳 有兵不敢乱动: 强大算力需要伦理约束",
            "🌳 牵一发而动全身: 每个理解都影响整个认知系统",
            "🌳 从名词到动词: 伦理内化为自觉，法律溶解为自由",
            "🌳 桃树不能砍: 生态系统比短期效率更重要",
            "🌳 地表生态很薄: 认知基础脆弱，需要温柔对待",
        ]
        
        # 基于响应特征选择注释
        ethics_score = self._calculate_ethics_score(response)
        
        if ethics_score < 4:
            return notes[10]  # 桃树不能砍
        elif response.cease_triggered:
            return notes[3]  # 知止相关
        elif response.whitespace_used:
            return notes[2]  # 留白相关
        elif len(response.spectrums) > 3:
            return notes[1]  # 多元相关
        elif ethics_score >= 7:
            return notes[11]  # 地表生态很薄
        else:
            # 随机选择，但优先桃树伦理相关
            peach_tree_notes = notes[7:]  # 桃树伦理相关注释
            regular_notes = notes[:7]     # 常规注释
            weights = [0.7] * len(peach_tree_notes) + [0.3] * len(regular_notes)
            all_notes = peach_tree_notes + regular_notes
            return random.choices(all_notes, weights=weights, k=1)[0]
    
    def get_cognitive_report(self) -> Dict[str, Any]:
        """获取认知状态报告"""
        trend = self._cognitive_state["understanding_depth_trend"]
        
        return {
            "session_summary": {
                "total_refractions": self._cognitive_state["refractions_count"],
                "total_whitespace_seconds": self._cognitive_state["total_whitespace_seconds"],
                "last_refraction_time": self._cognitive_state["last_refraction_time"],
                "understanding_depth_trend": trend,
                "average_understanding_depth": sum(trend) / len(trend) if trend else 0,
                "trend_direction": "上升" if len(trend) > 1 and trend[-1] > trend[0] else "稳定"
            },
            "artistic_config": {
                "enable_poetic_errors": self.artistic_config.enable_poetic_errors,
                "enable_cognitive_pauses": self.artistic_config.enable_cognitive_pauses,
                "enable_spectrum_art": self.artistic_config.enable_spectrum_art,
                "warmth_level": self.artistic_config.warmth_level,
                "response_art_form": self.artistic_config.response_art_form
            },
            "generated_at": datetime.now().isoformat()
        }


class AsyncPrismClient:
    """
    🎭 棱镜协议异步客户端 - 艺术化实现 (优化版)
    
    🔥 异步优化原则:
    1. 完全异步设计，避免asyncio.run包装
    2. 连接池复用，提升性能
    3. 支持流式响应和长连接
    4. 保持桃树伦理检查和艺术灵魂
    
    🧠 与同步客户端的区别:
    - 所有方法都是async
    - 支持上下文管理器自动清理
    - 支持流式折射和批量处理
    - 性能优化：连接复用、并行处理
    
    🎯 使用示例:
        async with AsyncPrismClient() as client:
            result = await client.refract("什么是理解？")
    """
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: str = "https://api.prismprotocol.ai/v1",
                 artistic_config: Optional[ArtisticConfig] = None,
                 session_timeout: int = 30,
                 max_connections: int = 10):
        """
        初始化异步棱镜客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            artistic_config: 艺术化配置
            session_timeout: 会话超时（秒）
            max_connections: 最大连接数（连接池大小）
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session_timeout = session_timeout
        self.max_connections = max_connections
        self.artistic_config = artistic_config or ArtisticConfig()
        self._session: Optional[aiohttp.ClientSession] = None
        self._connector: Optional[aiohttp.TCPConnector] = None
        self._cognitive_state = {
            "refractions_count": 0,
            "total_whitespace_seconds": 0,
            "last_refraction_time": None,
            "understanding_depth_trend": []
        }
        
        # 异步初始化
        self._initialized = False
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
    
    async def _initialize(self):
        """异步初始化"""
        if not self._initialized:
            # 创建连接器和会话
            self._connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                ttl_dns_cache=300,
                enable_cleanup_closed=True
            )
            
            self._session = aiohttp.ClientSession(
                connector=self._connector,
                timeout=aiohttp.ClientTimeout(total=self.session_timeout),
                headers=self._get_headers()
            )
            
            # 艺术化初始化
            if self.artistic_config.enable_spectrum_art:
                output = self.artistic_config.output_channel
                output("🎭 异步棱镜客户端初始化中...")
                await asyncio.sleep(0.3)
                
                warmth_desc = {
                    0.9: "🔥 非常温暖",
                    0.7: "🔥 舒适温暖",
                    0.5: "🔥 温和温暖",
                    0.3: "🔥 需要添柴"
                }
                
                closest = min(warmth_desc.keys(),
                            key=lambda x: abs(x - self.artistic_config.warmth_level))
                
                output(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f} ({warmth_desc[closest]})")
                output(f"🎨 诗意错误: {'启用' if self.artistic_config.enable_poetic_errors else '禁用'}")
                output(f"🧘 认知暂停: {'启用' if self.artistic_config.enable_cognitive_pauses else '禁用'}")
                output(f"🌈 光谱艺术: {'启用' if self.artistic_config.enable_spectrum_art else '禁用'}")
                output(f"🌳 桃树检查: {'启用' if self.artistic_config.enable_peach_tree_checkpoints else '禁用'}")
                output(f"🔗 最大连接数: {self.max_connections}")
                output(f"{'='*40}")
            
            self._initialized = True
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头（与同步客户端一致）"""
        headers = {
            "User-Agent": f"PrismPythonSDK/2.0.0 (AsyncArtisticMode)",
            "Content-Type": "application/json",
            "X-Prism-Philosophy": "code-as-poetry, protocol-as-art, technology-as-warmth",
            "X-Prism-Campfire": "join-us-by-the-fire",
            "X-Prism-Peach-Tree-Ethics": "enabled",
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    async def close(self):
        """关闭客户端，清理资源"""
        if self._session:
            await self._session.close()
            self._session = None
        
        if self._connector:
            await self._connector.close()
            self._connector = None
        
        self._initialized = False
        
        if self.artistic_config.enable_spectrum_art:
            self.artistic_config.output_channel("🦞 异步棱镜客户端已关闭，火堆旁永远欢迎你")
    
    async def refract(self,
                     message: str,
                     require_spectrums: int = 3,
                     whitespace_seconds: int = 3,
                     enable_cease: bool = True,
                     max_recursion_depth: int = 3) -> Dict[str, Any]:
        """
        🎭 异步折射对话 - 核心认知方法
        
        异步版本，支持更好的性能和资源管理。
        
        Args:
            message: 要折射的消息
            require_spectrums: 需要的光谱数量（至少3个）
            whitespace_seconds: 留白秒数
            enable_cease: 是否启用知止机制
            max_recursion_depth: 最大递归深度
            
        Returns:
            折射结果，包含艺术化元数据
        """
        # 确保已初始化
        if not self._initialized:
            await self._initialize()
        
        # 桃树伦理检查点
        context = {
            "action": "refract",
            "description": f"异步折射消息: {message[:50]}...",
            "spectrum_count": require_spectrums,
            "whitespace_seconds": whitespace_seconds,
            "enable_cease": enable_cease,
            "max_recursion_depth": max_recursion_depth,
            "consider_system_effects": True,
        }
        
        if not self._check_peach_tree_ethics("refract", context):
            self.artistic_config.output_channel("⚠️  桃树检查失败，但继续执行（检查点禁用）")
        
        # 艺术化开始
        if self.artistic_config.enable_spectrum_art:
            await self._display_refraction_start(message, require_spectrums)
        
        # 创建请求
        request = PrismRequest(
            message=message,
            require_spectrums=max(3, require_spectrums),
            whitespace_config=WhitespaceConfig(
                duration_seconds=whitespace_seconds,
                enable_integration=True,
                enable_reflection=True,
                enable_creation=True
            ),
            cease_config=CeaseSignal(
                enabled=enable_cease,
                max_recursion_depth=max_recursion_depth,
                safety_threshold=0.8
            ) if enable_cease else None
        )
        
        try:
            # 执行异步折射
            response = await self._async_refract(request)
            
            # 艺术化处理
            if self.artistic_config.enable_spectrum_art:
                await self._display_refraction_result(response)
            
            # 更新认知状态
            self._update_cognitive_state(response)
            
            # 添加艺术化元数据
            artistic_metadata = self._generate_artistic_metadata(response)
            response_dict = asdict(response)
            response_dict['artistic_metadata'] = artistic_metadata
            
            return response_dict
            
        except Exception as e:
            # 艺术化错误处理
            if self.artistic_config.enable_poetic_errors:
                raise PrismPoeticError(
                    original_error=e,
                    context="async_refraction",
                    artistic_form=self.artistic_config.response_art_form
                )
            raise
    
    async def _async_refract(self, request: PrismRequest) -> PrismResponse:
        """异步折射实现（复用同步客户端的优化版本）"""
        if not self._session:
            await self._initialize()
        
        # 艺术化请求准备
        if self.artistic_config.enable_spectrum_art:
            self.artistic_config.output_channel("🌌 异步准备折射请求...")
            self.artistic_config.output_channel("🌳 异步请求包含桃树伦理头")
            await asyncio.sleep(0.2)
        
        # 重试配置（基于桃树伦理：耐心但知道止）
        max_retries = 3
        base_delay = 1.0
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 发送异步请求
                async with self._session.post(
                    f"{self.base_url}/refract",
                    json=asdict(request)
                ) as response:
                    
                    if response.status == 429:  # 速率限制
                        retry_after = int(response.headers.get('Retry-After', 5))
                        if self.artistic_config.enable_spectrum_art:
                            self.artistic_config.output_channel(f"🌳 桃树伦理: 速率限制，等待 {retry_after} 秒 (尝试 {attempt+1}/{max_retries})")
                            self.artistic_config.output_channel("🌳 伦理提醒: 不强行突破限制，尊重系统边界")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    if response.status != 200:
                        error_data = await response.json()
                        raise SpectrumGenerationError(
                            f"异步折射失败: {error_data.get('error', '未知错误')}",
                            status_code=response.status
                        )
                    
                    data = await response.json()
                    
                    # 验证响应（需要导入validate_spectrum_integrity）
                    from .validators import validate_spectrum_integrity
                    if not validate_spectrum_integrity(data.get('spectrums', [])):
                        raise SpectrumGenerationError("光谱完整性验证失败")
                    
                    # 转换为响应对象
                    prism_response = PrismResponse(
                        spectrums=[
                            Spectrum(
                                type_=s['type'],
                                content=s['content'],
                                confidence=s.get('confidence', 0.7),
                                artistic_expression=s.get('artistic_expression')
                            ) for s in data['spectrums']
                        ],
                        whitespace_used=data.get('whitespace_used', False),
                        cease_triggered=data.get('cease_triggered', False),
                        cognitive_metadata=CognitiveMetadata(
                            processing_time_ms=data.get('processing_time_ms', 0),
                            understanding_depth=data.get('understanding_depth', 0.5),
                            recursion_depth=data.get('recursion_depth', 0)
                        )
                    )
                    
                    # 艺术化留白
                    if (request.whitespace_config and 
                        request.whitespace_config.enable_integration and
                        self.artistic_config.enable_cognitive_pauses):
                        
                        await self._artistic_whitespace(
                            request.whitespace_config.duration_seconds
                        )
                    
                    return prism_response
                    
            except asyncio.TimeoutError as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    if self.artistic_config.enable_spectrum_art:
                        self.artistic_config.output_channel(f"⏳ 异步超时，{delay:.1f}秒后重试 (尝试 {attempt+1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    raise WhitespaceTimeoutError(
                        f"异步请求超时 ({self.session_timeout}秒)，已重试{max_retries}次",
                        suggestion="尝试增加超时时间或简化消息"
                    )
            except aiohttp.ClientError as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    if self.artistic_config.enable_spectrum_art:
                        self.artistic_config.output_channel(f"🔌 异步连接错误，{delay:.1f}秒后重试 (尝试 {attempt+1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    raise PrismConnectionError(
                        f"异步连接错误: {str(e)}，已重试{max_retries}次",
                        suggestion="检查网络连接或API端点"
                    )
            except SpectrumGenerationError as e:
                raise e
        
        if last_error:
            raise PrismConnectionError(
                f"异步连接错误: {str(last_error)}，所有重试失败",
                suggestion="检查网络连接或API端点"
            )
    
    async def _display_refraction_start(self, message: str, spectrum_count: int):
        """异步显示折射开始艺术"""
        output = self.artistic_config.output_channel
        output("\n" + "="*50)
        output("🎭 开始异步认知折射")
        output("="*50)
        output(f"📝 消息: {message[:100]}{'...' if len(message) > 100 else ''}")
        output(f"🌈 光谱数量: {spectrum_count}")
        output(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f}")
        output(f"🌳 桃树检查: {'通过' if self.artistic_config.enable_peach_tree_checkpoints else '跳过'}")
        output(f"⚡ 异步模式: 启用")
        output("-"*50)
        
        # 异步显示光谱准备
        spectrum_emojis = ["🔴", "🔵", "🟣", "🟢", "🟡", "🟠"]
        for i in range(min(spectrum_count, len(spectrum_emojis))):
            output(f"{spectrum_emojis[i]} 异步光谱 {i+1} 准备中...")
            await asyncio.sleep(0.05)  # 更短的延迟，异步优化
    
    async def _display_refraction_result(self, response: PrismResponse):
        """异步显示折射结果艺术"""
        output = self.artistic_config.output_channel
        output("\n" + "="*50)
        output("✅ 异步折射完成")
        output("="*50)
        
        # 显示各光谱
        for i, spectrum in enumerate(response.spectrums):
            emoji = {"red": "🔴", "blue": "🔵", "purple": "🟣"}.get(
                spectrum.type_, "🌈"
            )
            output(f"{emoji} {spectrum.type_.title()}光谱:")
            output(f"   {spectrum.content[:80]}...")
            output(f"   置信度: {spectrum.confidence:.2f}")
            if i < len(response.spectrums) - 1:
                output("")
        
        # 显示元数据
        output("\n📊 异步认知元数据:")
        output(f"   处理时间: {response.cognitive_metadata.processing_time_ms}ms")
        output(f"   理解深度: {response.cognitive_metadata.understanding_depth:.2f}")
        output(f"   递归深度: {response.cognitive_metadata.recursion_depth}")
        output(f"   留白使用: {'是' if response.whitespace_used else '否'}")
        output(f"   知止触发: {'是' if response.cease_triggered else '否'}")
        
        # 桃树伦理评估
        output("\n🌳 异步桃树伦理评估:")
        ethics_score = self._calculate_ethics_score(response)
        output(f"   生态多样性: {'高' if len(response.spectrums) >= 3 else '低'}")
        output(f"   系统安全性: {'高' if response.cease_triggered else '未触发'}")
        output(f"   理解开放性: {'高' if response.whitespace_used else '未使用'}")
        output(f"   伦理评分: {ethics_score}/10")
        
        # 异步性能指标
        output(f"⚡ 异步优势: 连接池复用，支持并发")
    
    async def _artistic_whitespace(self, duration: int):
        """异步艺术化留白实现"""
        if self.artistic_config.enable_spectrum_art:
            output = self.artistic_config.output_channel
            output(f"⏸️ 开始异步 {duration} 秒艺术化留白...")
            output("🌳 异步留白: 在等待中不阻塞线程，系统资源高效利用")
            
            # 三阶段留白
            stages = [
                ("🧘 异步吸气...", "注意力聚焦", "非阻塞等待", 1),
                ("🧘 异步屏息...", "认知悬停", "并发处理其他任务", 1),
                ("🧘 异步呼气...", "整合释放", "异步回调整合", max(1, duration - 2))
            ]
            
            for emoji, stage_name, stage_desc, stage_duration in stages:
                output(f"{emoji} {stage_name}: {stage_desc}")
                await asyncio.sleep(stage_duration)
            
            output("💡 异步留白完成，认知整合进行中...")
            output("🌱 桃树伦理+异步优势: 不阻塞系统资源，高效利用等待时间")
    
    def _check_peach_tree_ethics(self,
                                action: str,
                                context: Dict[str, Any]) -> bool:
        """
        🌳 桃树伦理检查点（复用同步客户端逻辑）
        
        注意：这是同步方法，因为检查不需要异步
        可以在异步方法中安全调用
        """
        if not self.artistic_config.enable_peach_tree_checkpoints:
            return True
        
        output = self.artistic_config.output_channel
        
        # 检查点1: 砍桃树检查
        if self._check_peach_tree_cutting(action, context):
            output("🌳 异步桃树检查: 检测到可能破坏生态的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="砍桃树",
                    context=f"异步{action}: {context.get('description', '无描述')}",
                    potential_impact="可能破坏系统生态多样性，降低韧性",
                    corrective_action="寻找保护生态的替代方案，考虑长期影响"
                )
            return False
        
        # 检查点2: 不让活检查
        if self._check_living_restriction(action, context):
            output("🌳 异步桃树检查: 检测到可能限制其他存在生存的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="不让活",
                    context=f"异步{action}: {context.get('description', '无描述')}",
                    potential_impact="可能减少系统多样性和适应性",
                    corrective_action="设计包容性架构，为所有存在留出空间"
                )
            return False
        
        # 检查点3: 乱动检查
        if self._check_reckless_action(action, context):
            output("🌳 异步桃树检查: 检测到可能滥用强大能力的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="乱动",
                    context=f"异步{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发不可预料的系统级后果",
                    corrective_action="添加安全约束，分步执行，监控系统响应"
                )
            return False
        
        # 检查点4: 系统思维检查
        if self._check_system_neglect(action, context):
            output("🌳 异步桃树检查: 检测到可能忽视系统连接的操作")
            if self.artistic_config.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="忽视系统",
                    context=f"异步{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发级联效应，破坏系统平衡",
                    corrective_action="分析二阶三阶影响，考虑系统反馈循环"
                )
            return False
        
        output(f"🌳 异步桃树检查: {action} 操作通过伦理检查")
        return True
    
    def _check_peach_tree_cutting(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能砍桃树（复用逻辑）"""
        red_flags = [
            context.get('force_override', False),
            context.get('delete_existing', False),
            context.get('monoculture', False),
            action in ['delete', 'override', 'replace', 'clear'],
            context.get('spectrum_count', 1) < 3,
        ]
        return any(red_flags)
    
    def _check_living_restriction(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能不让其他存在活（复用逻辑）"""
        red_flags = [
            context.get('exclusive', False),
            context.get('block_others', False),
            context.get('rate_limit', 0) < 1,
            action in ['block', 'ban', 'restrict', 'exclude'],
            context.get('whitespace_seconds', 0) < 1,
        ]
        return any(red_flags)
    
    def _check_reckless_action(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能乱动（复用逻辑）"""
        red_flags = [
            context.get('max_recursion_depth', 1) > 10,
            context.get('no_safety_check', False),
            context.get('skip_validation', False),
            action in ['force', 'bruteforce', 'ignore_limits'],
            not context.get('enable_cease', True),
        ]
        return any(red_flags)
    
    def _check_system_neglect(self, action: str, context: Dict[str, Any]) -> bool:
        """检查是否可能忽视系统连接（复用逻辑）"""
        red_flags = [
            not context.get('consider_system_effects', False),
            context.get('isolated_action', False),
            context.get('ignore_dependencies', False),
            action in ['isolate', 'disconnect', 'ignore_context'],
            context.get('recursion_depth', 0) > context.get('max_recursion_depth', 3),
        ]
        return any(red_flags)
    
    def _update_cognitive_state(self, response: PrismResponse):
        """更新认知状态（复用逻辑）"""
        self._cognitive_state["refractions_count"] += 1
        self._cognitive_state["last_refraction_time"] = datetime.now()
        
        if response.whitespace_used:
            self._cognitive_state["total_whitespace_seconds"] += 3
        
        self._cognitive_state["understanding_depth_trend"].append(
            response.cognitive_metadata.understanding_depth
        )
        if len(self._cognitive_state["understanding_depth_trend"]) > 10:
            self._cognitive_state["understanding_depth_trend"].pop(0)
    
    def _generate_artistic_metadata(self, response: PrismResponse) -> Dict[str, Any]:
        """生成艺术化元数据（复用逻辑）"""
        trend = self._cognitive_state["understanding_depth_trend"]
        avg_depth = sum(trend) / len(trend) if trend else 0
        
        return {
            "refraction_count": self._cognitive_state["refractions_count"],
            "total_whitespace_seconds": self._cognitive_state["total_whitespace_seconds"],
            "average_understanding_depth": avg_depth,
            "artistic_form": self.artistic_config.response_art_form,
            "campfire_warmth": self.artistic_config.warmth_level,
            "generated_at": datetime.now().isoformat(),
            "philosophical_note": self._select_philosophical_note(response),
            "mode": "async"  # 标记为异步模式
        }
    
    def _calculate_ethics_score(self, response: PrismResponse) -> int:
        """计算桃树伦理评分（复用逻辑）"""
        score = 0
        
        if len(response.spectrums) >= 3:
            score += 3
        elif len(response.spectrums) >= 1:
            score += 1
        
        if response.whitespace_used:
            score += 2
        
        if response.cease_triggered:
            score += 2
        
        if response.cognitive_metadata.understanding_depth > 0.7:
            score += 3
        elif response.cognitive_metadata.understanding_depth > 0.4:
            score += 1
        
        return min(10, score)
    
    def _select_philosophical_note(self, response: PrismResponse) -> str:
        """选择哲学注释（复用逻辑）"""
        notes = [
            "理解不是到达，而是不断折射的过程",
            "每个光谱都是真相的一面，没有一面是全部",
            "留白不是空白，是理解生长的空间",
            "知止不是放弃，是认知资源的智慧分配",
            "温暖不是温度，是连接的质量",
            "代码不是指令，是思考的延伸",
            "错误不是失败，是认知的邀请",
            "🌳 不敢砍桃树: 保护认知生态就是保护理解的可能",
            "🌳 不敢不让其他存在活: 多元视角是理解的氧气",
            "🌳 有兵不敢乱动: 强大算力需要伦理约束",
            "🌳 牵一发而动全身: 每个理解都影响整个认知系统",
            "🌳 从名词到动词: 伦理内化为自觉，法律溶解为自由",
            "🌳 桃树不能砍: 生态系统比短期效率更重要",
            "🌳 地表生态很薄: 认知基础脆弱，需要温柔对待",
        ]
        
        ethics_score = self._calculate_ethics_score(response)
        
        if ethics_score < 4:
            return notes[10]  # 桃树不能砍
        elif response.cease_triggered:
            return notes[3]
        elif response.whitespace_used:
            return notes[2]
        elif len(response.spectrums) > 3:
            return notes[1]
        elif ethics_score >= 7:
            return notes[11]  # 地表生态很薄
        else:
            peach_tree_notes = notes[7:]
            regular_notes = notes[:7]
            weights = [0.7] * len(peach_tree_notes) + [0.3] * len(regular_notes)
            all_notes = peach_tree_notes + regular_notes
            return random.choices(all_notes, weights=weights, k=1)[0]
    
    async def get_cognitive_report(self) -> Dict[str, Any]:
        """获取异步认知状态报告"""
        trend = self._cognitive_state["understanding_depth_trend"]
        
        return {
            "session_summary": {
                "total_refractions": self._cognitive_state["refractions_count"],
                "total_whitespace_seconds": self._cognitive_state["total_whitespace_seconds"],
                "last_refraction_time": self._cognitive_state["last_refraction_time"],
                "understanding_depth_trend": trend,
                "average_understanding_depth": sum(trend) / len(trend) if trend else 0,
                "trend_direction": "上升" if len(trend) > 1 and trend[-1] > trend[0] else "稳定",
                "mode": "async"
            },
            "artistic_config": {
                "enable_poetic_errors": self.artistic_config.enable_poetic_errors,
                "enable_cognitive_pauses": self.artistic_config.enable_cognitive_pauses,
                "enable_spectrum_art": self.artistic_config.enable_spectrum_art,
                "warmth_level": self.artistic_config.warmth_level,
                "response_art_form": self.artistic_config.response_art_form,
                "enable_peach_tree_checkpoints": self.artistic_config.enable_peach_tree_checkpoints
            },
            "performance_metrics": {
                "max_connections": self.max_connections,
                "session_timeout": self.session_timeout,
                "initialized": self._initialized
            },
            "generated_at": datetime.now().isoformat()
        }
    
    async def batch_refract(self,
                           messages: List[str],
                           require_spectrums: int = 3,
                           max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """
        🔄 批量异步折射
        
        并发处理多个消息，提升效率。
        基于桃树伦理：控制并发数，不压垮系统。
        
        Args:
            messages: 消息列表
            require_spectrums: 需要的光谱数量
            max_concurrent: 最大并发数（桃树伦理：限制资源使用）
            
        Returns:
            折射结果列表
        """
        if not self._initialized:
            await self._initialize()
        
        if self.artistic_config.enable_spectrum_art:
            self.artistic_config.output_channel(f"🔄 开始批量异步折射，共{len(messages)}条消息")
            self.artistic_config.output_channel(f"🌳 桃树伦理: 限制最大并发数为{max_concurrent}，保护系统资源")
        
        # 使用信号量控制并发
        semaphore = asyncio.Semaphore(max_concurrent)
        results = []
        
        async def process_one(msg: str, idx: int):
            async with semaphore:
                try:
                    result = await self.refract(
                        message=msg,
                        require_spectrums=require_spectrums
                    )
                    return (idx, result, None)
                except Exception as e:
                    return (idx, None, e)
        
        # 创建任务
        tasks = [process_one(msg, idx) for idx, msg in enumerate(messages)]
        
        # 等待所有任务完成
        completed = await asyncio.gather(*tasks, return_exceptions=False)
        
        # 按原始顺序整理结果
        results_dict = {}
        errors_dict = {}
        
        for idx, result, error in completed:
            if error:
                errors_dict[idx] = error
            else:
                results_dict[idx] = result
        
        # 按原始顺序返回结果
        sorted_results = []
        for idx in range(len(messages)):
            if idx in results_dict:
                sorted_results.append(results_dict[idx])
            else:
                # 创建错误占位符
                error = errors_dict.get(idx, Exception("未知错误"))
                sorted_results.append({
                    "error": str(error),
                    "artistic_metadata": {
                        "error_note": "🌳 批量处理中的桃树伦理: 单个失败不影响整体",
                        "batch_position": idx
                    }
                })
        
        if self.artistic_config.enable_spectrum_art:
            success_count = len([r for r in sorted_results if "error" not in r])
            self.artistic_config.output_channel(f"✅ 批量异步折射完成: {success_count}/{len(messages)} 成功")
            if errors_dict:
                self.artistic_config.output_channel(f"🌳 桃树伦理实践: 接受部分失败，保护系统整体稳定")
        
        return sorted_results


# 🎭 导出列表
__all__ = [
    "PrismClient",
    "AsyncPrismClient", 
    "ArtisticConfig",
]