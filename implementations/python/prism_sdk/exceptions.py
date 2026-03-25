"""
🧠 棱镜协议异常类
定义所有自定义异常
"""

from typing import Optional, Dict, Any
from .models import ValidationResult, ErrorCode


class PrismError(Exception):
    """棱镜协议基础异常"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or ErrorCode.CLIENT_ERROR.value
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error": self.__class__.__name__,
            "code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class SpectrumGenerationError(PrismError):
    """光谱生成异常"""
    
    def __init__(
        self,
        message: str = "光谱生成失败",
        spectrum_type: Optional[str] = None,
        generation_context: Optional[Dict[str, Any]] = None
    ):
        details = {
            "spectrum_type": spectrum_type,
            "generation_context": generation_context or {}
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.SPECTRUM_GENERATION_FAILED.value,
            details=details
        )


class ValidationError(PrismError):
    """验证异常"""
    
    def __init__(
        self,
        message: str,
        validation_result: Optional[ValidationResult] = None
    ):
        details = {}
        if validation_result:
            details.update({
                "errors": validation_result.errors,
                "warnings": validation_result.warnings,
                "suggestions": validation_result.suggestions
            })
        
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_FAILED.value,
            details=details
        )


class AuthenticationError(PrismError):
    """认证异常"""
    
    def __init__(
        self,
        message: str = "认证失败",
        auth_method: Optional[str] = None,
        required_scopes: Optional[list] = None
    ):
        details = {
            "auth_method": auth_method,
            "required_scopes": required_scopes or []
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.PERMISSION_DENIED.value,
            details=details
        )


class RateLimitError(PrismError):
    """速率限制异常"""
    
    def __init__(
        self,
        message: str = "速率限制",
        limit: Optional[int] = None,
        reset_time: Optional[int] = None,
        current_usage: Optional[int] = None
    ):
        details = {
            "limit": limit,
            "reset_time": reset_time,
            "current_usage": current_usage
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.RESOURCE_LIMIT.value,
            details=details
        )


class RecursionDepthError(PrismError):
    """递归深度异常"""
    
    def __init__(
        self,
        message: str = "递归深度超限",
        current_depth: int = 0,
        attempted_depth: int = 0,
        max_depth: int = 5
    ):
        details = {
            "current_depth": current_depth,
            "attempted_depth": attempted_depth,
            "max_depth": max_depth,
            "available_depth": max_depth - current_depth
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.RECURSION_LIMIT.value,
            details=details
        )


class NetworkError(PrismError):
    """网络异常"""
    
    def __init__(
        self,
        message: str = "网络错误",
        url: Optional[str] = None,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None
    ):
        details = {
            "url": url,
            "status_code": status_code,
            "response_preview": response_text[:100] if response_text else None
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.NETWORK_ERROR.value,
            details=details
        )


class TimeoutError(PrismError):
    """超时异常"""
    
    def __init__(
        self,
        message: str = "操作超时",
        timeout_seconds: Optional[float] = None,
        operation: Optional[str] = None
    ):
        details = {
            "timeout_seconds": timeout_seconds,
            "operation": operation
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.TIMEOUT_ERROR.value,
            details=details
        )


class ConfigurationError(PrismError):
    """配置异常"""
    
    def __init__(
        self,
        message: str = "配置错误",
        config_key: Optional[str] = None,
        expected_value: Optional[Any] = None,
        actual_value: Optional[Any] = None
    ):
        details = {
            "config_key": config_key,
            "expected_value": expected_value,
            "actual_value": actual_value
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.CLIENT_ERROR.value,
            details=details
        )


class ResourceExhaustedError(PrismError):
    """资源耗尽异常"""
    
    def __init__(
        self,
        message: str = "资源耗尽",
        resource_type: Optional[str] = None,
        limit: Optional[int] = None,
        usage: Optional[int] = None
    ):
        details = {
            "resource_type": resource_type,
            "limit": limit,
            "usage": usage,
            "available": limit - usage if limit and usage else None
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.RESOURCE_LIMIT.value,
            details=details
        )


class MaintenanceError(PrismError):
    """维护模式异常"""
    
    def __init__(
        self,
        message: str = "系统维护中",
        estimated_resume_time: Optional[str] = None,
        maintenance_reason: Optional[str] = None
    ):
        details = {
            "estimated_resume_time": estimated_resume_time,
            "maintenance_reason": maintenance_reason
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.MAINTENANCE_MODE.value,
            details=details
        )


class EthicalViolationError(PrismError):
    """伦理违规异常"""
    
    def __init__(
        self,
        message: str = "伦理规则违规",
        violated_principle: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        suggested_alternative: Optional[str] = None
    ):
        details = {
            "violated_principle": violated_principle,
            "context": context or {},
            "suggested_alternative": suggested_alternative
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.CLIENT_ERROR.value,
            details=details
        )


class CognitiveOverloadError(PrismError):
    """认知过载异常"""
    
    def __init__(
        self,
        message: str = "认知过载保护触发",
        current_load: Optional[float] = None,
        max_load: Optional[float] = None,
        load_factors: Optional[Dict[str, float]] = None
    ):
        details = {
            "current_load": current_load,
            "max_load": max_load,
            "load_factors": load_factors or {},
            "suggestion": "建议进行整合留白或结束当前会话"
        }
        super().__init__(
            message=message,
            error_code=ErrorCode.CLIENT_ERROR.value,
            details=details
        )


# 异常处理工具函数
def handle_prism_error(error: Exception) -> Dict[str, Any]:
    """
    处理棱镜异常，返回标准化错误响应
    
    Args:
        error: 捕获的异常
        
    Returns:
        标准化错误响应字典
    """
    if isinstance(error, PrismError):
        return error.to_dict()
    
    # 处理非棱镜异常
    return {
        "error": error.__class__.__name__,
        "code": ErrorCode.SERVER_ERROR.value,
        "message": str(error),
        "details": {
            "exception_type": error.__class__.__name__,
            "suggestion": "请检查输入数据或联系系统管理员"
        }
    }


def is_recoverable_error(error: PrismError) -> bool:
    """
    判断错误是否可恢复
    
    Args:
        error: 棱镜异常
        
    Returns:
        是否可恢复
    """
    # 网络错误、超时错误、速率限制通常可恢复
    recoverable_codes = {
        ErrorCode.NETWORK_ERROR.value,
        ErrorCode.TIMEOUT_ERROR.value,
        ErrorCode.RATE_LIMIT.value,
        ErrorCode.MAINTENANCE_MODE.value
    }
    
    return error.error_code in recoverable_codes


def get_retry_delay(error: PrismError, attempt: int) -> float:
    """
    获取重试延迟时间（指数退避）
    
    Args:
        error: 棱镜异常
        attempt: 当前尝试次数
        
    Returns:
        重试延迟时间（秒）
    """
    base_delay = 1.0
    
    # 根据错误类型调整基础延迟
    if error.error_code == ErrorCode.RATE_LIMIT.value:
        base_delay = 5.0
    elif error.error_code == ErrorCode.MAINTENANCE_MODE.value:
        base_delay = 30.0
    
    # 指数退避：base_delay * 2^(attempt-1)
    return base_delay * (2 ** (attempt - 1))