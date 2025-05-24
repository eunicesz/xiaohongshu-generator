import streamlit as st

from utils import generate_xiaohongshu

st.header("爆款小红书写作助手🌟 ")
with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

theme = st.text_input("主题")
submit = st.button("开始写作")
if submit and not openai_api_key:
    st.info("请输入OpenAI API密钥")
    st.stop()
if submit and not theme:
    st.info("请输入主题")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，请等待……"):
         result = generate_xiaohongshu(theme, openai_api_key)
    st.divider()
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("##### 小红书标题1")
        st.write(result.titles[0])
        st.markdown("##### 小红书标题2")
        st.write(result.titles[1])
        st.markdown("##### 小红书标题3")
        st.write(result.titles[2])
        st.markdown("##### 小红书标题4")
        st.write(result.titles[3])
        st.markdown("##### 小红书标题5")
        st.write(result.titles[4])
    with right_column:
        st.markdown("##### 小红书正文")
        st.write(result.content)





# st.header("爆款小红书AI写作助手 ✏️")
# with st.sidebar:
#     openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
#     st.markdown ("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
#
# theme = st.text_input("主题")
# submit = st.button("开始写作")
#
# if submit and not openai_api_key:
#     st.info("请输入你的OpenAI API密钥")
#     st.stop()
# if submit and not theme:
#     st.info("请输入生成内容的主题")
#     st.stop()
# if submit:
#     try:
#         with st.spinner("AI正在努力创作中，请稍等..."):
#             result = generate_xiaohongshu(theme, openai_api_key)
#         st.divider()
#         left_column, right_column = st.columns(2)
#         with left_column:
#             st.markdown("##### 小红书标题1")
#             st.write(result.titles[0])
#             st.markdown("##### 小红书标题2")
#             st.write(result.titles[1])
#             st.markdown("##### 小红书标题3")
#             st.write(result.titles[2])
#             st.markdown("##### 小红书标题4")
#             st.write(result.titles[3])
#             st.markdown("##### 小红书标题5")
#             st.write(result.titles[4])
#         with right_column:
#             st.markdown("##### 小红书正文")
#             st.write(result.content)
#     except Exception as e:
#         st.error(f"发生错误: {str(e)}")
#         st.stop()