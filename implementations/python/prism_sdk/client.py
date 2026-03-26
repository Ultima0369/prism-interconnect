"""
🎭 棱镜协议客户端 - 艺术化实现
🔥 这不是普通的HTTP客户端，这是火堆旁的对话使者

设计哲学：
1. 每个请求都是一次认知邀请
2. 每个响应都是一面理解镜子  
3. 每个错误都是一次学习机会
4. 每个连接都是一次关系建立

艺术承诺：
- 温暖的错误信息
- 诗意的API调用
- 美学的响应处理
- 存在的连接体验
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import aiohttp
from dataclasses import dataclass, asdict

from .exceptions import (
    PrismConnectionError,
    SpectrumGenerationError,
    WhitespaceTimeoutError,
    CeaseSignalReceived,
    PrismPoeticError,
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
    """艺术化配置"""
    enable_poetic_errors: bool = True
    enable_cognitive_pauses: bool = True
    enable_spectrum_art: bool = True
    warmth_level: float = 0.7  # 0.0-1.0
    response_art_form: str = "haiku"  # haiku, free_verse, visual


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
        """艺术化初始化"""
        if self.artistic_config.enable_spectrum_art:
            print("🎭 棱镜客户端初始化中...")
            time.sleep(0.3)
            
            warmth_desc = {
                0.9: "🔥 非常温暖",
                0.7: "🔥 舒适温暖",
                0.5: "🔥 温和温暖", 
                0.3: "🔥 需要添柴"
            }
            
            closest = min(warmth_desc.keys(), 
                         key=lambda x: abs(x - self.artistic_config.warmth_level))
            
            print(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f} ({warmth_desc[closest]})")
            print(f"🎨 诗意错误: {'启用' if self.artistic_config.enable_poetic_errors else '禁用'}")
            print(f"🧘 认知暂停: {'启用' if self.artistic_config.enable_cognitive_pauses else '禁用'}")
            print(f"🌈 光谱艺术: {'启用' if self.artistic_config.enable_spectrum_art else '禁用'}")
            print(f"{'='*40}")
    
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
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def refract(self, 
                message: str,
                require_spectrums: int = 3,
                whitespace_seconds: int = 3,
                enable_cease: bool = True,
                max_recursion_depth: int = 3) -> Dict[str, Any]:
        """
        🎭 折射对话 - 核心认知方法
        
        将单一消息折射为多光谱理解。
        这不是API调用，这是认知的舞蹈。
        
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
        """
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
        """异步折射实现"""
        session = self._get_session()
        
        # 艺术化请求准备
        if self.artistic_config.enable_spectrum_art:
            print("🌌 准备折射请求...")
            await asyncio.sleep(0.2)
        
        try:
            # 发送请求
            async with session.post(
                f"{self.base_url}/refract",
                json=asdict(request)
            ) as response:
                
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
                
        except asyncio.TimeoutError:
            raise WhitespaceTimeoutError(
                f"请求超时 ({self.session_timeout}秒)",
                suggestion="尝试增加超时时间或简化消息"
            )
        except aiohttp.ClientError as e:
            raise PrismConnectionError(
                f"连接错误: {str(e)}",
                suggestion="检查网络连接或API端点"
            )
    
    async def _artistic_whitespace(self, duration: int):
        """艺术化留白实现"""
        if self.artistic_config.enable_spectrum_art:
            print(f"⏸️ 开始 {duration} 秒艺术化留白...")
            
            # 三阶段留白
            stages = [
                ("🧘 吸气...", "注意力聚焦", 1),
                ("🧘 屏息...", "认知悬停", 1),
                ("🧘 呼气...", "整合释放", max(1, duration - 2))
            ]
            
            for emoji, desc, stage_duration in stages:
                print(f"{emoji} {desc}")
                await asyncio.sleep(stage_duration)
            
            print("💡 留白完成，认知整合进行中...")
    
    def _display_refraction_start(self, message: str, spectrum_count: int):
        """显示折射开始艺术"""
        print("\n" + "="*50)
        print("🎭 开始认知折射")
        print("="*50)
        print(f"📝 消息: {message[:100]}{'...' if len(message) > 100 else ''}")
        print(f"🌈 光谱数量: {spectrum_count}")
        print(f"🦞 温暖度: {self.artistic_config.warmth_level:.1f}")
        print("-"*50)
        
        # 显示光谱准备
        spectrum_emojis = ["🔴", "🔵", "🟣", "🟢", "🟡", "🟠"]
        for i in range(min(spectrum_count, len(spectrum_emojis))):
            print(f"{spectrum_emojis[i]} 光谱 {i+1} 准备中...")
            time.sleep(0.1)
    
    def _display_refraction_result(self, response: PrismResponse):
        """显示折射结果艺术"""
        print("\n" + "="*50)
        print("✅ 折射完成")
        print("="*50)
        
        # 显示各光谱
        for i, spectrum in enumerate(response.spectrums):
            emoji = {"red": "🔴", "blue": "🔵", "purple": "🟣"}.get(
                spectrum.type_, "🌈"
            )
            print(f"{emoji} {spectrum.type_.title()}光谱:")
            print(f"   {spectrum.content[:80]}...")
            print(f"   置信度: {spectrum.confidence:.2f}")
            if i < len(response.spectrums) - 1:
                print()
        
        # 显示元数据
        print("\n📊 认知元数据:")
        print(f"   处理时间: {response.cognitive_metadata.processing_time_ms}ms")
        print(f"   理解深度: {response.cognitive_metadata.understanding_depth:.2f}")
        print(f"   递归深度: {response.cognitive_metadata.recursion_depth}")
        print(f"   留白使用: {'是' if response.whitespace_used else '否'}")
        print(f"   知止触发: {'是' if response.cease_triggered else '否'}")
        
        # 艺术化总结
        if len(response.spectrums) >= 3:
            print("\n🎨 艺术化总结:")
            summary = self._generate_refraction_summary(response)
            for line in summary:
                print(f"   {line}")
    
    def _generate_refraction_summary(self, response: PrismResponse) -> List[str]:
        """生成折射艺术总结"""
        spectrum_types = [s.type_ for s in response.spectrums]
        
        if "red" in spectrum_types and "blue" in spectrum_types and "purple" in spectrum_types:
            return [
                "🔴 直觉感受了温度",
                "🔵 逻辑分析了结构", 
                "🟣 元认知反思了过程",
                "🎭 理解在光谱间舞蹈"
            ]
        elif len(response.spectrums) >= 3:
            return [
                f"🌈 {len(response.spectrums)} 种视角",
                "🎨 在认知画布上交融",
                "🧠 理解如多棱镜折射",
                "💫 每个角度都是真相"
            ]
        else:
            return ["🎭 折射完成，理解发生"]
    
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
        """选择哲学注释"""
        notes = [
            "理解不是到达，而是不断折射的过程",
            "每个光谱都是真相的一面，没有一面是全部",
            "留白不是空白，是理解生长的空间",
            "知止不是放弃，是认知资源的智慧分配",
            "温暖不是温度，是连接的质量",
            "代码不是指令，是思考的延伸",
            "错误不是失败，是认知的邀请"
        ]
        
        # 基于响应特征选择注释
        if response.cease_triggered:
            return notes[3]  # 知止相关
        elif response.whitespace_used:
            return notes[2]  # 留白相关
        elif len(response.spectrums) > 3:
            return notes[1]  # 多元相关
        else:
            return random.choice(notes)
    
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