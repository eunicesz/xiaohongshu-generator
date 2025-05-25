import streamlit as st
from utils_simple import generate_xiaohongshu_simple

st.set_page_config(
    page_title="爆款小红书写作助手",
    page_icon="🌟",
    layout="wide"
)

st.header("爆款小红书写作助手🌟")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的OpenAI API密钥")
    st.markdown("2. 输入想要创作的主题")
    st.markdown("3. 点击开始写作按钮")
    st.markdown("4. 等待AI生成内容")

theme = st.text_input("主题", placeholder="例如：健康饮食、旅行攻略、美妆护肤等")
submit = st.button("开始写作", type="primary")

if submit and not openai_api_key:
    st.error("请输入OpenAI API密钥")
    st.stop()

if submit and not theme:
    st.error("请输入主题")
    st.stop()

if submit:
    try:
        with st.spinner("AI正在思考中，请等待……"):
            result = generate_xiaohongshu_simple(theme, openai_api_key)
        
        st.success("生成完成！")
        st.divider()
        
        left_column, right_column = st.columns(2)
        
        with left_column:
            st.markdown("### 📝 小红书标题")
            for i, title in enumerate(result.titles, 1):
                st.markdown(f"**标题{i}：**")
                st.write(title)
                st.markdown("")
        
        with right_column:
            st.markdown("### 📄 小红书正文")
            st.write(result.content)
            
    except Exception as e:
        st.error(f"生成内容时出现错误：{str(e)}")
        st.info("请检查您的API密钥是否正确，或稍后重试。")