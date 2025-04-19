import streamlit as st
import pandas as pd
import json
from data_processor import DataProcessor
from data_analyzer import DataAnalyzer
from data_visualization import DataVisualizer
from api_handler import APIHandler
import os

# 设置页面配置
st.set_page_config(
    page_title="医疗数据分析系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .css-1d391kg {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class MedicalDataApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.data_analyzer = DataAnalyzer()
        self.data_visualizer = DataVisualizer()
        self.api_handler = APIHandler()
        self.processed_data = None
        self.analysis_results = None
        self.visualizations = None
    
    def run(self):
        """运行应用"""
        st.title("🏥 医疗数据分析系统")
        
        # 侧边栏
        with st.sidebar:
            st.header("📊 数据上传")
            uploaded_file = st.file_uploader("选择数据文件", type=['csv', 'json'])
            
            if uploaded_file:
                with st.spinner("正在处理数据..."):
                    try:
                        # 保存上传的文件
                        file_path = f"temp_{uploaded_file.name}"
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # 处理数据
                        self.processed_data = self.data_processor.process_data(file_path)
                        
                        # 分析数据
                        self.analysis_results = self.data_analyzer.analyze_data(
                            self.processed_data['json1'],
                            self.processed_data['json2']
                        )
                        
                        # 创建可视化
                        self.visualizations = self.data_visualizer.create_all_visualizations(
                            self.processed_data['json1'],
                            self.processed_data['json2']
                        )
                        
                        st.success("数据处理完成！")
                        
                        # 删除临时文件
                        os.remove(file_path)
                    except Exception as e:
                        st.error(f"数据处理失败: {str(e)}")
        
        # 主界面
        if self.processed_data:
            self._display_data_overview()
            self._display_analysis_results()
            self._display_visualizations()
            self._display_chat_interface()
    
    def _display_data_overview(self):
        """显示数据概览"""
        st.header("📈 数据概览")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("基本信息")
            st.json(self.processed_data['json1'][0])
        
        with col2:
            st.subheader("诊断信息")
            st.json(self.processed_data['json2'][0])
    
    def _display_analysis_results(self):
        """显示分析结果"""
        st.header("🔍 分析结果")
        
        tabs = st.tabs(["数值分析", "文本分析", "诊断分析", "时间分析"])
        
        with tabs[0]:
            st.subheader("数值型数据分析")
            st.json(self.analysis_results['numeric_analysis'])
        
        with tabs[1]:
            st.subheader("文本型数据分析")
            st.json(self.analysis_results['text_analysis'])
        
        with tabs[2]:
            st.subheader("诊断数据分析")
            st.json(self.analysis_results['diagnosis_analysis'])
        
        with tabs[3]:
            st.subheader("时间序列分析")
            st.json(self.analysis_results['temporal_analysis'])
    
    def _display_visualizations(self):
        """显示可视化结果"""
        st.header("📊 数据可视化")
        
        # 数值型数据可视化
        st.subheader("数值型数据分布")
        st.plotly_chart(self.visualizations['numeric']['box_plot'])
        st.plotly_chart(self.visualizations['numeric']['histogram'])
        st.plotly_chart(self.visualizations['numeric']['heatmap'])
        
        # 诊断数据可视化
        st.subheader("诊断数据分布")
        st.plotly_chart(self.visualizations['diagnosis']['diagnosis_bar'])
        st.plotly_chart(self.visualizations['diagnosis']['wordcloud'])
        
        # 时间序列可视化
        st.subheader("时间趋势分析")
        for fig in self.visualizations['temporal'].values():
            st.plotly_chart(fig)
    
    def _display_chat_interface(self):
        """显示聊天界面"""
        st.header("💬 智能问答")
        
        # 初始化聊天历史
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # 显示聊天历史
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("请输入您的问题"):
            # 添加用户消息到历史
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # 显示用户消息
            with st.chat_message("user"):
                st.write(prompt)
            
            # 生成回答
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    try:
                        # 调用 API 处理问题
                        answer = self.api_handler.analyze_data_question(
                            prompt,
                            self.processed_data['json2']  # 使用 json2 作为数据源
                        )
                        
                        st.write(answer)  # 直接显示回答
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"生成回答失败: {str(e)}")

if __name__ == "__main__":
    app = MedicalDataApp()
    app.run()