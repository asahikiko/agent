import os
from openai import OpenAI
import json

# It's a good practice to load API keys from environment variables or a secrets management system.
# For this example, we'll assume the API key is in an environment variable.
# You can also use st.secrets if this were a streamlit app.
# from dotenv import load_dotenv
# load_dotenv()

# Using the user-provided Silicon Flow API configuration
client = OpenAI(
    api_key="sk-jwaoksrekpmepnwbqfoaiktmgtlyjevobxujnwgyfgthbjai",
    base_url="https://api.siliconflow.cn/v1"
)


def extract_entities_with_llm(user_text: str) -> dict:
    """
    Uses an LLM to extract social media platforms, users, and investment products from user text.
    """
    prompt = f"""
    From the following user text, extract the specified social media platform, social media user, and investment product.
    The output should be a JSON object with the keys "platform", "user", and "product".
    If a piece of information is not present, the value should be null.

    User text: "{user_text}"

    JSON output:
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B", # Or any other suitable model
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
    Generates a final investment suggestion based on all gathered information.
    """
    # Build a comprehensive prompt
    prompt = f"""
    As a professional financial advisor, provide an investment suggestion based on the following information.

    1.  **User's Query Context**: The user is interested in {entities.get('product')}, and potentially influenced by {entities.get('user')} on {entities.get('platform')}.

    2.  **Social Media Intelligence**: Here are the recent posts from {entities.get('user')}:
        - {"\n        - ".join(social_media_info)}

    3.  **Market Data**: Here is the recent market data for {entities.get('product')}:
        - 3-Day High: ${market_data.get('high_3d')}
        - 3-Day Low: ${market_data.get('low_3d')}
        - 3-Day Volume: {market_data.get('volume_3d')}
        - 14-Day RSI: {market_data.get('rsi_14d')}
        - News Summary: {market_data.get('news_summary')}

    **Your Task**:
    Synthesize all this information to provide a balanced investment suggestion.
    - Analyze the sentiment from the social media posts.
    - Interpret the market data (e.g., is RSI indicating overbought/oversold?).
    - Conclude with a clear recommendation: should the user consider buying, selling, or holding?
    - Include a disclaimer that this is not financial advice and the user should do their own research.

    **Investment Suggestion**:
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {'role': 'system', 'content': 'You are a professional financial advisor providing investment suggestions based on data.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    
    return response.choices[0].message.content