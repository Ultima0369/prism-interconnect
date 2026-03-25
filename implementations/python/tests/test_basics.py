"""
🧠 棱镜协议基础测试
"""

import pytest
import asyncio
from datetime import datetime

from prism_sdk import (
    PrismClient,
    PrismMessage,
    Spectrum,
    Whitespace,
    Synthesis,
    SpectrumType,
    WhitespaceType,
    SessionConfig,
    UserPreferences
)
from prism_sdk.validators import validate_message
from prism_sdk.generators import generate_spectrums, generate_whitespace, generate_synthesis


class TestBasicModels:
    """测试基础数据模型"""
    
    def test_spectrum_creation(self):
        """测试光谱创建"""
        spectrum = Spectrum(
            type=SpectrumType.RED,
            name="测试光谱",
            perspective="这是一个测试视角，用于验证光谱创建功能。",
            confidence=0.7,
            limitations="这是一个测试，实际应用中需要更详细的局限性说明。",
            emotional_tone="neutral"
        )
        
        assert spectrum.type == SpectrumType.RED
        assert spectrum.name == "测试光谱"
        assert spectrum.confidence == 0.7
        assert spectrum.emotional_tone == "neutral"
    
    def test_whitespace_creation(self):
        """测试留白创建"""
        whitespace = Whitespace(
            type=WhitespaceType.INTEGRATION,
            duration_suggestion=45,
            prompt="测试留白提示",
            purpose="测试留白目的"
        )
        
        assert whitespace.type == WhitespaceType.INTEGRATION
        assert whitespace.duration_suggestion == 45
        assert whitespace.prompt == "测试留白提示"
    
    def test_synthesis_creation(self):
        """测试合成创建"""
        synthesis = Synthesis(
            emerging_insights=["测试洞见1", "测试洞见2"],
            new_questions=["测试问题1", "测试问题2"],
            action_suggestions=["测试建议1"],
            ethical_considerations=["测试伦理考量"]
        )
        
        assert len(synthesis.emerging_insights) == 2
        assert len(synthesis.new_questions) == 2
        assert len(synthesis.action_suggestions) == 1
        assert len(synthesis.ethical_considerations) == 1
    
    def test_prism_message_creation(self):
        """测试棱镜消息创建"""
        # 创建测试光谱
        spectrum = Spectrum(
            type=SpectrumType.RED,
            name="测试光谱",
            perspective="测试视角",
            confidence=0.7,
            limitations="测试局限性",
            emotional_tone="neutral"
        )
        
        # 创建测试留白
        whitespace = Whitespace(
            type=WhitespaceType.INTEGRATION,
            duration_suggestion=45,
            prompt="测试提示",
            purpose="测试目的"
        )
        
        # 创建消息
        message = PrismMessage(
            query="测试查询",
            spectrums=[spectrum, spectrum, spectrum],  # 3个相同光谱用于测试
            whitespace=whitespace
        )
        
        assert message.query == "测试查询"
        assert len(message.spectrums) == 3
        assert message.whitespace.type == WhitespaceType.INTEGRATION


class TestValidators:
    """测试验证器"""
    
    def test_message_validation(self):
        """测试消息验证"""
        # 创建有效消息
        spectrum = Spectrum(
            type=SpectrumType.RED,
            name="测试光谱",
            perspective="这是一个足够长的视角描述，满足验证要求。",
            confidence=0.7,
            limitations="这也是一个足够长的局限性描述。",
            emotional_tone="neutral"
        )
        
        whitespace = Whitespace(
            type=WhitespaceType.INTEGRATION,
            duration_suggestion=45,
            prompt="足够长的留白提示描述",
            purpose="足够长的留白目的描述"
        )
        
        message = PrismMessage(
            query="测试查询",
            spectrums=[spectrum, spectrum, spectrum],
            whitespace=whitespace
        )
        
        # 验证消息
        result = validate_message(message)
        assert result.valid is True
        assert len(result.errors) == 0
    
    def test_message_validation_failure(self):
        """测试消息验证失败"""
        # 创建无效消息（只有2个光谱）
        spectrum = Spectrum(
            type=SpectrumType.RED,
            name="测试光谱",
            perspective="测试视角",
            confidence=0.7,
            limitations="测试局限性",
            emotional_tone="neutral"
        )
        
        whitespace = Whitespace(
            type=WhitespaceType.INTEGRATION,
            duration_suggestion=45,
            prompt="测试提示",
            purpose="测试目的"
        )
        
        message = PrismMessage(
            query="测试查询",
            spectrums=[spectrum, spectrum],  # 只有2个光谱，应该失败
            whitespace=whitespace
        )
        
        # 验证消息
        result = validate_message(message)
        assert result.valid is False
        assert len(result.errors) > 0
        assert "至少需要3种光谱" in result.errors[0]


class TestGenerators:
    """测试生成器"""
    
    def test_spectrum_generation(self):
        """测试光谱生成"""
        query = "如何提高学习效率？"
        spectrums = generate_spectrums(
            query=query,
            min_count=3,
            max_count=5
        )
        
        assert len(spectrums) >= 3
        assert len(spectrums) <= 5
        
        # 检查光谱多样性
        spectrum_types = [s.type for s in spectrums]
        assert len(set(spectrum_types)) >= 2  # 至少2种不同类型
    
    def test_whitespace_generation(self):
        """测试留白生成"""
        # 先生成一些光谱
        query = "测试查询"
        spectrums = generate_spectrums(query=query, min_count=3, max_count=3)
        
        # 生成留白
        whitespace = generate_whitespace(spectrums=spectrums)
        
        assert whitespace.type in [WhitespaceType.INTEGRATION, WhitespaceType.REFLECTION, WhitespaceType.CREATIVE]
        assert 30 <= whitespace.duration_suggestion <= 300
        assert len(whitespace.prompt) > 10
        assert len(whitespace.purpose) > 10
    
    def test_synthesis_generation(self):
        """测试合成生成"""
        # 生成光谱
        query = "如何平衡工作与生活？"
        spectrums = generate_spectrums(query=query, min_count=3, max_count=3)
        
        # 生成合成
        synthesis = generate_synthesis(spectrums=spectrums, query=query)
        
        assert synthesis is not None
        # 合成应该至少有一些内容
        has_content = (
            len(synthesis.emerging_insights) > 0 or
            len(synthesis.new_questions) > 0 or
            len(synthesis.action_suggestions) > 0 or
            len(synthesis.ethical_considerations) > 0
        )
        assert has_content is True


class TestClientBasics:
    """测试客户端基础功能"""
    
    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """测试客户端初始化"""
        client = PrismClient(
            api_key="test-key",
            endpoint="https://api.test.prism.dev/v1"
        )
        
        assert client.api_key == "test-key"
        assert client.endpoint == "https://api.test.prism.dev/v1"
        assert client.session_id is not None
        
        # 清理
        await client.close()
    
    @pytest.mark.asyncio
    async def test_client_with_custom_config(self):
        """测试带自定义配置的客户端"""
        session_config = SessionConfig(
            min_spectrums=4,
            max_spectrums=6,
            max_recursion_depth=7
        )
        
        user_preferences = UserPreferences(
            preferred_spectrum_types=[SpectrumType.RED, SpectrumType.BLUE],
            cognitive_style="analytical"
        )
        
        client = PrismClient(
            session_config=session_config,
            user_preferences=user_preferences
        )
        
        assert client.session_config.min_spectrums == 4
        assert client.session_config.max_spectrums == 6
        assert client.user_preferences.cognitive_style == "analytical"
        
        # 清理
        await client.close()
    
    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """测试客户端上下文管理器"""
        async with PrismClient() as client:
            assert client.session is not None
            assert not client.session.closed
        
        # 离开上下文后应该已关闭
        assert client.session is None or client.session.closed


class TestUtils:
    """测试工具函数"""
    
    def test_session_id_generation(self):
        """测试会话ID生成"""
        from prism_sdk.utils import create_session_id
        
        session_id1 = create_session_id()
        session_id2 = create_session_id()
        
        assert session_id1.startswith("session-")
        assert session_id2.startswith("session-")
        assert session_id1 != session_id2  # 应该是唯一的
    
    def test_timestamp_formatting(self):
        """测试时间戳格式化"""
        from prism_sdk.utils import format_timestamp
        from datetime import datetime, timezone
        
        # 测试当前时间
        timestamp1 = format_timestamp()
        assert "T" in timestamp1  # ISO格式包含T
        
        # 测试指定时间
        test_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        timestamp2 = format_timestamp(test_time)
        assert "2023-01-01T12:00:00" in timestamp2
    
    def test_keyword_extraction(self):
        """测试关键词提取"""
        from prism_sdk.utils import extract_keywords
        
        text = "如何提高学习效率和工作效率？这是一个重要的问题。"
        keywords = extract_keywords(text, max_keywords=5)
        
        assert len(keywords) > 0
        assert "学习" in keywords or "效率" in keywords or "工作" in keywords
    
    def test_text_complexity(self):
        """测试文本复杂度计算"""
        from prism_sdk.utils import calculate_text_complexity
        
        simple_text = "你好。今天天气很好。"
        complex_text = "从认知科学的角度分析，元认知能力的发展需要系统性的训练和持续的反思实践，这涉及到多个认知维度的协同工作。"
        
        simple_score = calculate_text_complexity(simple_text)
        complex_score = calculate_text_complexity(complex_text)
        
        assert 0 <= simple_score <= 1
        assert 0 <= complex_score <= 1
        assert complex_score > simple_score  # 复杂文本应该得分更高


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])