"""
🔥 棱镜协议极简体验版
任何人都能立即体验的认知对话工具
"""

import streamlit as st
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from prism_sdk import PrismClient

# 页面配置
st.set_page_config(
    page_title="棱镜对话 · 极简体验",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化客户端
@st.cache_resource
def get_client():
    return PrismClient()

# 极简呼吸引导
def show_breath_guide():
    """显示三秒呼吸引导"""
    with st.expander("🧘‍♀️ 三秒呼吸练习（点击展开）", expanded=False):
        st.markdown("""
        ### 🌬️ 来，我们一起深呼吸
        
        这个练习能帮你体验"认知正在进行时"：
        
        1. **吸气**（3秒）：感受空气进入身体
        2. **屏息**（2秒）：感受身体的感受
        3. **呼气**（4秒）：让思绪自然流动
        
        **为什么有效？**
        - 呼吸调节能暂时打断自动化思维
        - 屏息时刻创造"认知间隙"
        - 呼气时大脑会自然重组信息
        
        **点击下方按钮开始练习：**
        """)
        
        if st.button("🌬️ 开始三秒呼吸练习", type="primary"):
            # 创建呼吸引导界面
            breath_container = st.empty()
            
            # 吸气阶段
            breath_container.markdown("### 🌬️ 吸气... 3秒")
            for i in range(3, 0, -1):
                breath_container.markdown(f"### 🌬️ 吸气... {i}秒")
                asyncio.sleep(1)
            
            # 屏息阶段
            breath_container.markdown("### ⏸️ 屏息... 2秒")
            for i in range(2, 0, -1):
                breath_container.markdown(f"### ⏸️ 屏息... {i}秒")
                asyncio.sleep(1)
            
            # 呼气阶段
            breath_container.markdown("### 💨 呼气... 4秒")
            for i in range(4, 0, -1):
                breath_container.markdown(f"### 💨 呼气... {i}秒")
                asyncio.sleep(1)
            
            # 完成
            breath_container.markdown("""
            ### 🎉 完成！
            
            **感受一下：**
            - 刚才那几秒，烦恼是不是暂时不见了？
            - 大脑是不是稍微清晰了一点？
            - 这就是"认知间隙"的力量。
            
            **现在，带着这个清晰的感受，继续下面的对话吧。**
            """)

# 侧边栏说明
def show_sidebar_guide():
    """显示侧边栏说明"""
    with st.sidebar:
        st.title("🔥 棱镜对话")
        st.markdown("---")
        
        st.markdown("""
        ### 🤔 这是什么？
        
        这是一个让你**看见自己思考过程**的工具。
        
        **为什么有三个声音？**
        - 🔥 **红色光谱**：直觉、感受、创意
        - 🔵 **蓝色光谱**：逻辑、分析、事实  
        - 🟣 **紫色光谱**：反思、元认知、学习
        
        就像看同一幅画，不同的人会看到不同的东西。
        
        ### ⏸️ 留白是什么？
        
        留白不是"等待"，而是**主动创造思考空间**。
        
        就像音乐中的休止符，让前面的音符更有意义。
        
        ### 🎯 怎么用？
        1. 写下你的困惑或问题
        2. 点击三个光谱按钮，看不同视角
        3. 在留白区停顿、呼吸、感受
        4. 看看合成后的完整视角
        
        **记住：没有"正确答案"，只有"更多看见"。**
        """)
        
        st.markdown("---")
        
        # 呼吸练习按钮
        if st.button("🧘‍♀️ 先做个三秒呼吸练习", type="secondary"):
            show_breath_guide()
        
        st.markdown("---")
        
        # 快速链接
        st.markdown("### 🔗 快速链接")
        st.markdown("- [GitHub项目](https://github.com/Ultima0369/prism-interconnect)")
        st.markdown("- [完整文档](https://github.com/Ultima0369/prism-interconnect#readme)")
        st.markdown("- [体验反馈](https://github.com/Ultima0369/prism-interconnect/discussions)")
        
        st.markdown("---")
        
        # 版本信息
        st.markdown("**版本**: v1.0.0 · 极简体验版")
        st.markdown("**状态**: 🟢 在线")

# 主界面
def main():
    """主界面"""
    
    # 显示侧边栏
    show_sidebar_guide()
    
    # 主标题
    st.title("🔥 棱镜对话 · 极简体验")
    st.markdown("---")
    
    # 简介
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🎯 欢迎来到火堆旁
        
        这里没有标准答案，只有**更多看见**。
        
        写下你的困惑，让三个不同的"你"一起对话。
        """)
    
    with col2:
        # 呼吸练习快速入口
        if st.button("🌬️ 先呼吸，再思考", use_container_width=True):
            show_breath_guide()
    
    st.markdown("---")
    
    # 输入区域
    st.subheader("📝 写下你的困惑或问题")
    
    # 示例问题
    example_questions = [
        "我该如何选择职业方向？",
        "为什么我总是拖延？",
        "如何与家人更好地沟通？",
        "我对未来感到迷茫，怎么办？",
        "最近压力很大，如何调整？"
    ]
    
    # 选择示例问题
    selected_example = st.selectbox(
        "或者选择一个示例问题：",
        ["自己写..."] + example_questions
    )
    
    # 文本输入
    if selected_example == "自己写...":
        user_query = st.text_area(
            "你的困惑：",
            placeholder="例如：我最近总是感到焦虑，不知道原因...",
            height=100
        )
    else:
        user_query = st.text_area(
            "你的困惑：",
            value=selected_example,
            height=100
        )
    
    # 光谱选择
    st.subheader("🌈 选择你想听的视角")
    
    col_red, col_blue, col_purple = st.columns(3)
    
    with col_red:
        red_btn = st.button("🔥 红色光谱 · 直觉", use_container_width=True, type="primary")
    
    with col_blue:
        blue_btn = st.button("🔵 蓝色光谱 · 逻辑", use_container_width=True, type="primary")
    
    with col_purple:
        purple_btn = st.button("🟣 紫色光谱 · 反思", use_container_width=True, type="primary")
    
    # 处理按钮点击
    if user_query and (red_btn or blue_btn or purple_btn):
        # 确定选择的光谱
        if red_btn:
            spectrum_type = "red"
            spectrum_name = "🔥 红色光谱 · 直觉"
        elif blue_btn:
            spectrum_type = "blue"
            spectrum_name = "🔵 蓝色光谱 · 逻辑"
        else:
            spectrum_type = "purple"
            spectrum_name = "🟣 紫色光谱 · 反思"
        
        st.markdown(f"---")
        st.subheader(f"{spectrum_name}")
        
        # 显示加载状态
        with st.spinner(f"正在从{spectrum_name}视角思考..."):
            try:
                # 创建客户端
                client = get_client()
                
                # 调用棱镜协议
                response = asyncio.run(client.prismatic_dialogue(
                    query=user_query,
                    spectrum_types=[spectrum_type],
                    whitespace_duration=3  # 3秒留白
                ))
                
                # 显示结果
                if spectrum_type in response.spectra:
                    spectrum_result = response.spectra[spectrum_type]
                    
                    # 显示分析
                    st.markdown("### 💭 分析结果")
                    st.markdown(spectrum_result.get("analysis", "暂无分析"))
                    
                    # 显示洞见
                    if "insights" in spectrum_result:
                        st.markdown("### 💡 关键洞见")
                        for insight in spectrum_result["insights"][:3]:  # 只显示前3个
                            st.markdown(f"- {insight}")
                    
                    # 显示建议
                    if "suggestions" in spectrum_result:
                        st.markdown("### 🎯 行动建议")
                        for suggestion in spectrum_result["suggestions"][:2]:  # 只显示前2个
                            st.markdown(f"- {suggestion}")
                
                # 显示留白提示
                st.markdown("---")
                st.markdown("### ⏸️ 留白时刻")
                st.markdown("""
                **停在这里，感受一下：**
                - 这个视角给你什么感觉？
                - 有什么新的想法浮现？
                - 想试试其他视角吗？
                
                **记住：** 留白不是结束，而是思考的开始。
                """)
                
                # 其他视角按钮
                st.markdown("### 🔄 还想看看其他视角吗？")
                other_cols = st.columns(3)
                
                with other_cols[0]:
                    if spectrum_type != "red":
                        if st.button("试试🔥直觉视角", use_container_width=True):
                            st.rerun()
                
                with other_cols[1]:
                    if spectrum_type != "blue":
                        if st.button("试试🔵逻辑视角", use_container_width=True):
                            st.rerun()
                
                with other_cols[2]:
                    if spectrum_type != "purple":
                        if st.button("试试🟣反思视角", use_container_width=True):
                            st.rerun()
                
            except Exception as e:
                st.error(f"出错了：{str(e)}")
                st.info("""
                **如果遇到技术问题：**
                1. 确保已安装依赖：`pip install prism-sdk streamlit`
                2. 或者直接使用在线版（见侧边栏链接）
                3. 在GitHub Discussions反馈问题
                """)
    
    elif not user_query:
        st.info("💡 先写下你的困惑，然后选择一个视角开始对话。")
    
    # 底部信息
    st.markdown("---")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("### 🔥 关于火堆")
        st.markdown("""
        火堆旁，每个人都能说话，
        每个人也都能倾听。
        这里没有专家，只有旅人。
        """)
    
    with col_info2:
        st.markdown("### 🧠 关于认知")
        st.markdown("""
        思考不是解决问题，
        而是看见问题的更多面。
        看见，就是改变的开始。
        """)
    
    with col_info3:
        st.markdown("### 🤝 关于你")
        st.markdown("""
        你的困惑有价值，
        你的思考有力量，
        你的存在有意义。
        
        **欢迎来到火堆旁。**
        """)
    
    # 分享提示
    st.markdown("---")
    st.markdown("""
    ### 🌐 想分享给朋友？
    
    1. **本地运行**：`streamlit run examples/streamlit_simple_app.py`
    2. **在线体验**：使用ngrok生成公网链接（见下方命令）
    3. **直接分享**：复制这个项目链接给朋友
    
    **生成公网链接命令：**
    ```bash
    # 安装ngrok
    pip install pyngrok
    
    # 运行应用并生成链接
    streamlit run examples/streamlit_simple_app.py &
    ngrok http 8501
    ```
    
    获得链接后，任何人都能通过浏览器访问。
    """)

if __name__ == "__main__":
    main()