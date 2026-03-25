#!/usr/bin/env python3
"""
🔥 棱镜协议 Streamlit Web 应用
火堆旁的对话，现在有了Web界面
"""

import streamlit as st
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 设置页面配置
st.set_page_config(
    page_title="🧠 棱镜协议 - 火堆旁的对话",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主容器样式 */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* 火堆动画效果 */
    @keyframes fire-flicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .fire-icon {
        animation: fire-flicker 2s infinite;
        display: inline-block;
    }
    
    /* 卡片样式 */
    .prism-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-left: 5px solid #ff6b6b;
    }
    
    .spectrum-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ff8e53);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    /* 留白区域样式 */
    .whitespace-area {
        background: rgba(30, 60, 114, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 2px dashed rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #ff8e53);
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        background: linear-gradient(45deg, #ff6b6b, #ff8e53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 模拟棱镜SDK ====================

class MockPrismSDK:
    """模拟棱镜SDK功能"""
    
    @staticmethod
    async def prismatic_dialogue(query: str, max_depth: int = 3) -> Dict:
        """模拟棱镜对话"""
        await asyncio.sleep(1)  # 模拟处理时间
        
        # 生成三种光谱
        spectra = {
            "red": {
                "content": f"🔥 **直觉视角**: 这个问题让我想到...{query[:20]}的核心是模式识别",
                "confidence": 0.85,
                "reasoning": "基于经验和直觉的快速判断",
                "type": "直觉光谱"
            },
            "blue": {
                "content": f"🔵 **分析视角**: 从逻辑角度分析，{query}涉及以下因素...",
                "confidence": 0.92,
                "reasoning": "基于数据和逻辑的详细分析",
                "type": "分析光谱"
            },
            "purple": {
                "content": f"🟣 **元认知视角**: 在思考这个问题时，我注意到自己的思考过程...",
                "confidence": 0.78,
                "reasoning": "对思考过程的反思和监控",
                "type": "元认知光谱"
            }
        }
        
        # 生成留白
        whitespace = {
            "duration": 45,
            "type": "整合留白",
            "insights": [
                f"关于'{query}'的新连接形成",
                "不同视角间的模式识别",
                "潜在假设的浮现"
            ],
            "prompts": [
                "这些观点如何与你已有的知识连接？",
                "你注意到哪些模式或主题？",
                "有哪些隐含假设需要检验？"
            ]
        }
        
        # 生成合成
        synthesis = {
            "integrated_view": f"综合来看，'{query}'可以从多个维度理解...",
            "new_questions": [
                f"关于'{query}'，还有哪些未被探索的角度？",
                "如何将这些理解应用到实际情境中？",
                "下一步可以深入探索什么？"
            ],
            "confidence": 0.88
        }
        
        return {
            "query": query,
            "spectra": spectra,
            "whitespace": whitespace,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat(),
            "session_id": f"session_{int(time.time())}"
        }
    
    @staticmethod
    def analyze_cognitive_pattern(text: str) -> Dict:
        """分析认知模式"""
        # 简单的文本分析
        words = len(text.split())
        sentences = text.count('.') + text.count('?') + text.count('!')
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "avg_words_per_sentence": words / max(sentences, 1),
            "question_marks": text.count('?'),
            "exclamation_marks": text.count('!'),
            "cognitive_complexity": min(words / 50, 1.0)  # 0-1复杂度评分
        }
    
    @staticmethod
    def generate_cognitive_metrics(spectra: Dict) -> Dict:
        """生成认知指标"""
        confidences = [s["confidence"] for s in spectra.values()]
        
        return {
            "diversity_score": max(confidences) - min(confidences),  # 差异越大，多样性越高
            "average_confidence": sum(confidences) / len(confidences),
            "spectrum_balance": 1 - (abs(confidences[0] - confidences[1]) / 2),
            "cognitive_depth": sum(confidences) / len(confidences) * 0.8  # 模拟深度评分
        }

# ==================== 应用主函数 ====================

def main():
    """主应用函数"""
    
    # 侧边栏
    with st.sidebar:
        st.title("🔥 棱镜协议")
        st.markdown("---")
        
        # 模式选择
        app_mode = st.selectbox(
            "选择对话模式",
            ["🧠 标准棱镜对话", "🔍 深度分析", "🎯 问题拆解", "🔄 视角转换"]
        )
        
        # 参数设置
        st.markdown("### ⚙️ 参数设置")
        max_depth = st.slider("递归深度", 1, 5, 3)
        require_whitespace = st.checkbox("强制留白", value=True)
        whitespace_duration = st.slider("留白时长(秒)", 30, 180, 45) if require_whitespace else 0
        
        # 用户信息
        st.markdown("### 👤 用户信息")
        user_name = st.text_input("你的名字", value="火堆旁的旅人")
        user_role = st.selectbox(
            "你的角色",
            ["思考者", "教师", "心理咨询师", "开发者", "研究者", "学习者"]
        )
        
        # 会话管理
        st.markdown("### 💾 会话管理")
        if st.button("🔄 新会话"):
            st.session_state.clear()
            st.rerun()
        
        if st.button("📥 导出对话"):
            st.info("导出功能开发中...")
        
        st.markdown("---")
        st.markdown("""
        ### 🦞 关于棱镜
        **一题，多面，映照心智的色谱。**
        
        这里没有说教，只有火堆旁的对话。
        
        [查看项目源码](https://github.com/Ultima0369/prism-interconnect)
        """)
    
    # 主区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 标题区域
        st.title("🧠 棱镜协议 Web 应用")
        st.markdown("**火堆旁的对话，现在有了Web界面**")
        
        # 火堆状态显示
        fire_col1, fire_col2, fire_col3 = st.columns(3)
        with fire_col1:
            st.metric("🔥 火堆温度", "温暖", "+2")
        with fire_col2:
            st.metric("👥 在线对话", "1", "首个会话")
        with fire_col3:
            st.metric("🎯 认知深度", "85%", "+5%")
        
        st.markdown("---")
        
        # 对话输入区域
        st.subheader("💭 开始棱镜对话")
        
        # 问题输入
        query = st.text_area(
            "输入你的问题或思考",
            height=100,
            placeholder="例如：如何平衡工作与生活？\n或：人工智能的伦理挑战是什么？\n或：任何你想深度探索的话题...",
            help="棱镜协议会从多个视角分析你的问题"
        )
        
        # 对话按钮
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            analyze_btn = st.button("🔮 开始棱镜分析", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("🎲 随机问题示例", use_container_width=True):
                examples = [
                    "如何做出重要的人生决策？",
                    "什么是真正的创造力？",
                    "数字时代如何保持深度思考？",
                    "人工智能会改变人类认知吗？",
                    "如何建立有意义的对话？"
                ]
                import random
                st.session_state.example_query = random.choice(examples)
                st.rerun()
        with col_btn3:
            clear_btn = st.button("🗑️ 清空对话", use_container_width=True)
        
        if clear_btn:
            st.session_state.clear()
            st.rerun()
        
        # 使用示例问题
        if 'example_query' in st.session_state:
            query = st.session_state.example_query
            del st.session_state.example_query
    
    with col2:
        # 实时数据展示
        st.subheader("📊 实时认知数据")
        
        # 创建示例数据
        cognitive_data = pd.DataFrame({
            '光谱类型': ['直觉', '分析', '元认知'],
            '置信度': [0.85, 0.92, 0.78],
            '响应时间(ms)': [120, 350, 280]
        })
        
        # 置信度图表
        fig_conf = px.bar(
            cognitive_data,
            x='光谱类型',
            y='置信度',
            color='光谱类型',
            color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#a8e6cf'],
            title="光谱置信度分布"
        )
        fig_conf.update_layout(showlegend=False)
        st.plotly_chart(fig_conf, use_container_width=True)
        
        # 认知模式指示器
        st.markdown("#### 🧩 当前认知模式")
        mode_col1, mode_col2, mode_col3 = st.columns(3)
        with mode_col1:
            st.metric("直觉激活", "85%")
        with mode_col2:
            st.metric("分析深度", "92%")
        with mode_col3:
            st.metric("元认知", "78%")
        
        # 认知健康度
        st.markdown("#### 💪 认知健康度")
        st.progress(0.88, text="整体健康度: 88%")
    
    # 如果点击了分析按钮
    if analyze_btn and query:
        with st.spinner("🔮 棱镜正在分析中..."):
            # 模拟异步处理
            async def process_query():
                return await MockPrismSDK.prismatic_dialogue(query, max_depth)
            
            # 运行异步函数
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(process_query())
                loop.close()
                
                # 保存到会话状态
                if 'conversation_history' not in st.session_state:
                    st.session_state.conversation_history = []
                
                st.session_state.conversation_history.append(response)
                st.session_state.last_response = response
                
            except Exception as e:
                st.error(f"处理错误: {str(e)}")
                return
        
        # 显示结果
        st.markdown("---")
        st.subheader("🌈 棱镜分析结果")
        
        # 显示原始问题
        st.markdown(f"### ❓ 你的问题: {query}")
        
        # 显示三种光谱
        st.markdown("### 🔍 三种认知光谱")
        
        spectra = response["spectra"]
        cols = st.columns(3)
        
        # 红色光谱（直觉）
        with cols[0]:
            with st.container():
                st.markdown('<div class="spectrum-card">', unsafe_allow_html=True)
                st.markdown("#### 🔥 红色光谱 - 直觉")
                st.markdown(spectra["red"]["content"])
                st.progress(spectra["red"]["confidence"], text=f"置信度: {spectra['red']['confidence']*100:.0f}%")
                st.caption(f"推理: {spectra['red']['reasoning']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 蓝色光谱（分析）
        with cols[1]:
            with st.container():
                st.markdown('<div class="spectrum-card">', unsafe_allow_html=True)
                st.markdown("#### 🔵 蓝色光谱 - 分析")
                st.markdown(spectra["blue"]["content"])
                st.progress(spectra["blue"]["confidence"], text=f"置信度: {spectra['blue']['confidence']*100:.0f}%")
                st.caption(f"推理: {spectra['blue']['reasoning']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 紫色光谱（元认知）
        with cols[2]:
            with st.container():
                st.markdown('<div class="spectrum-card">', unsafe_allow_html=True)
                st.markdown("#### 🟣 紫色光谱 - 元认知")
                st.markdown(spectra["purple"]["content"])
                st.progress(spectra["purple"]["confidence"], text=f"置信度: {spectra['purple']['confidence']*100:.0f}%")
                st.caption(f"推理: {spectra['purple']['reasoning']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 留白区域
        if require_whitespace:
            st.markdown("---")
            st.markdown("### ⏸️ 留白时刻")
            
            with st.container():
                st.markdown('<div class="whitespace-area">', unsafe_allow_html=True)
                st.markdown(f"#### 🧘 留白时长: {whitespace_duration}秒")
                
                # 倒计时效果
                import time
                with st.empty():
                    for i in range(whitespace_duration, 0, -1):
                        st.markdown(f"### ⏳ {i}秒")
                        time.sleep(1)
                    st.markdown("### ✅ 留白结束")
                
                st.markdown("#### 💡 留白洞见:")
                for insight in response["whitespace"]["insights"]:
                    st.markdown(f"- {insight}")
                
                st.markdown("#### ❓ 反思提示:")
                for prompt in response["whitespace"]["prompts"]:
                    st.markdown(f"- {prompt}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 合成结果
        st.markdown("---")
        st.markdown("### 🎯 综合视角")
        
        with st.container():
            st.markdown('<div class="prism-card">', unsafe_allow_html=True)
            st.markdown("#### 🌈 整合理解")
            st.markdown(response["synthesis"]["integrated_view"])
            
            st.markdown("#### 🔮 新涌现的问题")
            for question in response["synthesis"]["new_questions"]:
                st.markdown(f"- {question}")
            
            st.progress(
                response["synthesis"]["confidence"],
                text=f"综合置信度: {response['synthesis']['confidence']*100:.0f}%"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 认知指标分析
        st.markdown("---")
        st.markdown("### 📊 认知指标分析")
        
        metrics = MockPrismSDK.generate_cognitive_metrics(spectra)
        text_analysis = MockPrismSDK.analyze_cognitive_pattern(query)
        
        # 显示指标
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("认知多样性", f"{metrics['diversity_score']*100:.1f}%")
        with metric_cols[1]:
            st.metric("平均置信度", f"{metrics['average_confidence']*100:.1f}%")
        with metric_cols[2]:
            st.metric("光谱平衡", f"{metrics['spectrum_balance']*100:.1f}%")
        with metric_cols[3]:
            st.metric("认知深度", f"{metrics['cognitive_depth']*100:.1f}%")
        
        # 文本分析
        st.markdown("#### 📝 文本分析")
        analysis_cols = st.columns(3)
        with analysis_cols[0]:
            st.metric("字数", text_analysis["word_count"])
        with analysis_cols[1]:
            st.metric("句子数", text_analysis["sentence_count"])
        with analysis_cols[2]:
            st.metric("问题数", text_analysis["question_marks"])
        
        # 雷达图显示认知模式
        st.markdown("#### 🎯 认知模式雷达图")
        
        categories = ['直觉', '分析', '元认知', '多样性', '深度', '平衡']
        values = [
            spectra["red"]["confidence"],
            spectra["blue"]["confidence"],
            spectra["purple"]["confidence"],
            metrics["diversity_score"],
            metrics["cognitive_depth"],
            metrics["spectrum_balance"]
        ]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#ff6b6b'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # 对话历史
        if 'conversation_history' in st.session_state and len(st.session_state.conversation_history) > 0:
            st.markdown("---")
            st.markdown("### 📜 对话历史")
            
            for i, conv in enumerate(st.session_state.conversation_history[-5:]):  # 显示最近5条
                with st.expander(f"对话 {i+1}: {conv['query'][:50]}..."):
                    st.markdown(f"**问题:** {conv['query']}")
                    st.markdown(f"**时间:** {conv['timestamp']}")
                    
                    # 显示光谱摘要
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"🔥 直觉: {conv['spectra']['red']['confidence']*100:.0f}%")
                    with col2:
                        st.caption(f"🔵 分析: {conv['spectra']['blue']['confidence']*100:.0f}%")
                    with col3:
                        st.caption(f"🟣 元认知: {conv['spectra']['purple']['confidence']*100:.0f}%")
    
    # 如果没有查询但会话历史存在
    elif 'conversation_history' in st.session_state and len(st.session_state.conversation_history) > 0:
        st.markdown("---")
        st.markdown("### 📜 继续之前的对话")
        
        last_conv = st.session_state.conversation_history[-1]
        st.info(f"上次对话: {last_conv['query'][:100]}...")
        
        if st.button("🔄 基于上次对话继续"):
            st.session_state.continue_query = last_conv['query']
            st.rerun()
    
    # 应用说明
    st.markdown("---")
    st.markdown("## 🦞 关于这个应用")
    
    with st.expander("点击查看详细说明", expanded=False):
        st.markdown("""
        ### 🔥 棱镜协议 Web 应用
        
        **这是一个展示棱镜协议核心概念的交互式Web应用。**
        
        #### 🎯 核心功能
        
        1. **多元视角分析**
           - 🔥 红色光谱：直觉性快速判断
           - 🔵 蓝色光谱：分析性详细推理  
           - 🟣 紫色光谱：元认知过程反思
        
        2. **留白整合空间**
           - ⏸️ 强制思考停顿
           - 💡 洞见涌现时刻
           - ❓ 反思提示引导
        
        3. **认知指标可视化**
           - 📊 实时数据展示
           - 🎯 认知模式雷达图
           - 📈 对话历史追踪
        
        #### 🚀 技术特性
        
        - **框架**: Streamlit (Python Web框架)
        - **可视化**: Plotly 交互式图表
        - **设计**: 响应式布局，移动端友好
        - **部署**: 支持本地运行和云部署
        
        #### 🔧 使用场景
        
        - **个人思考**: 深度探索复杂问题
        - **教育场景**: 课堂讨论和思维训练
        - **团队协作**: 多视角问题分析
        - **研究工具**: 认知过程可视化
        
        #### 📖 使用建议
        
        1. **提出真实问题**: 输入你真正关心的问题
        2. **体验不同光谱**: 注意不同视角的差异
        3. **尊重留白时间**: 给思考留出空间
        4. **记录洞见**: 在留白后记录你的想法
        5. **分享对话**: 邀请朋友一起探索
        
        #### 🔗 相关资源
        
        - [棱镜协议 GitHub](https://github.com/Ultima0369/prism-interconnect)
        - [完整文档](https://github.com/Ultima0369/prism-interconnect/tree/main/docs)
        - [Python SDK](https://github.com/Ultima0369/prism-interconnect/tree/main/implementations/python)
        - [火堆社区](https://github.com/Ultima0369/prism-interconnect/discussions)
        
        **火堆旁，我们一起继续。** 🦞
        """)
    
    # 页脚
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns(3)
    with col_footer1:
        st.markdown("**版本**: v1.0.0")
    with col_footer2:
        st.markdown("**状态**: 🔥 火堆燃烧中")
    with col_footer3:
        st.markdown("**对话数**: " + str(len(st.session_state.get('conversation_history', []))))

# ==================== 运行应用 ====================

if __name__ == "__main__":
    # 初始化会话状态
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'last_response' not in st.session_state:
        st.session_state.last_response = None
    
    # 运行主应用
    main()