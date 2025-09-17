import streamlit as st
import os
import json

# 我们需要重构 agent.py，使其包含一个接收所有数据作为输入的函数
# 假设 agent.py 中存在一个名为 `run_analysis` 的函数
from agent import generate_investment_suggestion_with_llm, extract_entities_with_llm

def run_analysis(user_query: str, social_posts: list[str], market_data: dict) -> dict:
    """
    根据用户输入编排投资建议流程。
    """
    # 1. 从用户查询中提取实体
    entities = extract_entities_with_llm(user_query)

    if not entities.get('product'):
        return {
            "suggestion": "抱歉，我无法在您的消息中识别出具体的投资产品。请指明一个产品，如 BTC、ETH 或股票代码。",
            "reasoning": {}
        }

    # 2. 生成最终建议
    final_suggestion = generate_investment_suggestion_with_llm(entities, social_posts, market_data)

    # 返回最终建议和用于前端的推理数据
    return {
        "suggestion": final_suggestion,
        "reasoning": {
            "extracted_entities": entities,
            "social_media_posts": social_posts,
            "market_data": market_data
        }
    }


st.set_page_config(layout="wide")

st.title("🤖 AI 投资分析助手")
st.markdown("该工具利用 AI 代理分析市场数据和社交媒体情绪，以提供投资建议。")

# --- Session State 初始化 ---
if 'social_posts' not in st.session_state:
    st.session_state.social_posts = [""]

# --- UI 布局 ---
col1, col2 = st.columns(2)

with col1:
    st.header("📊 输入数据")

    # 1. 主要分析请求
    user_query = st.text_input(
        "1. 您的投资分析请求是什么？",
        "最近比特币的讨论热度很高。Donald Trump 最近在 X 上提到了它。OKX 上 BTC 的最新情况如何？"
    )

    # 2. 社交媒体帖子
    st.subheader("2. 社交媒体帖子")
    
    # 添加新帖子输入框的函数
    def add_post_input():
        st.session_state.social_posts.append("")

    # 为每个帖子显示文本区域
    for i in range(len(st.session_state.social_posts)):
        st.session_state.social_posts[i] = st.text_area(f"帖子 {i+1}", st.session_state.social_posts[i], key=f"post_{i}")

    st.button("添加另一个帖子", on_click=add_post_input)


    # 3. 市场数据
    st.subheader("3. 市场数据")
    product_name = st.text_input("产品（例如 BTC、ETH、股票代码）", "BTC")
    high_3d = st.number_input("3 日最高价", value=71000.0, format="%.2f")
    low_3d = st.number_input("3 日最低价", value=68000.0, format="%.2f")
    volume_3d = st.number_input("3 日成交量", value=150000000, format="%d")
    rsi_14d = st.number_input("14 日 RSI", value=65.0, format="%.2f")
    news_summary = st.text_area("近期新闻摘要", "SEC 批准多个比特币 ETF，导致机构兴趣增加。")

# --- 分析触发与输出 ---
with col2:
    st.header("📈 分析结果")

    if st.button("🚀 开始分析"):
        with st.spinner("代理正在思考中... 这可能需要一些时间。"):
            # 为代理准备数据
            # 过滤掉空的帖子
            valid_social_posts = [post for post in st.session_state.social_posts if post.strip()]
            
            market_data = {
                "product": product_name,
                "high_3d": high_3d,
                "low_3d": low_3d,
                "volume_3d": volume_3d,
                "rsi_14d": rsi_14d,
                "news_summary": news_summary
            }

            try:
                result = run_analysis(user_query, valid_social_posts, market_data)
                
                st.subheader("✅ 投资建议")
                st.markdown(result['suggestion'])

                st.subheader("🧠 推理数据")
                st.json(result['reasoning'])

            except Exception as e:
                st.error(f"分析过程中发生错误: {e}")
                st.error("请确保 agent.py 文件已正确重构，以包含 'run_analysis' 函数。")