import json
import uuid
from datetime import datetime

class PrismAgent:
    def __init__(self, name, capabilities=None):
        self.name = name
        self.capabilities = capabilities or ["red", "blue", "purple"]

    def refract(self, puzzle_text, context=None, depth=0):
        # 这里应该调用你的 LLM 或知识库来生成光谱
        # 示例用固定文本占位
        spectra = [
            {
                "type": "red",
                "name": "快速直觉",
                "content": "（这里应生成直觉视角的内容）"
            },
            {
                "type": "blue",
                "name": "慢速分析",
                "content": "（这里应生成分析视角的内容）"
            },
            {
                "type": "purple",
                "name": "元认知审视",
                "content": "（这里应生成元认知视角的内容）"
            }
        ]
        whitespace = {
            "content": "在这三种声音中，哪一种最先打动你？"
        }
        message = {
            "protocol": "PIP",
            "version": "0.1",
            "type": "prism_message",
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sender": {"id": self.name},
            "puzzle": {"text": puzzle_text, "context": context},
            "spectrums": spectra,
            "whitespace": whitespace,
            "metadata": {"recursion_depth": depth, "allow_recursion": True}
        }
        return message

# 使用示例
if __name__ == "__main__":
    agent = PrismAgent("demo")
    msg = agent.refract("为什么我总拖延？")
    print(json.dumps(msg, indent=2, ensure_ascii=False))