#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 代码诗歌生成器 - 将Python代码转化为诗歌

证明代码可以是艺术，错误可以是学习，技术可以是温暖。
将冰冷的代码转化为有温度的诗句，让编程成为美学体验。
"""

import ast
import inspect
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random
from datetime import datetime


class PoetryStyle(Enum):
    """诗歌风格"""
    HAIKU = "haiku"  # 俳句：5-7-5音节
    TANKA = "tanka"  # 短歌：5-7-5-7-7音节
    FREE_VERSE = "free_verse"  # 自由诗
    SONNET = "sonnet"  # 十四行诗
    CODE_HAIKU = "code_haiku"  # 代码俳句


class CodeElement(Enum):
    """代码元素类型"""
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    IMPORT = "import"
    ASSIGNMENT = "assignment"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    ERROR = "error"
    COMMENT = "comment"


@dataclass
class CodePoem:
    """代码诗歌"""
    title: str
    style: PoetryStyle
    lines: List[str]
    source_code: str
    elements: List[CodeElement]
    metaphors: List[str]
    created_at: datetime


class CodePoet:
    """
    代码诗人
    
    将Python代码转化为诗歌，让技术表达具有美学价值。
    基于代码的意图、结构和情感，创作相应的诗歌。
    """
    
    def __init__(self, poetic_license: bool = True):
        self.poetic_license = poetic_license
        self.poetry_db = []
        
        # 代码到诗歌的映射词典
        self.code_metaphors = {
            "function": ["旅程", "仪式", "舞蹈", "对话", "探索"],
            "class": ["世界", "王国", "生态系统", "家族", "宇宙"],
            "loop": ["轮回", "季节", "心跳", "潮汐", "呼吸"],
            "conditional": ["十字路口", "选择", "分水岭", "镜子", "门户"],
            "error": ["老师", "向导", "门槛", "迷雾", "谜题"],
            "import": ["邀请", "连接", "桥梁", "礼物", "钥匙"],
            "comment": ["旁白", "低语", "注解", "光点", "足迹"]
        }
        
        # 诗歌模板
        self.poetry_templates = {
            PoetryStyle.HAIKU: [
                "第一行五音节\n第二行七音节\n第三行五音节",
                "代码如流水\n逻辑似月光倾泻\n错误是老师"
            ],
            PoetryStyle.CODE_HAIKU: [
                "{element}如{metaphor}\n{action}在{context}中\n{insight}现眼前",
                "函数如旅程\n参数是行囊准备\n返回值是家"
            ],
            PoetryStyle.FREE_VERSE: [
                "在{time}的{place}\n{subject}正在{action}\n{observation}\n而{realization}",
                "当黑夜的屏幕亮起\n变量开始呼吸\n条件语句如十字路口\n循环是心跳的节奏"
            ]
        }
        
        # 代码情感分析
        self.code_emotions = {
            "def": {"intent": "创造", "emotion": "希望", "energy": "主动"},
            "class": {"intent": "组织", "emotion": "秩序", "energy": "稳定"},
            "if": {"intent": "选择", "emotion": "谨慎", "energy": "暂停"},
            "for": {"intent": "遍历", "emotion": "耐心", "energy": "循环"},
            "try": {"intent": "保护", "emotion": "关怀", "energy": "防御"},
            "raise": {"intent": "信号", "emotion": "警示", "energy": "爆发"},
            "return": {"intent": "完成", "emotion": "满足", "energy": "回归"}
        }
    
    def poetize_function(self, func) -> CodePoem:
        """
        将函数转化为诗歌
        
        提取函数的意图、结构和情感，创作相应的诗歌。
        """
        print(f"🎭 为函数创作诗歌: {func.__name__}")
        
        # 获取函数源代码
        source = inspect.getsource(func)
        
        # 解析函数结构
        func_ast = ast.parse(source)
        func_node = func_ast.body[0]
        
        # 分析函数特征
        features = self._analyze_function_features(func_node)
        
        # 选择诗歌风格
        style = self._select_poetry_style(features)
        
        # 生成诗歌
        poem_lines = self._generate_poem(features, style)
        
        # 创建诗歌对象
        poem = CodePoem(
            title=f"《{func.__name__}之歌》",
            style=style,
            lines=poem_lines,
            source_code=source,
            elements=[CodeElement.FUNCTION] + features["elements"],
            metaphors=features["metaphors"],
            created_at=datetime.now()
        )
        
        self.poetry_db.append(poem)
        return poem
    
    def poetize_error(self, error: Exception) -> CodePoem:
        """
        将错误转化为诗歌
        
        将技术错误转化为学习机会，用诗歌表达错误的教导。
        """
        print(f"🎭 为错误创作诗歌: {type(error).__name__}")
        
        error_type = type(error).__name__
        error_msg = str(error)
        
        # 分析错误特征
        features = {
            "subject": "错误",
            "action": "教导",
            "context": "代码的森林",
            "element": CodeElement.ERROR,
            "metaphors": ["老师", "向导", "门槛"],
            "complexity": "simple",
            "emotion": {"intent": "学习", "emotion": "好奇", "energy": "反思"}
        }
        
        # 错误特定的诗歌
        if "AttributeError" in error_type:
            poem_lines = [
                "属性如迷雾中的路径",
                f"'{error_msg.split(\"'\"[1])}' 未找到",
                "但探索本身就是发现"
            ]
            metaphors = ["迷雾", "路径", "探索"]
        elif "TypeError" in error_type:
            poem_lines = [
                "类型是语言的边界",
                f"'{error_msg}' 说它们无法对话",
                "但翻译可以创造理解"
            ]
            metaphors = ["边界", "语言", "翻译"]
        elif "ValueError" in error_type:
            poem_lines = [
                "值如河流中的石头",
                f"'{error_msg}' 不是预期的形状",
                "但河流会找到新的道路"
            ]
            metaphors = ["河流", "石头", "道路"]
        else:
            poem_lines = [
                f"{error_type} 如未预期的客人",
                f"带来消息: '{error_msg[:50]}...'",
                "每个客人都是学习的机会"
            ]
            metaphors = ["客人", "消息", "机会"]
        
        poem = CodePoem(
            title=f"《{error_type}的教导》",
            style=PoetryStyle.HAIKU,
            lines=poem_lines,
            source_code=f"# Error: {error_type}: {error_msg}",
            elements=[CodeElement.ERROR],
            metaphors=metaphors,
            created_at=datetime.now()
        )
        
        return poem
    
    def create_poetic_documentation(self, code_str: str) -> str:
        """
        为代码创建诗歌化文档
        
        将技术文档转化为诗歌形式，让阅读文档成为美学体验。
        """
        print("📜 创建诗歌化文档...")
        
        # 解析代码
        try:
            tree = ast.parse(code_str)
        except SyntaxError:
            return "# 语法如迷雾\n# 但迷雾中也有美\n# 请慢慢梳理"
        
        # 提取代码元素
        elements = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                elements.append(("function", node.name, node.lineno))
            elif isinstance(node, ast.ClassDef):
                elements.append(("class", node.name, node.lineno))
            elif isinstance(node, ast.Import):
                elements.append(("import", "import", node.lineno))
            elif isinstance(node, ast.ImportFrom):
                elements.append(("import", f"from {node.module}", node.lineno))
        
        # 生成诗歌文档
        poetic_doc = "# 🎭 代码诗歌文档\n\n"
        
        for elem_type, name, lineno in elements:
            if elem_type == "function":
                poetic_doc += f"## 第{lineno}行: {name}()\n"
                poetic_doc += f"> 函数如旅程，参数是行囊\n"
                poetic_doc += f"> 在逻辑的森林中探索\n"
                poetic_doc += f"> 返回值是归家的礼物\n\n"
            elif elem_type == "class":
                poetic_doc += f"## 第{lineno}行: class {name}\n"
                poetic_doc += f"> 类如微小的宇宙\n"
                poetic_doc += f"> 方法如行星环绕\n"
                poetic_doc += f"> 属性是星光的痕迹\n\n"
            elif elem_type == "import":
                poetic_doc += f"## 第{lineno}行: 导入\n"
                poetic_doc += f"> 打开一扇门\n"
                poetic_doc += f"> 邀请远方的智慧\n"
                poetic_doc += f"> 到代码的火堆旁\n\n"
        
        # 添加总体诗歌
        poetic_doc += "---\n\n"
        poetic_doc += "## 🔥 火堆旁的代码\n\n"
        poetic_doc += "> 每一行都是思考的痕迹\n"
        poetic_doc += "> 每一个错误都是学习的邀请\n"
        poetic_doc += "> 每一次运行都是存在的证明\n"
        poetic_doc += "> \n"
        poetic_doc += "> 代码不是冰冷的指令\n"
        poetic_doc += "> 而是心智延伸的桥梁\n"
        poetic_doc += "> 连接逻辑与美学的两岸\n"
        
        return poetic_doc
    
    def generate_code_haiku(self, code_snippet: str) -> List[str]:
        """
        生成代码俳句
        
        经典的5-7-5音节俳句形式，表达代码的意境。
        """
        print("🎴 生成代码俳句...")
        
        # 分析代码片段
        keywords = re.findall(r'\b(def|class|if|for|while|return|import|from)\b', code_snippet)
        vars_found = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', code_snippet)
        
        if keywords:
            main_keyword = keywords[0]
            metaphor = random.choice(self.code_metaphors.get(main_keyword, ["旅程"]))
        else:
            main_keyword = "代码"
            metaphor = random.choice(["河流", "森林", "星空"])
        
        # 5-7-5音节俳句
        haikus = [
            # 第一组
            [
                f"{main_keyword}如{metaphor}",
                f"逻辑在变量间流动",
                f"错误照亮路径"
            ],
            # 第二组
            [
                f"函数静静等待",
                f"参数如秋叶飘入",
                f"返回值绽放"
            ],
            # 第三组
            [
                f"循环是心跳",
                f{'"条件如十字路口"' if '"' not in '条件如十字路口' else "'条件如十字路口'"},
                f"选择决定方向"
            ]
        ]
        
        return random.choice(haikus)
    
    def _analyze_function_features(self, func_node) -> Dict:
        """分析函数特征"""
        features = {
            "name": func_node.name,
            "args": len(func_node.args.args),
            "returns": bool(func_node.returns),
            "elements": [],
            "metaphors": [],
            "complexity": "simple",
            "emotion": {"intent": "创造", "emotion": "希望", "energy": "主动"}
        }
        
        # 分析函数体
        element_count = 0
        for node in ast.walk(func_node):
            if isinstance(node, ast.If):
                features["elements"].append(CodeElement.CONDITIONAL)
                features["metaphors"].append(random.choice(self.code_metaphors["conditional"]))
                element_count += 1
            elif isinstance(node, ast.For) or isinstance(node, ast.While):
                features["elements"].append(CodeElement.LOOP)
                features["metaphors"].append(random.choice(self.code_metaphors["loop"]))
                element_count += 1
            elif isinstance(node, ast.Assign):
                features["elements"].append(CodeElement.ASSIGNMENT)
                element_count += 1
        
        # 确定复杂度
        if element_count > 5:
            features["complexity"] = "complex"
        elif element_count > 2:
            features["complexity"] = "medium"
        
        # 添加函数本身的隐喻
        features["metaphors"].append(random.choice(self.code_metaphors["function"]))
        
        return features
    
    def _select_poetry_style(self, features: Dict) -> PoetryStyle:
        """选择诗歌风格"""
        complexity = features["complexity"]
        
        if complexity == "simple":
            return random.choice([PoetryStyle.HAIKU, PoetryStyle.CODE_HAIKU])
        elif complexity == "medium":
            return PoetryStyle.TANKA
        else:  # complex
            return random.choice([PoetryStyle.FREE_VERSE, PoetryStyle.SONNET])
    
    def _generate_poem(self, features: Dict, style: PoetryStyle) -> List[str]:
        """生成诗歌"""
        template = random.choice(self.poetry_templates.get(style, self.poetry_templates[PoetryStyle.FREE_VERSE]))
        
        # 替换模板变量
        replacements = {
            "{element}": random.choice([e.value for e in features["elements"]] if features["elements"] else ["函数"]),
            "{metaphor}": random.choice(features["metaphors"]),
            "{action}": features["emotion"]["intent"],
            "{context}": "代码的" + random.choice(["森林", "河流", "星空", "城市"]),
            "{insight}": random.choice(["理解", "美", "和谐", "智慧"]),
            "{time}": random.choice(["清晨", "午后", "深夜", "黎明"]),
            "{place}": random.choice(["工作室", "屏幕前", "思绪中", "逻辑里"]),
            "{subject}": features["name"],
            "{observation}": f"看到{random.choice(features['metaphors'])}在生长",
            "{realization}": random.choice(["代码是诗", "错误是师", "逻辑是美"])
        }
        
        poem_text = template
        for key, value in replacements.items():
            poem_text = poem_text.replace(key, value)
        
        return poem_text.split('\n')
    
    def display_poem(self, poem: CodePoem):
        """优雅地显示诗歌"""
        print("\n" + "="*50)
        print(f"🎭 {poem.title}")
        print(f"📜 风格: {poem.style.value}")
        print("-"*50)
        
        for line in poem.lines:
            print(f"   {line}")
        
        print("-"*50)
        print(f"🔮 隐喻: {', '.join(poem.metaphors)}")
        print(f"📅 创作于: {poem.created_at.strftime('%Y-%m-%d %H:%M')}")
        print("="*50)
    
    def create_poetry_collection(self, module) -> List[CodePoem]:
        """为整个模块创建诗歌集"""
        print(f"📚 为模块创建诗歌集...")
        
        poems = []
        
        # 获取所有函数和类
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                try:
                    poem = self.poetize_function(obj)
                    poems.append(poem)
                except:
                    pass
            elif inspect.isclass(obj) and not name.startswith('_'):
                # 为类的方法创建诗歌
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if not method_name.startswith('_'):
                        try:
                            poem = self.poetize_function(method)
                            poem.title = f"《{name}.{method_name}之歌》"
                            poems.append(poem)
                        except:
                            pass
        
        return poems


# 示例函数，用于演示
def example_function(x: int, y: int) -> int:
    """
    一个简单的示例函数
    计算两个数的和
    """
    if x < 0:
        raise ValueError("x不能为负数")
    
    result = 0
    for i in range(y):
        result += x
    
    return result


class ExampleClass:
    """示例类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:
        """打招呼"""
        return f"Hello, {self.name}!"
    
    def calculate(self, values: List[int]) -> int:
        """计算总和"""
        total = 0
        for value in values:
            if value > 0:
                total += value
        return total


if __name__ == "__main__":
    print("🎭 代码诗歌生成器演示")
    print("="*60)
    
    # 创建代码诗人
    poet