import numpy as np
import pandas as pd
import streamlit as st

from helper import _agg_on_mentioned_data, _agg_on_sentiment_data, _process_and_display_sentiment_percentage, _display_sentiments_data, _display_bar_chart

review_data = pd.read_csv('database/summarized_food_review_data.csv')
food_review_data = pd.read_csv('database/detailed_food_review.csv')

agg_mentioned_restaurant_name = _agg_on_mentioned_data(review_data, 'restaurant_name')
agg_mentioned_review_source = _agg_on_mentioned_data(review_data, 'review_source')
agg_sentiment_restaurant_name = _agg_on_sentiment_data(review_data, 'restaurant_name')
agg_sentiment_review_source = _agg_on_sentiment_data(review_data, 'review_source')

tab1, tab2 = st.tabs(["Restaurant Performance", "Food Review"])

with tab1:
    selected_restaurant = st.selectbox("Select a Restaurant", review_data['restaurant_name'].unique())
    st.header('Percentage of Sentiments for Each Review Category')
    fig_percentage = _process_and_display_sentiment_percentage(agg_sentiment_restaurant_name[agg_sentiment_restaurant_name.index == selected_restaurant])
    st.plotly_chart(fig_percentage)

    st.header('Review Aspects on A Restaurant')
    all_review_source_mention = review_data.loc[review_data['restaurant_name'] == selected_restaurant, 'review_source']
    st.dataframe(agg_mentioned_review_source.loc[agg_mentioned_review_source.index.isin(all_review_source_mention), :])

    st.header('Sentiments for each Review Aspects')
    all_review_source_sentiment = review_data.loc[review_data['restaurant_name'] == selected_restaurant, 'review_source']
    positive_data, negative_data, neutral_data = _display_sentiments_data(agg_sentiment_review_source, all_review_source_sentiment)
    st.subheader('Positive Sentiments')
    st.dataframe(positive_data)
    st.subheader('Negative Sentiments')
    st.dataframe(negative_data)
    st.subheader('Neutral Sentiments')
    st.dataframe(neutral_data)

with tab2:
    st.header('Sentiment Percentage for Each Menu Item')
    selected_restaurant = st.selectbox("Select a Restaurant ", review_data['restaurant_name'].unique())
    fig = _display_bar_chart(food_review_data, selected_restaurant)
    st.plotly_chart(fig)

    st.header('In-Depth Review for a Menu Item')
    selected_menu = st.selectbox("Select a menu", food_review_data.loc[food_review_data['restaurant'] == selected_restaurant, 'menu'].unique())
    menu_detailed_review = food_review_data.loc[
            np.all((food_review_data['restaurant'] == selected_restaurant, food_review_data['menu'] == selected_menu), axis=0)
        ] \
        .drop(columns=['menu', 'restaurant']) \
        .reset_index(drop=True)

    menu_detailed_review
