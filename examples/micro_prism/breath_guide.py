#!/usr/bin/env python3
"""
🌬️ 三秒呼吸引导工具
极简的认知间隙创造工具
"""

import time
import sys
import argparse
from datetime import datetime
from typing import Optional, Dict, List
import json
import os


class BreathGuide:
    """呼吸引导器"""
    
    def __init__(self, session_name: str = "默认会话"):
        """初始化呼吸引导器
        
        Args:
            session_name: 会话名称
        """
        self.session_name = session_name
        self.start_time = None
        self.end_time = None
        self.breath_patterns = {
            "basic": {"inhale": 3, "hold": 2, "exhale": 4, "name": "基础版 (3-2-4)"},
            "relax": {"inhale": 4, "hold": 7, "exhale": 8, "name": "放松版 (4-7-8)"},
            "focus": {"inhale": 4, "hold": 4, "exhale": 4, "hold2": 4, "name": "专注版 (盒式呼吸)"},
            "quick": {"inhale": 2, "hold": 1, "exhale": 3, "name": "快速版 (2-1-3)"},
        }
        
        # 会话记录
        self.session_data = {
            "session_name": session_name,
            "start_time": None,
            "end_time": None,
            "pattern_used": None,
            "duration_seconds": 0,
            "breath_count": 0,
            "user_notes": "",
            "pre_mood": None,
            "post_mood": None,
        }
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """显示标题"""
        print("\n" + "="*60)
        print(" " * 20 + "🌬️ 三秒呼吸练习")
        print("="*60)
        print("🧠 认知间隙创造工具 · 极简棱镜体验")
        print("-"*60)
    
    def select_pattern(self) -> Dict:
        """选择呼吸模式"""
        print("\n请选择呼吸模式：")
        for i, (key, pattern) in enumerate(self.breath_patterns.items(), 1):
            print(f"{i}. {pattern['name']}")
        
        while True:
            try:
                choice = input(f"\n选择 (1-{len(self.breath_patterns)}，默认1): ").strip()
                if choice == "":
                    choice = "1"
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.breath_patterns):
                    pattern_key = list(self.breath_patterns.keys())[choice_idx]
                    return self.breath_patterns[pattern_key]
                else:
                    print("❌ 请输入有效选项")
            except ValueError:
                print("❌ 请输入数字")
    
    def collect_pre_session_info(self):
        """收集练习前信息"""
        print("\n📝 练习前记录（可选）")
        print("-"*40)
        
        # 情绪状态
        moods = ["平静", "焦虑", "兴奋", "疲惫", "专注", "分心", "其他"]
        print("当前情绪状态：")
        for i, mood in enumerate(moods, 1):
            print(f"{i}. {mood}")
        
        mood_choice = input("选择情绪（可选，按回车跳过）: ").strip()
        if mood_choice and mood_choice.isdigit():
            idx = int(mood_choice) - 1
            if 0 <= idx < len(moods):
                self.session_data["pre_mood"] = moods[idx]
        
        # 主要困扰
        concern = input("主要困扰或想法（可选）: ").strip()
        if concern:
            self.session_data["user_notes"] += f"练习前困扰: {concern}\n"
    
    def guide_breath(self, pattern: Dict, cycles: int = 3):
        """引导呼吸练习
        
        Args:
            pattern: 呼吸模式
            cycles: 循环次数
        """
        print(f"\n🚀 开始 {pattern['name']} 呼吸练习")
        print(f"循环次数: {cycles} 次")
        print("准备好后按回车开始...")
        input()
        
        self.clear_screen()
        self.session_data["pattern_used"] = pattern["name"]
        self.session_data["start_time"] = datetime.now().isoformat()
        self.start_time = time.time()
        
        for cycle in range(1, cycles + 1):
            print(f"\n{'='*50}")
            print(f"第 {cycle}/{cycles} 循环")
            print(f"{'='*50}\n")
            
            # 吸气阶段
            if "inhale" in pattern:
                print(f"🌬️ 吸气... {pattern['inhale']}秒")
                for i in range(pattern["inhale"], 0, -1):
                    print(f"  {i}...", end="\r")
                    time.sleep(1)
                print(" " * 20, end="\r")
            
            # 第一次屏息
            if "hold" in pattern:
                print(f"⏸️  屏息... {pattern['hold']}秒")
                for i in range(pattern["hold"], 0, -1):
                    print(f"  {i}...", end="\r")
                    time.sleep(1)
                print(" " * 20, end="\r")
            
            # 呼气阶段
            if "exhale" in pattern:
                print(f"💨 呼气... {pattern['exhale']}秒")
                for i in range(pattern["exhale"], 0, -1):
                    print(f"  {i}...", end="\r")
                    time.sleep(1)
                print(" " * 20, end="\r")
            
            # 第二次屏息（盒式呼吸）
            if "hold2" in pattern:
                print(f"⏸️  屏息... {pattern['hold2']}秒")
                for i in range(pattern["hold2"], 0, -1):
                    print(f"  {i}...", end="\r")
                    time.sleep(1)
                print(" " * 20, end="\r")
            
            self.session_data["breath_count"] += 1
            
            # 循环间休息
            if cycle < cycles:
                print("\n🔄 准备下一个循环...")
                time.sleep(2)
        
        self.end_time = time.time()
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["duration_seconds"] = int(self.end_time - self.start_time)
        
        print(f"\n{'='*50}")
        print("🎉 练习完成！")
        print(f"{'='*50}")
    
    def collect_post_session_info(self):
        """收集练习后信息"""
        print("\n📝 练习后感受（可选）")
        print("-"*40)
        
        # 情绪变化
        mood_changes = ["更平静", "更清晰", "更放松", "更专注", "变化不大", "其他"]
        print("情绪变化：")
        for i, change in enumerate(mood_changes, 1):
            print(f"{i}. {change}")
        
        mood_choice = input("选择情绪变化（可选）: ").strip()
        if mood_choice and mood_choice.isdigit():
            idx = int(mood_choice) - 1
            if 0 <= idx < len(mood_changes):
                self.session_data["post_mood"] = mood_changes[idx]
        
        # 新出现的想法
        new_thoughts = input("新出现的想法或感受: ").strip()
        if new_thoughts:
            self.session_data["user_notes"] += f"练习后想法: {new_thoughts}\n"
        
        # 身体感受
        body_feelings = input("身体感受变化: ").strip()
        if body_feelings:
            self.session_data["user_notes"] += f"身体感受: {body_feelings}\n"
    
    def show_summary(self):
        """显示练习总结"""
        print("\n" + "="*60)
        print("📊 练习总结")
        print("="*60)
        
        print(f"会话名称: {self.session_data['session_name']}")
        print(f"呼吸模式: {self.session_data['pattern_used']}")
        print(f"开始时间: {self.session_data['start_time']}")
        print(f"结束时间: {self.session_data['end_time']}")
        print(f"持续时间: {self.session_data['duration_seconds']} 秒")
        print(f"呼吸循环: {self.session_data['breath_count']} 次")
        
        if self.session_data["pre_mood"]:
            print(f"练习前情绪: {self.session_data['pre_mood']}")
        
        if self.session_data["post_mood"]:
            print(f"练习后情绪: {self.session_data['post_mood']}")
        
        if self.session_data["user_notes"]:
            print(f"\n📝 记录:")
            print(self.session_data["user_notes"])
        
        print("\n🧠 神经科学提示:")
        print("- 刚才的呼吸练习改变了你的大脑状态")
        print("- 前额叶皮层活动增强，自动化思维减少")
        print("- 这种状态最适合深度思考或重要决策")
        print("- 建议在需要清晰思考时进行呼吸练习")
    
    def save_session(self, filename: Optional[str] = None):
        """保存会话记录"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"breath_session_{timestamp}.json"
        
        # 确保目录存在
        os.makedirs("sessions", exist_ok=True)
        filepath = os.path.join("sessions", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 会话记录已保存到: {filepath}")
        return filepath
    
    def start_session(self, pattern: Optional[Dict] = None, cycles: int = 3):
        """开始完整的呼吸会话
        
        Args:
            pattern: 呼吸模式，如果为None则让用户选择
            cycles: 循环次数
        """
        try:
            self.clear_screen()
            self.display_header()
            
            # 收集练习前信息
            self.collect_pre_session_info()
            
            # 选择呼吸模式
            if pattern is None:
                pattern = self.select_pattern()
            
            # 引导呼吸练习
            self.guide_breath(pattern, cycles)
            
            # 收集练习后信息
            self.collect_post_session_info()
            
            # 显示总结
            self.show_summary()
            
            # 保存记录
            save_choice = input("\n💾 是否保存会话记录？ (y/n, 默认y): ").strip().lower()
            if save_choice != "n":
                self.save_session()
            
            # 下一步建议
            print("\n" + "="*60)
            print("🎯 下一步建议")
            print("="*60)
            print("1. 🧠 立即进行重要思考或决策")
            print("2. 📝 记录刚才浮现的想法")
            print("3. 🔄 再练习一次巩固效果")
            print("4. 🔥 体验完整棱镜对话")
            print("5. 💤 休息一下，让大脑整合")
            
            print(f"\n🔥 感谢使用三秒呼吸练习！")
            print("   欢迎在火堆旁分享你的体验。")
            
        except KeyboardInterrupt:
            print("\n\n⏹️  练习中断")
            print("感谢使用，下次再见！")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print("请重试或反馈问题")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="🌬️ 三秒呼吸引导工具")
    parser.add_argument("--pattern", choices=["basic", "relax", "focus", "quick"], 
                       default="basic", help="呼吸模式")
    parser.add_argument("--cycles", type=int, default=3, help="循环次数")
    parser.add_argument("--name", type=str, default="命令行会话", help="会话名称")
    parser.add_argument("--quick", action="store_true", help="快速模式，跳过信息收集")
    
    args = parser.parse_args()
    
    # 创建引导器
    guide = BreathGuide(session_name=args.name)
    
    if args.quick:
        # 快速模式，直接开始
        pattern = guide.breath_patterns[args.pattern]
        guide.guide_breath(pattern, args.cycles)
        guide.show_summary()
    else:
        # 完整模式
        pattern = guide.breath_patterns[args.pattern]
        guide.start_session(pattern=pattern, cycles=args.cycles)


if __name__ == "__main__":
    main()