# c:\Users\kiko\Desktop\ai_agent_course\llmagent\agent.py

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


def get_social_media_data_from_user(platform: str, user: str) -> list[str]:
    """
    Prompts the user to enter social media posts.
    """
    posts = []
    if platform and user:
        print(f"\nPlease enter recent posts for {user} on {platform}. Enter an empty line to finish.")
        while True:
            post = input(f"Post [{len(posts) + 1}]: ")
            if not post:
                break
            posts.append(post)
    return posts


def get_market_data_from_user(product: str) -> dict:
    """
    Prompts the user to enter market data for a specific product.
    """
    if not product:
        return {}

    print(f"\nPlease enter the market data for {product}.")
    try:
        high_3d_str = input("3-Day High: ")
        high_3d = float(high_3d_str.replace(',', ''))
        
        low_3d_str = input("3-Day Low: ")
        low_3d = float(low_3d_str.replace(',', ''))
        
        volume_3d_str = input("3-Day Volume: ")
        volume_3d = int(volume_3d_str.replace(',', ''))
        
        rsi_14d_str = input("14-Day RSI: ")
        rsi_14d = float(rsi_14d_str.replace(',', ''))
        
        news_summary = input("News Summary: ")

        return {
            "product": product,
            "high_3d": high_3d,
            "low_3d": low_3d,
            "volume_3d": volume_3d,
            "rsi_14d": rsi_14d,
            "news_summary": news_summary
        }
    except ValueError:
        print("Invalid input. Please enter numerical values for market data.")
        return {}


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


def get_investment_suggestion(user_text: str) -> dict:
    """
    Main function to orchestrate the investment suggestion process.
    """
    # 1. Extract entities from user text
    print("Step 1: Extracting entities from user text...")
    entities = extract_entities_with_llm(user_text)
    print(f"  -> Extracted: {entities}")

    if not entities.get('product'):
        return {
            "suggestion": "I'm sorry, but I couldn't identify a specific investment product in your message. Please specify a product like BTC, ETH, or a stock ticker.",
            "reasoning": {}
        }

    # 2. Get social media information
    print("Step 2: Fetching social media information...")
    social_media_info = get_social_media_data_from_user(entities.get('platform'), entities.get('user'))
    print(f"  -> Fetched {len(social_media_info)} posts.")

    # 3. Get market data
    print("Step 3: Fetching market data...")
    market_data = get_market_data_from_user(entities.get('product'))
    if not market_data:
        return {
            "suggestion": "Could not proceed without market data. Please try again.",
            "reasoning": {}
        }
    print(f"  -> Fetched data for {market_data.get('product')}")

    # 4. Generate final suggestion
    print("Step 4: Generating final investment suggestion...")
    final_suggestion = generate_investment_suggestion_with_llm(entities, social_media_info, market_data)
    print("  -> Suggestion generated.")

    # Return the final suggestion and the reasoning data for the frontend
    return {
        "suggestion": final_suggestion,
        "reasoning": {
            "extracted_entities": entities,
            "social_media_posts": social_media_info,
            "market_data": market_data
        }
    }

if __name__ == '__main__':
    # Example usage:
    # user_query = "What do you think about BTC? I saw Trump tweeted something about it on Twitter."
    user_query = "I've been seeing a lot of buzz around Bitcoin lately. Donald Trump mentioned it on X recently. What's the latest on OKX for BTC?"
    
    result = get_investment_suggestion(user_query)

    print("\n--- Final Result ---")
    print("\n[Investment Suggestion]")
    print(result['suggestion'])

    print("\n[Reasoning Data for Frontend]")
    print(json.dumps(result['reasoning'], indent=2))