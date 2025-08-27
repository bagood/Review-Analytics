import re
import time
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

def _get_url_for_all_restaurant(restaurant_name):
    driver = webdriver.Chrome()

    formatted_rest_name = restaurant_name.replace(' ', '+')
    target_url = f'https://pergikuliner.com/restaurants?utf8=%E2%9C%93&search_place=&default_search=&search_name_cuisine={formatted_rest_name}'
    driver.get(target_url)
    
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    all_restaurant_best_rating = driver.find_elements(By.XPATH, "//div[@class='restaurant-result-wrapper best-rating']")
    all_restaurant_good_rating = driver.find_elements(By.XPATH, "//div[@class='restaurant-result-wrapper good-rating']")
    all_restaurant_rating = all_restaurant_best_rating + all_restaurant_good_rating
    
    all_urls = []
    for restaurant_rating in all_restaurant_rating:
        item_name = restaurant_rating.find_elements(By.XPATH, "//a")
        all_urls.append([val.get_attribute('href') for val in item_name])
    
    all_urls_cleaned = np.unique(np.concatenate(all_urls, axis=0).astype(str))
    
    pattern = r'^https:\/\/pergikuliner\.com\/restaurants\/(?!new\/?$).*'
    restaurant_urls = [re.match(pattern, val).group() for val in all_urls_cleaned if re.match(pattern, val) != None]
        
    driver.close()

    return restaurant_urls

def _get_all_reviews_from_a_restaurant(url_to_restaurant):
    driver = webdriver.Chrome()
    
    driver.get(url_to_restaurant)
    
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    all_restaurant_reviews = driver.find_elements(By.XPATH, "//div[@itemprop='reviewBody']")
    all_restaurant_reviews = [val.text.replace('\n', '') for val in all_restaurant_reviews]
    
    emoji_pattern = r'[^\x20-\x7E]'
    all_restaurant_reviews = [re.sub(emoji_pattern, '', val) for val in all_restaurant_reviews]
    
    driver.close()

    return all_restaurant_reviews