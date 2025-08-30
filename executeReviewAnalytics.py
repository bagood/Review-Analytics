import pandas as pd

from reviewAnalytics.main import summarize_and_categorize_review, categorize_aspects_of_food_review

data = pd.read_csv('database/food_review_data.csv')

summarized_data = summarize_and_categorize_review(data, 'restaurant_review')
summarized_data.to_csv('database/summarized_food_review_data.csv', index=False)

detailed_food_review = categorize_aspects_of_food_review(summarized_data)
detailed_food_review.to_csv('database/detailed_food_review.csv', index=False)