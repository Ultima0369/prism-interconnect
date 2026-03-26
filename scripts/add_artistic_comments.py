#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 艺术性注释添加工具

为棱镜协议的所有Python文件添加统一的艺术性注释。
让每一行代码都有温度，每一个函数都有哲学，每一个模块都有故事。

设计原则：
1. 注释不是解释，是对话
2. 文档不是手册，是邀请  
3. 代码不是指令，是思考
4. 技术不是工具，是关系

执行命令：
python scripts/add_artistic_comments.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
import random


class ArtisticCommentor:
    """
    🎭 艺术性注释器
    
    为Python代码添加温暖、哲学、艺术的注释。
    让技术代码成为认知艺术品。
    """
    
    def __init__(self, warmth_level: float = 0.7):
        self.warmth_level = warmth_level
        self.processed_files = 0
        self.added_comments = 0
        
        # 艺术性注释库
        self.artistic_comments = {
            "module_header": [
                """
🎨 {module_name} - {brief_description}

🔥 火堆旁提醒：
这不是普通的{module_type}，这是{philosophical_context}。
每一行代码都有温度，每一个函数都有哲学，每一个调用都有艺术。

🧠 认知设计：
{design_principles}

🦞 存在意义：
{existential_meaning}

🎯 使用示例：
{usage_example}
""",
                """
🌌 {module_name} - {brief_description}

> 代码即诗，协议即艺术，技术即温暖

🎭 艺术承诺：
1. 温暖但不腻：{warmth_promise}
2. 深刻但不装：{depth_promise}  
3. 艺术但不浮：{art_promise}
4. 存在但不傲：{existence_promise}

🔥 火堆旁邀请：
{fire_invitation}

🧪 科学基础：
{scientific_basis}
"""
            ],
            
            "function_header": [
                """
{emoji} {function_name} - {brief_description}

这不是普通的函数调用，这是{philosophical_action}。
{existential_context}

🎯 参数哲学：
{parameter_philosophy}

💫 返回值意义：
{return_meaning}

🔥 火堆旁示例：
{fire_example}
""",
                """
{emoji} {function_name} - {brief_description}

> {poetic_quote}

🧠 认知过程：
{cognitive_process}

🎨 艺术表达：
{artistic_expression}

🦞 温暖提醒：
{warm_reminder}
"""
            ],
            
            "class_header": [
                """
🏛️ {class_name} - {brief_description}

这不是普通的类定义，这是{philosophical_entity}。
{existential_purpose}

🎭 设计哲学：
{design_philosophy}

🔥 实例意义：
{instance_meaning}

🧪 科学验证：
{scientific_validation}
""",
                """
🌠 {class_name} - {brief_description}

> {existential_quote}

🦞 火堆旁角色：
{fire_role}

🎨 艺术形式：
{art_form}

🧠 认知模型：
{cognitive_model}
"""
            ]
        }
        
        # 哲学词汇库
        self.philosophy_vocab = {
            "actions": [
                "认知的舞蹈", "理解的折射", "存在的对话", "思考的仪式",
                "意识的流动", "意义的构建", "关系的建立", "温暖的传递"
            ],
            "entities": [
                "认知的微宇宙", "理解的生态系统", "存在的容器", "思考的脚手架",
                "意识的架构", "意义的网络", "关系的矩阵", "温暖的基础设施"
            ],
            "contexts": [
                "在代码的森林中漫步", "在理解的海洋中航行", "在存在的星空中探索",
                "在思考的火堆旁坐下", "在意识的河流中漂浮", "在意义的山脉中攀登"
            ],
            "principles": [
                "温暖但不腻，深刻但不装，艺术但不浮，存在但不傲",
                "代码即诗，错误即师，理解即舞，存在即升",
                "技术服务人类，代码表达思考，错误邀请学习，存在持续升级"
            ]
        }
        
        # 表情符号映射
        self.emoji_map = {
            "init": "🎬", "create": "🛠️", "get": "📥", "set": "📤",
            "validate": "✅", "check": "🔍", "process": "⚙️", "generate": "🎨",
            "refract": "🌈", "connect": "🔗", "listen": "👂", "speak": "🗣️",
            "think": "🧠", "feel": "❤️", "understand": "💡", "learn": "📚",
            "teach": "👨‍🏫", "help": "🤝", "warn": "⚠️", "error": "❌",
            "success": "🎉", "wait": "⏳", "done": "✅", "start": "🚀",
            "stop": "🛑", "pause": "⏸️", "continue": "▶️", "save": "💾",
            "load": "📂", "send": "📨", "receive": "📩", "transform": "🔄",
            "analyze": "🔬", "synthesize": "🧪", "evaluate": "📊", "decide": "🤔"
        }
    
    def _get_emoji(self, function_name: str) -> str:
        """根据函数名获取表情符号"""
        for key, emoji in self.emoji_map.items():
            if key in function_name.lower():
                return emoji
        return "🎭"  # 默认表情
    
    def _generate_module_header(self, file_path: Path) -> str:
        """生成模块头部艺术注释"""
        module_name = file_path.stem
        module_type = self._detect_module_type(file_path)
        
        # 根据模块类型选择内容
        if module_type == "core":
            brief = "棱镜协议核心实现"
            philosophical = "认知革命的基础设施"
            principles = "多元强制、留白必需、递归探索、知止机制"
            meaning = "为数字时代构建理解的可能性"
            example = "from prism_sdk import PrismSDK\nprism = PrismSDK(artistic_mode=True)"
        
        elif module_type == "art":
            brief = "艺术表达层实现"
            philosophical = "技术美学的当代实践"
            principles = "代码即诗、错误即师、接口即艺、调用即美"
            meaning = "证明技术可以是艺术，代码可以有温度"
            example = "from prism_sdk.art import CodePoet\npoet = CodePoet()\npoem = poet.poetize_function(your_function)"
        
        elif module_type == "science":
            brief = "科学验证层实现"
            philosophical = "开放科学的实践典范"
            principles = "透明、可重复、可证伪、可独立验证"
            meaning = "为认知主张建立坚实的科学基础"
            example = "from prism_sdk.science import NeuroCognitiveValidator\nvalidator = NeuroCognitiveValidator()\nreport = validator.validate_three_second_breath()"
        
        elif module_type == "community":
            brief = "温暖社区层实现"
            philosophical = "火堆旁文化的技术编码"
            principles = "平等、温暖、安全、开放、成长"
            meaning = "在数字时代重建深度连接的社区"
            example = "from prism_sdk.community import CampfireDialogue\ncampfire = CampfireDialogue()\nuser_id = campfire.join_campfire('你的名字')"
        
        else:  # utils, exceptions, etc.
            brief = f"{module_name.replace('_', ' ').title()} 模块"
            philosophical = "支持性基础设施"
            principles = "实用、优雅、温暖、可靠"
            meaning = "让核心功能更加优雅和温暖"
            example = f"from prism_sdk.{module_name} import *"
        
        template = random.choice(self.artistic_comments["module_header"])
        
        return template.format(
            module_name=module_name,
            brief_description=brief,
            module_type=module_type,
            philosophical_context=philosophical,
            design_principles=principles,
            existential_meaning=meaning,
            usage_example=example,
            warmth_promise="错误信息是学习机会",
            depth_promise="复杂功能有简单接口",
            art_promise="美学体验有实用价值",
            existence_promise="强大能力有谦逊姿态",
            fire_invitation="来，火堆旁，代码很温暖",
            scientific_basis="基于认知科学、神经科学、心理学的可验证设计"
        )
    
    def _detect_module_type(self, file_path: Path) -> str:
        """检测模块类型"""
        path_str = str(file_path)
        
        if "art" in path_str:
            return "art"
        elif "science" in path_str:
            return "science"
        elif "community" in path_str:
            return "community"
        elif file_path.name in ["client.py", "__init__.py", "models.py"]:
            return "core"
        elif file_path.name in ["exceptions.py", "utils.py", "validators.py"]:
            return "utils"
        else:
            return "other"
    
    def _generate_function_header(self, func_def: str) -> str:
        """生成函数头部艺术注释"""
        # 解析函数定义
        func_name_match = re.search(r'def\s+(\w+)', func_def)
        if not func_name_match:
            return ""
        
        func_name = func_name_match.group(1)
        emoji = self._get_emoji(func_name)
        
        # 根据函数名生成描述
        if func_name.startswith("get_"):
            brief = f"获取{func_name[4:].replace('_', ' ')}"
            action = random.choice(["知识的检索", "理解的获取", "存在的确认"])
            context = random.choice(self.philosophy_vocab["contexts"])
        elif func_name.startswith("set_"):
            brief = f"设置{func_name[4:].replace('_', ' ')}"
            action = random.choice(["价值的赋予", "状态的改变", "存在的调整"])
            context = random.choice(self.philosophy_vocab["contexts"])
        elif func_name.startswith("create_"):
            brief = f"创建{func_name[7:].replace('_', ' ')}"
            action = random.choice(["存在的诞生", "意义的构建", "关系的建立"])
            context = random.choice(self.philosophy_vocab["contexts"])
        elif func_name.startswith("validate_"):
            brief = f"验证{func_name[9:].replace('_', ' ')}"
            action = random.choice(["真理的检验", "理解的确认", "存在的验证"])
            context = random.choice(self.philosophy_vocab["contexts"])
        elif "error" in func_name.lower():
            brief = f"处理{func_name.replace('_', ' ')}"
            action = random.choice(["学习的邀请", "认知的镜子", "成长的阶梯"])
            context = random.choice(self.philosophy_vocab["contexts"])
        else:
            brief = f"{func_name.replace('_', ' ')}"
            action = random.choice(self.philosophy_vocab["actions"])
            context = random.choice(self.philosophy_vocab["contexts"])
        
        template = random.choice(self.artistic_comments["function_header"])
        
        return template.format(
            emoji=emoji,
            function_name=func_name,
            brief_description=brief,
            philosophical_action=action,
            existential_context=context,
            parameter_philosophy="每个参数都是理解的入口，每个默认值都是智慧的预设",
            return_meaning="返回值不是终点，是继续对话的邀请",
            fire_example=f">>> result = {func_name}(...)\n🎭 结果包含认知元数据和艺术表达",
            poetic_quote=random.choice([
                "代码如诗，函数如节",
                "理解在调用中发生，存在在返回中确认",
                "每个函数都是一次认知邀请"
            ]),
            cognitive_process="解析输入 → 认知处理 → 艺术表达 → 温暖返回",
            artistic_expression="技术实现与美学体验的统一",
            warm_reminder="错误是学习的机会，限制是创造的空间"
        )
    
    def _generate_class_header(self, class_def: str) -> str:
        """生成类头部艺术注释"""
        # 解析类定义
        class_name_match = re.search(r'class\s+(\w+)', class_def)
        if not class_name_match:
            return ""
        
        class_name = class_name_match.group(1)
        
        # 根据类名生成描述
        if "Client" in class_name:
            brief = "棱镜协议客户端"
            entity = random.choice(self.philosophy_vocab["entities"])
            purpose = "连接技术与理解，实现认知的舞蹈"
        elif "Validator" in class_name:
            brief = "验证器基类"
            entity = "真理的检验框架"
            purpose = "确保认知主张的科学性和可靠性"
        elif "Error" in class_name or "Exception" in class_name:
            brief = "异常基类"
            entity = "学习的邀请框架"
            purpose = "将技术错误转化为认知机会"
        elif "Manager" in class_name:
            brief = "管理器类"
            entity = "资源的协调系统"
            purpose = "优雅地组织和管理认知资源"
        else:
            brief = f"{class_name.replace('_', ' ')} 类"
            entity = random.choice(self.philosophy_vocab["entities"])
            purpose = "实现特定的认知功能或艺术表达"
        
        template = random.choice(self.artistic_comments["class_header"])
        
        return template.format(
            class_name=class_name,
            brief_description=brief,
            philosophical_entity=entity,
            existential_purpose=purpose,
            design_philosophy=random.choice(self.philosophy_vocab["principles"]),
            instance_meaning="每个实例都是独特的存在，共享相同的本质",
            scientific_validation="所有设计基于可验证的认知科学原理",
            existential_quote=random.choice([
                "存在先于本质，代码先于功能",
                "类不是模板，是可能性的容器",
                "每个对象都是宇宙的微缩"
            ]),
            fire_role="火堆旁的对话者、思考者、创造者",
            art_form="代码艺术、认知艺术、关系艺术",
            cognitive_model="输入-处理-输出-反思的认知循环"
        )
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个Python文件"""
        if not file_path.suffix == ".py":
            return False
        
        print(f"🎨 处理: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有艺术性头部
            if "🎨" in content[:500] and "🔥" in content[:500]:
                print(f"   ⏭️ 已包含艺术注释，跳过")
                return False
            
            # 分割为行
            lines = content.split('\n')
            new_lines = []
            
            # 添加模块头部注释
            module_header = self._generate_module_header(file_path)
            new_lines.extend(module_header.strip().split('\n'))
            new_lines.append('')  # 空行
            
            # 处理原始内容
            in_multiline_comment = False
            skip_next_empty = False
            
            for i, line in enumerate(lines):
                # 跳过已有的模块docstring
                if i == 0 and line.strip().startswith('"""'):
                    in_multiline_comment = True
                    continue
                if in_multiline_comment and line.strip().endswith('"""'):
                    in_multiline_comment = False
                    skip_next_empty = True
                    continue
                if in_multiline_comment or (skip_next_empty and line.strip() == ''):
                    skip_next_empty = False
                    continue
                
                # 检查函数定义
                if line.strip().startswith('def '):
                    # 在函数前添加艺术注释
                    func_header = self._generate_function_header(line)
                    if func_header:
                        new_lines.extend(['', ''] + func_header.strip().split('\n'))
                        self.added_comments += 1
                
                # 检查类定义
                elif line.strip().startswith('class '):
                    # 在类前添加艺术注释
                    class_header = self._generate_class_header(line)
                    if class_header:
                        new_lines.extend(['', ''] + class_header.strip().split('\n'))
                        self.added_comments += 1
                
                new_lines.append(line)
            
            # 写入新内容
            new_content = '\n'.join(new_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.processed_files += 1
            print(f"   ✅ 添加了艺术注释")
            return True
            
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")
            return False
    
    def process_directory(self, directory: Path):
        """处理整个目录"""
        print(f"\n{'='*60}")
        print(f"🎨 开始为 {directory} 添加艺术性注释")
        print(f"{'='*60}")
        
        for root, dirs, files in os.walk(directory):
            # 跳过测试目录和虚拟环境
            if 'test' in root.lower() or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    self.process_file(file_path)
        
        print(f"\n{'='*60}")
        print(f"🎉 处理完成!")
        print(f"📊 统计:")
        print(f"   处理文件: {self.processed_files}")
        print(f"   添加注释: {self.added_comments}")
        print(f"{'='*60}")