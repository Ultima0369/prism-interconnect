#!/usr/bin/env python3
"""
🎯 棱镜协议完整使用示例
展示从基础到高级的各种使用场景
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "implementations", "python"))

try:
    from prism_sdk import PrismClient, PrismResponse
except ImportError:
    print("❌ 无法导入prism_sdk，请先安装")
    print("运行: pip install -e implementations/python/[dev]")
    sys.exit(1)


class CompleteExamples:
    """完整示例集合"""
    
    def __init__(self):
        self.client = None
        self.results = {}
        
    async def setup(self):
        """设置环境"""
        print("🦞 棱镜协议完整示例集合")
        print("="*60)
        
        # 创建客户端
        self.client = PrismClient(
            base_url="http://localhost:8000",  # 开发环境
            timeout=120,
            logging_level="INFO"
        )
        
        print("✅ 客户端初始化完成")
        return True
    
    async def run_all_examples(self):
        """运行所有示例"""
        examples = [
            self.example_personal_reflection,
            self.example_educational_use,
            self.example_team_decision,
            self.example_research_analysis,
            self.example_creative_writing,
            self.example_problem_solving,
            self.example_learning_journal,
            self.example_career_planning,
            self.example_relationship_advice,
            self.example_philosophical_inquiry
        ]
        
        print(f"\n🚀 开始运行 {len(examples)} 个完整示例")
        print("="*60)
        
        for i, example_func in enumerate(examples, 1):
            print(f"\n🎯 示例 {i}/{len(examples)}: {example_func.__name__.replace('example_', '').replace('_', ' ').title()}")
            print("-"*40)
            
            try:
                result = await example_func()
                self.results[example_func.__name__] = {
                    "success": True,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
                print(f"✅ 示例完成")
            except Exception as e:
                print(f"❌ 示例失败: {e}")
                self.results[example_func.__name__] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            
            # 短暂暂停
            await asyncio.sleep(1)
        
        print(f"\n🎉 所有示例运行完成!")
        return self.results
    
    async def example_personal_reflection(self):
        """示例1: 个人反思日记"""
        print("场景: 个人深度反思和成长")
        
        # 创建反思会话
        session = await self.client.create_session(
            user_id="personal_reflection_001",
            context="2026年3月个人成长反思",
            metadata={
                "goal": "提升自我认知",
                "frequency": "weekly",
                "focus_areas": ["工作", "健康", "关系", "学习"]
            }
        )
        
        session_id = session.get("id")
        
        # 反思问题序列
        reflection_questions = [
            "过去一周，我最自豪的成就是什么？为什么？",
            "我在哪些方面遇到了挑战？如何应对的？",
            "从这些经历中，我学到了什么关于自己的事情？",
            "下周我希望在哪些方面有所改进？",
            "为了成为更好的自己，我需要培养什么习惯？"
        ]
        
        reflections = []
        
        for i, question in enumerate(reflection_questions, 1):
            print(f"\n  🔍 反思问题 {i}: {question}")
            
            response = await self.client.prismatic_dialogue(
                query=question,
                session_id=session_id,
                max_depth=3,
                whitespace_duration=30,
                metadata={"question_type": "weekly_reflection"}
            )
            
            reflection = {
                "question": question,
                "insights": response.whitespace.insights,
                "synthesis": response.synthesis.integrated_view,
                "new_questions": response.synthesis.new_questions,
                "timestamp": datetime.now().isoformat()
            }
            
            reflections.append(reflection)
            
            print(f"    洞见: {', '.join(response.whitespace.insights[:2])}")
            print(f"    综合: {response.synthesis.integrated_view[:80]}...")
        
        # 周度总结
        print(f"\n  📊 周度反思总结")
        summary_query = "基于这周的反思，总结我的主要成长和需要改进的地方"
        
        summary_response = await self.client.prismatic_dialogue(
            query=summary_query,
            session_id=session_id,
            max_depth=4,
            whitespace_duration=45
        )
        
        weekly_summary = {
            "total_reflections": len(reflections),
            "main_insights": summary_response.whitespace.insights,
            "growth_areas": summary_response.synthesis.new_questions,
            "overall_synthesis": summary_response.synthesis.integrated_view,
            "confidence": summary_response.confidence
        }
        
        # 结束会话
        await self.client.end_session(session_id)
        
        result = {
            "session": session,
            "reflections": reflections,
            "weekly_summary": weekly_summary
        }
        
        print(f"  ✅ 完成 {len(reflections)} 个反思问题")
        print(f"  📈 总体置信度: {weekly_summary['confidence']:.2%}")
        
        return result
    
    async def example_educational_use(self):
        """示例2: 教育场景应用"""
        print("场景: 课堂讨论和思维训练")
        
        # 教育主题
        educational_topics = [
            {
                "subject": "历史",
                "question": "第二次世界大战对现代世界格局的影响是什么？",
                "learning_objectives": ["因果分析", "多视角思考", "历史意义评估"]
            },
            {
                "subject": "科学",
                "question": "气候变化的主要科学证据和应对策略是什么？",
                "learning_objectives": ["证据评估", "系统思考", "解决方案设计"]
            },
            {
                "subject": "文学",
                "question": "《红楼梦》中贾宝玉的人物形象和象征意义是什么？",
                "learning_objectives": ["文本分析", "象征解读", "文化理解"]
            }
        ]
        
        lesson_plans = []
        
        for topic in educational_topics:
            print(f"\n  📚 学科: {topic['subject']}")
            print(f"    问题: {topic['question']}")
            print(f"    学习目标: {', '.join(topic['learning_objectives'])}")
            
            # 教师视角分析
            teacher_response = await self.client.prismatic_dialogue(
                query=f"从教师角度分析: {topic['question']}",
                max_depth=4,
                metadata={
                    "role": "teacher",
                    "subject": topic['subject'],
                    "objectives": topic['learning_objectives']
                }
            )
            
            # 学生可能视角
            student_perspectives = []
            student_roles = ["初学者", "进阶学生", "批判性思考者"]
            
            for role in student_roles:
                student_query = f"从{role}的角度思考: {topic['question']}"
                
                student_response = await self.client.prismatic_dialogue(
                    query=student_query,
                    max_depth=3,
                    metadata={"role": role}
                )
                
                student_perspectives.append({
                    "role": role,
                    "insights": student_response.whitespace.insights,
                    "synthesis": student_response.synthesis.integrated_view
                })
            
            # 教学设计
            teaching_design = await self.client.synthesize_perspectives(
                spectra_results=[
                    {"source": "教师分析", "content": teacher_response.synthesis.integrated_view},
                    {"source": "学生视角", "content": "多种学生视角需要考虑"}
                ],
                whitespace_insights=teacher_response.whitespace.insights,
                synthesis_method="integrated"
            )
            
            lesson_plan = {
                "topic": topic,
                "teacher_analysis": {
                    "insights": teacher_response.whitespace.insights,
                    "synthesis": teacher_response.synthesis.integrated_view
                },
                "student_perspectives": student_perspectives,
                "teaching_design": teaching_design,
                "discussion_questions": teacher_response.synthesis.new_questions
            }
            
            lesson_plans.append(lesson_plan)
            
            print(f"    生成 {len(student_perspectives)} 个学生视角")
            print(f"    设计 {len(teacher_response.synthesis.new_questions)} 个讨论问题")
        
        result = {
            "lesson_plans": lesson_plans,
            "total_topics": len(educational_topics),
            "generated_questions": sum(len(p['discussion_questions']) for p in lesson_plans)
        }
        
        print(f"\n  ✅ 完成 {len(lesson_plans)} 个课程设计")
        return result
    
    async def example_team_decision(self):
        """示例3: 团队决策支持"""
        print("场景: 团队重要决策分析")
        
        # 模拟团队决策场景
        decision_scenario = {
            "problem": "是否应该将产品定价提高20%？",
            "stakeholders": ["产品经理", "销售总监", "市场分析师", "客户代表"],
            "criteria": ["收入影响", "客户接受度", "竞争反应", "长期价值"],
            "timeframe": "季度决策"
        }
        
        print(f"  决策问题: {decision_scenario['problem']}")
        print(f"  相关方: {', '.join(decision_scenario['stakeholders'])}")
        print(f"  评估标准: {', '.join(decision_scenario['criteria'])}")
        
        # 各相关方分析
        stakeholder_analyses = []
        
        for stakeholder in decision_scenario['stakeholders']:
            print(f"\n    👤 {stakeholder}视角分析...")
            
            query = f"作为{stakeholder}，分析{decision_scenario['problem']}，考虑{', '.join(decision_scenario['criteria'])}"
            
            response = await self.client.prismatic_dialogue(
                query=query,
                max_depth=4,
                whitespace_duration=40,
                metadata={
                    "stakeholder": stakeholder,
                    "decision_context": decision_scenario
                }
            )
            
            analysis = {
                "stakeholder": stakeholder,
                "perspective": response.synthesis.integrated_view,
                "key_insights": response.whitespace.insights,
                "concerns": [q for q in response.synthesis.new_questions if '?' in q],
                "confidence": response.confidence,
                "spectra_analysis": {
                    color: {
                        "content": spectrum.content[:100] + "...",
                        "confidence": spectrum.confidence
                    }
                    for color, spectrum in response.spectra.items()
                }
            }
            
            stakeholder_analyses.append(analysis)
            
            print(f"      主要观点: {response.synthesis.integrated_view[:80]}...")
            print(f"      置信度: {response.confidence:.2%}")
        
        # 综合决策分析
        print(f"\n    🤝 综合决策分析...")
        
        # 准备综合输入
        perspectives_text = "\n".join([
            f"{a['stakeholder']}: {a['perspective']}"
            for a in stakeholder_analyses
        ])
        
        synthesis_query = f"""基于以下各相关方分析，提供综合决策建议：
{perspectives_text}

决策问题: {decision_scenario['problem']}
评估标准: {', '.join(decision_scenario['criteria'])}
请考虑所有视角，提供平衡的建议。"""
        
        synthesis_response = await self.client.prismatic_dialogue(
            query=synthesis_query,
            max_depth=5,
            whitespace_duration=60
        )
        
        # 决策矩阵
        decision_matrix = []
        for criterion in decision_scenario['criteria']:
            criterion_query = f"从{criterion}角度评估{decision_scenario['problem']}"
            
            criterion_response = await self.client.prismatic_dialogue(
                query=criterion_query,
                max_depth=3
            )
            
            decision_matrix.append({
                "criterion": criterion,
                "analysis": criterion_response.synthesis.integrated_view,
                "confidence": criterion_response.confidence
            })
        
        # 最终建议
        final_recommendation = {
            "problem": decision_scenario['problem'],
            "stakeholder_analyses": stakeholder_analyses,
            "synthesis": synthesis_response.synthesis.integrated_view,
            "key_recommendations": synthesis_response.whitespace.insights,
            "next_steps": synthesis_response.synthesis.new_questions,
            "decision_matrix": decision_matrix,
            "overall_confidence": synthesis_response.confidence,
            "generated_at": datetime.now().isoformat()
        }
        
        result = {
            "scenario": decision_scenario,
            "final_recommendation": final_recommendation,
            "total_analyses": len(stakeholder_analyses) + len(decision_matrix) + 1
        }
        
        print(f"    ✅ 完成综合决策分析")
        print(f"    📊 总体置信度: {final_recommendation['overall_confidence']:.2%}")
        
        return result
    
    async def example_research_analysis(self):
        """示例4: 研究分析支持"""
        print("场景: 学术研究问题分析")
        
        research_topic = {
            "field": "认知科学",
            "topic": "人工智能对人类认知的影响",
            "research_questions": [
                "AI如何改变我们的思考方式？",
                "人机协作的认知效应是什么？",
                "AI时代的认知技能需求变化？"
            ],
            "methodology": ["文献综述", "理论分析", "案例研究"]
        }
        
        print(f"  研究领域: {research_topic['field']}")
        print(f"  研究主题: {research_topic['topic']}")
        print(f"  研究方法: {', '.join(research_topic['methodology'])}")
        
        research_analyses = []
        
        # 文献综述模拟
        print(f"\n    📚 文献综述分析...")
        literature_query = f"对'{research_topic['topic']}'进行文献综述，重点关注{', '.join(research_topic['research_questions'][:2])}"
        
        literature_response = await self.client.prismatic_dialogue(
            query=literature_query,
            max_depth=5,
            whitespace_duration=60,
            metadata={
                "analysis_type": "literature_review",
                "field": research_topic['field']
            }
        )
        
        literature_analysis = {
            "type": "literature_review",
            "key_findings": literature_response.whitespace.insights,
            "theoretical_framework": literature_response.synthesis.integrated_view,
            "research_gaps": literature_response.synthesis.new_questions,
            "confidence": literature_response.confidence
        }
        
        research_analyses.append(literature_analysis)
        
        # 研究问题分析
        print(f"\n    🔍 研究问题分析...")
        question_analyses = []
        
        for i, question in enumerate(research_topic['research_questions'], 1):
            print(f"      分析问题 {i}: {question}")
            
            question_response = await self.client.prismatic_dialogue(
                query=question,
                max_depth=4,
                whitespace_duration=45,
                metadata={
                    "research_question": True,
                    "question_index": i
                }
            )
            
            question_analysis = {
                "question": question,
                "analysis": question_response.synthesis.integrated_view,
                "methodological_approaches": question_response.whitespace.insights,
                "sub_questions": question_response.synthesis.new_questions,
                "confidence": question_response.confidence
            }
            
            question_analyses.append(question_analysis)
        
        # 研究方法设计
        print(f"\n    🛠️ 研究方法设计...")
        methodology_query = f"为研究'{research_topic['topic']}'设计研究方法，考虑{', '.join(research_topic['methodology'])}"
        
        methodology_response = await self.client.prismatic_dialogue(
            query=methodology_query,
            max_depth=4,
            whitespace_duration=50
        )
        
        methodology_design = {
            "proposed_methods": methodology_response.whitespace.insights,
            "methodological_considerations": methodology_response.synthesis.integrated_view,
            "implementation_steps": methodology_response.synthesis.new_questions,
            "confidence": methodology_response.confidence
        }
        
        # 研究计划综合
        print(f"\n    📋 研究计划综合...")
        research_plan_query = f"""基于以上分析，制定完整的研究计划：
研究主题: {research_topic['topic']}
关键问题: {', '.join(research_topic['research_questions'])}
研究方法: {', '.join(research_topic['methodology'])}

请提供详细的研究计划。"""
        
        research_plan_response = await self.client.prismatic_dialogue(
            query=research_plan_query,
            max_depth=5,
            whitespace_duration=75
        )
        
        research_plan = {
            "topic": research_topic['topic'],
            "literature_review": literature_analysis,
            "question_analyses": question_analyses,
            "methodology_design": methodology_design,
            "integrated_plan": research_plan_response.synthesis.integrated_view,
            "timeline_suggestions": research_plan_response.whitespace