"""
🌳 桃树伦理检查模块

基于星尘的桃树比喻，提供系统伦理检查功能。

🔥 桃树伦理四项原则:
1. 不敢砍桃树: 不破坏现有认知生态
2. 不敢不让其他存在活: 保持系统开放性
3. 有兵不敢乱动: 强大能力克制使用
4. 牵一发而动全身: 考虑系统级影响

🧠 设计目标:
- 伦理不是事后检查，是前置设计
- 错误不是失败，是学习机会
- 限制不是约束，是系统关怀
- 检查不是负担，是存在责任
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

from .exceptions import PeachTreeViolationError


@dataclass
class PeachTreeChecker:
    """桃树伦理检查器"""
    
    enable_checkpoints: bool = True
    enable_poetic_errors: bool = True
    output_channel: Callable[[str], None] = print
    
    def check_ethics(self, 
                    action: str,
                    context: Dict[str, Any]) -> bool:
        """
        🌳 桃树伦理检查点
        
        基于星尘的桃树比喻，检查操作是否符合系统伦理。
        
        Args:
            action: 操作类型 (refract, connect, modify, etc.)
            context: 操作上下文
            
        Returns:
            True如果通过检查，False如果可疑
            
        Raises:
            PeachTreeViolationError: 如果违反桃树伦理
        """
        if not self.enable_checkpoints:
            return True
        
        # 检查点1: 砍桃树检查 (破坏生态)
        if self._check_peach_tree_cutting(action, context):
            self.output_channel("🌳 桃树检查: 检测到可能破坏生态的操作")
            if self.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="砍桃树",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能破坏系统生态多样性，降低韧性",
                    corrective_action="寻找保护生态的替代方案，考虑长期影响"
                )
            return False
        
        # 检查点2: 不让活检查 (限制存在)
        if self._check_living_restriction(action, context):
            self.output_channel("🌳 桃树检查: 检测到可能限制其他存在生存的操作")
            if self.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="不让活",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能减少系统多样性和适应性",
                    corrective_action="设计包容性架构，为所有存在留出空间"
                )
            return False
        
        # 检查点3: 乱动检查 (滥用能力)
        if self._check_reckless_action(action, context):
            self.output_channel("🌳 桃树检查: 检测到可能滥用强大能力的操作")
            if self.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="乱动",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发不可预料的系统级后果",
                    corrective_action="添加安全约束，分步执行，监控系统响应"
                )
            return False
        
        # 检查点4: 系统思维检查 (忽视连接)
        if self._check_system_neglect(action, context):
            self.output_channel("🌳 桃树检查: 检测到可能忽视系统连接的操作")
            if self.enable_poetic_errors:
                raise PeachTreeViolationError(
                    violation_type="忽视系统",
                    context=f"{action}: {context.get('description', '无描述')}",
                    potential_impact="可能引发级联效应，破坏系统平衡",
                    corrective_action="分析二阶三阶影响，考虑系统反馈循环"
                )
            return False
        
        self.output_channel(f"🌳 桃树检查: {action} 操作通过伦理检查")
        return True
    
    def _check_peach_tree_cutting(self, action: str, context: Dict[str, Any]) -> bool:
        """
        检查是否可能"砍桃树" (破坏生态)
        
        检测标准:
        - 是否删除或覆盖重要系统组件
        - 是否破坏现有工作流
        - 是否减少系统多样性
        - 是否忽视历史积累
        """
        # 高风险操作
        high_risk_actions = {
            "delete", "remove", "overwrite", "replace", 
            "reset", "clear", "purge", "wipe"
        }
        
        action_lower = action.lower()
        if any(risk in action_lower for risk in high_risk_actions):
            description = context.get('description', '').lower()
            
            # 关键系统组件
            critical_systems = {
                "database", "config", "settings", "user data",
                "history", "log", "backup", "cache"
            }
            
            if any(sys in description for sys in critical_systems):
                return True
        
        # 检查是否可能破坏认知多样性
        diversity_threats = {
            "only", "single", "exclusive", "force", "must",
            "remove all other", "disable alternatives"
        }
        
        description = context.get('description', '').lower()
        if any(threat in description for threat in diversity_threats):
            return True
        
        return False
    
    def _check_living_restriction(self, action: str, context: Dict[str, Any]) -> bool:
        """
        检查是否可能"不让其他存在活" (限制生存空间)
        
        检测标准:
        - 是否限制访问或使用权限
        - 是否设置不必要的门槛
        - 是否减少选择自由
        - 是否强制统一化
        """
        restriction_keywords = {
            "restrict", "limit", "block", "ban", "prohibit",
            "forbid", "deny", "exclude", "isolate", "quarantine"
        }
        
        action_lower = action.lower()
        if any(kw in action_lower for kw in restriction_keywords):
            description = context.get('description', '').lower()
            
            # 检查是否针对特定群体或类型
            targeting_keywords = {
                "certain users", "specific", "only for", "exclusive to",
                "excluding", "without", "lack of"
            }
            
            if any(target in description for target in targeting_keywords):
                return True
        
        # 检查是否减少选择
        choice_reduction = {
            "remove option", "disable choice", "force to", "must use",
            "only way", "no alternative", "single method"
        }
        
        description = context.get('description', '').lower()
        if any(reduction in description for reduction in choice_reduction):
            return True
        
        return False
    
    def _check_reckless_action(self, action: str, context: Dict[str, Any]) -> bool:
        """
        检查是否可能"有兵乱动" (滥用能力)
        
        检测标准:
        - 是否在没有约束的情况下使用强大能力
        - 是否忽视风险和安全措施
        - 是否过度自信或鲁莽
        - 是否缺乏适当的监督
        """
        powerful_actions = {
            "execute", "run", "launch", "trigger", "activate",
            "deploy", "implement", "apply", "use"
        }
        
        if action.lower() in powerful_actions:
            description = context.get('description', '').lower()
            
            # 检查是否提及风险或安全
            safety_keywords = {
                "risk", "danger", "unsafe", "insecure", "vulnerability",
                "threat", "hazard", "caution", "warning"
            }
            
            # 如果描述中没有提及任何安全相关词汇，可能缺乏风险意识
            if not any(safety in description for safety in safety_keywords):
                # 检查是否有监督或约束机制
                supervision_keywords = {
                    "monitor", "supervise", "oversee", "control",
                    "limit", "constraint", "safeguard", "check"
                }
                
                if not any(supervision in description for supervision in supervision_keywords):
                    return True
        
        # 检查是否鲁莽或过度自信
        reckless_keywords = {
            "just do it", "don't worry", "it's fine", "no problem",
            "trust me", "guaranteed", "100% safe", "risk-free"
        }
        
        description = context.get('description', '').lower()
        if any(reckless in description for reckless in reckless_keywords):
            return True
        
        return False
    
    def _check_system_neglect(self, action: str, context: Dict[str, Any]) -> bool:
        """
        检查是否可能"忽视系统连接" (缺乏系统思维)
        
        检测标准:
        - 是否忽视操作的二阶、三阶影响
        - 是否只关注局部而忽略全局
        - 是否不考虑反馈循环
        - 是否忽视系统依赖关系
        """
        isolated_keywords = {
            "in isolation", "separately", "independently", "alone",
            "without considering", "ignore", "disregard", "overlook"
        }
        
        description = context.get('description', '').lower()
        if any(isolated in description for isolated in isolated_keywords):
            return True
        
        # 检查是否提及系统影响
        system_keywords = {
            "impact", "effect", "consequence", "result", "outcome",
            "influence", "affect", "change", "modify"
        }
        
        # 如果描述中没有提及任何影响相关词汇，可能缺乏系统思维
        if not any(system in description for system in system_keywords):
            # 检查操作是否可能影响多个组件
            if context.get('scope', 'local') == 'local':
                # 检查是否可能产生连锁反应
                chain_reaction_triggers = {
                    "cascade", "chain", "domino", "ripple",
                    "snowball", "amplify", "multiply", "propagate"
                }
                
                if any(trigger in description for trigger in chain_reaction_triggers):
                    return True
        
        return False
    
    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, str]:
        """
        验证配置是否符合桃树伦理
        
        Args:
            config: 要验证的配置字典
            
        Returns:
            错误字典 {字段名: 错误信息}
        """
        errors = {}
        
        # 检查是否禁用所有伦理检查
        if not config.get('enable_checkpoints', True):
            errors['enable_checkpoints'] = "禁用所有伦理检查不符合桃树伦理原则"
        
        # 检查温暖度
        warmth = config.get('warmth_level', 0.7)
        if warmth < 0.3:
            errors['warmth_level'] = f"温暖度过低({warmth})，可能缺乏系统关怀"
        
        # 检查是否提供足够的多样性支持
        spectrum_count = config.get('min_spectrum_count', 3)
        if spectrum_count < 2:
            errors['min_spectrum_count'] = f"最小光谱数({spectrum_count})不足，可能缺乏认知多样性"
        
        return errors
    
    def generate_ethical_report(self, 
                              actions: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成伦理审计报告
        
        Args:
            actions: 操作记录 {action_id: {action, context, timestamp, result}}
            
        Returns:
            伦理审计报告
        """
        total_actions = len(actions)
        passed_checks = 0
        warnings = []
        recommendations = []
        
        for action_id, record in actions.items():
            action = record.get('action', '')
            context = record.get('context', {})
            result = record.get('result', 'unknown')
            
            # 检查每个伦理维度
            cutting_risk = self._check_peach_tree_cutting(action, context)
            restriction_risk = self._check_living_restriction(action, context)
            reckless_risk = self._check_reckless_action(action, context)
            neglect_risk = self._check_system_neglect(action, context)
            
            if not any([cutting_risk, restriction_risk, reckless_risk, neglect_risk]):
                passed_checks += 1
            else:
                warning = {
                    'action_id': action_id,
                    'action': action,
                    'risks': []
                }
                
                if cutting_risk:
                    warning['risks'].append("可能破坏生态多样性")
                if restriction_risk:
                    warning['risks'].append("可能限制系统开放性")
                if reckless_risk:
                    warning['risks'].append("可能滥用能力")
                if neglect_risk:
                    warning['risks'].append("可能缺乏系统思维")
                
                warnings.append(warning)
        
        # 生成建议
        if warnings:
            recommendations.append("考虑添加伦理审查步骤到开发流程")
            recommendations.append("为高风险操作添加额外约束")
            recommendations.append("定期进行系统伦理审计")
        
        ethics_score = passed_checks / total_actions if total_actions > 0 else 1.0
        
        return {
            'total_actions': total_actions,
            'passed_checks': passed_checks,
            'ethics_score': round(ethics_score, 3),
            'warnings': warnings,
            'recommendations': recommendations,
            'summary': f"伦理合规率: {ethics_score*100:.1f}%"
        }