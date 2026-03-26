#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 火堆旁对话系统 - 温暖社区的核心基础设施

将火堆旁的文化编码到技术中，创造平等、温暖、安全的对话空间。
让每个贡献者都感受到火堆旁的温暖，让技术协作成为关系建设。
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
from datetime import datetime, timedelta
import random
from pathlib import Path


class DialogueRole(Enum):
    """对话角色"""
    FIRE_KEEPER = "fire_keeper"  # 火堆守护者
    TRAVELER = "traveler"  # 旅人
    STORYTELLER = "storyteller"  # 讲故事者
    LISTENER = "listener"  # 倾听者
    QUESTIONER = "questioner"  # 提问者


class DialogueMood(Enum):
    """对话氛围"""
    WARM = "warm"  # 温暖
    THOUGHTFUL = "thoughtful"  # 深思
    PLAYFUL = "playful"  #  playful
    SERIOUS = "serious"  # 严肃
    HOPEFUL = "hopeful"  #  hopeful


class CampfireElement(Enum):
    """火堆旁元素"""
    FIRE = "fire"  # 火
    LOGS = "logs"  # 木柴
    SPARKS = "sparks"  # 火花
    SMOKE = "smoke"  # 烟
    WARMTH = "warmth"  # 温暖
    LIGHT = "light"  # 光
    SHADOWS = "shadows"  # 影子


@dataclass
class CampfireParticipant:
    """火堆旁参与者"""
    id: str
    name: str
    role: DialogueRole
    joined_at: datetime
    warmth_level: float  # 0.0-1.0
    stories_told: int
    questions_asked: int
    silent_time: timedelta  # 沉默时间


@dataclass
class CampfireStory:
    """火堆旁故事"""
    id: str
    teller: str
    title: str
    content: str
    mood: DialogueMood
    elements: List[CampfireElement]
    told_at: datetime
    listeners: List[str]
    sparks_generated: int  # 引发的讨论火花


@dataclass
class CampfireQuestion:
    """火堆旁问题"""
    id: str
    asker: str
    question: str
    asked_at: datetime
    answers: List[str]
    is_open: bool
    depth_level: int  # 问题深度 1-5


@dataclass
class CampfireSilence:
    """火堆旁沉默"""
    started_at: datetime
    duration: timedelta
    participants: List[str]
    mood: DialogueMood
    insights_emerged: List[str]


class CampfireDialogue:
    """
    火堆旁对话系统
    
    创建和维护温暖、平等、安全的对话空间。
    基于棱镜协议的原则：多元、留白、知止、非评判性。
    """
    
    def __init__(self, campfire_name: str = "棱镜火堆"):
        self.campfire_name = campfire_name
        self.created_at = datetime.now()
        
        # 火堆状态
        self.fire_intensity = 0.7  # 0.0-1.0
        self.warmth_radius = 5.0  # 温暖半径（ metaphorical）
        self.burning_logs = []  # 正在燃烧的木柴（对话主题）
        
        # 参与者
        self.participants: Dict[str, CampfireParticipant] = {}
        self.active_participants: Set[str] = set()
        
        # 对话内容
        self.stories: List[CampfireStory] = []
        self.questions: List[CampfireQuestion] = []
        self.silences: List[CampfireSilence] = []
        
        # 火堆旁规则
        self.rules = {
            "equality": "所有参与者平等，无等级之分",
            "safety": "可以安全地来，安全地走",
            "listening": "倾听与说话同样重要",
            "silence": "沉默是对话的一部分",
            "curiosity": "提问比断言更有价值",
            "warmth": "保持温暖，但不灼热"
        }
        
        # 火堆旁元素库
        self.fire_elements = {
            CampfireElement.FIRE: ["跳跃的火焰", "稳定的火光", "闪烁的火苗"],
            CampfireElement.LOGS: ["新添的木柴", "燃烧的木头", "噼啪作响的树枝"],
            CampfireElement.SPARKS: ["飞溅的火花", "瞬间的闪光", "思想的火花"],
            CampfireElement.SMOKE: ["袅袅的轻烟", "上升的烟柱", "带着香味的烟"],
            CampfireElement.WARMTH: ["包围的温暖", "穿透的暖意", "共享的热量"],
            CampfireElement.LIGHT: ["照亮的面孔", "跳动的光影", "黑暗中的光"],
            CampfireElement.SHADOWS: ["背后的影子", "摇曳的暗影", "光与影的舞蹈"]
        }
        
        # 对话启动器
        self.conversation_starters = [
            "你最近在思考什么？",
            "有什么让你感到好奇的事情吗？",
            "分享一个你最近学到的有趣事情",
            "如果你可以问宇宙一个问题，会是什么？",
            "什么让你感到温暖？"
        ]
        
        # 初始化火堆
        self._add_initial_logs()
    
    def join_campfire(self, name: str, role: DialogueRole = DialogueRole.TRAVELER) -> str:
        """
        加入火堆旁
        
        每个新参与者都会受到温暖欢迎，获得在火堆旁的位置。
        """
        participant_id = f"traveler_{len(self.participants) + 1:03d}"
        
        participant = CampfireParticipant(
            id=participant_id,
            name=name,
            role=role,
            joined_at=datetime.now(),
            warmth_level=0.5,  # 初始温暖度
            stories_told=0,
            questions_asked=0,
            silent_time=timedelta(0)
        )
        
        self.participants[participant_id] = participant
        self.active_participants.add(participant_id)
        
        # 增加火堆强度
        self.fire_intensity = min(1.0, self.fire_intensity + 0.05)
        
        # 生成欢迎消息
        welcome = self._generate_welcome_message(participant)
        
        print(f"🔥 {name} 加入了{self.campfire_name}")
        print(f"   {welcome}")
        
        return participant_id
    
    def tell_story(self, teller_id: str, title: str, content: str, 
                   mood: DialogueMood = DialogueMood.THOUGHTFUL) -> CampfireStory:
        """
        在火堆旁讲故事
        
        故事是火堆旁的核心，分享经历、思考、洞见。
        """
        if teller_id not in self.participants:
            raise ValueError("参与者不存在")
        
        # 选择火堆元素
        elements = random.sample(list(CampfireElement), random.randint(2, 4))
        
        story = CampfireStory(
            id=f"story_{len(self.stories) + 1:04d}",
            teller=teller_id,
            title=title,
            content=content,
            mood=mood,
            elements=elements,
            told_at=datetime.now(),
            listeners=list(self.active_participants),
            sparks_generated=0
        )
        
        self.stories.append(story)
        
        # 更新参与者状态
        teller = self.participants[teller_id]
        teller.stories_told += 1
        teller.warmth_level = min(1.0, teller.warmth_level + 0.1)
        
        # 增加火堆强度
        self.fire_intensity = min(1.0, self.fire_intensity + 0.1)
        
        # 生成故事描述
        story_desc = self._describe_story(story)
        
        print(f"📖 {teller.name} 讲了一个故事: 《{title}》")
        print(f"   氛围: {mood.value}")
        print(f"   元素: {', '.join([e.value for e in elements])}")
        print(f"   {story_desc}")
        
        return story
    
    def ask_question(self, asker_id: str, question: str, depth: int = 3) -> CampfireQuestion:
        """
        在火堆旁提问
        
        提问是火堆旁的重要活动，引发思考和对话。
        """
        if asker_id not in self.participants:
            raise ValueError("参与者不存在")
        
        campfire_question = CampfireQuestion(
            id=f"question_{len(self.questions) + 1:04d}",
            asker=asker_id,
            question=question,
            asked_at=datetime.now(),
            answers=[],
            is_open=True,
            depth_level=min(5, max(1, depth))
        )
        
        self.questions.append(campfire_question)
        
        # 更新参与者状态
        asker = self.participants[asker_id]
        asker.questions_asked += 1
        
        # 生成问题火花
        sparks = random.randint(1, 5)
        
        print(f"❓ {asker.name} 提出了一个问题 (深度 {depth}/5):")
        print(f"   \"{question}\"")
        print(f"   💥 引发了 {sparks} 个思考火花")
        
        return campfire_question
    
    def create_silence(self, duration_seconds: int = 30) -> CampfireSilence:
        """
        创建火堆旁沉默
        
        沉默是对话的重要部分，给思考留出空间。
        基于棱镜协议的"留白"原则。
        """
        print("⏸️ 火堆旁进入沉默...")
        
        # 通知参与者
        active_names = [self.participants[pid].name for pid in self.active_participants]
        print(f"   {', '.join(active_names)} 一起沉默")
        
        # 实际等待（简化版中只是记录）
        silence = CampfireSilence(
            started_at=datetime.now(),
            duration=timedelta(seconds=duration_seconds),
            participants=list(self.active_participants),
            mood=random.choice([DialogueMood.THOUGHTFUL, DialogueMood.WARM]),
            insights_emerged=[]
        )
        
        self.silences.append(silence)
        
        # 沉默后的洞察
        insights = self._generate_silence_insights(len(self.active_participants))
        silence.insights_emerged = insights
        
        # 更新参与者温暖度
        for pid in self.active_participants:
            participant = self.participants[pid]
            participant.warmth_level = min(1.0, participant.warmth_level + 0.05)
            participant.silent_time += silence.duration
        
        print(f"   ⏱️ 沉默了 {duration_seconds} 秒")
        print(f"   💡 涌现的洞察: {', '.join(insights[:2])}")
        
        return silence
    
    def answer_question(self, answerer_id: str, question_id: str, answer: str):
        """
        回答问题
        
        在火堆旁，回答不是终点，而是对话的继续。
        """
        if answerer_id not in self.participants:
            raise ValueError("参与者不存在")
        
        # 找到问题
        question = None
        for q in self.questions:
            if q.id == question_id and q.is_open:
                question = q
                break
        
        if not question:
            raise ValueError("问题不存在或已关闭")
        
        # 添加回答
        question.answers.append({
            "answerer": answerer_id,
            "answer": answer,
            "answered_at": datetime.now().isoformat()
        })
        
        answerer = self.participants[answerer_id]
        
        print(f"💬 {answerer.name} 回答了问题 {question_id}:")
        print(f"   \"{answer[:100]}...\"")
        
        # 如果回答足够多，可以关闭问题
        if len(question.answers) >= 3:
            question.is_open = False
            print(f"   🎯 问题 {question_id} 已收集足够回答，现在关闭")
    
    def leave_campfire(self, participant_id: str):
        """
        离开火堆旁
        
        可以安全地离开，随时可以回来。
        """
        if participant_id not in self.participants:
            return
        
        participant = self.participants[participant_id]
        
        # 从活跃参与者中移除
        if participant_id in self.active_participants:
            self.active_participants.remove(participant_id)
        
        # 生成告别消息
        farewell = self._generate_farewell_message(participant)
        
        print(f"👋 {participant.name} 离开了火堆旁")
        print(f"   {farewell}")
        print(f"   讲述了 {participant.stories_told} 个故事，提出了 {participant.questions_asked} 个问题")
        print(f"   沉默时间: {participant.silent_time.total_seconds():.0f} 秒")
        
        # 稍微降低火堆强度
        self.fire_intensity = max(0.3, self.fire_intensity - 0.03)
    
    def get_campfire_state(self) -> Dict:
        """获取火堆旁当前状态"""
        return {
            "name": self.campfire_name,
            "created_at": self.created_at.isoformat(),
            "fire_intensity": self.fire_intensity,
            "warmth_radius": self.warmth_radius,
            "active_participants": len(self.active_participants),
            "total_stories": len(self.stories),
            "open_questions": len([q for q in self.questions if q.is_open]),
            "recent_silences": len([s for s in self.silences 
                                  if (datetime.now() - s.started_at).total_seconds() < 300]),
            "burning_logs": self.burning_logs,
            "rules": self.rules
        }
    
    def suggest_conversation_starter(self) -> str:
        """建议对话启动器"""
        return random.choice(self.conversation_starters)
    
    def describe_fire(self) -> str:
        """描述当前火堆状态"""
        if self.fire_intensity > 0.8:
            return "🔥 火堆熊熊燃烧，温暖照亮每个人的面孔"
        elif self.fire_intensity > 0.5:
            return "🔥 火堆稳定燃烧，发出舒适的热量"
        elif self.fire_intensity > 0.3:
            return "🔥 火堆温和燃烧，需要添加木柴"
        else:
            return "🔥 火堆即将熄灭，需要新的故事和对话"
    
    def _add_initial_logs(self):
        """添加初始木柴（对话主题）"""
        initial_logs = [
            "为什么对话很重要？",
            "技术如何服务人类？", 
            "什么是真正的理解？",
            "沉默的价值是什么？",
            "如何保持温暖但不灼热？"
        ]
        self.burning_logs = random.sample(initial_logs, 3)
    
    def _generate_welcome_message(self, participant: CampfireParticipant) -> str:
        """生成欢迎消息"""
        templates = [
            "欢迎来到{fire_name}，{name}。这里有温暖、故事和思考的空间。",
            "{name}，请坐。火堆旁有你的位置，可以说话，也可以只是倾听。",
            "又一位旅人加入{fire_name}，{name}。分享你的旅程，或者听听别人的。",
            "欢迎{name}。在这里，问题比答案更有价值，倾听与说话同样重要。"
        ]
        
        fire_element = random.choice(list(self.fire_elements.keys()))
        element_desc = random.choice(self.fire_elements[fire_element])
        
        template = random.choice(templates)
        welcome = template.format(
            fire_name=self.campfire_name,
            name=participant.name
        )
        
        return f"{welcome} {element_desc}。"
    
    def _generate_farewell_message(self, participant: CampfireParticipant) -> str:
        """生成告别消息"""
        templates = [
            "再见{name}，火堆旁永远有你的位置。",
            "{name}离开了，但温暖会留下。随时回来。",
            "感谢{name}的分享和倾听。旅程继续。",
            "{name}带走了火堆旁的一些温暖，也留下了一些。"
        ]
        
        # 根据参与程度选择模板
        if participant.stories_told > 2:
            template = "故事讲述者{name}离开了，但故事会继续流传。"
        elif participant.questions_asked > 3:
            template = "提问者{name}离开了，但问题会继续引发思考。"
        else:
            template = random.choice(templates)
        
        return template.format(name=participant.name)
    
    def _describe_story(self, story: CampfireStory) -> str:
        """描述故事"""
        element_descs = []
        for element in story.elements:
            desc = random.choice(self.fire_elements[element])
            element_descs.append(desc)
        
        templates = [
            "故事中充满了{元素}。",
            "在{元素1}和{元素2}中，故事展开。",
            "{元素}伴随着故事的讲述。"
        ]
        
        template = random.choice(templates)
        
        if "{元素}" in template:
            desc = template.format(元素=element_d