import pandas as pd

from warnings import simplefilter
simplefilter('ignore')

from reviewAnalytics.helper import _summarize_and_categorize_review, _categorize_aspects_of_food_review

def summarize_and_categorize_review(data, review_column):
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

def categorize_aspects_of_food_review(data):
    data.dropna(subset='Food - summary', inplace=True)
    all_menu_reviewed = pd.DataFrame()

    for summary, restaurant in zip(data['Food - summary'].values, data['restaurant_name'].values):
        response = _categorize_aspects_of_food_review(summary)

        for menu, feedbacks in response.items():
            menu_reviewed = pd.DataFrame(feedbacks)
            menu_reviewed['menu'] = menu
            menu_reviewed['restaurant'] = restaurant

            all_menu_reviewed = pd.concat((all_menu_reviewed, menu_reviewed))

    all_menu_reviewed.reset_index(drop=True, inplace=True)
    
    return all_menu_reviewed