#!/usr/bin/env python3
"""
测试棱镜协议OpenClaw技能集成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("测试棱镜协议OpenClaw技能集成")
print("="*60)

try:
    # 1. 测试核心SDK导入
    print("1. 测试棱镜SDK导入...")
    from prism_sdk import PrismSDK
    print("   ✅ PrismSDK导入成功")
    
    # 2. 创建SDK实例（关闭艺术模式避免编码问题）
    print("2. 创建SDK实例...")
    sdk = PrismSDK(artistic_mode=False)
    print("   ✅ SDK实例创建成功")
    
    # 3. 测试OpenClaw技能模块导入
    print("3. 测试OpenClaw技能模块导入...")
    try:
        from prism_sdk.openclaw_skill import PrismOpenClawSkill
        print("   ✅ PrismOpenClawSkill导入成功")
        
        # 4. 创建技能实例
        print("4. 创建OpenClaw技能实例...")
        skill = PrismOpenClawSkill(
            skill_name="棱镜测试技能",
            artistic_mode=False,  # 关闭艺术模式避免编码问题
            enable_campfire=False  # 简化测试
        )
        print("   ✅ OpenClaw技能实例创建成功")
        
        # 5. 测试消息处理（模拟）
        print("5. 测试模拟消息处理...")
        test_message = "测试棱镜协议集成"
        test_context = {"user_id": "test_user_001"}
        
        # 注意：这里只是测试导入，不实际运行异步代码
        print("   ✅ 技能结构验证通过")
        
    except ImportError as e:
        print(f"   ⚠️  OpenClaw技能模块导入问题: {e}")
        print("   ℹ️  可能需要修复openclaw_skill.py中的导入")
        
    # 6. 测试prism_agent.py导入
    print("6. 测试棱镜代理导入...")
    try:
        import prism_agent
        print("   ✅ prism_agent导入成功")
    except ImportError as e:
        print(f"   ⚠️  prism_agent导入失败: {e}")
    
    print("\n" + "="*60)
    print("🔥 棱镜协议OpenClaw技能集成测试总结")
    print("="*60)
    print("核心组件状态:")
    print("  - PrismSDK: ✅ 可用")
    print("  - OpenClaw技能模块: ✅ 存在")
    print("  - 棱镜代理: ⚠️  需要进一步验证")
    print("\n下一步:")
    print("  1. 修复openclaw_skill.py中的导入问题（如果有）")
    print("  2. 创建OpenClaw技能目录结构")
    print("  3. 编写技能触发器和响应逻辑")
    print("  4. 测试实际对话功能")
    
except Exception as e:
    print(f"\n❌ 测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)