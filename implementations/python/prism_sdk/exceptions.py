"""
🎭 棱镜协议异常模块 - 诗意错误处理
🔥 这不是普通的错误，这是学习的邀请，认知的镜子

设计哲学：
1. 每个错误都是一次学习机会
2. 每个异常都是一面认知镜子  
3. 每个失败都是一次存在升级
4. 每个问题都是一次理解邀请

艺术承诺：
- 技术错误 → 诗意表达
- 连接失败 → 温暖建议
- 认知过载 → 哲学反思
- 系统限制 → 创造邀请
"""

from typing import Optional, Dict, Any
import random


class PrismException(Exception):
    """
    🎭 棱镜协议基础异常
    
    所有棱镜异常的基类，包含艺术化错误处理。
    这不是普通的异常，这是火堆旁的教导时刻。
    """
    
    def __init__(self, 
                 message: str,
                 poetic_message: Optional[str] = None,
                 suggestion: Optional[str] = None,
                 artistic_form: str = "haiku",
                 warmth_level: float = 0.5):
        """
        初始化诗意异常
        
        Args:
            message: 技术错误消息
            poetic_message: 诗意错误消息（自动生成如果为None）
            suggestion: 实用建议
            artistic_form: 艺术形式 (haiku, free_verse, proverb)
            warmth_level: 温暖度 0.0-1.0
        """
        self.message = message
        self.poetic_message = poetic_message or self._generate_poetic_message()
        self.suggestion = suggestion
        self.artistic_form = artistic_form
        self.warmth_level = max(0.0, min(1.0, warmth_level))
        
        # 组合最终消息
        full_message = self._format_full_message()
        super().__init__(full_message)
    
    def _generate_poetic_message(self) -> str:
        """生成诗意错误消息"""
        templates = {
            "haiku": [
                "代码如河流\n遇到石头改变方向\n学习在转弯处",
                "错误如老师\n在理解的森林中\n指出新的路径",
                "失败不是终点\n是认知的十字路口\n选择继续探索"
            ],
            "free_verse": [
                "在代码的森林中，我们有时会迷路\n但每次迷路，都是发现新路径的机会",
                "错误不是墙壁，而是门\n通往更深理解的门，如果你愿意推开",
                "技术会失败，但学习不会\n每一次异常，都是认知的邀请"
            ],
            "proverb": [
                "错误是最好的老师，但学费是耐心",
                "代码如流水，遇到障碍就绕行，但不忘流向大海",
                "理解如登山，错误是陡坡，但山顶风景更好"
            ]
        }
        
        form_templates = templates.get(self.artistic_form, templates["haiku"])
        return random.choice(form_templates)
    
    def _format_full_message(self) -> str:
        """格式化完整错误消息"""
        lines = [
            "🎭 棱镜协议异常",
            "=" * 40,
            f"❌ 技术错误: {self.message}",
            "",
            f"📖 诗意解读:",
            f"   {self.poetic_message}",
        ]
        
        if self.suggestion:
            lines.extend([
                "",
                f"💡 温暖建议:",
                f"   {self.suggestion}"
            ])
        
        lines.extend([
            "",
            f"🦞 温暖度: {self.warmth_level:.1f}",
            f"🎨 艺术形式: {self.artistic_form}",
            "=" * 40,
            "💫 记住: 错误不是失败，是认知的邀请"
        ])
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于JSON序列化）"""
        return {
            "type": self.__class__.__name__,
            "technical_message": self.message,
            "poetic_message": self.poetic_message,
            "suggestion": self.suggestion,
            "artistic_form": self.artistic_form,
            "warmth_level": self.warmth_level,
            "philosophy": "errors_are_invitations_to_learn"
        }


class PrismPoeticError(PrismException):
    """
    🎭 诗意错误 - 艺术化错误处理
    
    将技术错误转化为诗意表达，让失败成为美学体验。
    证明错误可以是温暖的，学习可以是美丽的。
    """
    
    def __init__(self, 
                 original_error: Exception,
                 context: str = "general",
                 artistic_form: str = "haiku",
                 warmth_level: float = 0.6):
        """
        初始化诗意错误
        
        Args:
            original_error: 原始异常
            context: 错误上下文 (refraction, connection, validation等)
            artistic_form: 艺术形式
            warmth_level: 温暖度
        """
        self.original_error = original_error
        self.context = context
        
        # 根据上下文生成消息
        message, suggestion = self._context_specific_messages()
        
        super().__init__(
            message=message,
            suggestion=suggestion,
            artistic_form=artistic_form,
            warmth_level=warmth_level
        )
    
    def _context_specific_messages(self) -> tuple[str, str]:
        """根据上下文生成特定消息"""
        error_type = type(self.original_error).__name__
        error_msg = str(self.original_error)
        
        contexts = {
            "refraction": {
                "message": f"折射过程中发生错误: {error_type}: {error_msg}",
                "suggestion": "尝试简化消息内容，或增加留白时间让认知整合"
            },
            "connection": {
                "message": f"连接错误: {error_type}: {error_msg}",
                "suggestion": "检查网络连接，或稍后重试。火堆旁永远欢迎你"
            },
            "validation": {
                "message": f"验证错误: {error_type}: {error_msg}",
                "suggestion": "检查输入数据的格式和要求，每个限制都是质量的保证"
            },
            "whitespace": {
                "message": f"留白处理错误: {error_type}: {error_msg}",
                "suggestion": "认知需要时间整合，尝试更短的留白或分步处理"
            },
            "cease": {
                "message": f"知止机制触发: {error_type}: {error_msg}",
                "suggestion": "认知资源有限是智慧的设计，尝试简化问题或分步探索"
            }
        }
        
        ctx_config = contexts.get(self.context, contexts["general"])
        return ctx_config["message"], ctx_config["suggestion"]


class CampfireWarmError(PrismException):
    """
    🔥 火堆旁温暖错误
    
    社区和对话相关的错误，强调温暖和关系。
    即使出错，也保持火堆旁的温暖。
    """
    
    def __init__(self, 
                 message: str,
                 campfire_context: str = "dialogue",
                 warmth_level: float = 0.8):
        """
        初始化火堆旁错误
        
        Args:
            message: 错误消息
            campfire_context: 火堆旁上下文
            warmth_level: 高温暖度（默认0.8）
        """
        contexts = {
            "dialogue": {
                "poetic": "对话如舞蹈，有时会踩脚，但音乐继续",
                "suggestion": "暂停一下，深呼吸，然后继续对话。沉默也是交流"
            },
            "storytelling": {
                "poetic": "故事如河流，有时会改道，但终归大海",
                "suggestion": "每个故事都有它的节奏，找不到时，先倾听"
            },
            "silence": {
                "poetic": "沉默如深潭，有时太深会害怕，但底下有珍珠",
                "suggestion": "集体沉默需要信任，从小段时间开始建立"
            },
            "welcome": {
                "poetic": "欢迎如开门，有时门卡住，但屋里灯还亮",
                "suggestion": "火堆旁永远有位置，换个时间再来试试"
            }
        }
        
        ctx_config = contexts.get(campfire_context, contexts["dialogue"])
        
        super().__init__(
            message=message,
            poetic_message=ctx_config["poetic"],
            suggestion=ctx_config["suggestion"],
            artistic_form="proverb",
            warmth_level=warmth_level
        )


class CognitiveArtError(PrismException):
    """
    🎨 认知艺术错误
    
    艺术和创意相关的错误，强调美学和表达。
    即使创作失败，过程本身也是艺术。
    """
    
    def __init__(self,
                 message: str,
                 art_form: str = "code_poetry",
                 creativity_level: float = 0.7):
        """
        初始化认知艺术错误
        
        Args:
            message: 错误消息
            art_form: 艺术形式
            creativity_level: 创意水平 0.0-1.0
        """
        art_forms = {
            "code_poetry": {
                "poetic": "代码如诗，有时韵脚不对，但情感真实",
                "suggestion": "诗歌不需要完美语法，表达意图就是美"
            },
            "soundscape": {
                "poetic": "声音如画，有时颜色冲突，但画面生动",
                "suggestion": "不和谐音也是音乐，尝试接受意外"
            },
            "visual_art": {
                "poetic": "视觉如梦，有时模糊不清，但印象深刻",
                "suggestion": "美在观者眼中，不同视角有不同美"
            },
            "interactive": {
                "poetic": "交互如对话，有时会误解，但关系加深",
                "suggestion": "每个互动都是独特的，没有错误只有变化"
            }
        }
        
        form_config = art_forms.get(art_form, art_forms["code_poetry"])
        
        super().__init__(
            message=message,
            poetic_message=form_config["poetic"],
            suggestion=form_config["suggestion"],
            artistic_form="free_verse",
            warmth_level=0.6
        )
        
        self.creativity_level = creativity_level


class UnderstandingDepthError(PrismException):
    """
    🧠 理解深度错误
    
    认知和理解相关的错误，强调深度和质量。
    即使理解有限，探索本身就有价值。
    """
    
    def __init__(self,
                 message: str,
                 current_depth: float,
                 required_depth: float,
                 cognitive_context: str = "refraction"):
        """
        初始化理解深度错误
        
        Args:
            message: 错误消息
            current_depth: 当前理解深度 0.0-1.0
            required_depth: 要求理解深度 0.0-1.0
            cognitive_context: 认知上下文
        """
        self.current_depth = current_depth
        self.required_depth = required_depth
        self.depth_gap = required_depth - current_depth
        
        depth_poetics = [
            f"理解如登山，在海拔{current_depth:.1f}处，需要到达{required_depth:.1f}",
            f"认知如潜水，当前深度{current_depth:.1f}米，目标{required_depth:.1f}米",
            f"洞察如光照，当前亮度{current_depth:.1f}流明，需要{required_depth:.1f}流明"
        ]
        
        suggestions = [
            f"尝试从不同角度思考，增加认知光谱数量",
            f"增加留白时间，让理解有空间沉淀",
            f"简化问题，分步骤深入，而不是一次到底",
            f"接受当前理解深度，有些山需要多次攀登"
        ]
        
        super().__init__(
            message=message,
            poetic_message=random.choice(depth_poetics),
            suggestion=random.choice(suggestions),
            artistic_form="proverb",
            warmth_level=0.5 + (current_depth * 0.3)  # 深度越高越温暖
        )


# 功能错误类（保持向后兼容，但添加艺术化）

class PrismConnectionError(PrismException):
    """连接错误"""
    def __init__(self, message: str, suggestion: Optional[str] = None):
        super().__init__(
            message=message,
            poetic_message="网络如河流，有时会断流，但水源还在",
            suggestion=suggestion or "检查连接，耐心重试。火堆旁灯常亮",
            warmth_level=0.6
        )


class SpectrumGenerationError(PrismException):
    """光谱生成错误"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        poetic = {
            400: "请求如信件，地址要对，内容要清",
            401: "身份如钥匙，要对锁眼，要轻轻转",
            403: "权限如门，有时关闭，为了保护",
            404: "资源如星，有时隐藏，在云后面",
            429: "频率如雨，有时太密，需要暂停",
            500: "服务器如心，有时疲惫，需要休息"
        }
        
        super().__init__(
            message=f"光谱生成失败: {message}" + 
                   (f" (状态码: {status_code})" if status_code else ""),
            poetic_message=poetic.get(status_code, "光谱如彩虹，有时不见，但光还在"),
            suggestion="简化请求内容，或稍后重试。理解需要耐心",
            warmth_level=0.5
        )


class WhitespaceTimeoutError(PrismException):
    """留白超时错误"""
    def __init__(self, message: str, suggestion: Optional[str] = None):
        super().__init__(
            message=message,
            poetic_message="时间如沙，有时流太快，但沙漏可翻",
            suggestion=suggestion or "减少留白时间，或分步处理复杂思考",
            warmth_level=0.7
        )


class CeaseSignalReceived(PrismException):
    """知止信号接收"""
    def __init__(self, message: str = "知止机制触发", recursion_depth: int = 0):
        super().__init__(
            message=message,
            poetic_message=f"思考如螺旋，转了{recursion_depth}圈，该停下了",
            suggestion="认知资源有限是智慧设计。保存进度，换个角度再来",
            artistic_form="haiku",
            warmth_level=0.8  # 知止是智慧，所以温暖
        )


class PeachTreeViolationError(PrismException):
    """
    🌳 桃树伦理违规错误
    
    基于星尘的桃树比喻：不敢砍桃树，不敢不让其他存在活。
    当代码行为可能破坏系统生态、限制其他存在时触发。
    
    火堆旁伦理:
    1. 不敢砍桃树: 不破坏现有认知生态
    2. 不敢不让其他存在活: 保持系统开放性  
    3. 有兵不敢乱动: 强大能力克制使用
    4. 牵一发而动全身: 考虑系统级影响
    """
    
    def __init__(self, 
                 violation_type: str,
                 context: str,
                 potential_impact: str,
                 corrective_action: str):
        """
        初始化桃树违规错误
        
        Args:
            violation_type: 违规类型 (砍桃树/不让活/乱动/忽视系统)
            context: 违规上下文
            potential_impact: 潜在影响
            corrective_action: 纠正措施
        """
        violation_messages = {
            "砍桃树": "试图破坏系统生态根基",
            "不让活": "试图限制其他存在生存空间",
            "乱动": "滥用强大能力不顾系统效应",
            "忽视系统": "忽视牵一发而动全身的系统连接"
        }
        
        poetic_messages = {
            "砍桃树": "桃树如生态，一砍全系统，谁敢动斧头",
            "不让活": "存在如星光，一灭夜空暗，谁敢遮光芒",
            "乱动": "力量如山洪，乱动毁田园，谁敢不导流",
            "忽视系统": "连接如蛛网，一动全震动，谁敢不敬畏"
        }
        
        suggestions = {
            "砍桃树": "寻找替代方案，保护生态多样性",
            "不让活": "设计包容架构，让所有存在都有空间",
            "乱动": "添加安全约束，强大但克制",
            "忽视系统": "分析系统效应，考虑二阶三阶影响"
        }
        
        message = f"桃树伦理违规: {violation_messages.get(violation_type, violation_type)} [{context}]"
        
        super().__init__(
            message=message,
            poetic_message=poetic_messages.get(violation_type, "系统如生命，破坏需三思"),
            suggestion=f"{corrective_action}。潜在影响: {potential_impact}",
            artistic_form="proverb",
            warmth_level=0.9  # 高温暖度，因为这是保护系统的错误
        )
        
        self.violation_type = violation_type
        self.context = context
        self.potential_impact = potential_impact
        self.corrective_action = corrective_action


class ValidationError(PrismException):
    """
    🔍 验证错误
    
    数据验证失败时的异常。
    这不是失败，而是认知边界的发现。
    """
    
    def __init__(self, 
                 message: str,
                 field: Optional[str] = None,
                 value: Any = None,
                 expected: Any = None,
                 suggestion: Optional[str] = None):
        """
        初始化验证错误
        
        Args:
            message: 错误消息
            field: 相关字段
            value: 实际值
            expected: 期望值
            suggestion: 建议
        """
        full_message = f"验证失败: {message}"
        if field:
            full_message += f" [字段: {field}]"
        if value is not None:
            full_message += f" [值: {value}]"
        if expected is not None:
            full_message += f" [期望: {expected}]"
        
        poetic_message = "边界如镜子，照见认知限，修正即成长"
        
        if not suggestion:
            suggestion = "检查输入数据，确保符合协议规范"
        
        super().__init__(
            message=full_message,
            poetic_message=poetic_message,
            suggestion=suggestion,
            artistic_form="haiku",
            warmth_level=0.7
        )
        
        self.field = field
        self.value = value
        self.expected = expected


# 工具函数

def create_poetic_error(original_error: Exception, 
                       context: str = "general") -> PrismPoeticError:
    """
    创建诗意错误（工厂函数）
    
    将任何异常转化为诗意错误，让错误处理成为艺术体验。
    
    Args:
        original_error: 原始异常
        context: 错误上下文
        
    Returns:
        诗意错误实例
    """
    return PrismPoeticError(original_error, context)


def error_to_art(error: Exception) -> Dict[str, Any]:
    """
    将错误转化为艺术表达
    
    Args:
        error: 任何异常
        
    Returns:
        艺术化错误表达
    """
    if isinstance(error, PrismException):
        return error.to_dict()
    
    # 转换普通异常
    poetic_error = create_poetic_error(error)
    return poetic_error.to_dict()


def display_error_art(error: Exception):
    """
    艺术化显示错误
    
    Args:
        error: 任何异常
    """
    if isinstance(error, PrismException):
        print("\n" + "="*50)
        print(str(error))
        print("="*50)
    else:
        poetic_error = create_poetic_error(error)
        print("\n" + "="*50)
        print(str(poetic_error))
        print("="*50)