import pandas as pd

from warnings import simplefilter
simplefilter('ignore')

from dataCollection.helper import _get_url_for_all_restaurant, _get_all_reviews_from_a_restaurant

def get_restaurant_reviews(restaurant_name):
    all_reviews = pd.DataFrame()

    restaurant_urls = _get_url_for_all_restaurant(restaurant_name)
    for rest_url in restaurant_urls:
        all_restaurant_reviews = _get_all_reviews_from_a_restaurant(rest_url)
        temp_all_reviews = pd.DataFrame()
        temp_all_reviews['restaurant_review'] = all_restaurant_reviews
        temp_all_reviews['restaurant_name'] = restaurant_name
        temp_all_reviews['review_source'] = rest_url
        
        all_reviews = pd.concat((all_reviews, temp_all_reviews))

    all_reviews.reset_index(drop=True, inplace=True)

    return all_reviews