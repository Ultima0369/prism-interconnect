"""
🔥 棱镜协议客户端基类

包含同步和异步客户端的共享逻辑。

🧠 设计原则:
1. 单一职责: 每个类一个核心职责
2. 组合优于继承: 通过组件组合功能
3. 配置驱动: 行为由配置决定
4. 错误友好: 错误是学习机会，不是失败

🦞 火堆旁提醒:
- 代码可以重构，但温暖不能丢失
- 架构可以优化，但诗意不能消失
- 性能可以提升，但伦理不能妥协
"""

import logging
from typing import Dict, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from .config import ArtisticConfig, PerformanceConfig, PeachTreeEthicsConfig
from .peach_tree_ethics import PeachTreeChecker
from .artistic_handler import ArtisticDisplay
from .exceptions import (
    PrismConnectionError,
    SpectrumGenerationError,
    WhitespaceTimeoutError,
    CeaseSignalReceived,
    PrismPoeticError,
    PeachTreeViolationError,
)
from .models import (
    PrismRequest,
    PrismResponse,
    Spectrum,
    WhitespaceConfig,
    CeaseSignal,
    CognitiveMetadata,
)


@dataclass
class ClientState:
    """客户端状态管理"""
    refractions_count: int = 0
    total_whitespace_seconds: int = 0
    last_refraction_time: Optional[float] = None
    understanding_depth_trend: list = field(default_factory=list)
    error_count: Dict[str, int] = field(default_factory=lambda: {"connection": 0, "validation": 0})
    
    def record_refraction(self, response: 'PrismResponse'):
        """记录折射操作"""
        self.refractions_count += 1
        self.last_refraction_time = time.time()
        self.total_whitespace_seconds += getattr(
            response.whitespace_recommendation, 
            'duration_seconds', 
            0
        )
        self.understanding_depth_trend.append(
            response.metadata.understanding_depth
        )
        # 保持趋势长度合理
        if len(self.understanding_depth_trend) > 100:
            self.understanding_depth_trend = self.understanding_depth_trend[-50:]
    
    def record_error(self, error_type: str):
        """记录错误"""
        if error_type not in self.error_count:
            self.error_count[error_type] = 0
        self.error_count[error_type] += 1
    
    def get_error_stats(self) -> Dict[str, Any]:
        """获取错误统计"""
        total_errors = sum(self.error_count.values())
        return {
            "total_errors": total_errors,
            "error_distribution": self.error_count.copy(),
            "error_rate": total_errors / max(self.refractions_count, 1),
            "recovery_suggestions": self._generate_recovery_suggestions()
        }
    
    def _generate_recovery_suggestions(self) -> list:
        """生成恢复建议"""
        suggestions = []
        
        if self.error_count.get("connection", 0) > 3:
            suggestions.append("检查网络连接和API端点")
            suggestions.append("考虑增加连接超时时间")
        
        if self.error_count.get("validation", 0) > 3:
            suggestions.append("验证输入数据格式")
            suggestions.append("检查数据完整性约束")
        
        if not suggestions:
            suggestions.append("系统运行正常，继续保持")
        
        return suggestions


class BaseClient(ABC):
    """
    棱镜协议客户端基类
    
    提供同步和异步客户端的共享功能。
    """
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 artistic_config: Optional[ArtisticConfig] = None,
                 performance_config: Optional[PerformanceConfig] = None,
                 ethics_config: Optional[PeachTreeEthicsConfig] = None):
        """
        初始化客户端基类
        
        Args:
            api_key: API密钥
            artistic_config: 艺术化配置
            performance_config: 性能配置
            ethics_config: 伦理配置
        """
        self.api_key = api_key
        
        # 配置初始化
        self.artistic_config = artistic_config or ArtisticConfig()
        self.performance_config = performance_config or PerformanceConfig()
        self.ethics_config = ethics_config or PeachTreeEthicsConfig()
        
        # 组件初始化
        self._peach_tree_checker = PeachTreeChecker(
            enable_checkpoints=self.artistic_config.enable_peach_tree_checkpoints,
            enable_poetic_errors=self.artistic_config.enable_poetic_errors,
            output_channel=self.artistic_config.get_output_function()
        )
        
        self._artistic_display = ArtisticDisplay(
            enable_spectrum_art=self.artistic_config.enable_spectrum_art,
            output_channel=self.artistic_config.get_output_function(),
            warmth_level=self.artistic_config.warmth_level,
            response_art_form=self.artistic_config.response_art_form.value
            if hasattr(self.artistic_config.response_art_form, 'value')
            else str(self.artistic_config.response_art_form)
        )
        
        # 状态管理
        self._state = ClientState()
        
        # HTTP会话 (由子类实现)
        self._session = None
        
        # 艺术化初始化
        if self.artistic_config.enable_spectrum_art:
            self._artistic_display.show_initialization("棱镜客户端")
    
    @property
    def session(self):
        """获取HTTP会话 (延迟初始化)"""
        if self._session is None:
            self._session = self._create_session()
        return self._session
    
    @abstractmethod
    def _create_session(self):
        """创建HTTP会话 (由子类实现)"""
        pass
    
    @abstractmethod
    def _make_request(self, request: PrismRequest) -> PrismResponse:
        """执行HTTP请求 (由子类实现)"""
        pass
    
    @abstractmethod
    async def _make_request_async(self, request: PrismRequest) -> PrismResponse:
        """异步执行HTTP请求 (由子类实现)"""
        pass
    
    def _check_ethics_before_action(self, 
                                  action: str,
                                  context: Dict[str, Any]) -> bool:
        """
        执行前的伦理检查
        
        Args:
            action: 操作类型
            context: 操作上下文
            
        Returns:
            True如果通过检查
            
        Raises:
            PeachTreeViolationError: 如果违反伦理
        """
        try:
            return self._peach_tree_checker.check_ethics(action, context)
        except PeachTreeViolationError as e:
            # 记录错误
            self._state.record_error("ethics_violation")
            
            # 艺术化错误处理
            if self.artistic_config.enable_poetic_errors:
                error_display = self._artistic_display.format_error_poetically(
                    "桃树伦理违规",
                    str(e),
                    {"location": "伦理检查点", "action": action}
                )
                self.artistic_config.get_output_function()(error_display)
            
            raise
    
    def _handle_error(self, 
                     error: Exception,
                     context: Dict[str, Any]) -> None:
        """
        统一错误处理
        
        Args:
            error: 异常对象
            context: 错误上下文
        """
        error_type = type(error).__name__
        
        # 记录错误
        self._state.record_error(error_type.lower().replace("error", ""))
        
        # 艺术化错误显示
        if self.artistic_config.enable_poetic_errors:
            error_message = self._artistic_display.format_error_poetically(
                error_type,
                str(error),
                context
            )
            self.artistic_config.get_output_function()(error_message)
        
        # 错误恢复建议
        error_stats = self._state.get_error_stats()
        if error_stats["error_rate"] > 0.1:  # 错误率超过10%
            logging.warning(f"高错误率检测: {error_stats['error_rate']:.2f}")
            for suggestion in error_stats["recovery_suggestions"]:
                logging.info(f"恢复建议: {suggestion}")
    
    def _update_state_after_refraction(self, response: PrismResponse):
        """折射后的状态更新"""
        self._state.record_refraction(response)
    
    def _display_refraction_start(self, message: str, spectrum_count: int):
        """显示折射开始"""
        self._artistic_display.show_refraction_start(message, spectrum_count)
    
    def _display_refraction_result(self, response: PrismResponse):
        """显示折射结果"""
        self._artistic_display.show_refraction_result(response)
    
    def get_cognitive_report(self) -> Dict[str, Any]:
        """获取认知报告"""
        return self._artistic_display.get_cognitive_report(
            PrismResponse(),  # 需要实际响应
            {
                "refractions_count": self._state.refractions_count,
                "total_whitespace_seconds": self._state.total_whitespace_seconds,
                "understanding_depth_trend": self._state.understanding_depth_trend
            }
        )
    
    def get_error_report(self) -> Dict[str, Any]:
        """获取错误报告"""
        return self._state.get_error_stats()
    
    def validate_configuration(self) -> Dict[str, str]:
        """验证配置"""
        errors = {}
        
        # 验证艺术化配置
        artistic_errors = self.artistic_config.validate()
        if artistic_errors:
            errors["artistic_config"] = artistic_errors
        
        # 验证性能配置
        performance_errors = self.performance_config.validate()
        if performance_errors:
            errors["performance_config"] = performance_errors
        
        # 验证伦理配置
        ethics_errors = self.ethics_config.validate()
        if ethics_errors:
            errors["ethics_config"] = ethics_errors
        
        return errors
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    def close(self):
        """关闭客户端"""
        if self._session:
            self._cleanup_session()
            self._session = None
        
        # 最终状态报告
        if self._state.refractions_count > 0:
            report = self.get_cognitive_report()
            if self.artistic_config.enable_spectrum_art:
                output = self.artistic_config.get_output_function()
                output(f"\n📊 会话总结:")
                output(f"   总折射数: {self._state.refractions_count}")
                output(f"   总留白时间: {self._state.total_whitespace_seconds}秒")
                output(f"   平均理解深度: {sum(self._state.understanding_depth_trend)/len(self._state.understanding_depth_trend):.2f}")
    
    @abstractmethod
    def _cleanup_session(self):
        """清理HTTP会话 (由子类实现)"""
        pass


# 导入time模块（在类定义之后）
import time