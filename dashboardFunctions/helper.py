import pandas as pd
import plotly.express as px

def _agg_on_mentioned_data(data, column_to_agg):
    mentioned_columns = [col for col in data.columns if 'mentioned' in col]
    total_mentions = pd.DataFrame()
    for value in data[column_to_agg].unique():
        temp_total_mentions = pd.DataFrame()
        temp_total_mentions[column_to_agg] = [value]
        for col in mentioned_columns:
            temp_total_mentions[col] = data.loc[data[column_to_agg] == value, col].sum()
    
        total_mentions = pd.concat((total_mentions, temp_total_mentions))
    
    total_mentions.set_index(column_to_agg, inplace=True)
    total_mentions.columns = [col.strip().split('-')[0] for col in total_mentions]
 
    return total_mentions

def _agg_on_sentiment_data(data, column_to_agg):
    sentiment_columns = [col for col in data.columns if 'sentiment' in col]
    total_sentiments = pd.DataFrame()
    for value in data[column_to_agg].unique():
        temp_total_sentiments = pd.DataFrame()
        temp_total_sentiments[column_to_agg] = [value]
        for col in sentiment_columns:
            agg_data = data.loc[data[column_to_agg] == value, :]
            temp_total_sentiments[f'{col} - Positive'] = [len(agg_data.loc[agg_data[col] == 'Positive', :])]
            temp_total_sentiments[f'{col} - Negative'] = [len(agg_data.loc[agg_data[col] == 'Negative', :])]
            temp_total_sentiments[f'{col} - Neutral'] = [len(agg_data.loc[agg_data[col] == 'Neutral', :])]
    
        total_sentiments = pd.concat((total_sentiments, temp_total_sentiments))

    total_sentiments.set_index(column_to_agg, inplace=True)
    total_sentiments.columns = [col.replace(' - sentiment - ', ' ') for col in total_sentiments]

    return total_sentiments

def _process_and_display_sentiment_percentage(df):
    processed_data = []
    categories = ['Ambience', 'Food', 'Price', 'Service']
    
    for category in categories:
        total = df[f'{category} Positive'].sum() + df[f'{category} Negative'].sum() + df[f'{category} Neutral'].sum()
        if total > 0:
            pos_perc = (df[f'{category} Positive'].sum() / total) * 100
            neg_perc = (df[f'{category} Negative'].sum() / total) * 100
            neu_perc = (df[f'{category} Neutral'].sum() / total) * 100
            
            processed_data.append({'Category': category, 'Sentiment': 'Positive', 'Percentage': pos_perc})
            processed_data.append({'Category': category, 'Sentiment': 'Negative', 'Percentage': neg_perc})
            processed_data.append({'Category': category, 'Sentiment': 'Neutral', 'Percentage': neu_perc})


    df_processed = pd.DataFrame(processed_data)
    
    fig = px.bar(
        df_processed,
        x='Percentage',
        y='Category',
        color='Sentiment',
        orientation='h',
        labels={
            'Percentage': 'Percentage of Reviews (%)',
            'Category': 'Review Category'
        },
        color_discrete_map={
            'Positive': 'mediumseagreen',
            'Negative': '#ff6961',
            'Neutral': 'lightgray'
        }
    )

    return fig

def _display_sentiments_data(data, index_filter):
    positive_data = data.loc[data.index.isin(index_filter), [col for col in data.columns if 'Positive' in col]]
    positive_data.columns = [col.split(' ')[0] for col in positive_data.columns]

    negative_data = data.loc[data.index.isin(index_filter), [col for col in data.columns if 'Negative' in col]]
    negative_data.columns = [col.split(' ')[0] for col in negative_data.columns]
    
    neutral_data = data.loc[data.index.isin(index_filter), [col for col in data.columns if 'Neutral' in col]]
    neutral_data.columns = [col.split(' ')[0] for col in neutral_data.columns]

    return positive_data, negative_data, neutral_data

def _display_bar_chart(data, restaurant_name):
    data_to_display = (data.loc[data['restaurant'] == restaurant_name, :] \
                            .groupby('menu')['sentiment'] \
                            .value_counts('sentiment') * 100) \
                            .to_frame('Percentage (%)') \
                            .reset_index()

    fig = px.bar(
        data_to_display,
        y='menu',
        x='Percentage (%)',
        color='sentiment',
        color_discrete_map={
            'Positive': 'mediumseagreen',
            'Negative': '#ff6961'
        },
        labels={
            'Percentage (%)': 'Percentage Score',
            'menu': 'Menu Item'
            }
        )
    
    return fig
