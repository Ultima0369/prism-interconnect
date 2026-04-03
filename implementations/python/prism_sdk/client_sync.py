"""
🎭 棱镜协议同步客户端

继承BaseClient，提供同步API接口。

🔥 同步设计原则:
1. 简单直接: 同步调用，同步返回
2. 错误透明: 异常直接抛出，不隐藏
3. 资源安全: 上下文管理器确保资源清理
4. 性能可控: 超时和重试机制

🧠 使用场景:
- 脚本和命令行工具
- 简单集成场景
- 需要直接控制流的应用
- 教育和演示环境
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import aiohttp
import asyncio

from .client_base import BaseClient, ClientState
from .config import ArtisticConfig, PerformanceConfig, PeachTreeEthicsConfig
from .models import PrismRequest, PrismResponse, Spectrum
from .exceptions import (
    PrismConnectionError,
    SpectrumGenerationError,
    WhitespaceTimeoutError,
    CeaseSignalReceived,
    PrismPoeticError,
)
from .validators import validate_spectrum_integrity
from .utils import create_cognitive_pause, measure_understanding_depth


class PrismClient(BaseClient):
    """
    🎭 棱镜协议同步客户端
    
    提供同步的棱镜协议API访问。
    """
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: str = "https://api.prismprotocol.ai/v1",
                 artistic_config: Optional[ArtisticConfig] = None,
                 performance_config: Optional[PerformanceConfig] = None,
                 ethics_config: Optional[PeachTreeEthicsConfig] = None):
        """
        初始化同步客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            artistic_config: 艺术化配置
            performance_config: 性能配置
            ethics_config: 伦理配置
        """
        super().__init__(
            api_key=api_key,
            artistic_config=artistic_config,
            performance_config=performance_config,
            ethics_config=ethics_config
        )
        
        self.base_url = base_url.rstrip('/')
        self._http_session = None
        self._request_counter = 0
    
    def _create_session(self):
        """创建HTTP会话 (同步)"""
        # 同步客户端使用requests库，但这里使用aiohttp的同步模式
        # 实际实现可能需要根据HTTP库调整
        return None  # 延迟初始化
    
    def _get_http_session(self):
        """获取HTTP会话 (延迟初始化)"""
        if self._http_session is None:
            # 这里应该使用适当的HTTP库
            # 为了简化，我们假设有同步HTTP客户端
            self._http_session = self._init_sync_session()
        return self._http_session
    
    def _init_sync_session(self):
        """初始化同步HTTP会话"""
        # 这里应该实现实际的同步HTTP客户端初始化
        # 例如使用requests.Session()或httpx.Client()
        # 返回一个可以执行同步HTTP请求的对象
        return {"type": "sync_session", "base_url": self.base_url}
    
    def _cleanup_session(self):
        """清理HTTP会话"""
        if self._http_session:
            # 清理同步会话资源
            if hasattr(self._http_session, 'close'):
                self._http_session.close()
            self._http_session = None
    
    def _make_request(self, request: PrismRequest) -> PrismResponse:
        """
        执行同步HTTP请求
        
        Args:
            request: 请求对象
            
        Returns:
            响应对象
            
        Raises:
            PrismConnectionError: 连接错误
            SpectrumGenerationError: 光谱生成错误
        """
        self._request_counter += 1
        
        # 伦理检查
        context = {
            "request_id": f"sync_{self._request_counter}",
            "message": request.message[:50] + "..." if len(request.message) > 50 else request.message,
            "spectrum_count": request.require_spectrums,
            "description": "执行棱镜折射请求"
        }
        
        if not self._check_ethics_before_action("refract", context):
            raise PrismPoeticError("伦理检查失败，请求被阻止")
        
        # 显示开始
        self._display_refraction_start(request.message, request.require_spectrums)
        
        try:
            # 模拟请求延迟 (实际实现中应删除)
            if self.artistic_config.enable_cognitive_pauses:
                time.sleep(0.5)
            
            # 这里应该执行实际的HTTP请求
            # response_data = self._perform_http_request(request)
            # 为演示目的，返回模拟响应
            response_data = self._generate_mock_response(request)
            
            # 验证响应
            if not response_data:
                raise PrismConnectionError("API请求返回空响应")
            
            # 转换为PrismResponse对象
            response = self._parse_response(response_data)
            
            # 验证光谱完整性
            if not validate_spectrum_integrity(response.spectrums):
                raise SpectrumGenerationError("生成的光谱完整性验证失败")
            
            # 更新状态
            self._update_state_after_refraction(response)
            
            # 显示结果
            self._display_refraction_result(response)
            
            return response
            
        except Exception as e:
            # 统一错误处理
            error_context = {
                "request": request.dict() if hasattr(request, 'dict') else str(request),
                "request_id": context["request_id"],
                "action": "refract"
            }
            self._handle_error(e, error_context)
            
            # 重新抛出经过处理的异常
            if isinstance(e, (PrismConnectionError, SpectrumGenerationError, 
                            WhitespaceTimeoutError, CeaseSignalReceived)):
                raise
            else:
                # 包装未知错误
                raise PrismConnectionError(f"请求失败: {str(e)}") from e
    
    async def _make_request_async(self, request: PrismRequest) -> PrismResponse:
        """异步请求 (同步客户端的存根实现)"""
        raise NotImplementedError("同步客户端不支持异步请求，请使用AsyncPrismClient")
    
    def _perform_http_request(self, request: PrismRequest) -> Dict[str, Any]:
        """
        执行实际的HTTP请求
        
        注意: 这是占位符实现，需要根据实际的HTTP库实现
        """
        # 这里应该使用实际的HTTP库发送请求
        # 例如: requests.post, httpx.post等
        
        # 模拟实现
        return {
            "spectrums": [
                {
                    "type": "red",
                    "name": "直觉视角",
                    "perspective": "这是一个直观的感受...",
                    "confidence": 0.8,
                    "limitations": "基于快速判断，可能缺乏深度分析",
                    "emotional_tone": "curious"
                },
                {
                    "type": "blue",
                    "name": "分析视角",
                    "perspective": "从逻辑角度分析...",
                    "confidence": 0.7,
                    "limitations": "可能过于理性，忽视情感因素",
                    "emotional_tone": "analytical"
                }
            ],
            "metadata": {
                "understanding_depth": 0.75,
                "processing_time_ms": 1200,
                "recursion_level": 1
            },
            "whitespace_recommendation": {
                "type": "reflection",
                "duration_seconds": 60,
                "guidance": "思考这些不同视角之间的关系"
            }
        }
    
    def _generate_mock_response(self, request: PrismRequest) -> Dict[str, Any]:
        """生成模拟响应 (用于演示和测试)"""
        from .models import SpectrumType
        
        # 生成指定数量的光谱
        spectrums = []
        spectrum_types = list(SpectrumType)
        
        for i in range(min(request.require_spectrums, len(spectrum_types))):
            spectrum_type = spectrum_types[i]
            
            spectrum = {
                "type": spectrum_type.value,
                "name": f"{spectrum_type.value.capitalize()}视角",
                "perspective": f"这是关于'{request.message[:20]}...'的{spectrum_type.value}视角。",
                "confidence": 0.5 + (i * 0.1),
                "reasoning": "基于棱镜协议的认知折射算法生成。",
                "limitations": "每个视角都有其认知边界和假设。",
                "sources": ["棱镜协议认知引擎"],
                "emotional_tone": "reflective"
            }
            spectrums.append(spectrum)
        
        # 生成元数据
        metadata = {
            "understanding_depth": 0.5 + (len(spectrums) * 0.05),
            "processing_time_ms": 800 + (len(spectrums) * 200),
            "recursion_level": 1,
            "ethical_score": 75,
            "cognitive_balance": "良好"
        }
        
        # 生成留白建议
        whitespace_recommendation = {
            "type": "integration",
            "duration_seconds": 30 + (len(spectrums) * 10),
            "guidance": "整合这些不同视角，寻找共同点。",
            "prompt": "这些视角如何相互补充？"
        }
        
        return {
            "spectrums": spectrums,
            "metadata": metadata,
            "whitespace_recommendation": whitespace_recommendation
        }
    
    def _parse_response(self, response_data: Dict[str, Any]) -> PrismResponse:
        """解析响应数据为PrismResponse对象"""
        from .models import PrismResponse, CognitiveMetadata, Whitespace
        
        # 解析光谱
        spectrums = []
        for spectrum_data in response_data.get("spectrums", []):
            spectrum = Spectrum(**spectrum_data)
            spectrums.append(spectrum)
        
        # 解析元数据
        metadata_data = response_data.get("metadata", {})
        metadata = CognitiveMetadata(**metadata_data)
        
        # 解析留白建议
        whitespace_data = response_data.get("whitespace_recommendation", {})
        whitespace = Whitespace(**whitespace_data) if whitespace_data else None
        
        return PrismResponse(
            spectrums=spectrums,
            metadata=metadata,
            whitespace_recommendation=whitespace
        )
    
    def refract(self, 
               message: str, 
               require_spectrums: int = 3,
               **kwargs) -> PrismResponse:
        """
        折射消息 (生成多个认知视角)
        
        Args:
            message: 要折射的消息
            require_spectrums: 需要的光谱数量 (1-5)
            **kwargs: 其他请求参数
            
        Returns:
            PrismResponse: 包含多个光谱视角的响应
            
        Example:
            >>> client = PrismClient()
            >>> response = client.refract("什么是理解？", require_spectrums=3)
            >>> for spectrum in response.spectrums:
            ...     print(f"{spectrum.type}: {spectrum.perspective}")
        """
        # 参数验证
        if require_spectrums < 1 or require_spectrums > 5:
            require_spectrums = max(1, min(5, require_spectrums))
            logging.warning(f"光谱数量调整为{require_spectrums} (必须在1-5之间)")
        
        # 创建请求
        request = PrismRequest(
            message=message,
            require_spectrums=require_spectrums,
            **kwargs
        )
        
        # 执行请求
        return self._make_request(request)
    
    def batch_refract(self,
                     messages: List[str],
                     require_spectrums: int = 3,
                     **kwargs) -> List[PrismResponse]:
        """
        批量折射消息
        
        Args:
            messages: 消息列表
            require_spectrums: 每个消息需要的光谱数量
            **kwargs: 其他请求参数
            
        Returns:
            响应列表
            
        Note:
            批量处理可能会受到性能配置中的并发限制
        """
        responses = []
        
        for i, message in enumerate(messages):
            try:
                response = self.refract(message, require_spectrums, **kwargs)
                responses.append(response)
                
                # 批量处理间的暂停
                if i < len(messages) - 1 and self.artistic_config.enable_cognitive_pauses:
                    time.sleep(0.2)
                    
            except Exception as e:
                logging.error(f"消息{i+1}折射失败: {str(e)}")
                # 可以选择继续处理或停止
                if kwargs.get("stop_on_error", False):
                    raise
        
        return responses
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """获取当前认知状态"""
        return {
            "refractions_count": self._state.refractions_count,
            "total_whitespace_seconds": self._state.total_whitespace_seconds,
            "last_refraction_time": self._state.last_refraction_time,
            "understanding_trend": self._state.understanding_depth_trend[-10:],  # 最近10次
            "error_stats": self.get_error_report()
        }
    
    def create_cognitive_pause(self, duration_seconds: int = 30) -> Dict[str, Any]:
        """创建认知暂停"""
        if not self.artistic_config.enable_cognitive_pauses:
            return {"status": "认知暂停已禁用"}
        
        return create_cognitive_pause(duration_seconds)
    
    def measure_understanding_depth(self, response: PrismResponse) -> float:
        """测量理解深度"""
        return measure_understanding_depth(response)