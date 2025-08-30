import pandas as pd

from dataCollection.main import get_restaurant_reviews

all_restaurant_name = [
    'Sushi Groove',
    "The People's Cafe",
    'Tokyo Belly', 
    'Pizza e Birra' 
]

entire_reviews = pd.DataFrame()

for restaurant_name in all_restaurant_name:
    try:
        all_reviews = get_restaurant_reviews(restaurant_name)
        entire_reviews = pd.concat((entire_reviews, all_reviews))
    except:
        pass
    break

entire_reviews.reset_index(drop=True, inplace=True)
entire_reviews.to_csv('database/food_review_data.csv', index=False)