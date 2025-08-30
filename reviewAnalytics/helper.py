import os
import json

from litellm import completion
from dotenv import load_dotenv

def _get_credentials():
    """
    (Internal Helper) Load the crendentials required to run the LLM
    """
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    custom_endpoint = os.getenv("CUSTOM_ENDPOINT")

    os.environ["OPENAI_API_KEY"] = openai_api_key

    return custom_endpoint

def _perform_completion(system_prompt: str, user_prompt: str, response_format: str = 'json_object') -> any:
    """
    (Internal Helper) Streamlining the process of making a request to the LLM
    
    Args:
      system_prompt (str): A system prompt to specify what the LLM should do
      user_prompt (str): A query made by the user to be given to the LLM
      response_format (str): The format of output for the LLM

    Returns:
      any: A JSON formatted value of the response from the LLM
    """
    custom_endpoint = _get_credentials()

    response = completion(
      model="openai/vllm-qwen3",
      messages=[
        {
          "role": "system",
          "content": system_prompt
        },
        {
          "role": "user",
          "content": user_prompt
        }
      ],
      api_base=custom_endpoint,
      response_format={"type": response_format} 
    )

    return json.loads(response.choices[0].message.content)

def _summarize_and_categorize_review(user_prompt: str) -> any:
    """
    (Internal Helper) Utilize the LLM to get the summary for each review category
    """
    system_prompt = """
    You are a specialized AI model for restaurant review analysis, capable of processing reviews written in both **English and Indonesian**.

    Your primary function is to extract and categorize specific aspects of the dining experience. **Crucially, regardless of the input language of the review, your entire JSON output, including all summary texts, must be written in professional English.**

    You must focus exclusively on the following four English categories:
    1.  **Ambience**: The atmosphere, decor, cleanliness, and overall environment of the restaurant.
    2.  **Food**: The taste, quality, presentation, and portion size of the dishes.
    3.  **Price**: Comments related to value, cost, and whether the experience was worth the money.
    4.  **Service**: The friendliness, attentiveness, speed, and professionalism of the staff.

    Your response MUST be a single, valid JSON object and nothing else. Do not include any explanatory text before or after the JSON.

    The JSON object should have a key for each category. For each category, provide:
    - A boolean `mentioned` flag.
    - A `summary` (in English) of the reviewer's comments on that topic.

    If a category is not mentioned in the review, set `mentioned` to false, `summary` to null, and `sentiment` to "Neutral".
    """

    response = _perform_completion(system_prompt, user_prompt)

    return response

def _categorize_aspects_of_food_review(user_prompt: str) -> any:
    """
    (Internal Helper) Utilize the LLM to get detailed review for each menu getting reviewed
    """
    system_prompt_1 = """
    You are an AI assistant that extracts menu items from a text. Read the review and identify all unique food and drink items mentioned.

    Your response must be ONLY a valid JSON object. This object must contain a single key named "menus", and its value must be an array of strings representing the identified food items.

    For example, if the foods are 'Pizza' and 'Coke', the output should be:
    {"menus": ["Pizza", "Coke"]}
    """

    system_prompt_2 = """
    You are a highly detailed Food Review Analyst AI. You are capable of processing reviews in both English and Indonesian, but your entire output must be in professional English.

    The user will provide a full review and a list of specific menu items to analyze. Your task is to analyze the review and extract all feedback for ONLY the items in the provided list.

    **Your Final Output MUST BE a single JSON object with the following structure:**
    - The **keys** of the object must be the exact, case-sensitive names of the food items from the provided list.
    - The **value** for each food key must be an array of feedback objects.
    - If a food item from the list is not mentioned in the review, its value should be an empty array `[]`.

    Each feedback object in the array must contain three keys: `aspect`, `summary`, and `sentiment` ("Positive", "Negative", or "Neutral").

    **Example:**
    If the user provides a review and the list `["Nasi Goreng Gila", "Es Teh Manis"]`, your output should be a JSON object like this:
    ```json
    {
    "Nasi Goreng Gila": [
        {
        "aspect": "Taste & Flavor",
        "summary": "The taste was good and the spiciness level was just right.",
        "sentiment": "Positive"
        },
        {
        "aspect": "Portion Size",
        "summary": "The portion was a bit small for the price.",
        "sentiment": "Negative"
        }
    ],
    "Es Teh Manis": [
        {
        "aspect": "Taste",
        "summary": "The taste was standard and weak because of too much ice.",
        "sentiment": "Negative"
        }
    ]
    }
    """

    response_1 = _perform_completion(system_prompt_1, user_prompt)

    adjusted_user_prompt = f"""
    Full Review:
    \"\"\"
    {user_prompt}
    \"\"\"

    Analyze feedback for the following menu items:
    {response_1['menus']}
    """

    response_2 = _perform_completion(system_prompt_2, adjusted_user_prompt)
        
    return response_2