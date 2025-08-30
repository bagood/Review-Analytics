import os

from litellm import completion
from dotenv import load_dotenv

def _get_credentials():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    custom_endpoint = os.getenv("CUSTOM_ENDPOINT")

    return openai_api_key, custom_endpoint

def _summarize_and_categorize_review(review_text, custom_endpoint):
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

    response = completion(
      model="openai/vllm-qwen3",
      messages=[
        {
          "role": "system",
          "content": system_prompt
        },
        {
          "role": "user",
          "content": review_text
        }
      ],
      api_base=custom_endpoint,
      response_format={"type": "json_object"} 
    )

    return response.choices[0].message.content