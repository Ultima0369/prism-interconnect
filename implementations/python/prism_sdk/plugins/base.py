"""
🔌 插件基础类
定义所有插件的基类和异常
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class PluginError(Exception):
    """插件基础异常"""
    pass


class PluginConfigError(PluginError):
    """插件配置异常"""
    pass


class PluginRuntimeError(PluginError):
    """插件运行时异常"""
    pass


class BasePlugin(ABC):
    """插件基类"""
    
    # 必需属性（子类必须定义）
    plugin_id: str = None          # 插件唯一标识符
    plugin_name: str = None        # 插件显示名称
    plugin_version: str = None     # 插件版本
    
    # 可选属性
    plugin_description: str = ""   # 插件描述
    plugin_author: str = ""        # 插件作者
    plugin_license: str = "MIT"    # 插件许可证
    
    # 配置模式（JSON Schema）
    config_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "enabled": {"type": "boolean", "default": True},
            "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"], "default": "INFO"},
        },
        "required": ["enabled"]
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """初始化插件
        
        Args:
            config: 插件配置字典
        """
        self.config = config or {}
        self._apply_default_config()
        self._validate_config()
        
        # 初始化状态
        self.initialized = False
        self.enabled = self.config.get("enabled", True)
        
        # 设置日志
        self.logger = logging.getLogger(f"prism.plugin.{self.plugin_id}")
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        self.logger.setLevel(log_level)
        
        # 性能指标
        self.metrics = {
            "call_count": 0,
            "total_duration": 0.0,
            "error_count": 0,
            "last_call_time": None,
            "startup_time": datetime.now(),
        }
    
    def _apply_default_config(self):
        """应用默认配置"""
        if "properties" in self.config_schema:
            for prop_name, prop_schema in self.config_schema["properties"].items():
                if prop_name not in self.config and "default" in prop_schema:
                    self.config[prop_name] = prop_schema["default"]
    
    def _validate_config(self):
        """验证配置"""
        if "required" in self.config_schema:
            for required_field in self.config_schema["required"]:
                if required_field not in self.config:
                    raise PluginConfigError(
                        f"缺少必需配置字段: {required_field}"
                    )
    
    async def initialize(self):
        """初始化插件
        
        子类可以重写此方法执行初始化逻辑
        """
        if not self.enabled:
            self.logger.info("插件已禁用，跳过初始化")
            return
        
        try:
            await self._initialize()
            self.initialized = True
            self.logger.info(f"插件初始化完成: {self.plugin_name} v{self.plugin_version}")
        except Exception as e:
            self.logger.error(f"插件初始化失败: {e}")
            raise PluginError(f"初始化失败: {e}") from e
    
    @abstractmethod
    async def _initialize(self):
        """子类实现的初始化逻辑"""
        pass
    
    async def cleanup(self):
        """清理插件资源
        
        子类可以重写此方法执行清理逻辑
        """
        if not self.initialized:
            return
        
        try:
            await self._cleanup()
            self.initialized = False
            self.logger.info("插件清理完成")
        except Exception as e:
            self.logger.error(f"插件清理失败: {e}")
            raise PluginError(f"清理失败: {e}") from e
    
    async def _cleanup(self):
        """子类实现的清理逻辑"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "id": self.plugin_id,
            "name": self.plugin_name,
            "version": self.plugin_version,
            "description": self.plugin_description,
            "author": self.plugin_author,
            "license": self.plugin_license,
            "enabled": self.enabled,
            "initialized": self.initialized,
            "config": self.config,
            "metrics": self.get_metrics(),
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取插件性能指标"""
        avg_duration = 0.0
        if self.metrics["call_count"] > 0:
            avg_duration = self.metrics["total_duration"] / self.metrics["call_count"]
        
        error_rate = 0.0
        if self.metrics["call_count"] > 0:
            error_rate = self.metrics["error_count"] / self.metrics["call_count"]
        
        uptime = (datetime.now() - self.metrics["startup_time"]).total_seconds()
        
        return {
            "call_count": self.metrics["call_count"],
            "avg_duration_ms": avg_duration * 1000,
            "error_count": self.metrics["error_count"],
            "error_rate": error_rate,
            "last_call_time": self.metrics["last_call_time"],
            "uptime_seconds": uptime,
        }
    
    async def call_with_metrics(self, func, *args, **kwargs):
        """带性能监控的调用"""
        if not self.enabled or not self.initialized:
            raise PluginRuntimeError("插件未启用或未初始化")
        
        start_time = datetime.now()
        self.metrics["call_count"] += 1
        
        try:
            result = await func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            self.metrics["total_duration"] += duration
            self.metrics["last_call_time"] = datetime.now().isoformat()
            return result
        except Exception as e:
            self.metrics["error_count"] += 1
            self.logger.error(f"插件调用失败: {e}")
            raise
    
    def enable(self):
        """启用插件"""
        if self.enabled:
            return
        
        self.enabled = True
        self.config["enabled"] = True
        self.logger.info("插件已启用")
    
    def disable(self):
        """禁用插件"""
        if not self.enabled:
            return
        
        self.enabled = False
        self.config["enabled"] = False
        self.logger.info("插件已禁用")
    
    def update_config(self, new_config: Dict[str, Any]):
        """更新插件配置"""
        # 保留现有配置，只更新提供的字段
        for key, value in new_config.items():
            self.config[key] = value
        
        self._validate_config()
        
        # 重新应用配置
        if "log_level" in new_config:
            log_level = getattr(logging, new_config["log_level"])
            self.logger.setLevel(log_level)
        
        if "enabled" in new_config:
            if new_config["enabled"] and not self.enabled:
                self.enable()
            elif not new_config["enabled"] and self.enabled:
                self.disable()
        
        self.logger.info("配置已更新")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "plugin_id": self.plugin_id,
            "plugin_name": self.plugin_name,
            "plugin_version": self.plugin_version,
            "config": self.config,
            "info": self.get_info(),
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.plugin_name} v{self.plugin_version} ({self.plugin_id})"
    
    def __repr__(self) -> str:
        """详细表示"""
        return (f"{self.__class__.__name__}("
                f"id={self.plugin_id!r}, "
                f"name={self.plugin_name!r}, "
                f"version={self.plugin_version!r}, "
                f"enabled={self.enabled})")