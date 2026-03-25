#!/usr/bin/env python3
"""
棱镜互联协议 - Python参考实现
Prism Interconnect Protocol - Python Reference Implementation

一个完整、生产就绪的棱镜协议实现，支持：
- 完整的协议规范实现
- 多光谱类型生成
- 递归对话管理
- 协议验证和错误处理
- 性能优化和缓存
- 可扩展的架构设计
"""

import asyncio
import json
import uuid
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import hashlib
from functools import lru_cache

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# 数据类型定义
# ============================================================================

class SpectrumType(Enum):
    """光谱类型枚举"""
    RED = "red"       # 快速直觉
    BLUE = "blue"     # 慢速分析
    PURPLE = "purple" # 元认知审视
    GREEN = "green"   # 生态视角（自定义示例）
    ORANGE = "orange" # 历史经验（自定义示例）

class MessageType(Enum):
    """消息类型枚举"""
    PRISM_MESSAGE = "prism_message"
    CEASE_SIGNAL = "cease_signal"

class CeaseType(Enum):
    """知止类型枚举"""
    TEMPORARY = "temporary"  # 临时暂停
    PERMANENT = "permanent"  # 永久终止
    SAFETY = "safety"        # 安全原因

@dataclass
class Puzzle:
    """困惑定义"""
    text: str
    context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """验证困惑有效性"""
        if not self.text or not self.text.strip():
            raise ValueError("困惑文本不能为空")
    
    @property
    def hash(self) -> str:
        """生成困惑哈希，用于缓存"""
        content = f"{self.text}:{self.context or ''}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"text": self.text}
        if self.context:
            result["context"] = self.context
        if self.metadata:
            result["metadata"] = self.metadata
        return result

@dataclass
class Spectrum:
    """光谱定义"""
    type: SpectrumType
    name: str
    content: str
    confidence: float = 1.0  # 置信度分数
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """验证光谱有效性"""
        if not self.content or not self.content.strip():
            raise ValueError("光谱内容不能为空")
        if not 0 <= self.confidence <= 1:
            raise ValueError("置信度必须在0-1之间")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "type": self.type.value,
            "name": self.name,
            "content": self.content
        }
        if self.confidence < 1.0:
            result["confidence"] = round(self.confidence, 2)
        if self.metadata:
            result["metadata"] = self.metadata
        return result
    
    @property
    def cognitive_style(self) -> str:
        """返回认知风格描述"""
        styles = {
            SpectrumType.RED: "直觉性、故事性、身体感知",
            SpectrumType.BLUE: "分析性、结构性、逻辑推理", 
            SpectrumType.PURPLE: "元认知性、反思性、开放性",
            SpectrumType.GREEN: "系统性、生态性、关系思维",
            SpectrumType.ORANGE: "历史性、经验性、模式识别"
        }
        return styles.get(self.type, "未知风格")

@dataclass
class Whitespace:
    """留白定义"""
    content: str
    prompt_type: str = "reflection"  # reflection, integration, pause
    duration_suggestion: Optional[int] = None  # 建议的留白时间（秒）
    
    def __post_init__(self):
        """验证留白有效性"""
        if not self.content or not self.content.strip():
            raise ValueError("留白内容不能为空")
        if len(self.content) > 200:  # 留白不宜过长
            logger.warning(f"留白内容较长（{len(self.content)}字符），建议精简")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"content": self.content}
        if self.prompt_type != "reflection":
            result["prompt_type"] = self.prompt_type
        if self.duration_suggestion:
            result["duration_suggestion"] = self.duration_suggestion
        return result

# ============================================================================
# 抽象接口定义
# ============================================================================

class SpectrumEngine(ABC):
    """光谱生成引擎抽象基类"""
    
    @abstractmethod
    async def generate(self, puzzle: Puzzle) -> Spectrum:
        """生成光谱"""
        pass
    
    @property
    @abstractmethod
    def spectrum_type(self) -> SpectrumType:
        """返回光谱类型"""
        pass
    
    @property
    @abstractmethod
    def engine_name(self) -> str:
        """返回引擎名称"""
        pass

class WhitespaceGenerator(ABC):
    """留白生成器抽象基类"""
    
    @abstractmethod
    async def generate(self, spectra: List[Spectrum], puzzle: Puzzle) -> Whitespace:
        """基于光谱和困惑生成留白"""
        pass

# ============================================================================
# 具体实现类
# ============================================================================

class IntuitionEngine(SpectrumEngine):
    """直觉光谱引擎"""
    
    def __init__(self, model_name: str = "intuition-v1"):
        self.model_name = model_name
        self.temperature = 0.8  # 较高的温度鼓励创造性
    
    @property
    def spectrum_type(self) -> SpectrumType:
        return SpectrumType.RED
    
    @property
    def engine_name(self) -> str:
        return f"IntuitionEngine-{self.model_name}"
    
    async def generate(self, puzzle: Puzzle) -> Spectrum:
        """生成直觉光谱"""
        # 这里应该集成实际的LLM或知识库
        # 示例实现：
        content = f"""直觉上，这个问题让我想到一个故事...

{puzzle.text} 让我联想到一种身体感受：像是站在岔路口，既想向前又怕选错。
这可能是因为我们内心住着一位古老的"部落守卫者"，它的工作就是保护我们免受伤害。
当面对不确定时，它会拉响警报："危险！上次这样很痛！"

这种直觉警报不是弱点，而是演化给我们的保护机制。
它想说的是："请慢一点，看清楚再走。"而不是"不要走"。

你的身体在说什么？那个胃部发紧或心跳加速的感觉，
如果它会说话，它会告诉你什么？"""
        
        return Spectrum(
            type=self.spectrum_type,
            name="快速直觉",
            content=content,
            confidence=0.85,
            metadata={
                "engine": self.engine_name,
                "temperature": self.temperature,
                "generation_time": datetime.now().isoformat()
            }
        )

class AnalysisEngine(SpectrumEngine):
    """分析光谱引擎"""
    
    def __init__(self, model_name: str = "analysis-v1"):
        self.model_name = model_name
        self.temperature = 0.3  # 较低的温度鼓励准确性
    
    @property
    def spectrum_type(self) -> SpectrumType:
        return SpectrumType.BLUE
    
    @property
    def engine_name(self) -> str:
        return f"AnalysisEngine-{self.model_name}"
    
    async def generate(self, puzzle: Puzzle) -> Spectrum:
        """生成分析光谱"""
        # 这里应该集成实际的LLM或知识库
        # 示例实现：
        content = f"""从分析角度看，{puzzle.text} 可能涉及以下几个层面：

1. **认知层面**
   - 目标清晰度：目标是否具体、可衡量？
   - 任务分解：大任务是否分解为可执行的小步骤？
   - 反馈机制：是否有及时的进展反馈？

2. **情绪层面**
   - 预期情绪：对结果的预期情绪是什么？
   - 过程情绪：执行过程中的情绪体验如何？
   - 调节策略：现有的情绪调节策略是否有效？

3. **环境层面**
   - 干扰因素：环境中存在哪些干扰因素？
   - 支持资源：可用的支持资源有哪些？
   - 时间结构：时间安排是否合理？

4. **动机层面**
   - 内在动机：任务与个人价值观的关联度？
   - 外在激励：外部奖励或惩罚的影响？
   - 自我效能：对自身能力的信心程度？

建议的解决路径：
1. 将模糊目标转化为具体、可测量的指标
2. 建立"启动仪式"降低开始的心理成本
3. 设置微小胜利点，提供即时反馈
4. 调整环境减少干扰，增加提示线索"""
        
        return Spectrum(
            type=self.spectrum_type,
            name="慢速分析",
            content=content,
            confidence=0.9,
            metadata={
                "engine": self.engine_name,
                "temperature": self.temperature,
                "generation_time": datetime.now().isoformat(),
                "analysis_framework": "认知-情绪-环境-动机四维模型"
            }
        )

class MetacognitionEngine(SpectrumEngine):
    """元认知光谱引擎"""
    
    def __init__(self, model_name: str = "metacognition-v1"):
        self.model_name = model_name
        self.temperature = 0.5  # 中等温度鼓励深度思考
    
    @property
    def spectrum_type(self) -> SpectrumType:
        return SpectrumType.PURPLE
    
    @property
    def engine_name(self) -> str:
        return f"MetacognitionEngine-{self.model_name}"
    
    async def generate(self, puzzle: Puzzle) -> Spectrum:
        """生成元认知光谱"""
        # 这里应该集成实际的LLM或知识库
        # 示例实现：
        content = f"""让我们先暂停问"如何解决"，而是问"我们如何思考这个问题"：

**第一层：问题定义**
- 当我们说"{puzzle.text}"时，我们真正在问什么？
- 这个问题背后有哪些未言明的假设？
- "解决"对这个问题的具体含义是什么？

**第二层：思考过程观察**
- 在思考这个问题时，你的注意力流向哪里？
- 哪些部分让你感到清晰，哪些部分让你困惑？
- 你注意到自己有哪些自动化的思维模式？

**第三层：认知立场反思**
- 你从什么位置观察这个问题？（内部参与者/外部观察者）
- 你的思考受到哪些认知偏差的影响？（确认偏误、可得性启发等）
- 如果换一个完全不同的视角，这个问题会变成什么？

**第四层：元认知调节**
- 当前的思考策略是否有效？
- 是否需要切换到不同的认知模式？
- 如何创造思考的"留白空间"让新见解浮现？

关键问题：不是"答案是什么"，而是"好问题是什么"？"""
        
        return Spectrum(
            type=self.spectrum_type,
            name="元认知审视",
            content=content,
            confidence=0.8,
            metadata={
                "engine": self.engine_name,
                "temperature": self.temperature,
                "generation_time": datetime.now().isoformat(),
                "metacognition_levels": 4
            }
        )

class EcologyEngine(SpectrumEngine):
    """生态视角引擎（自定义光谱示例）"""
    
    def __init__(self, model_name: str = "ecology-v1"):
        self.model_name = model_name
    
    @property
    def spectrum_type(self) -> SpectrumType:
        return SpectrumType.GREEN
    
    @property
    def engine_name(self) -> str:
        return f"EcologyEngine-{self.model_name}"
    
    async def generate(self, puzzle: Puzzle) -> Spectrum:
        """生成生态视角光谱"""
        content = f"""从生态系统视角看{puzzle.text}：

**系统关系**
- 这个问题涉及哪些相互关联的部分？
- 这些部分如何形成反馈循环？
- 改变一个部分会如何影响整体？

**时间尺度**
- 短期行动可能带来哪些长期影响？
- 历史模式对当前情况有什么启示？
- 未来可能涌现哪些新特性？

**平衡与韧性**
- 系统当前的平衡点在哪里？
- 系统的韧性（承受扰动的能力）如何？
- 如何增强系统的适应性和学习能力？

**能量与资源流动**
- 注意力、时间、情感等"认知资源"如何流动？
- 是否存在资源"淤塞"或"泄漏"？
- 如何优化资源的分配和循环？

生态智慧：不是控制，而是共舞；不是解决，而是适应。"""
        
        return Spectrum(
            type=self.spectrum_type,
            name="生态视角",
            content=content,
            confidence=0.75,
            metadata={
                "engine": self.engine_name,
                "generation_time": datetime.now().isoformat(),
                "perspective": "systems_thinking"
            }
        )

class ReflectiveWhitespaceGenerator(WhitespaceGenerator):
    """反思型留白生成器"""
    
    async def generate(self, spectra: List[Spectrum], puzzle: Puzzle) -> Whitespace:
        """基于光谱生成留白"""
        
        # 分析光谱特点
        spectrum_types = [s.type.value for s in spectra]
        confidence_scores = [s.confidence for s in spectra]
        
        # 根据光谱内容生成个性化的留白
        if SpectrumType.PURPLE in [s.type for s in spectra]:
            # 如果有元认知光谱，引导深度反思
            content = """在这些视角中，哪一个问题让你最想深入思考？
            
暂停一下，感受你的身体反应：
- 哪个观点让你点头认同？
- 哪个观点让你想反驳？
- 哪个观点让你感到好奇？

这种反应本身，就是你需要倾听的内心声音。
给自己一分钟的沉默，只是感受，不急于回答。"""
            prompt_type = "deep_reflection"
            duration = 60
            
        elif any(c < 0.7 for c in confidence_scores):
            # 如果有低置信度光谱，引导谨慎思考
            content = """有些视角的确定性较低，这本身是重要的信息。

不确定性不是缺陷，而是探索的邀请。
在这些不够确定的观点中，你看到了什么可能性？
如果这些观点只是部分正确，完整的图景可能是什么？

让问题保持开放，比急于关闭更有价值。"""
            prompt_type = "uncertainty_embrace"
            duration = 45
            
        else:
            # 默认留白
            content = f"""在{len(spectra)}种视角中（{', '.join(spectrum_types)}）：

哪一种最先触动你？为什么？
哪一种让你想追问更多？追问什么？
哪一种与你原有的理解不同？这种不同意味着什么？

给自己一点时间，让这些视角在你内心沉淀。
不急于整合，先让它们各自发声。"""
            prompt_type = "reflection"
            duration = 30
        
        return Whitespace(
            content=content,
            prompt_type=prompt_type,
            duration_suggestion=duration
        )

# ============================================================================
# 会话管理
# ============================================================================

class PrismSession:
    """棱镜会话管理器"""
    
    def __init__(self, session_id: Optional[str] = None, max_depth: int = 3):
        self.session_id = session_id or str(uuid.uuid4())
        self.max_depth = max_depth
        self.current_depth = 0
        self.message_history: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        self.cease_signals: List[Dict[str, Any]] = []
        
    def can_recurs(self, depth: int) -> bool:
        """检查是否可以继续递归"""
        return depth < self.max_depth
    
    def add_message(self, message: Dict[str, Any]):
        """添加消息到历史"""
        self.message_history.append({
            "timestamp": datetime.now().isoformat(),
            "depth": message.get("metadata", {}).get("recursion_depth", 0),
            "message_id": message.get("id"),
            "type": message.get("type")
        })
    
    def add_cease_signal(self, signal: Dict[str, Any]):
        """添加知止信号"""
        self.cease_signals.append({
            "timestamp": datetime.now().isoformat(),
            "reason": signal.get("metadata", {}).get("reason", "unknown"),
            "signal": signal
        })
    
    def get_session_summary(self) -> Dict[str, Any]:
        """获取会话摘要"""
        return {
            "session_id": self.session_id,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "total_messages": len(self.message_history),
            "max_depth_reached": max([m["depth"] for m in self.message_history], default=0),
            "cease_signals": len(self.cease_signals),
            "start_time": self.start_time.isoformat(),
            "current_depth": self.current_depth
        }

# ============================================================================
# 主代理类
# ============================================================================

class PrismAgent:
    """
    棱镜代理 - 核心实现类
    
    功能：
    - 完整的协议实现
    - 多引擎光谱生成
    - 会话管理
    - 性能优化
    - 错误处理
    """
    
    def __init__(
        self,
        agent_id: str,
        capabilities: Optional[List[SpectrumType]] = None,
        max_depth: int = 3,
        enable_caching: bool = True,
        session_manager: Optional[PrismSession] = None
    ):
        """
        初始化棱镜代理
        
        Args:
            agent_id: 代理标识符
            capabilities: 支持的光谱类型
            max_depth: 最大递归深度
            enable_caching: 是否启用缓存
            session_manager: 可选的会话管理器
        """
        self.agent_id = agent_id
        self.capabilities = capabilities or [
            SpectrumType.RED,
            SpectrumType.BLUE, 
            SpectrumType.PURPLE
        ]
        self.max_depth = max_depth
        self.enable_caching = enable_caching
        
        # 初始化引擎
        self.engines: Dict[SpectrumType, SpectrumEngine] = {}
        self._init_engines()
        
        # 初始化留白生成器
        self.whitespace_generator = ReflectiveWhitespaceGenerator()
        
        # 会话管理
        self.session_manager = session_manager or PrismSession(
            session_id=f"session-{agent_id}-{uuid.uuid4().hex[:8]}",
            max_depth=max_depth
        )
        
        # 缓存
        self.spectrum_cache: Dict[str, List[Spectrum]] = {}
        self.puzzle_cache: Dict[str, Puzzle] = {}
        
        logger.info(f"棱镜代理初始化完成: {agent_id}, 能力: {[c.value for c in self.capabilities]}")
    
    def _init_engines(self):
        """初始化光谱引擎"""
        engine_map = {
            SpectrumType.RED: IntuitionEngine(),
            SpectrumType.BLUE: AnalysisEngine(),
            SpectrumType.PURPLE: MetacognitionEngine(),
            SpectrumType.GREEN: EcologyEngine(),
        }
        
        for capability in self.capabilities:
            if capability in engine_map:
                self.engines[capability] = engine_map[capability]
            else:
                logger.warning(f"未找到{capability.value}光谱的引擎实现")
    
    async def refract(
        self,
        puzzle_text: str,
        context: Optional[str] = None,
        depth: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        折射困惑，生成棱镜响应
        
        Args:
            puzzle_text: 困惑文本
            context: 上下文信息
            depth: 当前递归深度
            metadata: 附加元数据
            
        Returns:
            符合PIP规范的棱镜消息
            
        Raises:
            ValueError: 如果输入无效
            RuntimeError: 如果生成失败
        """
        try:
            # 1. 创建困惑对象
            puzzle = Puzzle(
                text=puzzle_text,
                context=context,
                metadata=metadata or {}
            )
            
            # 2. 检查递归深度
            if not self.session_manager.can_recurs(depth):
                logger.warning(f"达到最大递归深度 {depth}，发送知止信号")
                return await self.send_cease_signal(
                    reason="达到最大递归深度",
                    cease_type=CeaseType.SAFETY
                )
            
            # 3. 生成光谱
            spectra = await self._generate_spectra(puzzle, depth)
            
            # 4. 生成留白
            whitespace = await self.whitespace_generator.generate(spectra, puzzle)
            
            # 5. 组装消息
            message = self._assemble_message(puzzle, spectra, whitespace, depth)
            
            # 6. 记录会话
            self.session_manager.add_message(message)
            self.session_manager.current_depth = depth
            
            logger.info(f"成功生成棱镜消息，深度: {depth}, 光谱数: {len(spectra)}")
            
            return message
            
        except Exception as e:
            logger.error(f"折射失败: {str(e)}", exc_info=True)
            # 优雅降级：返回错误信息作为知止信号
            return await self.send_cease_signal(
                reason=f"处理失败: {str(e)}",
                cease_type=CeaseType.SAFETY
            )
    
    async def _generate_spectra(self, puzzle: Puzzle, depth: int) -> List[Spectrum]:
        """生成光谱数组"""
        
        # 检查缓存
        if self.enable_caching:
            cache_key = f"{puzzle.hash}:{depth}"
            if cache_key in self.spectrum_cache:
                logger.debug(f"使用缓存光谱: {cache_key}")
                return self.spectrum_cache[cache_key]
        
        # 确定要生成的光谱类型（至少三种）
        target_types = self.capabilities[:3]  # 至少取前三种
        if len(target_types) < 3:
            # 如果能力不足，重复使用已有的
            while len(target_types) < 3:
                target_types.append(target_types[-1] if target_types else SpectrumType.RED)
            logger.warning(f"能力不足，使用重复类型生成三种光谱")
        
        # 并行生成光谱
        tasks = []
        for spec_type in target_types:
            if spec_type in self.engines:
                tasks.append(self.engines[spec_type].generate(puzzle))
            else:
                # 如果引擎不存在，使用默认引擎
                logger.warning(f"引擎{spec_type.value}不存在，使用直觉引擎替代")
                tasks.append(self.engines[SpectrumType.RED].generate(puzzle))
        
        # 等待所有任务完成
        spectra = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常
        valid_spectra = []
        for i, result in enumerate(spectra):
            if isinstance(result, Exception):
                logger.error(f"光谱生成失败 ({target_types[i].value}): {str(result)}")
                # 创建降级光谱
                fallback = Spectrum(
                    type=target_types[i],
                    name=f"{target_types[i].value}（生成失败）",
                    content=f"暂时无法生成{target_types[i].value}视角，请稍后重试或尝试其他视角。",
                    confidence=0.1
                )
                valid_spectra.append(fallback)
            else:
                valid_spectra.append(result)
        
        # 确保至少有三个光谱
        if len(valid_spectra) < 3:
            logger.error(f"有效光谱数量不足: {len(valid_spectra)}")
            raise RuntimeError(f"无法生成足够的光谱，只有{len(valid_spectra)}个有效")
        
        # 缓存结果
        if self.enable_caching:
            cache_key = f"{puzzle.hash}:{depth}"
            self.spectrum_cache[cache_key] = valid_spectra
            self.puzzle_cache[cache_key] = puzzle
        
        return valid_spectra
    
    def _assemble_message(
        self,
        puzzle: Puzzle,
        spectra: List[Spectrum],
        whitespace: Whitespace,
        depth: int
    ) -> Dict[str, Any]:
        """组装棱镜消息"""
        
        # 转换光谱为字典
        spectrum_dicts = [s.to_dict() for s in spectra]
        
        # 计算平均置信度
        avg_confidence = sum(s.confidence for s in spectra) / len(spectra)
        
        message = {
            "protocol": "PIP",
            "version": "0.1",
            "type": MessageType.PRISM_MESSAGE.value,
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sender": {
                "id": self.agent_id,
                "capabilities": [c.value for c in self.capabilities],
                "metadata": {
                    "max_depth": self.max_depth,
                    "caching_enabled": self.enable_caching
                }
            },
            "puzzle": puzzle.to_dict(),
            "spectrums": spectrum_dicts,
            "whitespace": whitespace.to_dict(),
            "metadata": {
                "recursion_depth": depth,
                "allow_recursion": depth < self.max_depth - 1,
                "cease_signal": False,
                "generation_quality": {
                    "avg_confidence": round(avg_confidence, 2),
                    "spectrum_count": len(spectra),
                    "unique_types": len({s.type for s in spectra})
                },
                "session_id": self.session_manager.session_id
            }
        }
        
        return message
    
    async def send_cease_signal(
        self,
        reason: str,
        cease_type: CeaseType = CeaseType.TEMPORARY,
        resumable: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        发送知止信号
        
        Args:
            reason: 知止原因
            cease_type: 知止类型
            resumable: 是否可恢复（如果为None，根据类型自动决定）
            
        Returns:
            知止信号消息
        """
        if resumable is None:
            resumable = cease_type == CeaseType.TEMPORARY
        
        message = {
            "protocol": "PIP",
            "version": "0.1",
            "type": MessageType.CEASE_SIGNAL.value,
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sender": {"id": self.agent_id},
            "metadata": {
                "reason": reason,
                "cease_type": cease_type.value,
                "resumable": resumable,
                "session_id": self.session_manager.session_id,
                "session_summary": self.session_manager.get_session_summary()
            }
        }
        
        # 记录知止信号
        self.session_manager.add_cease_signal(message)
        
        logger.info(f"发送知止信号: {reason} ({cease_type.value})")
        
        return message
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理接收到的棱镜消息
        
        Args:
            message: 接收到的消息
            
        Returns:
            响应消息
        """
        try:
            # 1. 验证消息类型
            msg_type = message.get("type")
            
            if msg_type == MessageType.CEASE_SIGNAL.value:
                # 处理知止信号
                logger.info("收到知止信号，结束会话")
                self.session_manager.add_cease_signal(message)
                return await self.send_cease_signal(
                    reason="确认收到知止信号",
                    cease_type=CeaseType.PERMANENT,
                    resumable=False
                )
            
            elif msg_type == MessageType.PRISM_MESSAGE.value:
                # 处理棱镜消息
                puzzle_data = message.get("puzzle", {})
                metadata = message.get("metadata", {})
                
                # 提取递归深度
                depth = metadata.get("recursion_depth", 0) + 1
                
                # 生成响应
                return await self.refract(
                    puzzle_text=puzzle_data.get("text", ""),
                    context=puzzle_data.get("context"),
                    depth=depth,
                    metadata={
                        "parent_message_id": message.get("id"),
                        "responding_to": message.get("sender", {}).get("id")
                    }
                )
            
            else:
                # 未知消息类型
                logger.warning(f"未知消息类型: {msg_type}")
                return await self.send_cease_signal(
                    reason=f"不支持的消息类型: {msg_type}",
                    cease_type=CeaseType.SAFETY
                )
                
        except Exception as e:
            logger.error(f"消息处理失败: {str(e)}", exc_info=True)
            return await self.send_cease_signal(
                reason=f"处理失败: {str(e)}",
                cease_type=CeaseType.SAFETY
            )
    
    def get_session_info(self) -> Dict[str, Any]:
        """获取会话信息"""
        return self.session_manager.get_session_summary()
    
    def clear_cache(self):
        """清空缓存"""
        self.spectrum_cache.clear()
        self.puzzle_cache.clear()
        logger.info("缓存已清空")
    
    def add_custom_engine(self, spectrum_type: SpectrumType, engine: SpectrumEngine):
        """添加自定义引擎"""
        self.engines[spectrum_type] = engine
        if spectrum_type not in self.capabilities:
            self.capabilities.append(spectrum_type)
        logger.info(f"添加自定义引擎: {spectrum_type.value} - {engine.engine_name}")

# ============================================================================
# 工具函数
# ============================================================================

def validate_prism_message(message: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    验证棱镜消息是否符合协议规范
    
    Args:
        message: 要验证的消息
        
    Returns:
        (是否有效, 错误列表)
    """
    errors = []
    
    # 检查必填字段
    required_fields = ["protocol", "version", "type"]
    for field in required_fields:
        if field not in message:
            errors.append(f"缺少必填字段: {field}")
    
    # 检查协议标识
    if message.get("protocol") != "PIP":
        errors.append("protocol字段必须为'PIP'")
    
    # 检查消息类型
    msg_type = message.get("type")
    if msg_type not in [t.value for t in MessageType]:
        errors.append(f"无效的消息类型: {msg_type}")
    
    # 如果是棱镜消息，检查额外字段
    if msg_type == MessageType.PRISM_MESSAGE.value:
        prism_required = ["puzzle", "spectrums", "whitespace"]
        for field in prism_required:
            if field not in message:
                errors.append(f"棱镜消息缺少必填字段: {field}")
        
        # 检查光谱数量
        spectrums = message.get("spectrums", [])
        if len(spectrums) < 3:
            errors.append(f"光谱数量不足: 需要至少3个，当前{len(spectrums)}个")
        
        # 检查留白内容
        whitespace = message.get("whitespace", {})
        if not whitespace.get("content", "").strip():
            errors.append("留白内容不能为空")
        
        # 检查困惑文本
        puzzle = message.get("puzzle", {})
        if not puzzle.get("text", "").strip():
            errors.append("困惑文本不能为空")
    
    # 如果是知止信号，检查原因
    elif msg_type == MessageType.CEASE_SIGNAL.value:
        metadata = message.get("metadata", {})
        if not metadata.get("reason", "").strip():
            errors.append("知止信号应该包含原因说明")
    
    return len(errors) == 0, errors

def format_prism_message(message: Dict[str, Any], indent: int = 2) -> str:
    """
    格式化棱镜消息为易读字符串
    
    Args:
        message: 棱镜消息
        indent: 缩进空格数
        
    Returns:
        格式化后的字符串
    """
    try:
        msg_type = message.get("type")
        
        if msg_type == MessageType.PRISM_MESSAGE.value:
            puzzle = message.get("puzzle", {})
            spectrums = message.get("spectrums", [])
            whitespace = message.get("whitespace", {})
            metadata = message.get("metadata", {})
            
            output = []
            output.append("=" * 60)
            output.append("棱镜消息")
            output.append("=" * 60)
            output.append(f"困惑: {puzzle.get('text')}")
            if puzzle.get('context'):
                output.append(f"上下文: {puzzle.get('context')}")
            output.append("")
            output.append("光谱:")
            for i, spectrum in enumerate(spectrums, 1):
                output.append(f"  {i}. [{spectrum.get('type')}] {spectrum.get('name')}")
                content = spectrum.get('content', '')
                if len(content) > 100:
                    content = content[:97] + "..."
                output.append(f"     {content}")
                output.append("")
            
            output.append("留白:")
            output.append(f"  {whitespace.get('content')}")
            output.append("")
            output.append(f"元数据: 深度={metadata.get('recursion_depth', 0)}, "
                         f"允许递归={metadata.get('allow_recursion', False)}")
            output.append("=" * 60)
            
            return "\n".join(output)
        
        elif msg_type == MessageType.CEASE_SIGNAL.value:
            metadata = message.get("metadata", {})
            
            output = []
            output.append("=" * 60)
            output.append("知止信号")
            output.append("=" * 60)
            output.append(f"原因: {metadata.get('reason')}")
            output.append(f"类型: {metadata.get('cease_type')}")
            output.append(f"可恢复: {metadata.get('resumable')}")
            output.append("=" * 60)
            
            return "\n".join(output)
        
        else:
            return json.dumps(message, indent=indent, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"格式化失败: {str(e)}")
        return json.dumps(message, indent=indent, ensure_ascii=False)

# ============================================================================
# 示例和测试
# ============================================================================

async def example_usage():
    """使用示例"""
    print("棱镜协议Python实现 - 使用示例")
    print("=" * 60)
    
    # 创建代理
    agent = PrismAgent(
        agent_id="demo_agent",
        capabilities=[
            SpectrumType.RED,
            SpectrumType.BLUE,
            SpectrumType.PURPLE,
            SpectrumType.GREEN  # 自定义光谱
        ],
        max_depth=3,
        enable_caching=True
    )
    
    # 示例1: 基础折射
    print("\n1. 基础折射示例:")
    puzzle = "为什么我总在重要决定前犹豫不决？"
    response = await agent.refract(puzzle, depth=0)
    
    is_valid, errors = validate_prism_message(response)
    if is_valid:
        print("✅ 消息验证通过")
        print(format_prism_message(response))
    else:
        print("❌ 消息验证失败:")
        for error in errors:
            print(f"  - {error}")
    
    # 示例2: 递归折射
    print("\n2. 递归折射示例:")
    # 假设我们对第一个光谱进行递归
    if response.get("type") == MessageType.PRISM_MESSAGE.value:
        first_spectrum = response.get("spectrums", [])[0]
        recursive_puzzle = f"对'{first_spectrum.get('name')}'的深度探索: {first_spectrum.get('content', '')[:50]}..."
        
        recursive_response = await agent.refract(recursive_puzzle, depth=1)
        
        is_valid, errors = validate_prism_message(recursive_response)
        if is_valid:
            print("✅ 递归消息验证通过")
            print(f"递归深度: {recursive_response.get('metadata', {}).get('recursion_depth', 0)}")
        else:
            print("❌ 递归消息验证失败")
    
    # 示例3: 知止信号
    print("\n3. 知止信号示例:")
    cease_response = await agent.send_cease_signal(
        reason="示例演示结束",
        cease_type=CeaseType.TEMPORARY,
        resumable=True
    )
    print(format_prism_message(cease_response))
    
    # 示例4: 会话信息
    print("\n4. 会话信息:")
    session_info = agent.get_session_info()
    print(f"会话ID: {session_info.get('session_id')}")
    print(f"消息总数: {session_info.get('total_messages')}")
    print(f"最大深度: {session_info.get('max_depth_reached')}")
    print(f"持续时间: {session_info.get('duration_seconds'):.1f}秒")
    
    # 示例5: 消息处理
    print("\n5. 消息处理示例:")
    test_message = {
        "protocol": "PIP",
        "version": "0.1",
        "type": "prism_message",
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sender": {"id": "test_user"},
        "puzzle": {"text": "测试消息处理功能"},
        "spectrums": [
            {"type": "red", "name": "测试", "content": "测试内容1"},
            {"type": "blue", "name": "测试", "content": "测试内容2"},
            {"type": "purple", "name": "测试", "content": "测试内容3"}
        ],
        "whitespace": {"content": "测试留白"},
        "metadata": {"recursion_depth": 0, "allow_recursion": True}
    }
    
    processed_response = await agent.process_message(test_message)
    print(f"处理响应类型: {processed_response.get('type')}")
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)

async def performance_test():
    """性能测试"""
    print("\n性能测试:")
    print("-" * 40)
    
    agent = PrismAgent(
        agent_id="perf_test",
        max_depth=2,
        enable_caching=True
    )
    
    import time
    
    # 测试缓存效果
    puzzles = [
        "测试问题1: 如何提高学习效率？",
        "测试问题2: 为什么团队合作经常出现沟通问题？",
        "测试问题3: 在快速变化的环境中如何保持专注？"
    ]
    
    print("第一次生成（无缓存）:")
    start_time = time.time()
    for i, puzzle in enumerate(puzzles, 1):
        await agent.refract(puzzle)
        print(f"  问题{i}: 完成")
    first_duration = time.time() - start_time
    print(f"  总时间: {first_duration:.2f}秒")
    
    print("\n第二次生成（有缓存）:")
    start_time = time.time()
    for i, puzzle in enumerate(puzzles, 1):
        await agent.refract(puzzle)
        print(f"  问题{i}: 完成")
    second_duration = time.time() - start_time
    print(f"  总时间: {second_duration:.2f}秒")
    
    if second_duration > 0:
        speedup = first_duration / second_duration
        print(f"\n缓存加速比: {speedup:.1f}x")
    
    # 清空缓存
    agent.clear_cache()

def main():
    """主函数"""
    print("🔮 棱镜互联协议 - Python参考实现")
    print("版本: 1.0.0 | 协议: PIP v0.1")
    print("=" * 60)
    
    # 运行示例
    asyncio.run(example_usage())
    
    # 运行性能测试
    asyncio.run(performance_test())
    
    print("\n🎉 所有测试完成!")
    print("\n使用说明:")
    print("1. 创建代理: agent = PrismAgent('your_id')")
    print("2. 折射困惑: response = await agent.refract('你的困惑')")
    print("3. 处理消息: response = await agent.process_message(received_message)")
    print("4. 发送知止: await agent.send_cease_signal('原因')")
    print("\n详细文档请参考: https://github.com/Ultima0369/prism-interconnect")

if __name__ == "__main__":
    main()
