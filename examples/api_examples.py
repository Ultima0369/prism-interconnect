#!/usr/bin/env python3
"""
🎯 棱镜协议API使用示例
展示各种API的使用方法和最佳实践
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys

# 添加项目路径
sys.path.insert(0, "implementations/python")

from prism_sdk import PrismClient, PrismResponse, Spectrum, Whitespace, Synthesis


class APIExamples:
    """API使用示例类"""
    
    def __init__(self):
        self.client = None
        
    async def setup_client(self):
        """设置客户端"""
        print("🔧 设置棱镜协议客户端...")
        
        # 创建客户端
        self.client = PrismClient(
            # 生产环境使用以下配置
            # api_key="your-api-key",
            # base_url="https://api.prism.dev",
            
            # 开发环境配置
            base_url="http://localhost:8000",
            timeout=60,
            logging_level="INFO",
            cache_enabled=True,
            cache_ttl=300
        )
        
        print("✅ 客户端设置完成")
        return self.client
    
    async def example_basic_dialogue(self):
        """示例1: 基础对话"""
        print("\n" + "="*60)
        print("🎯 示例1: 基础棱镜对话")
        print("="*60)
        
        query = "如何平衡工作与生活？"
        print(f"问题: {query}")
        
        # 执行对话
        response = await self.client.prismatic_dialogue(
            query=query,
            max_depth=3,
            whitespace_duration=30  # 示例中缩短留白时间
        )
        
        # 显示结果
        print(f"\n📊 对话完成!")
        print(f"处理时间: {response.duration:.2f}秒")
        print(f"总体置信度: {response.confidence:.2%}")
        
        # 显示光谱结果
        print(f"\n🌈 光谱分析:")
        for color, spectrum in response.spectra.items():
            color_name = {
                "red": "🔥 红色光谱（直觉）",
                "blue": "🔵 蓝色光谱（分析）",
                "purple": "🟣 紫色光谱（元认知）"
            }[color]
            
            print(f"\n{color_name}:")
            print(f"  内容: {spectrum.content[:100]}...")
            print(f"  置信度: {spectrum.confidence:.2%}")
        
        # 显示留白洞见
        print(f"\n⏸️ 留白洞见:")
        for i, insight in enumerate(response.whitespace.insights, 1):
            print(f"  {i}. {insight}")
        
        # 显示综合视角
        print(f"\n🎯 综合视角:")
        print(f"  {response.synthesis.integrated_view[:150]}...")
        
        print(f"\n🔮 新问题:")
        for i, question in enumerate(response.synthesis.new_questions, 1):
            print(f"  {i}. {question}")
        
        return response
    
    async def example_advanced_analysis(self):
        """示例2: 高级分析"""
        print("\n" + "="*60)
        print("🎯 示例2: 高级光谱分析")
        print("="*60)
        
        query = "人工智能会改变人类认知吗？"
        print(f"复杂问题: {query}")
        
        # 深度光谱分析
        spectra_results = await self.client.analyze_spectra(
            query=query,
            spectra=["red", "blue", "purple"],
            depth=3,
            include_confidence=True,
            include_reasoning=True
        )
        
        print(f"\n🔍 深度分析完成!")
        
        # 显示详细分析
        for color, analysis in spectra_results.items():
            color_name = {
                "red": "🔥 红色光谱",
                "blue": "🔵 蓝色光谱",
                "purple": "🟣 紫色光谱"
            }[color]
            
            print(f"\n{color_name}分析:")
            print(f"  内容: {analysis['content'][:120]}...")
            print(f"  置信度: {analysis.get('confidence', 0):.2%}")
            
            if analysis.get('reasoning'):
                print(f"  推理过程: {analysis['reasoning'][:80]}...")
            
            if analysis.get('key_points'):
                print(f"  关键点:")
                for point in analysis['key_points'][:3]:
                    print(f"    • {point}")
        
        return spectra_results
    
    async def example_whitespace_experience(self):
        """示例3: 留白体验"""
        print("\n" + "="*60)
        print("🎯 示例3: 深度留白体验")
        print("="*60)
        
        # 准备初始洞见
        initial_insights = [
            "工作与生活的平衡不是时间分配，而是能量管理",
            "真正的平衡来自内在的和谐，而非外在的安排",
            "不同人生阶段需要不同的平衡策略"
        ]
        
        print("初始洞见:")
        for insight in initial_insights:
            print(f"  • {insight}")
        
        # 体验留白
        print(f"\n⏸️ 开始60秒留白体验...")
        whitespace = await self.client.experience_whitespace(
            insights=initial_insights,
            duration=60,
            prompts=[
                "这些洞见之间有什么联系？",
                "它们如何应用到我的具体情境中？",
                "我还需要考虑哪些因素？"
            ],
            include_timer=True
        )
        
        print(f"\n💡 留白完成!")
        print(f"时长: {whitespace.duration}秒")
        print(f"涌现洞见:")
        
        for i, insight in enumerate(whitespace.insights, 1):
            print(f"  {i}. {insight}")
        
        return whitespace
    
    async def example_synthesis_techniques(self):
        """示例4: 合成技术"""
        print("\n" + "="*60)
        print("🎯 示例4: 多元视角合成")
        print("="*60)
        
        # 模拟不同视角的分析结果
        perspectives = [
            {
                "source": "直觉视角",
                "content": "这个问题本质上是关于内在和谐",
                "confidence": 0.85
            },
            {
                "source": "逻辑视角", 
                "content": "需要系统分析时间分配和优先级",
                "confidence": 0.92
            },
            {
                "source": "元认知视角",
                "content": "我们正在用二分法思考一个连续谱问题",
                "confidence": 0.78
            }
        ]
        
        print("多元视角:")
        for perspective in perspectives:
            print(f"  • {perspective['source']}: {perspective['content']}")
        
        # 使用不同合成方法
        synthesis_methods = ["integrated", "hierarchical", "emergent"]
        
        for method in synthesis_methods:
            print(f"\n🔮 {method}合成方法:")
            
            synthesis = await self.client.synthesize_perspectives(
                spectra_results=perspectives,
                synthesis_method=method,
                include_new_questions=True,
                include_confidence=True
            )
            
            print(f"  整合视角: {synthesis['integrated_view'][:100]}...")
            print(f"  置信度: {synthesis.get('confidence', 0):.2%}")
            
            if synthesis.get('new_questions'):
                print(f"  新问题:")
                for question in synthesis['new_questions'][:2]:
                    print(f"    • {question}")
        
        return synthesis_methods
    
    async def example_session_management(self):
        """示例5: 会话管理"""
        print("\n" + "="*60)
        print("🎯 示例5: 连续对话会话")
        print("="*60)
        
        # 创建会话
        print("创建新会话...")
        session = await self.client.create_session(
            user_id="example_user",
            context="个人成长对话",
            metadata={
                "goal": "探索自我认知",
                "topic": "工作与生活平衡"
            }
        )
        
        print(f"会话ID: {session['id']}")
        print(f"创建时间: {session['created_at']}")
        
        # 第一次对话
        print(f"\n第一次对话...")
        response1 = await self.client.prismatic_dialogue(
            query="如何找到工作的意义？",
            session_id=session['id'],
            max_depth=2
        )
        
        print(f"响应1: {response1.synthesis.integrated_view[:80]}...")
        
        # 继续对话
        print(f"\n继续对话...")
        response2 = await self.client.continue_session(
            session_id=session['id'],
            query="基于刚才的讨论，如何将意义转化为日常动力？",
            previous_response=response1
        )
        
        print(f"响应2: {response2.synthesis.integrated_view[:80]}...")
        
        # 获取会话历史
        print(f"\n获取会话历史...")
        history = await self.client.get_session_history(
            session_id=session['id'],
            limit=10
        )
        
        print(f"历史记录数: {len(history)}")
        for i, record in enumerate(history[:3], 1):
            print(f"  {i}. {record['query'][:50]}...")
        
        # 结束会话
        print(f"\n结束会话...")
        await self.client.end_session(session_id=session['id'])
        print("✅ 会话已结束")
        
        return session
    
    async def example_batch_processing(self):
        """示例6: 批量处理"""
        print("\n" + "="*60)
        print("🎯 示例6: 批量问题分析")
        print("="*60)
        
        # 批量问题
        questions = [
            "什么是真正的幸福？",
            "如何培养深度思考能力？",
            "科技发展如何影响人际关系？",
            "什么是有效的沟通？",
            "如何面对失败和挫折？"
        ]
        
        print(f"批量分析{len(questions)}个问题:")
        for q in questions:
            print(f"  • {q}")
        
        # 批量处理
        print(f"\n🚀 开始批量处理...")
        batch_results = await self.client.batch_prismatic_dialogue(
            queries=questions,
            max_depth=2,
            whitespace_duration=20,  # 批量处理缩短留白时间
            concurrency=2  # 并发数
        )
        
        print(f"\n✅ 批量处理完成!")
        print(f"成功: {len([r for r in batch_results if r])}/{len(questions)}")
        
        # 显示结果摘要
        for i, (question, result) in enumerate(zip(questions, batch_results), 1):
            if result:
                print(f"\n{i}. {question}")
                print(f"   综合视角: {result.synthesis.integrated_view[:60]}...")
                print(f"   置信度: {result.confidence:.2%}")
        
        return batch_results
    
    async def example_custom_configurations(self):
        """示例7: 自定义配置"""
        print("\n" + "="*60)
        print("🎯 示例7: 自定义分析配置")
        print("="*60)
        
        # 创建自定义配置
        print("创建自定义配置...")
        config = await self.client.create_configuration(
            name="哲学深度分析配置",
            parameters={
                "max_depth": 5,
                "whitespace_duration": 90,
                "temperature": 0.8,
                "spectra_weights": {
                    "red": 0.25,    # 降低直觉权重
                    "blue": 0.35,   # 提高分析权重
                    "purple": 0.40  # 提高元认知权重
                },
                "synthesis_method": "emergent",
                "include_detailed_reasoning": True
            },
            description="用于深度哲学问题的分析配置"
        )
        
        print(f"配置ID: {config['id']}")
        print(f"配置名称: {config['name']}")
        
        # 使用自定义配置
        print(f"\n使用自定义配置进行分析...")
        response = await self.client.prismatic_dialogue(
            query="生命的意义是什么？",
            config_id=config['id']
        )
        
        print(f"分析完成!")
        print(f"使用配置: {config['name']}")
        print(f"光谱权重: {config['parameters']['spectra_weights']}")
        
        # 显示加权结果
        print(f"\n加权光谱分析:")
        for color, spectrum in response.spectra.items():
            weight = config['parameters']['spectra_weights'].get(color, 0.33)
            weighted_confidence = spectrum.confidence * weight
            
            color_name = {
                "red": "🔥 红色光谱",
                "blue": "🔵 蓝色光谱",
                "purple": "🟣 紫色光谱"
            }[color]
            
            print(f"  {color_name}:")
            print(f"    原始置信度: {spectrum.confidence:.2%}")
            print(f"    权重: {weight:.2%}")
            print(f"    加权置信度: {weighted_confidence:.2%}")
        
        return config
    
    async def example_error_handling(self):
        """示例8: 错误处理"""
        print("\n" + "="*60)
        print("🎯 示例8: 健壮的错误处理")
        print("="*60)
        
        error_cases = [
            {
                "query": "",  # 空查询
                "expected_error": "查询不能为空"
            },
            {
                "query": "a" * 1001,  # 超长查询
                "expected_error": "查询过长"
            },
            {
                "query": "正常问题",
                "max_depth": 10,  # 超出范围
                "expected_error": "深度超出范围"
            }
        ]
        
        print("测试错误处理场景:")
        
        for i, case in enumerate(error_cases, 1):
            print(f"\n{i}. 测试: {case['expected_error']}")
            print(f"   查询: {case['query'][:50] if case['query'] else '(空)'}")
            
            try:
                response = await self.client.prismatic_dialogue(
                    query=case['query'],
                    max_depth=case.get('max_depth', 3)
                )
                print(f"   ❌ 预期错误但成功返回")
            except Exception as e:
                print(f"   ✅ 正确捕获错误: {str(e)[:80]}...")
        
        # 测试重试机制
        print(f"\n测试重试机制...")
        try:
            # 模拟网络问题
            original_timeout = self.client.timeout
            self.client.timeout = 1  # 设置极短超时
            
            response = await self.client.prismatic_dialogue(
                query="测试重试的问题",
                max_depth=1
            )
            print(f"   ❌ 预期超时但成功返回")
        except Exception as e:
            print(f"   ✅ 超时错误: {str(e)[:80]}...")
        finally:
            self.client.timeout = original_timeout  # 恢复超时
        
        return error_cases
    
    async def example_performance_monitoring(self):
        """示例9: 性能监控"""
        print("\n" + "="*60)
        print("🎯 示例9: 性能分析和监控")
        print("="*60)
        
        # 性能测试
        test_queries = [
            "简单问题测试",
            "中等复杂度问题需要更多分析",
            "这是一个相当复杂的哲学问题需要深度思考和分析"
        ]
        
        performance_results = []
        
        print("运行性能测试...")
        for query in test_queries:
            start_time = datetime.now()
            
            response = await self.client.prismatic_dialogue(
                query=query,
                max_depth=2,
                whitespace_duration=10  # 测试中缩短留白
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            performance_results.append({
                "query_length": len(query),
                "response_length": len(str(response)),
                "duration": duration,
                "confidence": response.confidence
            })
            
            print(f"  查询: '{query[:30]}...'")
            print(f"    长度: {len(query)} 字符")
            print(f"    耗时: {duration:.2f} 秒")
            print(f"    置信度: {response.confidence:.2%}")
        
        # 分析性能数据
        print(f"\n📊 性能分析:")
        avg_duration = sum(r["duration"] for r in performance_results) / len(performance_results)
        avg_confidence = sum(r["confidence"] for r in performance_results) / len(performance_results)
        
        print(f"  平均耗时: {avg_duration:.2f} 秒")
        print(f"  平均置信度: {avg_confidence:.2%}")
        print(f"  查询长度范围: {min(r['query_length'] for r in performance_results)}"
              f" - {max(r['query_length'] for r in performance_results)} 字符")
        
        return performance_results
    
    async def example_integration_scenarios(self):
        """示例10: 集成场景"""
        print("\n" + "="*60)
        print("🎯 示例10: 实际集成场景")
        print("="*60)
        
        integration_scenarios = [
            {
                "name": "个人日记集成",
                "description": "将棱镜协议集成到个人日记应用中",
                "use_case": "每日反思和洞见提取"
            },
            {
                "name": "教育平台集成",
                "description": "在在线教育平台中集成思考训练",
                "use_case": "学生思维训练和作业辅导"
            },
            {
                "name": "团队协作工具集成",
                "