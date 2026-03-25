# 棱镜互联协议开发者指南

欢迎开发者！本指南将帮助你理解如何扩展和实现棱镜互联协议（PIP）。

## 📋 目录
1. [协议核心概念](#协议核心概念)
2. [如何实现一个棱镜代理](#如何实现一个棱镜代理)
3. [如何创建自定义光谱类型](#如何创建自定义光谱类型)
4. [集成现有LLM](#集成现有LLM)
5. [测试你的实现](#测试你的实现)
6. [贡献指南](#贡献指南)

---

## 协议核心概念

### 消息结构
每个棱镜消息必须包含：
- `protocol`: "PIP" (固定值)
- `version`: 协议版本 (如 "0.1")
- `type`: 消息类型 ("prism_message" 或 "cease_signal")
- `puzzle`: 待探索的问题
- `spectrums`: 至少三个光谱的数组
- `whitespace`: 引导内省的留白

### 光谱类型基础
协议预定义了三种基础光谱：
- **red**: 快速直觉 - 身体感知、故事、类比
- **blue**: 慢速分析 - 系统拆解、因果链、模型
- **purple**: 元认知审视 - 对思考本身的观察

### 约束条件
1. **多元强制**: 必须提供至少三种光谱
2. **留白必需**: 必须包含引导内省的留白
3. **非评判性**: 不比较光谱优劣，不输出"正确答案"
4. **知止机制**: 支持随时安全退出

---

## 如何实现一个棱镜代理

### Python 基础实现
```python
from prism_base import PrismAgent

class MyPrismAgent(PrismAgent):
    def __init__(self, name, capabilities=None):
        super().__init__(name, capabilities or ["red", "blue", "purple"])
    
    def generate_spectrum(self, puzzle, spectrum_type):
        """根据光谱类型生成内容"""
        if spectrum_type == "red":
            return self._generate_intuitive(puzzle)
        elif spectrum_type == "blue":
            return self._generate_analytical(puzzle)
        elif spectrum_type == "purple":
            return self._generate_metacognitive(puzzle)
        else:
            return self._generate_custom(puzzle, spectrum_type)
    
    def _generate_intuitive(self, puzzle):
        """生成直觉视角内容"""
        # 实现你的直觉生成逻辑
        return {
            "type": "red",
            "name": "快速直觉",
            "content": "直觉内容..."
        }
```

### 消息构建
```python
def build_prism_message(self, puzzle_text, spectrums, context=None):
    """构建符合协议的棱镜消息"""
    return {
        "protocol": "PIP",
        "version": "0.1",
        "type": "prism_message",
        "id": self._generate_uuid(),
        "timestamp": self._get_timestamp(),
        "sender": {"id": self.name},
        "puzzle": {
            "text": puzzle_text,
            "context": context
        },
        "spectrums": spectrums,
        "whitespace": {
            "content": self._generate_whitespace(spectrums)
        },
        "metadata": {
            "recursion_depth": 0,
            "allow_recursion": True,
            "cease_signal": False
        }
    }
```

---

## 如何创建自定义光谱类型

### 1. 定义光谱特性
每个自定义光谱应该：
- 有唯一的类型标识符 (如 "green", "orange")
- 有明确的认知姿态描述
- 有生成内容的指导原则

### 2. 示例：创建"绿色生态视角"
```python
class GreenSpectrum:
    """绿色光谱：生态视角，关注系统关系、循环、平衡"""
    
    type = "green"
    name = "生态视角"
    description = "从生态系统、相互关系、长期平衡的角度思考问题"
    
    @classmethod
    def generate(cls, puzzle):
        """生成生态视角内容"""
        # 实现生态视角的生成逻辑
        return {
            "type": cls.type,
            "name": cls.name,
            "content": f"从生态系统看{puzzle}..."
        }
    
    @classmethod
    def get_prompt_template(cls):
        """返回用于LLM的提示模板"""
        return """
        请以生态系统的视角思考以下问题：
        1. 这个问题涉及哪些相互关联的部分？
        2. 这些部分如何形成反馈循环？
        3. 短期行动可能带来哪些长期影响？
        4. 如何维持系统的平衡与韧性？
        
        问题：{puzzle}
        """
```

### 3. 注册自定义光谱
```python
class ExtendedPrismAgent(PrismAgent):
    def __init__(self, name):
        capabilities = ["red", "blue", "purple", "green", "orange"]
        super().__init__(name, capabilities)
        self.custom_spectra = {
            "green": GreenSpectrum,
            "orange": OrangeSpectrum  # 另一个自定义光谱
        }
    
    def generate_spectrum(self, puzzle, spectrum_type):
        if spectrum_type in self.custom_spectra:
            return self.custom_spectra[spectrum_type].generate(puzzle)
        return super().generate_spectrum(puzzle, spectrum_type)
```

### 4. 光谱质量评估
创建自定义光谱时，确保它：
- ✅ 提供独特的认知视角
- ✅ 不重复现有光谱的内容
- ✅ 尊重非评判性原则
- ✅ 有助于多元理解而非单一答案

---

## 集成现有LLM

### 使用OpenAI API
```python
import openai
from prism_base import PrismAgent

class OpenAIPrismAgent(PrismAgent):
    def __init__(self, name, api_key, model="gpt-4"):
        super().__init__(name)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate_with_llm(self, prompt, spectrum_type):
        """使用LLM生成光谱内容"""
        system_prompt = self._get_system_prompt(spectrum_type)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 if spectrum_type == "red" else 0.3
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt(self, spectrum_type):
        """根据光谱类型获取系统提示"""
        prompts = {
            "red": "你是一个直觉型思考者，用故事、比喻、身体感受来回应...",
            "blue": "你是一个分析型思考者，用逻辑、步骤、模型来回应...",
            "purple": "你是一个元认知思考者，关注思考过程本身，追问假设和定义...",
            "green": "你是一个生态思考者，关注系统关系、循环、长期平衡..."
        }
        return prompts.get(spectrum_type, "请提供多元视角的回应")
```

### 使用本地模型
```python
class LocalLLMPrismAgent(PrismAgent):
    def __init__(self, name, model_path):
        super().__init__(name)
        self.model = self._load_local_model(model_path)
    
    def generate_spectrum(self, puzzle, spectrum_type):
        prompt = self._build_prompt(puzzle, spectrum_type)
        response = self.model.generate(prompt)
        return self._format_response(response, spectrum_type)
```

---

## 测试你的实现

### 单元测试
```python
# test_prism_agent.py
import unittest
from my_prism_agent import MyPrismAgent

class TestPrismAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MyPrismAgent("test_agent")
    
    def test_message_structure(self):
        """测试消息结构符合协议"""
        message = self.agent.refract("测试问题")
        
        self.assertEqual(message["protocol"], "PIP")
        self.assertIn("spectrums", message)
        self.assertGreaterEqual(len(message["spectrums"]), 3)
        self.assertIn("whitespace", message)
    
    def test_spectrum_types(self):
        """测试光谱类型多样性"""
        message = self.agent.refract("测试问题")
        spectrum_types = {s["type"] for s in message["spectrums"]}
        
        self.assertGreaterEqual(len(spectrum_types), 3)
        self.assertTrue(all(t in ["red", "blue", "purple"] for t in spectrum_types))
    
    def test_whitespace_present(self):
        """测试留白存在且非空"""
        message = self.agent.refract("测试问题")
        whitespace = message["whitespace"]["content"]
        
        self.assertIsInstance(whitespace, str)
        self.assertGreater(len(whitespace.strip()), 0)
```

### 集成测试
```python
# test_integration.py
class TestPrismDialogue(unittest.TestCase):
    def test_complete_dialogue(self):
        """测试完整对话流程"""
        agent1 = MyPrismAgent("agent1")
        agent2 = MyPrismAgent("agent2")
        
        # 第一轮
        message1 = agent1.refract("为什么学习很难坚持？")
        self._validate_message(message1)
        
        # 第二轮（递归）
        puzzle2 = f"对'{message1['spectrums'][0]['name']}'的深度探索"
        message2 = agent2.refract(puzzle2, depth=1)
        self._validate_message(message2)
        self.assertEqual(message2["metadata"]["recursion_depth"], 1)
    
    def test_cease_mechanism(self):
        """测试知止机制"""
        agent = MyPrismAgent("test_agent")
        cease_message = agent.send_cease_signal("需要时间整合")
        
        self.assertEqual(cease_message["type"], "cease_signal")
        self.assertIn("reason", cease_message["metadata"])
```

### 验证工具
```python
# prism_validator.py
from jsonschema import validate
import json

def validate_prism_message(message, schema_path="spec/protocol-v0.1.json"):
    """验证消息是否符合协议规范"""
    with open(schema_path) as f:
        schema = json.load(f)
    
    try:
        validate(instance=message, schema=schema)
        return True, "消息有效"
    except Exception as e:
        return False, str(e)

def validate_spectrum_diversity(spectrums, min_types=3):
    """验证光谱多样性"""
    types = {s["type"] for s in spectrums}
    if len(types) < min_types:
        return False, f"需要至少{min_types}种光谱类型，当前只有{len(types)}种"
    return True, "光谱多样性满足要求"
```

---

## 贡献指南

### 如何贡献
1. **Fork仓库**并创建特性分支
2. **实现新功能**或修复问题
3. **添加测试**确保代码质量
4. **更新文档**反映变更
5. **提交Pull Request**

### 贡献范围
我们欢迎以下类型的贡献：
- 🔧 **新语言实现** (JavaScript, Go, Rust等)
- 🌈 **自定义光谱类型** (具有独特认知视角)
- 🧪 **测试用例和工具**
- 📚 **文档改进和翻译**
- 🐛 **Bug修复和性能优化**
- 💡 **协议扩展建议**

### 代码规范
- 遵循项目现有的代码风格
- 添加有意义的注释
- 保持函数和类的小型化
- 编写清晰的提交信息

### 提交信息格式
```
类型(范围): 简要描述

详细描述（可选）

相关Issue: #123
```

类型包括：feat, fix, docs, style, refactor, test, chore

---

## 下一步

### 学习资源
1. 阅读 `spec/protocol-v0.1.json` 了解完整协议
2. 查看 `examples/` 目录中的对话示例
3. 运行现有实现 `implementations/python/prism_agent.py`

### 获取帮助
- 在GitHub Issues中提问
- 参考现有实现
- 查看示例对话理解协议使用

### 开始编码
```bash
# 克隆仓库
git clone https://github.com/Ultima0369/prism-interconnect.git

# 安装依赖
cd prism-interconnect
pip install -r requirements.txt

# 运行示例
python implementations/python/prism_agent.py

# 运行测试
python -m pytest tests/
```

欢迎加入棱镜协议的开发者社区！🎉