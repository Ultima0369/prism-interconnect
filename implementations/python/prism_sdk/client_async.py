"""
⚡ 棱镜协议异步客户端

继承BaseClient，提供异步API接口。

🔥 异步设计原则:
1. 非阻塞: 不阻塞主线程，支持并发
2. 高效: 复用连接，减少开销
3. 可扩展: 支持大量并发请求
4. 现代: 使用asyncio和async/await

🧠 使用场景:
- Web服务器和API服务
- 需要高并发的应用
- 实时数据处理
- 与其他异步系统集成
"""

import asyncio
import aiohttp
import time
import json
import logging
from typing import Dict, List, Any, Optional, Union, AsyncGenerator
from datetime import datetime
from contextlib import asynccontextmanager

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


class AsyncPrismClient(BaseClient):
    """
    ⚡ 棱镜协议异步客户端
    
    提供异步的棱镜协议API访问。
    """
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: str = "https://api.prismprotocol.ai/v1",
                 artistic_config: Optional[ArtisticConfig] = None,
                 performance_config: Optional[PerformanceConfig] = None,
                 ethics_config: Optional[PeachTreeEthicsConfig] = None):
        """
        初始化异步客户端
        
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
        self._semaphore = None
    
    def _create_session(self):
        """创建HTTP会话 (异步) - 基类要求"""
        # 异步客户端的会话在首次使用时创建
        return None
    
    async def _get_http_session(self) -> aiohttp.ClientSession:
        """获取HTTP会话 (异步，延迟初始化)"""
        if self._http_session is None or self._http_session.closed:
            self._http_session = await self._init_async_session()
            
            # 初始化信号量用于并发控制
            max_concurrent = self.performance_config.batch_max_concurrent
            self._semaphore = asyncio.Semaphore(max_concurrent)
        
        return self._http_session
    
    async def _init_async_session(self) -> aiohttp.ClientSession:
        """初始化异步HTTP会话"""
        timeout = aiohttp.ClientTimeout(total=self.performance_config.session_timeout)
        
        session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._get_default_headers()
        )
        
        return session
    
    def _cleanup_session(self):
        """同步清理HTTP会话 (由close()调用)"""
        # 异步清理在async_close()中处理
        pass
    
    async def async_close(self):
        """异步关闭客户端"""
        if self._http_session and not self._http_session.closed:
            await self._http_session.close()
            self._http_session = None
        
        # 调用基类的关闭逻辑
        self.close()
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.async_close()
    
    def _make_request(self, request: PrismRequest) -> PrismResponse:
        """同步请求 (异步客户端的存根实现)"""
        raise NotImplementedError("异步客户端不支持同步请求，请使用PrismClient")
    
    async def _make_request_async(self, request: PrismRequest) -> PrismResponse:
        """
        执行异步HTTP请求
        
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
            "request_id": f"async_{self._request_counter}",
            "message": request.message[:50] + "..." if len(request.message) > 50 else request.message,
            "spectrum_count": request.require_spectrums,
            "description": "执行棱镜折射请求"
        }
        
        if not self._check_ethics_before_action("refract", context):
            raise PrismPoeticError("伦理检查失败，请求被阻止")
        
        # 显示开始
        self._display_refraction_start(request.message, request.require_spectrums)
        
        try:
            # 认知暂停 (异步)
            if self.artistic_config.enable_cognitive_pauses:
                await asyncio.sleep(0.5)
            
            # 使用信号量控制并发
            async with self._semaphore:
                # 执行HTTP请求
                response_data = await self._perform_http_request_async(request)
            
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
    
    async def _perform_http_request_async(self, request: PrismRequest) -> Dict[str, Any]:
        """
        执行实际的异步HTTP请求
        
        注意: 这是占位符实现，需要根据实际的API端点调整
        """
        session = await self._get_http_session()
        
        # 准备请求数据
        request_data = {
            "message": request.message,
            "require_spectrums": request.require_spectrums,
            "whitespace_type": getattr(request, "whitespace_type", "integration"),
            "recursion_depth": getattr(request, "recursion_depth", 1)
        }
        
        try:
            # 发送请求
            async with session.post("/refract", json=request_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise PrismConnectionError(f"API返回错误: {response.status} - {error_text}")
                
                response_data = await response.json()
                return response_data
                
        except aiohttp.ClientError as e:
            raise PrismConnectionError(f"HTTP客户端错误: {str(e)}") from e
        except asyncio.TimeoutError:
            raise PrismConnectionError("请求超时") from None
        except json.JSONDecodeError as e:
            raise PrismConnectionError(f"响应JSON解析错误: {str(e)}") from e
    
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
    
    async def refract(self, 
                     message: str, 
                     require_spectrums: int = 3,
                     **kwargs) -> PrismResponse:
        """
        异步折射消息 (生成多个认知视角)
        
        Args:
            message: 要折射的消息
            require_spectrums: 需要的光谱数量 (1-5)
            **kwargs: 其他请求参数
            
        Returns:
            PrismResponse: 包含多个光谱视角的响应
            
        Example:
            >>> async with AsyncPrismClient() as client:
            >>>     response = await client.refract("什么是理解？", 3)
            >>>     for spectrum in response.spectrums:
            >>>         print(f"{spectrum.type}: {spectrum.perspective}")
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
        return await self._make_request_async(request)
    
    async def batch_refract(self,
                           messages: List[str],
                           require_spectrums: int = 3,
                           **kwargs) -> List[PrismResponse]:
        """
        异步批量折射消息
        
        Args:
            messages: 消息列表
            require_spectrums: 每个消息需要的光谱数量
            **kwargs: 其他请求参数
            
        Returns:
            响应列表
            
        Note:
            使用信号量控制并发，避免过多同时请求
        """
        tasks = []
        
        for message in messages:
            task = self.refract(message, require_spectrums, **kwargs)
            tasks.append(task)
        
        # 并发执行，但受信号量限制
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        processed_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                logging.error(f"消息{i+1}折射失败: {str(response)}")
                if kwargs.get("stop_on_error", False):
                    raise response
            else:
                processed_responses.append(response)
        
        return processed_responses
    
    async def stream_refract(self,
                            message: str,
                            require_spectrums: int = 3,
                            **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式折射消息 (实验性功能)
        
        逐步返回折射结果，支持实时显示。
        
        Args:
            message: 要折射的消息
            require_spectrums: 需要的光谱数量
            **kwargs: 其他参数
            
        Yields:
            部分结果字典
        """
        # 创建请求
        request = PrismRequest(
            message=message,
            require_spectrums=require_spectrums,
            **kwargs
        )
        
        # 显示开始
        self._display_refraction_start(message, require_spectrums)
        
        # 模拟流式响应
        for i in range(require_spectrums):
            await asyncio.sleep(0.3)  # 模拟处理延迟
            
            # 生成部分结果
            partial_result = {
                "spectrum_index": i,
                "status": "generating",
                "progress": (i + 1) / require_spectrums,
                "message": f"生成第{i+1}个光谱..."
            }
            
            yield partial_result
        
        # 生成最终结果
        response_data = self._generate_mock_response(request)
        response = self._parse_response(response_data)
        
        # 更新状态
        self._update_state_after_refraction(response)
        
        # 显示结果
        self._display_refraction_result(response)
        
        yield {
            "status": "complete",
            "response": response.dict() if hasattr(response, 'dict') else str(response),
            "metadata": self.get_cognitive_report()
        }
    
    async def create_cognitive_pause_async(self, duration_seconds: int = 30) -> Dict[str, Any]:
        """异步创建认知暂停"""
        if not self.artistic_config.enable_cognitive_pauses:
            return {"status": "认知暂停已禁用"}
        
        await asyncio.sleep(duration_seconds)
        
        return {
            "status": "completed",
            "duration_seconds": duration_seconds,
            "insight": "认知暂停有助于整合理解"
        }
    
    async def measure_understanding_depth_async(self, response: PrismResponse) -> float:
        """异步测量理解深度"""
        # 模拟异步处理
        await asyncio.sleep(0.1)
        return measure_understanding_depth(response)


