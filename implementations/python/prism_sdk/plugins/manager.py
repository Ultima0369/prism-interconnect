"""
🔌 插件管理器
管理插件的加载、卸载、配置和监控
"""

import asyncio
import logging
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
from datetime import datetime
import json
import yaml

from .base import BasePlugin, PluginError, PluginConfigError
from .registry import PluginRegistry


class PluginManager:
    """插件管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化插件管理器
        
        Args:
            config_path: 插件配置文件路径
        """
        self.logger = logging.getLogger("prism.plugin_manager")
        self.registry = PluginRegistry()
        self.plugins: Dict[str, BasePlugin] = {}
        self.config_path = config_path
        
        # 加载配置
        self.config = self._load_config()
        
        # 钩子系统
        self.hooks = {}
        
        # 性能指标
        self.metrics = {
            "total_plugins": 0,
            "enabled_plugins": 0,
            "loaded_plugins": 0,
            "startup_time": datetime.now(),
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """加载插件配置"""
        if not self.config_path:
            return {}
        
        config_path = Path(self.config_path)
        if not config_path.exists():
            self.logger.warning(f"配置文件不存在: {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f) or {}
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            return {}
    
    def _save_config(self):
        """保存插件配置"""
        if not self.config_path:
            return
        
        config_path = Path(self.config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                if config_path.suffix in ['.yaml', '.yml']:
                    yaml.dump(self.config, f, default_flow_style=False)
                else:
                    json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
    
    async def discover_plugins(self, directories: List[str] = None) -> List[Dict[str, Any]]:
        """发现可用插件
        
        Args:
            directories: 要搜索的目录列表
            
        Returns:
            发现的插件信息列表
        """
        directories = directories or []
        discovered = []
        
        # 搜索目录
        for directory in directories:
            dir_path = Path(directory).expanduser()
            if not dir_path.exists():
                continue
            
            for plugin_file in dir_path.glob("*.py"):
                if plugin_file.name.startswith("_"):
                    continue
                
                plugin_info = await self._discover_plugin_file(plugin_file)
                if plugin_info:
                    discovered.append(plugin_info)
        
        # 搜索已安装的包
        discovered.extend(await self._discover_installed_packages())
        
        self.logger.info(f"发现 {len(discovered)} 个插件")
        return discovered
    
    async def _discover_plugin_file(self, plugin_file: Path) -> Optional[Dict[str, Any]]:
        """从文件发现插件"""
        try:
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(
                f"prism_plugin_{plugin_file.stem}", 
                plugin_file
            )
            if spec is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            
            # 临时添加到sys.modules
            import sys
            sys.modules[spec.name] = module
            
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                self.logger.debug(f"加载模块失败 {plugin_file}: {e}")
                return None
            
            # 查找插件类
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePlugin) and 
                    attr != BasePlugin):
                    plugin_class = attr
                    break
            
            if plugin_class is None:
                return None
            
            # 创建临时实例获取信息
            plugin = plugin_class()
            info = plugin.get_info()
            
            return {
                "type": "file",
                "path": str(plugin_file),
                "class": plugin_class,
                "info": info,
            }
            
        except Exception as e:
            self.logger.debug(f"发现插件失败 {plugin_file}: {e}")
            return None
    
    async def _discover_installed_packages(self) -> List[Dict[str, Any]]:
        """从已安装的包发现插件"""
        discovered = []
        
        try:
            # 查找所有prism_plugin_开头的包
            for module_info in pkgutil.iter_modules():
                if module_info.name.startswith("prism_plugin_"):
                    try:
                        module = importlib.import_module(module_info.name)
                        
                        # 查找插件类
                        plugin_class = None
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                issubclass(attr, BasePlugin) and 
                                attr != BasePlugin):
                                plugin_class = attr
                                break
                        
                        if plugin_class is None:
                            continue
                        
                        # 创建临时实例获取信息
                        plugin = plugin_class()
                        info = plugin.get_info()
                        
                        discovered.append({
                            "type": "package",
                            "package": module_info.name,
                            "class": plugin_class,
                            "info": info,
                        })
                        
                    except Exception as e:
                        self.logger.debug(f"加载包失败 {module_info.name}: {e}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"搜索包失败: {e}")
        
        return discovered
    
    async def load_plugin(self, plugin_id: str, plugin_class: Type[BasePlugin] = None, 
                         config: Dict[str, Any] = None) -> BasePlugin:
        """加载插件
        
        Args:
            plugin_id: 插件ID
            plugin_class: 插件类（如果为None则从注册表查找）
            config: 插件配置
            
        Returns:
            加载的插件实例
        """
        if plugin_id in self.plugins:
            self.logger.warning(f"插件已加载: {plugin_id}")
            return self.plugins[plugin_id]
        
        # 获取插件类
        if plugin_class is None:
            plugin_class = self.registry.get_plugin_class(plugin_id)
            if plugin_class is None:
                raise PluginError(f"未找到插件: {plugin_id}")
        
        # 合并配置
        plugin_config = self.config.get(plugin_id, {})
        if config:
            plugin_config.update(config)
        
        try:
            # 创建插件实例
            plugin = plugin_class(config=plugin_config)
            
            # 初始化插件
            await plugin.initialize()
            
            # 注册插件
            self.plugins[plugin_id] = plugin
            self.metrics["loaded_plugins"] += 1
            if plugin.enabled:
                self.metrics["enabled_plugins"] += 1
            
            self.logger.info(f"插件加载成功: {plugin.plugin_name} v{plugin.plugin_version}")
            
            # 保存配置
            self.config[plugin_id] = plugin.config
            self._save_config()
            
            return plugin
            
        except Exception as e:
            self.logger.error(f"加载插件失败 {plugin_id}: {e}")
            raise PluginError(f"加载失败: {e}") from e
    
    async def unload_plugin(self, plugin_id: str):
        """卸载插件"""
        if plugin_id not in self.plugins:
            self.logger.warning(f"插件未加载: {plugin_id}")
            return
        
        plugin = self.plugins[plugin_id]
        
        try:
            # 清理插件
            await plugin.cleanup()
            
            # 从管理器中移除
            del self.plugins[plugin_id]
            self.metrics["loaded_plugins"] -= 1
            if plugin.enabled:
                self.metrics["enabled_plugins"] -= 1
            
            self.logger.info(f"插件卸载成功: {plugin.plugin_name}")
            
        except Exception as e:
            self.logger.error(f"卸载插件失败 {plugin_id}: {e}")
            raise PluginError(f"卸载失败: {e}") from e
    
    async def enable_plugin(self, plugin_id: str):
        """启用插件"""
        if plugin_id not in self.plugins:
            raise PluginError(f"插件未加载: {plugin_id}")
        
        plugin = self.plugins[plugin_id]
        plugin.enable()
        
        # 更新配置
        self.config[plugin_id] = plugin.config
        self._save_config()
        
        self.metrics["enabled_plugins"] += 1
        self.logger.info(f"插件已启用: {plugin_id}")
    
    async def disable_plugin(self, plugin_id: str):
        """禁用插件"""
        if plugin_id not in self.plugins:
            raise PluginError(f"插件未加载: {plugin_id}")
        
        plugin = self.plugins[plugin_id]
        plugin.disable()
        
        # 更新配置
        self.config[plugin_id] = plugin.config
        self._save_config()
        
        self.metrics["enabled_plugins"] -= 1
        self.logger.info(f"插件已禁用: {plugin_id}")
    
    async def update_plugin_config(self, plugin_id: str, new_config: Dict[str, Any]):
        """更新插件配置"""
        if plugin_id not in self.plugins:
            raise PluginError(f"插件未加载: {plugin_id}")
        
        plugin = self.plugins[plugin_id]
        
        # 检查是否启用状态变化
        was_enabled = plugin.enabled
        new_enabled = new_config.get("enabled", was_enabled)
        
        # 更新配置
        plugin.update_config(new_config)
        
        # 更新指标
        if was_enabled and not new_enabled:
            self.metrics["enabled_plugins"] -= 1
        elif not was_enabled and new_enabled:
            self.metrics["enabled_plugins"] += 1
        
        # 保存配置
        self.config[plugin_id] = plugin.config
        self._save_config()
        
        self.logger.info(f"插件配置已更新: {plugin_id}")
    
    async def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """获取插件实例"""
        return self.plugins.get(plugin_id)
    
    async def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """获取插件信息"""
        plugin = await self.get_plugin(plugin_id)
        if plugin is None:
            return None
        
        return plugin.get_info()
    
    async def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """列出所有插件"""
        result = {}
        for plugin_id, plugin in self.plugins.items():
            result[plugin_id] = plugin.get_info()
        return result
    
    async def get_plugin_status(self, plugin_id: str) -> Dict[str, Any]:
        """获取插件状态"""
        plugin = await self.get_plugin(plugin_id)
        if plugin is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "enabled" if plugin.enabled else "disabled",
            "initialized": plugin.initialized,
            "metrics": plugin.get_metrics(),
        }
    
    async def get_plugin_metrics(self) -> Dict[str, Dict[str, Any]]:
        """获取所有插件指标"""
        metrics = {}
        for plugin_id, plugin in self.plugins.items():
            metrics[plugin_id] = plugin.get_metrics()
        return metrics
    
    async def get_plugin_health(self) -> Dict[str, Dict[str, Any]]:
        """获取插件健康状态"""
        health = {}
        for plugin_id, plugin in self.plugins.items():
            health[plugin_id] = {
                "healthy": plugin.initialized and plugin.enabled,
                "enabled": plugin.enabled,
                "initialized": plugin.initialized,
                "last_metrics": plugin.get_metrics(),
            }
        return health
    
    async def validate_plugin_config(self, plugin_id: str, config: Dict[str, Any]) -> bool:
        """验证插件配置"""
        plugin_class = self.registry.get_plugin_class(plugin_id)
        if plugin_class is None:
            return False
        
        try:
            # 创建临时实例验证配置
            plugin = plugin_class(config=config)
            return True
        except PluginConfigError:
            return False
        except Exception:
            return False
    
    async def register_hook(self, hook_name: str, plugin_id: str, callback):
        """注册钩子"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append({
            "plugin_id": plugin_id,
            "callback": callback,
        })
        
        self.logger.debug(f"钩子已注册: {hook_name} -> {plugin_id}")
    
    async def call_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """调用钩子"""
        if hook_name not in self.hooks:
            return []
        
        results = []
        for hook in self.hooks[hook_name]:
            plugin_id = hook["plugin_id"]
            callback = hook["callback"]
            
            # 检查插件是否启用
            plugin = await self.get_plugin(plugin_id)
            if plugin is None or not plugin.enabled:
                continue
            
            try:
                result = await callback(*args, **kwargs)
                results.append({
                    "plugin_id": plugin_id,
                    "result": result,
                })
            except Exception as e:
                self.logger.error(f"钩子执行失败 {hook_name} -> {plugin_id}: {e}")
        
        return results
    
    async def cleanup(self):
        """清理所有插件"""
        self.logger.info("开始清理所有插件...")
        
        # 复制插件ID列表，避免在迭代时修改
        plugin_ids = list(self.plugins.keys())
        
        for plugin_id in plugin_ids:
            try:
                await self.unload_plugin(plugin_id)
            except Exception as e:
                self.logger.error(f"清理插件失败 {plugin_id}: {e}")
        
        self.logger.info("所有插件清理完成")
    
    def get_manager_metrics(self) -> Dict[str, Any]:
        """获取管理器指标"""
        uptime = (datetime.now() - self.metrics["startup_time"]).total_seconds()
        
        return {
            "total_plugins": self.metrics["total_plugins"],
            "loaded_plugins": self.metrics["loaded_plugins"],
            "enabled_plugins": self.metrics["enabled_plugins"],
            "uptime_seconds": uptime,
            "config_path": self.config_path,
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return (f"PluginManager(loaded={self.metrics['loaded_plugins']}, "
                f"enabled={self.metrics['enabled_plugins']})")