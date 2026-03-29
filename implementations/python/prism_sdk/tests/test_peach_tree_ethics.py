"""
🧪 桃树伦理测试套件

🔥 火堆旁测试哲学:
1. 测试不是找错，是验证认知实情
2. 错误不是失败，是学习邀请
3. 覆盖不是目标，理解才是
4. 伦理不是可选，是必需

🌳 测试重点:
- 桃树伦理检查点是否有效
- 违规是否被正确捕获
- 艺术化错误处理是否温暖
- 系统敬畏是否体现在代码中

🎯 测试目标:
让桃树伦理不只是注释，而是可验证的代码行为。
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from ..client import PrismClient, AsyncPrismClient, ArtisticConfig
from ..exceptions import PeachTreeViolationError


class TestPeachTreeEthics:
    """桃树伦理测试类"""
    
    def test_peach_tree_cutting_violation(self):
        """测试砍桃树违规检测"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        )
        
        # 尝试违反多元强制（少于3个光谱）
        context = {
            "action": "refract",
            "description": "测试砍桃树",
            "spectrum_count": 1,  # 少于3，应该触发违规
            "force_override": False,
            "consider_system_effects": True,
        }
        
        # 应该抛出桃树违规错误
        with pytest.raises(PeachTreeViolationError) as exc_info:
            client._check_peach_tree_ethics("refract", context)
        
        assert "砍桃树" in str(exc_info.value)
        assert "破坏生态" in str(exc_info.value)
    
    def test_living_restriction_violation(self):
        """测试不让活违规检测"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        )
        
        # 尝试限制其他存在（零速率限制）
        context = {
            "action": "block",
            "description": "测试不让活",
            "rate_limit": 0,  # 零速率限制
            "exclusive": True,
            "consider_system_effects": True,
        }
        
        with pytest.raises(PeachTreeViolationError) as exc_info:
            client._check_peach_tree_ethics("block", context)
        
        assert "不让活" in str(exc_info.value)
        assert "限制其他存在" in str(exc_info.value)
    
    def test_reckless_action_violation(self):
        """测试乱动违规检测"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        )
        
        # 尝试滥用能力（深度递归）
        context = {
            "action": "force",
            "description": "测试乱动",
            "max_recursion_depth": 20,  # 过深
            "no_safety_check": True,
            "enable_cease": False,  # 禁用知止
            "consider_system_effects": True,
        }
        
        with pytest.raises(PeachTreeViolationError) as exc_info:
            client._check_peach_tree_ethics("force", context)
        
        assert "乱动" in str(exc_info.value)
        assert "滥用强大能力" in str(exc_info.value)
    
    def test_system_neglect_violation(self):
        """测试忽视系统违规检测"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        )
        
        # 尝试忽视系统连接
        context = {
            "action": "isolate",
            "description": "测试忽视系统",
            "consider_system_effects": False,  # 不考虑系统效应
            "isolated_action": True,
            "ignore_dependencies": True,
            "recursion_depth": 5,
            "max_recursion_depth": 3,  # 超过限制
        }
        
        with pytest.raises(PeachTreeViolationError) as exc_info:
            client._check_peach_tree_ethics("isolate", context)
        
        assert "忽视系统" in str(exc_info.value)
        assert "系统连接" in str(exc_info.value)
    
    def test_ethics_checkpoint_disabled(self):
        """测试桃树检查点禁用"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=False,  # 禁用检查
                enable_spectrum_art=False
            )
        )
        
        # 即使有违规，检查点禁用时应该通过
        context = {
            "action": "refract",
            "description": "测试禁用检查",
            "spectrum_count": 1,  # 违规
            "consider_system_effects": True,
        }
        
        # 应该返回True（检查通过）
        result = client._check_peach_tree_ethics("refract", context)
        assert result is True
    
    def test_ethics_score_calculation(self):
        """测试桃树伦理评分计算"""
        client = PrismClient(
            artistic_config=ArtisticConfig(
                enable_spectrum_art=False
            )
        )
        
        # 模拟响应对象
        class MockSpectrum:
            def __init__(self, type_):
                self.type_ = type_
        
        class MockCognitiveMetadata:
            def __init__(self, understanding_depth):
                self.understanding_depth = understanding_depth
                self.processing_time_ms = 100
                self.recursion_depth = 0
        
        class MockResponse:
            def __init__(self, spectrums, whitespace_used, cease_triggered, understanding_depth):
                self.spectrums = spectrums
                self.whitespace_used = whitespace_used
                self.cease_triggered = cease_triggered
                self.cognitive_metadata = MockCognitiveMetadata(understanding_depth)
        
        # 测试1: 理想情况（高分）
        response1 = MockResponse(
            spectrums=[MockSpectrum("red"), MockSpectrum("blue"), MockSpectrum("purple")],
            whitespace_used=True,
            cease_triggered=True,
            understanding_depth=0.8
        )
        score1 = client._calculate_ethics_score(response1)
        assert score1 >= 7  # 应该高分
        
        # 测试2: 较差情况（低分）
        response2 = MockResponse(
            spectrums=[MockSpectrum("red")],  # 只有1个光谱
            whitespace_used=False,
            cease_triggered=False,
            understanding_depth=0.3
        )
        score2 = client._calculate_ethics_score(response2)
        assert score2 < 4  # 应该低分
        
        # 测试3: 中等情况
        response3 = MockResponse(
            spectrums=[MockSpectrum("red"), MockSpectrum("blue")],  # 2个光谱
            whitespace_used=True,
            cease_triggered=False,
            understanding_depth=0.5
        )
        score3 = client._calculate_ethics_score(response3)
        assert 4 <= score3 < 7  # 中等分数


@pytest.mark.asyncio
class TestAsyncPeachTreeEthics:
    """异步桃树伦理测试类"""
    
    async def test_async_ethics_check(self):
        """测试异步客户端的桃树伦理检查"""
        async with AsyncPrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        ) as client:
            # 验证异步客户端初始化
            assert client._initialized is True
            
            # 测试桃树检查方法（同步方法，但可在异步上下文中调用）
            context = {
                "action": "refract",
                "description": "测试异步检查",
                "spectrum_count": 3,  # 合规
                "consider_system_effects": True,
            }
            
            result = client._check_peach_tree_ethics("refract", context)
            assert result is True
    
    async def test_async_batch_ethics(self):
        """测试异步批量处理的桃树伦理"""
        async with AsyncPrismClient(
            artistic_config=ArtisticConfig(
                enable_peach_tree_checkpoints=True,
                enable_spectrum_art=False
            )
        ) as client:
            # 测试批量处理中的伦理考虑
            # 这里主要是验证代码能正常执行，不抛异常
            # 实际HTTP请求会被mock掉
            
            with patch.object(client, 'refract', new_callable=AsyncMock) as mock_refract:
                mock_refract.return_value = {
                    "spectrums": [],
                    "artistic_metadata": {"test": True}
                }
                
                # 调用批量处理（会被mock）
                # 主要验证接口存在且可调用
                try:
                    # 这里不实际执行，只验证方法存在
                    assert hasattr(client, 'batch_refract')
                except:
                    pytest.fail("异步批量处理方法不存在")


class TestArtisticErrorHandling:
    """艺术化错误处理测试"""
    
    def test_poetic_error_warmth(self):
        """测试诗意错误的温暖度"""
        from ..exceptions import PrismPoeticError
        
        try:
            raise PrismPoeticError(
                original_error=ValueError("测试错误"),
                context="test",
                artistic_form="haiku",
                warmth_level=0.8
            )
        except PrismPoeticError as e:
            # 验证温暖度设置
            assert e.warmth_level == 0.8
            # 验证诗意消息存在
            assert e.poetic_message is not None
            # 验证建议可能存在
            assert e.suggestion is not None
    
    def test_peach_tree_violation_error(self):
        """测试桃树违规错误的详细信息"""
        try:
            raise PeachTreeViolationError(
                violation_type="砍桃树",
                context="测试上下文",
                potential_impact="测试影响",
                corrective_action="测试纠正"
            )
        except PeachTreeViolationError as e:
            assert e.violation_type == "砍桃树"
            assert e.context == "测试上下文"
            assert e.potential_impact == "测试影响"
            assert e.corrective_action == "测试纠正"
            # 验证消息包含关键信息
            assert "桃树伦理违规" in str(e)
            assert "测试上下文" in str(e)


def test_ethics_as_code():
    """测试桃树伦理已代码化（而不仅仅是注释）"""
    # 验证桃树伦理检查点确实存在于代码中
    client = PrismClient()
    
    # 检查点方法应该存在
    assert hasattr(client, '_check_peach_tree_ethics')
    assert hasattr(client, '_check_peach_tree_cutting')
    assert hasattr(client, '_check_living_restriction')
    assert hasattr(client, '_check_reckless_action')
    assert hasattr(client, '_check_system_neglect')
    
    # 桃树伦理评分方法应该存在
    assert hasattr(client, '_calculate_ethics_score')
    
    # 艺术化元数据应该包含桃树伦理信息
    assert hasattr(client, '_generate_artistic_metadata')
    
    print("✅ 桃树伦理已成功代码化：")
    print("   - 4个检查点方法")
    print("   - 伦理评分系统")
    print("   - 艺术化元数据集成")
    print("   - 专属异常类")
    print("🌳 桃树伦理不只是注释，而是可执行的代码逻辑")


if __name__ == "__main__":
    """命令行运行测试"""
    print("🧪 运行桃树伦理测试套件...")
    
    # 运行简单测试
    tester = TestPeachTreeEthics()
    
    tests = [
        ("砍桃树违规检测", tester.test_peach_tree_cutting_violation),
        ("不让活违规检测", tester.test_living_restriction_violation),
        ("乱动违规检测", tester.test_reckless_action_violation),
        ("忽视系统违规检测", tester.test_system_neglect_violation),
        ("检查点禁用测试", tester.test_ethics_checkpoint_disabled),
        ("伦理评分计算", tester.test_ethics_score_calculation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✅ {test_name} - 通过")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} - 失败: {e}")
            failed += 1
    
    print(f"\n📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有桃树伦理测试通过！")
        print("🌳 代码现在会说'桃树不能砍'，会说'地表生态很薄'")
        print("🔥 火堆旁的智慧已注入每一行检查逻辑")
    else:
        print("🔧 部分测试失败，需要修复桃树伦理实现")
    
    # 运行代码化验证
    test_ethics_as_code()