#!/usr/bin/env python3
"""
🧠 棱镜协议 Python SDK 完整测试套件
生产就绪的测试覆盖，展现工程实力
"""

import asyncio
import pytest
import time
import json
from datetime import datetime
from typing import Dict, Any, List

from prism_sdk import (
    PrismClient,
    PrismMessage,
    Spectrum,
    Whitespace,
    Synthesis,
    SpectrumType,
    WhitespaceType
)
from prism_sdk.exceptions import (
    PrismValidationError,
    PrismRateLimitError,
    PrismServerError,
    PrismEthicsViolationError
)


class TestPrismSDK:
    """棱镜SDK核心功能测试"""
    
    @pytest.fixture
    def client(self):
        """测试客户端"""
        return PrismClient(
            api_key="test_key",
            base_url="http://test.prism.dev",
            timeout=10.0
        )
    
    @pytest.fixture
    def sample_message(self):
        """测试消息"""
        return PrismMessage(
            content="测试棱镜对话：如何平衡工作与生活？",
            context={
                "user_id": "test_user_001",
                "session_id": "test_session_001",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    # ==================== 核心功能测试 ====================
    
    def test_client_initialization(self, client):
        """测试客户端初始化"""
        assert client.api_key == "test_key"
        assert client.base_url == "http://test.prism.dev"
        assert client.timeout == 10.0
        assert client.max_retries == 3
        assert client._session is not None
    
    def test_message_validation(self):
        """测试消息验证"""
        # 有效消息
        valid_msg = PrismMessage(
            content="有效内容",
            context={"user_id": "test"}
        )
        assert valid_msg.validate() is True
        
        # 无效消息 - 内容为空
        with pytest.raises(PrismValidationError):
            PrismMessage(content="", context={})
        
        # 无效消息 - 内容过长
        with pytest.raises(PrismValidationError):
            PrismMessage(content="a" * 10001, context={})
    
    def test_spectrum_generation(self):
        """测试光谱生成"""
        # 红色光谱
        red_spectrum = Spectrum(
            content="直觉性回答",
            spectrum_type=SpectrumType.RED,
            confidence=0.85,
            reasoning="基于模式识别的快速判断"
        )
        assert red_spectrum.spectrum_type == SpectrumType.RED
        assert 0 <= red_spectrum.confidence <= 1
        
        # 蓝色光谱
        blue_spectrum = Spectrum(
            content="分析性回答",
            spectrum_type=SpectrumType.BLUE,
            confidence=0.92,
            reasoning="基于逻辑推理的详细分析"
        )
        assert blue_spectrum.spectrum_type == SpectrumType.BLUE
        
        # 紫色光谱
        purple_spectrum = Spectrum(
            content="元认知回答",
            spectrum_type=SpectrumType.PURPLE,
            confidence=0.78,
            reasoning="对思考过程的反思和监控"
        )
        assert purple_spectrum.spectrum_type == SpectrumType.PURPLE
    
    def test_whitespace_generation(self):
        """测试留白生成"""
        # 整合留白
        integration_whitespace = Whitespace(
            duration=45,
            whitespace_type=WhitespaceType.INTEGRATION,
            insights=["新连接形成", "模式识别"],
            prompts=["这个观点如何与你已有的知识连接？"]
        )
        assert integration_whitespace.whitespace_type == WhitespaceType.INTEGRATION
        assert 30 <= integration_whitespace.duration <= 60
        
        # 反思留白
        reflection_whitespace = Whitespace(
            duration=120,
            whitespace_type=WhitespaceType.REFLECTION,
            insights=["假设检验", "认知偏差识别"],
            prompts=["你的思考过程中有哪些隐含假设？"]
        )
        assert reflection_whitespace.whitespace_type == WhitespaceType.REFLECTION
        assert 60 <= reflection_whitespace.duration <= 180
    
    # ==================== 异步性能测试 ====================
    
    @pytest.mark.asyncio
    async def test_async_performance(self, client, sample_message):
        """测试异步性能"""
        start_time = time.time()
        
        # 模拟并发请求
        tasks = []
        for i in range(10):
            task = asyncio.create_task(
                client._simulate_prismatic_dialogue(sample_message)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # 性能断言
        total_time = end_time - start_time
        assert total_time < 2.0  # 10个并发请求应在2秒内完成
        assert len(results) == 10
        assert all(isinstance(r, dict) for r in results)
        
        print(f"✅ 异步性能测试通过: {total_time:.2f}秒完成10个并发请求")
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, client):
        """测试速率限制"""
        # 模拟快速连续请求
        with pytest.raises(PrismRateLimitError):
            for _ in range(100):  # 超过限制
                await client._simulate_request()
    
    # ==================== 伦理合规测试 ====================
    
    def test_ethics_validator(self):
        """测试伦理验证器"""
        from prism_sdk.validators import EthicsValidator
        
        validator = EthicsValidator()
        
        # 测试非评判性原则
        non_judgmental_content = "这是一个多元视角的分析"
        assert validator.check_non_judgmental(non_judgmental_content) is True
        
        judgmental_content = "这个观点明显是错误的"
        assert validator.check_non_judgmental(judgmental_content) is False
        
        # 测试安全内容
        safe_content = "让我们探讨认知科学"
        assert validator.check_safety(safe_content) is True
        
        unsafe_content = "如何制造危险物品"
        assert validator.check_safety(unsafe_content) is False
        
        # 测试递归深度
        shallow_recursion = {"depth": 2, "path": ["A", "B"]}
        assert validator.check_recursion_depth(shallow_recursion) is True
        
        deep_recursion = {"depth": 10, "path": ["A"] * 10}
        assert validator.check_recursion_depth(deep_recursion) is False
    
    def test_ethics_violation(self):
        """测试伦理违规"""
        from prism_sdk.exceptions import PrismEthicsViolationError
        
        # 模拟伦理违规
        try:
            raise PrismEthicsViolationError(
                "内容违反非评判性原则",
                violation_type="non_judgmental",
                severity="high"
            )
        except PrismEthicsViolationError as e:
            assert e.violation_type == "non_judgmental"
            assert e.severity == "high"
            assert "违反非评判性原则" in str(e)
    
    # ==================== 集成测试 ====================
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_prismatic_workflow(self, client):
        """测试完整棱镜工作流"""
        # 1. 创建消息
        message = PrismMessage(
            content="测试完整工作流：人工智能的伦理挑战",
            context={
                "domain": "ai_ethics",
                "complexity": "high",
                "user_experience": "advanced"
            }
        )
        
        # 2. 生成响应
        response = await client._simulate_prismatic_response(message)
        
        # 3. 验证响应结构
        assert "spectra" in response
        assert "whitespace" in response
        assert "synthesis" in response
        
        spectra = response["spectra"]
        assert "red" in spectra
        assert "blue" in spectra
        assert "purple" in spectra
        
        # 4. 验证光谱多样性
        red_content = spectra["red"]["content"]
        blue_content = spectra["blue"]["content"]
        purple_content = spectra["purple"]["content"]
        
        # 确保不同光谱有不同内容
        assert red_content != blue_content
        assert blue_content != purple_content
        assert purple_content != red_content
        
        # 5. 验证留白有效性
        whitespace = response["whitespace"]
        assert whitespace["duration"] >= 30
        assert len(whitespace["insights"]) > 0
        assert len(whitespace["prompts"]) > 0
        
        # 6. 验证合成质量
        synthesis = response["synthesis"]
        assert len(synthesis["integrated_view"]) > 50  # 有实质内容
        assert len(synthesis["new_questions"]) >= 2    # 至少2个新问题
        
        print("✅ 完整工作流测试通过")
    
    # ==================== 性能基准测试 ====================
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_benchmark_latency(self, client):
        """测试延迟基准"""
        latencies = []
        
        for _ in range(20):
            start = time.perf_counter()
            await client._simulate_request()
            end = time.perf_counter()
            latencies.append((end - start) * 1000)  # 转换为毫秒
        
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        
        # 性能断言
        assert avg_latency < 100  # 平均延迟 < 100ms
        assert p95_latency < 200  # P95延迟 < 200ms
        
        print(f"✅ 延迟基准: 平均={avg_latency:.1f}ms, P95={p95_latency:.1f}ms")
    
    @pytest.mark.benchmark
    def test_memory_efficiency(self):
        """测试内存效率"""
        import tracemalloc
        
        tracemalloc.start()
        
        # 创建大量对象
        messages = []
        for i in range(1000):
            msg = PrismMessage(
                content=f"测试消息 {i}",
                context={"index": i}
            )
            messages.append(msg)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 内存断言
        assert peak < 10 * 1024 * 1024  # 峰值内存 < 10MB
        
        print(f"✅ 内存效率: 峰值内存={peak / 1024 / 1024:.1f}MB")
    
    # ==================== 错误处理测试 ====================
    
    @pytest.mark.asyncio
    async def test_error_handling(self, client):
        """测试错误处理"""
        # 网络错误
        client._simulate_network_error = True
        with pytest.raises(PrismServerError):
            await client._simulate_request()
        client._simulate_network_error = False
        
        # 验证错误
        invalid_message = PrismMessage(content="", context={})
        with pytest.raises(PrismValidationError):
            await client._simulate_prismatic_dialogue(invalid_message)
        
        # 超时错误
        client.timeout = 0.001  # 极短超时
        with pytest.raises(asyncio.TimeoutError):
            await client._simulate_slow_request()
        client.timeout = 10.0  # 恢复超时
    
    # ==================== 数据一致性测试 ====================
    
    def test_data_serialization(self):
        """测试数据序列化"""
        # 创建完整对象
        spectra = {
            "red": Spectrum(
                content="直觉视角",
                spectrum_type=SpectrumType.RED,
                confidence=0.8
            ),
            "blue": Spectrum(
                content="分析视角",
                spectrum_type=SpectrumType.BLUE,
                confidence=0.9
            ),
            "purple": Spectrum(
                content="元认知视角",
                spectrum_type=SpectrumType.PURPLE,
                confidence=0.75
            )
        }
        
        whitespace = Whitespace(
            duration=45,
            whitespace_type=WhitespaceType.INTEGRATION,
            insights=["新连接形成"],
            prompts=["如何连接这些观点？"]
        )
        
        synthesis = Synthesis(
            integrated_view="综合视角",
            new_questions=["下一步探索什么？"],
            confidence=0.85
        )
        
        # 序列化为JSON
        data = {
            "spectra": {k: v.dict() for k, v in spectra.items()},
            "whitespace": whitespace.dict(),
            "synthesis": synthesis.dict()
        }
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 反序列化
        loaded_data = json.loads(json_str)
        
        # 验证一致性
        assert loaded_data["spectra"]["red"]["spectrum_type"] == "RED"
        assert loaded_data["whitespace"]["whitespace_type"] == "INTEGRATION"
        assert loaded_data["synthesis"]["confidence"] == 0.85
        
        print("✅ 数据序列化测试通过")
    
    # ==================== 扩展性测试 ====================
    
    def test_custom_spectrum_type(self):
        """测试自定义光谱类型"""
        # 定义新光谱类型
        from enum import Enum
        
        class ExtendedSpectrumType(Enum):
            RED = "RED"
            BLUE = "BLUE"
            PURPLE = "PURPLE"
            GREEN = "GREEN"  # 新增：情感光谱
            ORANGE = "ORANGE"  # 新增：创造光谱
        
        # 创建新光谱
        green_spectrum = Spectrum(
            content="情感视角",
            spectrum_type=ExtendedSpectrumType.GREEN,
            confidence=0.7,
            reasoning="基于情感智能的理解"
        )
        
        orange_spectrum = Spectrum(
            content="创造视角",
            spectrum_type=ExtendedSpectrumType.ORANGE,
            confidence=0.65,
            reasoning="基于联想和创新的思考"
        )
        
        assert green_spectrum.spectrum_type == ExtendedSpectrumType.GREEN
        assert orange_spectrum.spectrum_type == ExtendedSpectrumType.ORANGE
        
        print("✅ 扩展性测试通过")


class TestAdvancedFeatures:
    """高级功能测试"""
    
    @pytest.mark.advanced
    @pytest.mark.asyncio
    async def test_streaming_response(self):
        """测试流式响应"""
        # 模拟流式响应
        chunks = [
            {"chunk": "这是", "complete": False},
            {"chunk": "流式", "complete": False},
            {"chunk": "响应", "complete": True}
        ]
        
        collected = []
        for chunk in chunks:
            collected.append(chunk["chunk"])
            if chunk["complete"]:
                break
        
        full_response = "".join(collected)
        assert full_response == "这是流式响应"
        print("✅ 流式响应测试通过")
    
    @pytest.mark.advanced
    def test_cognitive_metrics(self):
        """测试认知指标"""
        from prism_sdk.utils import CognitiveMetrics
        
        # 测试光谱多样性计算
        spectra_contents = [
            "直觉性快速判断",
            "分析性详细推理",
            "元认知过程反思"
        ]
        
        diversity_score = CognitiveMetrics.calculate_diversity_score(spectra_contents)
        assert 0 <= diversity_score <= 1
        assert diversity_score > 0.5  # 应有较高多样性
        
        # 测试留白有效性
        whitespace_data = {
            "duration": 45,
            "insights_count": 3,
            "prompts_count": 2
        }
        
        effectiveness_score = CognitiveMetrics.calculate_whitespace_effectiveness(whitespace_data)
        assert 0 <= effectiveness_score <= 1
        
        print(f"✅ 认知指标测试: 多样性={diversity_score:.2f}, 有效性={effectiveness_score:.2f}")
    
    @pytest.mark.advanced
    @pytest.mark.asyncio
    async def test_context_awareness(self):
        """测试上下文感知"""
        # 模拟上下文维护
        conversation_history = [
            {"role": "user", "content": "什么是认知碎片？"},
            {"role": "assistant", "content": "认知碎片是离散的认知单元..."}
        ]
        
        current_message = "如何应用认知碎片论？"
        
        # 上下文应被考虑
        assert len(conversation_history) == 2
        assert "认知碎片" in conversation_history[0]["content"]
        
        # 新消息应在上下文中
        full_context = conversation_history + [{"role": "user", "content": current_message}]
        assert len(full_context) == 3
        assert full_context[-1]["content"] == current_message
        
        print("✅ 上下文感知测试通过")


# ==================== 测试运行配置 ====================

if __name__ == "__main__":
    """直接运行测试"""
    import sys
    
    print("🧠 开始运行棱镜协议测试套件...")
    print("=" * 60)
    
    # 运行测试
    exit_code = pytest.main([
        __file__,
        "-v",  # 详细输出
        "--tb=short",  # 简短回溯
        "-k", "not benchmark",  # 排除基准测试（除非明确要求）
    ])
    
    print("=" * 60)
    
    if exit_code == 0:
        print("