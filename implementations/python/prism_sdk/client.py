"""
🧠 棱镜协议客户端
核心通信接口实现
"""

import asyncio
import aiohttp
import json
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timedelta
from uuid import uuid4

from .models import (
    PrismMessage,
    PrismResponse,
    Spectrum,
    Whitespace,
    Synthesis,
    SessionConfig,
    UserPreferences,
    ValidationResult,
    SpectrumType,
    WhitespaceType,
    ErrorCode
)
from .exceptions import (
    PrismError,
    SpectrumGenerationError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    RecursionDepthError
)
from .validators import validate_message
from .generators import generate_spectrums, generate_whitespace, generate_synthesis
from .utils import create_session_id, format_timestamp, anonymize_user_data


class PrismClient:
    """棱镜协议客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = "https://api.prism.dev/v1",
        session_config: Optional[SessionConfig] = None,
        user_preferences: Optional[UserPreferences] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        初始化棱镜客户端
        
        Args:
            api_key: API密钥，本地模式可为None
            endpoint: API端点URL
            session_config: 会话配置
            user_preferences: 用户偏好
            timeout: 请求超时时间(秒)
            max_retries: 最大重试次数
        """
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.session_config = session_config or SessionConfig()
        self.user_preferences = user_preferences or UserPreferences()
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 会话状态
        self.session_id = create_session_id()
        self.recursion_depth = 0
        self.message_history: List[PrismResponse] = []
        
        # HTTP客户端
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "User-Agent": f"Prism-SDK/1.0.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        
        # 性能监控
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_latency_ms": 0,
            "last_request_time": None
        }
        
        # 日志
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"棱镜客户端初始化完成 - 会话ID: {self.session_id}")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
    
    async def connect(self):
        """连接到棱镜服务"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout,
                connector=aiohttp.TCPConnector(limit=100)
            )
            self.logger.debug("HTTP会话已创建")
    
    async def close(self):
        """关闭连接"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
            self.logger.debug("HTTP会话已关闭")
    
    async def prismatic_dialogue(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        min_spectrums: Optional[int] = None,
        max_spectrums: Optional[int] = None,
        enable_synthesis: Optional[bool] = None,
        recursion_path: Optional[List[str]] = None
    ) -> PrismResponse:
        """
        执行棱镜对话
        
        Args:
            query: 用户查询
            context: 对话上下文
            min_spectrums: 最小光谱数量
            max_spectrums: 最大光谱数量
            enable_synthesis: 是否启用合成
            recursion_path: 递归路径（用于深度探索）
            
        Returns:
            PrismResponse: 棱镜响应
            
        Raises:
            PrismError: 棱镜协议错误
            ValidationError: 验证错误
            AuthenticationError: 认证错误
            RateLimitError: 速率限制错误
        """
        start_time = datetime.now()
        
        try:
            # 1. 准备请求
            request_data = await self._prepare_request(
                query=query,
                context=context,
                min_spectrums=min_spectrums,
                max_spectrums=max_spectrums,
                enable_synthesis=enable_synthesis,
                recursion_path=recursion_path
            )
            
            # 2. 验证请求
            validation_result = validate_message(request_data["message"])
            if not validation_result.valid:
                raise ValidationError(
                    f"消息验证失败: {', '.join(validation_result.errors)}",
                    validation_result
                )
            
            # 3. 发送请求
            response_data = await self._send_request(request_data)
            
            # 4. 处理响应
            response = await self._process_response(response_data, recursion_path)
            
            # 5. 更新状态
            self.message_history.append(response)
            self.recursion_depth = response.metadata.get("recursion_depth", 0)
            
            # 6. 更新指标
            self._update_metrics(start_time, success=True)
            
            self.logger.info(
                f"棱镜对话完成 - "
                f"查询: {query[:50]}... "
                f"光谱数: {len(response.message.spectrums)} "
                f"递归深度: {self.recursion_depth} "
                f"耗时: {(datetime.now() - start_time).total_seconds():.2f}s"
            )
            
            return response
            
        except Exception as e:
            self._update_metrics(start_time, success=False)
            self.logger.error(f"棱镜对话失败: {str(e)}", exc_info=True)
            raise
    
    async def recursive_explore(
        self,
        spectrum_index: int,
        depth: int = 1,
        max_depth: Optional[int] = None
    ) -> PrismResponse:
        """
        递归探索特定光谱
        
        Args:
            spectrum_index: 要探索的光谱索引
            depth: 探索深度
            max_depth: 最大递归深度
            
        Returns:
            PrismResponse: 递归探索结果
            
        Raises:
            RecursionDepthError: 递归深度超限
        """
        if max_depth is None:
            max_depth = self.session_config.max_recursion_depth
        
        # 检查递归深度
        if self.recursion_depth + depth > max_depth:
            raise RecursionDepthError(
                f"递归深度超限: 当前{self.recursion_depth}, 尝试{depth}, 最大{max_depth}",
                current_depth=self.recursion_depth,
                attempted_depth=depth,
                max_depth=max_depth
            )
        
        # 获取要探索的光谱
        if not self.message_history:
            raise PrismError("没有历史消息可供递归探索")
        
        last_response = self.message_history[-1]
        spectrums = last_response.message.spectrums
        
        if spectrum_index < 0 or spectrum_index >= len(spectrums):
            raise PrismError(f"光谱索引无效: {spectrum_index}, 有效范围: 0-{len(spectrums)-1}")
        
        target_spectrum = spectrums[spectrum_index]
        
        # 构建递归查询
        recursion_query = f"请深入探索这个视角: {target_spectrum.perspective}"
        
        # 构建递归路径
        recursion_path = last_response.metadata.get("recursion_path", [])
        recursion_path.append(target_spectrum.name)
        
        # 执行递归对话
        response = await self.prismatic_dialogue(
            query=recursion_query,
            context={
                "recursion_context": {
                    "target_spectrum": target_spectrum.dict(),
                    "previous_perspective": target_spectrum.perspective,
                    "exploration_depth": depth
                }
            },
            recursion_path=recursion_path
        )
        
        # 更新递归深度
        response.metadata["recursion_depth"] = self.recursion_depth + 1
        response.metadata["recursion_path"] = recursion_path
        response.metadata["parent_message_id"] = last_response.message_id
        
        self.logger.info(
            f"递归探索完成 - "
            f"目标光谱: {target_spectrum.name} "
            f"新深度: {response.metadata['recursion_depth']}"
        )
        
        return response
    
    async def batch_dialogue(
        self,
        queries: List[str],
        parallel: bool = True,
        max_concurrent: int = 5
    ) -> List[PrismResponse]:
        """
        批量执行棱镜对话
        
        Args:
            queries: 查询列表
            parallel: 是否并行执行
            max_concurrent: 最大并发数
            
        Returns:
            List[PrismResponse]: 响应列表
        """
        if parallel:
            # 并行执行
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def limited_dialogue(query: str) -> PrismResponse:
                async with semaphore:
                    return await self.prismatic_dialogue(query)
            
            tasks = [limited_dialogue(query) for query in queries]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理异常
            results = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    self.logger.error(f"批量对话失败 - 查询{i}: {str(response)}")
                    results.append(None)
                else:
                    results.append(response)
            
            return results
        
        else:
            # 串行执行
            results = []
            for query in queries:
                try:
                    response = await self.prismatic_dialogue(query)
                    results.append(response)
                except Exception as e:
                    self.logger.error(f"批量对话失败: {str(e)}")
                    results.append(None)
            
            return results
    
    async def analyze_conversation_patterns(
        self,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        分析对话模式
        
        Args:
            session_id: 会话ID，None表示当前会话
            limit: 分析的消息数量限制
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        target_session_id = session_id or self.session_id
        messages = [m for m in self.message_history if m.session_id == target_session_id]
        
        if not messages:
            return {"error": "没有找到相关对话记录"}
        
        # 限制分析数量
        messages = messages[-limit:]
        
        # 分析模式
        analysis = {
            "session_id": target_session_id,
            "total_messages": len(messages),
            "spectrum_distribution": {},
            "recursion_patterns": [],
            "whitespace_usage": {},
            "cognitive_shifts": [],
            "timeline_analysis": {
                "start_time": messages[0].timestamp if messages else None,
                "end_time": messages[-1].timestamp if messages else None,
                "message_frequency": len(messages) / (limit / 10)  # 每10条消息的频率
            }
        }
        
        # 分析光谱分布
        spectrum_counts = {}
        for msg in messages:
            for spectrum in msg.message.spectrums:
                spectrum_type = spectrum.type.value
                spectrum_counts[spectrum_type] = spectrum_counts.get(spectrum_type, 0) + 1
        
        analysis["spectrum_distribution"] = spectrum_counts
        
        # 分析递归模式
        recursion_depths = [msg.metadata.get("recursion_depth", 0) for msg in messages]
        if recursion_depths:
            analysis["recursion_patterns"] = {
                "max_depth": max(recursion_depths),
                "avg_depth": sum(recursion_depths) / len(recursion_depths),
                "depth_changes": [
                    recursion_depths[i+1] - recursion_depths[i] 
                    for i in range(len(recursion_depths)-1)
                ]
            }
        
        # 分析留白使用
        whitespace_types = {}
        for msg in messages:
            whitespace_type = msg.message.whitespace.type.value
            whitespace_types[whitespace_type] = whitespace_types.get(whitespace_type, 0) + 1
        
        analysis["whitespace_usage"] = whitespace_types
        
        # 分析认知转移
        if len(messages) >= 2:
            cognitive_shifts = []
            for i in range(1, len(messages)):
                prev_spectrums = set(s.type.value for s in messages[i-1].message.spectrums)
                curr_spectrums = set(s.type.value for s in messages[i].message.spectrums)
                
                shift = {
                    "new_spectrums": list(curr_spectrums - prev_spectrums),
                    "dropped_spectrums": list(prev_spectrums - curr_spectrums),
                    "shift_magnitude": len(curr_spectrums.symmetric_difference(prev_spectrums))
                }
                cognitive_shifts.append(shift)
            
            analysis["cognitive_shifts"] = cognitive_shifts
        
        self.logger.info(f"对话模式分析完成 - 会话: {target_session_id}, 消息数: {len(messages)}")
        
        return analysis
    
    async def _prepare_request(
        self,
        query: str,
        context: Optional[Dict[str, Any]],
        min_spectrums: Optional[int],
        max_spectrums: Optional[int],
        enable_synthesis: Optional[bool],
        recursion_path: Optional[List[str]]
    ) -> Dict[str, Any]:
        """准备请求数据"""
        # 确定光谱数量范围
        min_spec = min_spectrums or self.session_config.min_spectrums
        max_spec = max_spectrums or self.session_config.max_spectrums
        min_spec = max(3, min(min_spec, max_spec))
        
        # 确定是否启用合成
        enable_synth = enable_synthesis if enable_synthesis is not None else self.session_config.enable_synthesis
        
        # 构建上下文
        full_context = {
            "user_state": {},
            "environment": {
                "timestamp": format_timestamp(),
                "session_id": self.session_id,
                "recursion_depth": self.recursion_depth
            },
            "preferences": self.user_preferences.dict() if self.user_preferences else {}
        }
        
        if context:
            full_context.update(context)
        
        if recursion_path:
            full_context["recursion_path"] = recursion_path
        
        # 构建消息ID
        message_id = str(uuid4())
        
        return {
            "protocol": "prism-interconnect",
            "version": "1.0",
            "message_id": message_id,
            "timestamp": format_timestamp(),
            "session_id": self.session_id,
            "type": "prism_message",
            "payload": {
                "query": query,
                "context": full_context,
                "min_spectrums": min_spec,
                "max_spectrums": max_spec,
                "enable_synthesis": enable_synth
            },
            "metadata": {
                "source": "prism-sdk-python",
                "language": "zh-CN",
                "recursion_depth": self.recursion_depth,
                "max_depth": self.session_config.max_recursion_depth,
                "ttl": 3600
            }
        }
    
    async def _send_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """发送HTTP请求"""
        if not self.session or self.session.closed:
            await self.connect()
        
        url = f"{self.endpoint}/dialogue"
        
        for attempt in range(self.max_retries):
            try:
                self.metrics["total_requests"] += 1
                
                async with self.session.post(url, json=request_data) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        self.metrics["successful_requests"] += 1
                        return json.loads(response_text)
                    
                    elif response.status == 401:
                        raise AuthenticationError("API密钥无效或过期")
                    
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(retry_after)
                            continue
                        raise RateLimitError(f"速率限制，请在{retry_after}秒后重试")
                    
                    elif response.status >= 500:
                        self.metrics["failed_requests"] += 1
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # 指数退避
                            continue
                        raise PrismError(f"服务器错误: {response.status}")
                    
                    else:
                        self.metrics["failed_requests"] += 1
                        error_data = json.loads(response_text) if response_text else {}
                        raise PrismError(
                            f"请求失败: {response.status} - {error_data.get('message', '未知错误')}",
                            error_code=error_data.get("code")
                        )
            
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.metrics["failed_requests"] += 1
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise PrismError(f"网络错误: {str(e)}")
        
        raise PrismError(f"请求失败，已达到最大重试次数: {self.max_retries}")
    
    async def _process_response(
        self, 
        response_data: Dict[str, Any],
        recursion_path: Optional[List[str]]
    ) -> PrismResponse:
        """处理响应数据"""
        try:
            # 提取消息数据
            message_data = response_data.get("payload", {})
            
            # 构建光谱对象
            spectrums = []
            for spec_data in message_data.get("spectrums", []):
                spectrum = Spectrum(
                    type=SpectrumType(spec_data["type"]),
                    name=spec_data["name"],
                    perspective=spec_data["perspective"],
                    confidence=spec_data.get("confidence", 0.5),
                    reasoning=spec_data.get("reasoning"),
                    limitations=spec_data["limitations"],
                    sources=spec_data.get("sources", []),
                    emotional_tone=spec_data.get("emotional_tone", "neutral")
                )
                spectrums.append(spectrum)
            
            # 构建留白对象
            whitespace_data = message_data["whitespace"]
            whitespace = Whitespace(
                type=WhitespaceType(whitespace_data["type"]),
                duration_suggestion=whitespace_data["duration_suggestion"],
                prompt=whitespace_data["prompt"],
                purpose=whitespace_data["purpose"]
            )
            
            # 构建合成对象（如果存在）
            synthesis = None
            if "synthesis" in message_data:
                synth_data = message_data["synthesis"]
                synthesis = Synthesis(
                    emerging_insights=synth_data.get("emerging_insights", []),
                    new_questions=synth_data.get("new_questions", []),
                    action_suggestions=synth_data.get("action_suggestions", []),
                    ethical_considerations=synth_data.get("ethical_considerations", [])
                )
            
            # 构建消息对象
            message = PrismMessage(
                query=message_data["query"],
                context=message_data.get("context", {}),
                spectrums=spectrums,
                whitespace=whitespace,
                synthesis=synthesis
            )
            
            # 构建响应对象
            response = PrismResponse(
                message_id=response_data.get("message_id", str(uuid4())),
                timestamp=response_data.get("timestamp", format_timestamp()),
                session_id=response_data.get("session_id", self.session_id),
                message=message,
                metadata=response_data.get("metadata", {})
            )
            
            # 更新递归相关信息
            if recursion_path:
                response.metadata["recursion_path"] = recursion_path
            
            # 添加处理时间信息
            processing_time = response_data.get("metadata", {}).get("processing_time_ms")
            if processing_time:
                response.metadata["server_processing_time_ms"] = processing_time
            
            return response
            
        except (KeyError, ValueError) as e:
            raise PrismError(f"响应数据解析失败: {str(e)}")
    
    def _update_metrics(self, start_time: datetime, success: bool):
        """更新性能指标"""
        latency = (datetime.now() - start_time).total_seconds() * 1000  # 毫秒
        self.metrics["total_latency_ms"] += latency
        self.metrics["last_request_time"] = datetime.now()
        
        if not success:
            self.metrics["failed_requests"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        total = self.metrics["total_requests"]
        success = self.metrics["successful_requests"]
        failed = self.metrics["failed_requests"]
        
        avg_latency = 0
        if total > 0:
            avg_latency = self.metrics["total_latency_ms"] / total
        
        return {
            "session_id": self.session_id,
            "total_requests": total,
            "successful_requests": success,
            "failed_requests": failed,
            "success_rate": success / total if total > 0 else 0,
            "average_latency_ms": avg_latency,
            "current_recursion_depth": self.recursion_depth,
            "message_history_count": len(self.message_history),
            "last_request_time": self.metrics["last_request_time"]
        }
    
    def clear_history(self, keep_last: int = 0):
        """
        清除对话历史
        
        Args:
            keep_last: 保留最近的消息数量
        """
        if keep_last > 0 and len(self.message_history) > keep_last:
            self.message_history = self.message_history[-keep_last:]
        else:
            self.message_history = []
        
        self.recursion_depth = 0
        self.logger.info(f"对话历史已清除，保留{len(self.message_history)}条消息")
    
    def export_history(
        self, 
        format: str = "json",
        include_metadata: bool = True
    ) -> Union[str, Dict[str, Any]]:
        """
        导出对话历史
        
        Args:
            format: 导出格式，支持"json"或"markdown"
            include_metadata: 是否包含元数据
            
        Returns:
            导出的历史数据
        """
        if format == "json":
            export_data = {
                "session_id": self.session_id,
                "export_timestamp": format_timestamp(),
                "total_messages": len(self.message_history),
                "messages": []
            }
            
            for msg in self.message_history:
                msg_dict = {
                    "message_id": msg.message_id,
                    "timestamp": msg.timestamp,
                    "query": msg.message.query,
                    "spectrum_count": len(msg.message.spectrums),
                    "whitespace_type": msg.message.whitespace.type.value,
                    "has_synthesis": msg.message.synthesis is not None
                }
                
                if include_metadata:
                    msg_dict["metadata"] = msg.metadata
                
                export_data["messages"].append(msg_dict)
            
            return json.dumps(export_data, ensure_ascii=False, indent=2)
        
        elif format == "markdown":
            markdown = f"""# 棱镜对话历史导出

**会话ID**: {self.session_id}
**导出时间**: {format_timestamp()}
**消息总数**: {len(self.message_history)}

---
"""
            for i, msg in enumerate(self.message_history, 1):
                markdown += f"""
## 消息 {i}

**时间**: {msg.timestamp}
**查询**: {msg.message.query}

### 光谱 ({len(msg.message.spectrums)}种)
"""
                for j, spectrum in enumerate(msg.message.spectrums, 1):
                    markdown += f"""
#### {j}. {spectrum.name} ({spectrum.type.value})

{spectrum.perspective}

*置信度*: {spectrum.confidence}
*局限性*: {spectrum.limitations}
"""
                
                markdown += f"""
### 留白
**类型**: {msg.message.whitespace.type.value}
**时长**: {msg.message.whitespace.duration_suggestion}秒
**提示**: {msg.message.whitespace.prompt}
**目的**: {msg.message.whitespace.purpose}
"""
                
                if msg.message.synthesis:
                    markdown += """
### 合成洞见
"""
                    if msg.message.synthesis.emerging_insights:
                        markdown += "**涌现洞见**:\n"
                        for insight in msg.message.synthesis.emerging_insights:
                            markdown += f"- {insight}\n"
                    
                    if msg.message.synthesis.new_questions:
                        markdown += "**新问题**:\n"
                        for question in msg.message.synthesis.new_questions:
                            markdown += f"- {question}\n"
                
                if include_metadata and msg.metadata:
                    markdown += "### 元数据\n"
                    for key, value in msg.metadata.items():
                        markdown += f"- **{key}**: {value}\n"
                
                markdown += "\n---\n"
            
            return markdown
        
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            健康状态信息
        """
        try:
            if not self.session or self.session.closed:
                await self.connect()
            
            url = f"{self.endpoint}/health"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "healthy",
                        "version": data.get("version"),
                        "uptime": data.get("uptime"),
                        "timestamp": format_timestamp()
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status}",
                        "timestamp": format_timestamp()
                    }
        
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": format_timestamp()
            }
    
    def __repr__(self) -> str:
        """客户端表示"""
        metrics = self.get_metrics()
        return (
            f"PrismClient("
            f"session_id={self.session_id}, "
            f"requests={metrics['total_requests']}, "
            f"success_rate={metrics['success_rate']:.1%}, "
            f"recursion_depth={self.recursion_depth}"
            f")"
        )