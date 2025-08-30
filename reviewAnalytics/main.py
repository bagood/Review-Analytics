import pandas as pd

from warnings import simplefilter
simplefilter('ignore')

from reviewAnalytics.helper import _summarize_and_categorize_review, _categorize_aspects_of_food_review

def summarize_and_categorize_review(data: pd.DataFrame, review_column: str) -> pd.DataFrame:
    """
    A pipeline for summarizing ech review category for all reviews

    Args:
        data (pd.DataFrame): A data containing all the reviews for all restaurants
        review_column (str): The name of the column containing the review

    Returns:
        pd.DataFrame: A data cotaining the summary for all review category
    """
    all_reviews = data[review_column].values
    review_data = pd.DataFrame()
    for review in all_reviews:
        response = _summarize_and_categorize_review(review)
        
        temp_review_data = pd.DataFrame()
        for category in response.keys():
            for sub_category, val in response[category].items():
                temp_review_data[f'{category} - {sub_category}'] = [val]
        
        review_data = pd.concat((review_data, temp_review_data))
        
    review_data.reset_index(drop=True, inplace=True)

    return pd.merge(data, review_data, left_index=True, right_index=True, how='inner')

def categorize_aspects_of_food_review(data: pd.DataFrame) -> pd.DataFrame:
    """
    A pipeline for getting in-depth detail for each menu that has been reviewed

    Args:
        data (pd.DataFrame): A data containing the summary for each review category

    Returns:
        pd.DataFrame: A data containing in-depth review for ecah menu
    """
    data.dropna(subset='Food - summary', inplace=True)
    all_menu_reviewed = pd.DataFrame()

    for summary, restaurant, restaurant_location in zip(data['Food - summary'].values, data['restaurant_name'].values, data['review_source'].values):
        response = _categorize_aspects_of_food_review(summary)

        for menu, feedbacks in response.items():
            menu_reviewed = pd.DataFrame(feedbacks)
            menu_reviewed['menu'] = menu
            menu_reviewed['restaurant'] = restaurant
            menu_reviewed['restaurant_location'] = restaurant_location

            all_menu_reviewed = pd.concat((all_menu_reviewed, menu_reviewed))

    all_menu_reviewed.reset_index(drop=True, inplace=True)
    
    return all_menu_reviewed