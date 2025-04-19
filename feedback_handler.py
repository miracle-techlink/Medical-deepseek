import streamlit as st

class FeedbackHandler:
    def __init__(self):
        self.feedback_data = []

    def display_feedback_section(self, response, confidence):
        """显示反馈和评分部分"""
        st.subheader("反馈与评分")
        
        # 显示模型响应和置信度
        if confidence < 0.7:  # 设定置信度阈值
            st.warning("模型生成的响应可能不可靠，请谨慎使用。")
        
        st.write(f"模型响应: {response} (置信度: {confidence:.2f})")
        
        # 用户评分
        rating = st.slider("请给出评分（1-5）", 1, 5, 3)
        feedback = st.text_area("请提供反馈意见（可选）")
        
        if st.button("提交反馈"):
            self.feedback_data.append({
                "response": response,
                "confidence": confidence,
                "rating": rating,
                "feedback": feedback
            })
            st.success("感谢您的反馈！")

    def get_feedback_data(self):
        """获取所有反馈数据"""
        return self.feedback_data