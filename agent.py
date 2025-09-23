import os
from openai import OpenAI
import json

# 从环境变量或密钥管理系统加载API密钥是一个好习惯。
# 在这个例子中，我们假设API密钥存储在环境变量中。
# 如果这是一个streamlit应用，你也可以使用st.secrets。
from dotenv import load_dotenv
load_dotenv()

# 使用用户提供的Silicon Flow API配置

client = OpenAI(
    api_key="sk-jwaoksrekpmepnwbqfoaiktmgtlyjevobxujnwgyfgthbjai",
    base_url="https://api.siliconflow.cn/v1"
)


def extract_entities_with_llm(user_text: str) -> dict:
    """
    使用大语言模型从用户文本中提取社交媒体平台、用户和投资产品信息。
    """
    prompt = f"""
    From the following user text, extract the specified social media platform, social media user, and investment product.
    The output should be a JSON object with the keys "platform", "user", and "product".
    If a piece of information is not present, the value should be null.

    User text: "{user_text}"

    JSON output:
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B", # 或任何其他合适的模型
        messages=[
            {'role': 'system', 'content': 'You are an expert at extracting specific entities from text and responding in JSON format.'},
            {'role': 'user', 'content': prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        extracted_info = json.loads(response.choices[0].message.content)
        return extracted_info
    except (json.JSONDecodeError, IndexError):
        return {"platform": None, "user": None, "product": None}


def generate_investment_suggestion_with_llm(entities: dict, social_media_info: list[str], market_data: dict) -> str:
    """
    根据收集到的所有信息，生成最终的投资建议。
    """
    # 构建一个更全面、更结构化的中文提示
    prompt = f"""
    作为一名专业的金融分析师，请根据以下信息提供一份详细的投资分析报告。

    ### 1. 核心分析目标
    - **投资产品**: {entities.get('product', '未知')}
    - **关键人物/事件**: {entities.get('user', '无特定人物')}
    - **相关平台**: {entities.get('platform', '无特定平台')}

    ### 2. 社交媒体情绪分析
    以下是近期相关的社交媒体帖子：
    - {"\n    - ".join(social_media_info) if social_media_info else "无"}

    ### 3. 市场数据解读
    以下是 {entities.get('product', '该产品')} 的最新市场数据：
    - **3日内最高价**: ${market_data.get('high_3d', 'N/A')}
    - **3日内最低价**: ${market_data.get('low_3d', 'N/A')}
    - **3日内成交量**: {market_data.get('volume_3d', 'N/A')}
    - **14日相对强弱指数 (RSI)**: {market_data.get('rsi_14d', 'N/A')}
    - **近期新闻摘要**: {market_data.get('news_summary', '无')}

    ### 4. 你的任务：一步一步思考（Chain of Thought）
    请遵循以下步骤，提供一份结构清晰的分析报告：

    **第一步：社交媒体情绪评估**
    - 分析上述社交媒体帖子的整体情绪（正面、负面、中性）。
    - 总结这些情绪背后的主要观点或原因。
    - 这对 {entities.get('product', '该产品')} 的短期价格可能意味着什么？

    **第二步：市场技术面分析**
    - 解读 14 日 RSI 指标。{market_data.get('rsi_14d', 'N/A')} 的值是处于超买（>70）、超卖（<30）还是中性区域？
    - 结合近期的价格波动（最高价与最低价）和成交量，给出波动的具体增长数量，判断市场动能是强劲还是疲软。
    - 新闻摘要中的信息是利好还是利空？

    **第三步：综合分析与核心结论**
    - 结合社交媒体情绪和市场技术面分析，进行综合评估。
    - 这两种信息源是否存在矛盾（例如，社交媒体看涨但技术指标看跌）？如果存在，你如何权衡？
    - 得出明确的投资建议：**买入**、**卖出** 或 **持有**。

    **第四步：置信度与风险提示**
    - 为你的建议给出一个置- 信度评分（1-10分，10分为最高）。
    - 明确指出该建议成立的关键假设和潜在风险。
    - **最后，必须包含免责声明**：此分析仅供参考，不构成任何财务建议。投资者应自行进行研究并承担风险。

    请将你的完整分析报告呈现出来。
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {'role': 'system', 'content': '你是一名专业的金融分析师，擅长结合市场数据和社交媒体情绪，提供结构清晰、逻辑严密的投资分析报告。'},
            {'role': 'user', 'content': prompt}
        ]
    )
    
    return response.choices[0].message.content