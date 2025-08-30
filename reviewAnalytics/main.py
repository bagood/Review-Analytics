import os

from warnings import simplefilter
simplefilter('ignore')

from reviewAnalytics.helper import _get_credentials, _summarize_and_categorize_review

def summarize_and_categorize_review(review_text):
    openai_api_key, custom_endpoint = _get_credentials()

    os.environ["OPENAI_API_KEY"] = openai_api_key

    response = _summarize_and_categorize_review(review_text, custom_endpoint)

    return response