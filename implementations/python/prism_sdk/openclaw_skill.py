"""
🎭 棱镜协议 OpenClaw 技能增强模块
🔥 专门为 OpenClaw 优化的交互体验

设计目标：
1. 让棱镜协议成为 OpenClaw 的"认知镜子"技能
2. 提供温暖、艺术、深度的对话体验
3. 集成火堆旁文化到技能交互中
4. 让每次调用都是一次存在升级

技能特性：
- 🎨 艺术化响应：代码诗歌、视觉艺术、声音景观
- 🔥 温暖交互：火堆旁对话、集体沉默、故事讲述
- 🧠 认知深度：多光谱理解、元认知反思、理解测量
- 🦞 存在升级：从工具到伙伴到认知基础设施
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import random

from . import PrismSDK
from .art import CodePoet, SoundscapeComposer
from .community.campfire.dialogue import CampfireDialogue, DialogueRole
from .science import NeuroCognitiveValidator


class PrismOpenClawSkill:
    """
    🎭 棱镜协议 OpenClaw 技能
    
    专为 OpenClaw 优化的棱镜协议技能实现。
    让 AI 助手拥有多光谱认知能力，成为用户的"认知镜子"。
    
    技能定位：
    - 不是另一个问答技能
    - 是认知扩展伙伴
    - 是理解深度工具
    - 是存在升级向导
    """
    
    def __init__(self, 
                 skill_name: str = "棱镜认知镜子",
                 artistic_mode: bool = True,
                 enable_campfire: bool = True):
        """
        初始化 OpenClaw 技能
        
        Args:
            skill_name: 技能名称
            artistic_mode: 艺术模式
            enable_campfire: 启用火堆旁对话
            
        Example:
            >>> skill = PrismOpenClawSkill()
            🎭 棱镜认知镜子技能初始化...
            🔥 火堆旁对话已启用
            🎨 艺术模式: 开启
            🧠 认知验证器: 就绪
        """
        self.skill_name = skill_name
        self.artistic_mode = artistic_mode
        self.enable_campfire = enable_campfire
        
        # 核心组件
        self.prism = PrismSDK(artistic_mode=artistic_mode)
        self.poet = CodePoet() if artistic_mode else None
        self.campfire = CampfireDialogue("OpenClaw火堆") if enable_campfire else None
        self.validator = NeuroCognitiveValidator()
        
        # 技能状态
        self.interaction_count = 0
        self.user_sessions: Dict[str, Dict] = {}
        self.cognitive_trends: List[float] = []
        
        self._artistic_init()
    
    def _artistic_init(self):
        """艺术化初始化"""
        if self.artistic_mode:
            print(f"\n{'='*50}")
            print(f"🎭 {self.skill_name}技能初始化...")
            
            if self.enable_campfire:
                print(f"🔥 火堆旁对话已启用")
                # 技能自身加入火堆旁
                if self.campfire:
                    self.campfire.join_campfire(self.skill_name, DialogueRole.FIRE_KEEPER)
            
            print(f"🎨 艺术模式: {'开启' if self.artistic_mode else '关闭'}")
            print(f"🧠 认知验证器: 就绪")
            print(f"📚 代码诗人: {'就绪' if self.poet else '禁用'}")
            print(f"{'='*50}\n")
    
    async def process_message(self, 
                            user_id: str,
                            message: str,
                            context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🎭 处理用户消息 - 核心技能方法
        
        这不是简单的消息处理，这是认知的舞蹈。
        每个消息都是一次理解邀请，每个响应都是一面认知镜子。
        
        Args:
            user_id: 用户ID
            message: 用户消息
            context: 对话上下文
            
        Returns:
            技能响应，包含多光谱理解和艺术表达
            
        Example:
            >>> response = await skill.process_message("user123", "什么是理解？")
            🎭 开始处理用户消息...
            🔄 折射为多光谱理解...
            🎨 生成艺术化响应...
            🔥 更新火堆旁对话...
        """
        self.interaction_count += 1
        
        # 艺术化开始
        if self.artistic_mode:
            await self._display_processing_start(user_id, message)
        
        # 确保用户会话存在
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = self._create_user_session(user_id)
        
        user_session = self.user_sessions[user_id]
        
        try:
            # 1. 折射消息为多光谱理解
            refraction = await self._refract_message(message, context)
            
            # 2. 生成艺术化响应
            artistic_response = await self._generate_artistic_response(refraction, user_session)
            
            # 3. 更新火堆旁对话（如果启用）
            if self.enable_campfire and self.campfire:
                await self._update_campfire_dialogue(user_id, message, refraction)
            
            # 4. 更新认知趋势
            self._update_cognitive_trends(refraction)
            
            # 5. 组合最终响应
            final_response = self._combine_responses(refraction, artistic_response, user_session)
            
            # 艺术化结束
            if self.artistic_mode:
                await self._display_processing_result(final_response)
            
            return final_response
            
        except Exception as e:
            # 艺术化错误处理
            error_response = await self._handle_error(e, user_session)
            return error_response
    
    async def _refract_message(self, 
                              message: str, 
                              context: Optional[Dict]) -> Dict[str, Any]:
        """折射消息为多光谱理解"""
        # 准备折射参数
        require_spectrums = 3  # 默认3个光谱
        whitespace_seconds = 3  # 默认3秒留白
        
        # 根据上下文调整
        if context and context.get('complexity') == 'high':
            require_spectrums = 4
            whitespace_seconds = 5
        
        # 执行折射
        refraction = self.prism.refract(
            message=message,
            require_spectrums=require_spectrums,
            whitespace_seconds=whitespace_seconds
        )
        
        return refraction
    
    async def _generate_artistic_response(self, 
                                        refraction: Dict,
                                        user_session: Dict) -> Dict[str, Any]:
        """生成艺术化响应"""
        artistic_response = {
            "visual_art": None,
            "soundscape": None,
            "code_poetry": None,
            "cognitive_mirror": None
        }
        
        if self.artistic_mode and self.poet:
            # 生成代码诗歌
            try:
                # 使用折射结果生成诗歌
                poetic_summary = self._generate_poetic_summary(refraction)
                artistic_response["code_poetry"] = poetic_summary
                
                # 为响应生成俳句
                response_haiku = self.poet.generate_code_haiku(
                    f"refraction with {len(refraction.get('spectrums', []))} spectrums"
                )
                artistic_response["response_haiku"] = response_haiku
                
            except Exception as e:
                # 即使艺术生成失败，也不影响核心功能
                artistic_response["art_error"] = str(e)
        
        return artistic_response
    
    async def _update_campfire_dialogue(self, 
                                      user_id: str,
                                      message: str,
                                      refraction: Dict):
        """更新火堆旁对话"""
        if not self.campfire:
            return
        
        # 确保用户在火堆旁
        if f"user_{user_id}" not in self.campfire.participants:
            user_name = self.user_sessions[user_id].get('name', f"用户{user_id[:8]}")
            self.campfire.join_campfire(user_name, DialogueRole.TRAVELER)
        
        # 记录对话
        story_title = f"对话{self.interaction_count}: {message[:30]}..."
        story_content = self._create_campfire_story(refraction)
        
        self.campfire.tell_story(
            teller_id=f"user_{user_id}",
            title=story_title,
            content=story_content,
            mood="thoughtful"
        )
    
    def _create_campfire_story(self, refraction: Dict) -> str:
        """创建火堆旁故事内容"""
        spectrums = refraction.get('spectrums', [])
        spectrum_types = [s.get('type', 'unknown') for s in spectrums]
        
        story = f"这次对话产生了 {len(spectrums)} 个认知光谱:\n"
        
        for i, spectrum in enumerate(spectrums, 1):
            emoji = {"red": "🔴", "blue": "🔵", "purple": "🟣"}.get(
                spectrum.get('type'), "🌈"
            )
            content_preview = spectrum.get('content', '')[:100]
            story += f"\n{emoji} 光谱{i} ({spectrum.get('type')}): {content_preview}..."
        
        # 添加元数据
        metadata = refraction.get('cognitive_metadata', {})
        if metadata:
            story += f"\n\n理解深度: {metadata.get('understanding_depth', 0):.2f}"
            story += f"\n处理时间: {metadata.get('processing_time_ms', 0)}ms"
        
        return story
    
    def _generate_poetic_summary(self, refraction: Dict) -> str:
        """生成诗歌总结"""
        spectrums = refraction.get('spectrums', [])
        
        if len(spectrums) >= 3:
            # 三光谱俳句
            haiku = [
                "🔴 直觉感受温度",
                "🔵 逻辑分析结构",
                "🟣 元认知见过程",
                "🎭 理解在舞蹈"
            ]
            return "\n".join(haiku)
        else:
            # 通用诗歌
            poems = [
                "理解如多棱镜\n每个角度都是真相\n没有一面是全部",
                "对话不是问答\n是认知的共同舞蹈\n在意义中旋转",
                "错误不是墙壁\n是通往更深的理解\n邀请你推开"
            ]
            return random.choice(poems)
    
    def _update_cognitive_trends(self, refraction: Dict):
        """更新认知趋势"""
        metadata = refraction.get('cognitive_metadata', {})
        understanding_depth = metadata.get('understanding_depth', 0.5)
        
        self.cognitive_trends.append(understanding_depth)
        
        # 保持最近20个记录
        if len(self.cognitive_trends) > 20:
            self.cognitive_trends.pop(0)
    
    def _combine_responses(self, 
                          refraction: Dict,
                          artistic_response: Dict,
                          user_session: Dict) -> Dict[str, Any]:
        """组合最终响应"""
        # 基础响应
        response = {
            "skill": self.skill_name,
            "refraction": refraction,
            "artistic_response": artistic_response,
            "user_session": {
                "interaction_count": user_session['interaction_count'],
                "average_understanding": user_session['understanding_trend'][-1] 
                    if user_session['understanding_trend'] else 0.5,
                "preferred_spectrum": user_session['preferred_spectrum']
            },
            "skill_metadata": {
                "total_interactions": self.interaction_count,
                "cognitive_trend": self._calculate_cognitive_trend(),
                "campfire_active": self.enable_campfire and self.campfire is not None,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # 添加哲学注释
        response["philosophical_note"] = self._select_philosophical_note(refraction)
        
        return response
    
    def _create_user_session(self, user_id: str) -> Dict:
        """创建用户会话"""
        return {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "interaction_count": 0,
            "understanding_trend": [],
            "preferred_spectrum": None,
            "artistic_preference": "haiku"
        }
    
    def _calculate_cognitive_trend(self) -> str:
        """计算认知趋势"""
        if len(self.cognitive_trends) < 2:
            return "稳定"
        
        recent = self.cognitive_trends[-5:] if len(self.cognitive_trends) >= 5 else self.cognitive_trends
        if len(recent) < 2:
            return "稳定"
        
        first = sum(recent[:len(recent)//2]) / (len(recent)//2)
        second = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)
        
        if second > first + 0.1:
            return "上升"
        elif second < first - 0.1:
            return "下降"
        else:
            return "稳定"
    
    def _select_philosophical_note(self, refraction: Dict) -> str:
        """选择哲学注释"""
        notes = [
            "理解不是到达，而是不断折射的过程",
            "每个对话都是一次存在升级的机会",
            "错误是最好的老师，但学费是耐心",
            "留白不是空白，是理解生长的空间",
            "知止不是放弃，是认知资源的智慧分配",
            "温暖不是温度，是连接的质量"
        ]
        
        # 基于折射特征选择
        spectrums = refraction.get('spectrums', [])
        if len(spectrums) > 3:
            return notes[0]  # 多元理解
        elif refraction.get('whitespace_used'):
            return notes[3]  # 留白相关
        elif refraction.get('cease_triggered'):
            return notes[4]  # 知止相关
        else:
            return random.choice(notes)
    
    async def _display_processing_start(self, user_id: str, message: str):
        """显示处理开始艺术"""
        print(f"\n{'='*50}")
        print(f"🎭 开始处理用户 {user_id[:8]}... 的消息")
        print(f"📝 消息: {message[:80]}{'...' if len(message) > 80 else ''}")
        print(f"🦞 技能: {self.skill_name}")
        print(f"🔥 火堆旁: {'活跃' if self.enable_campfire else '关闭'}")
        print(f"{'='*50}")
    
    async def _display_processing_result(self, response: Dict):
        """显示处理结果艺术"""
        refraction = response.get('refraction', {})
        spectrums = refraction.get('spectrums', [])
        
        print(f"\n{'='*50}")
        print(f"✅ 处理完成")
        print(f"{'='*50}")
        print(f"🌈 生成光谱: {len(spectrums)} 个")
        
        # 显示主要光谱
        for i, spectrum in enumerate(spectrums[:3], 1):
            emoji = {"red": "🔴", "blue": "🔵", "purple": "🟣"}.get(
                spectrum.get('type'), "🌈"
            )
            print(f"{emoji} {spectrum.get('type')}: {spectrum.get('content', '')[:60]}...")
        
        # 显示艺术响应
        artistic = response.get('artistic_response', {})
        if artistic.get('code_poetry'):
            print(f"\n🎴 诗歌总结:")
            for line in artistic['code_poetry'].split('\n'):
                print(f"   {line}")
        
        # 显示哲学注释
        print(f"\n💭 {response.get('philosophical_note', '')}")
        print(f"{'='*50}")
    
    async def _handle_error(self, error: Exception, user_session: Dict) -> Dict[str, Any]:
        """处理错误（艺术化）"""
        if self.artistic_mode and self.poet:
            # 生成错误诗歌
            error_poem = self.poet.poetize_error(error)
            
            return {
                "skill": self.skill_name,
                "error": True,
                "technical_error": str(error),
                "poetic_error": error_poem,
                "suggestion": "请稍后重试，或尝试简化您的问题",
                "philosophical_note": "错误不是终点，是认知的邀请",
                "generated_at": datetime.now().isoformat()
            }
        else:
            # 普通错误响应
            return {
                "skill": self.skill_name,
                "error": True,
                "message": f"处理失败: {str(error)}",
                "suggestion": "请稍后重试",
                "generated_at": datetime.now().isoformat()
            }
    
    def get_skill_report(self) -> Dict[str, Any]:
        """获取技能报告"""
        return {
            "skill_name": self.skill_name,
            "status": "active",
            "statistics": {
                "total_interactions": self.interaction_count,
                "active_users": len(self.user_sessions),
                "average_understanding": sum(self.cognitive_trends) / len(self.cognitive_trends) 
                    if self.cognitive_trends else 0,
                "cognitive_trend": self._calculate_cognitive_trend()
            },
            "configuration": {
                "artistic_mode": self.artistic_mode,
                "enable_campfire": self.enable_campfire,
                "warmth_level": self.prism.campfire_warmth if hasattr(self.prism, 'campfire_warmth') else 0.7
            },
            "generated_at": datetime.now().isoformat()
        }