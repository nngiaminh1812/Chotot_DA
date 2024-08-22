from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
import requests
from bs4 import BeautifulSoup
import urllib.robotparser
import numpy as np
import pandas as pd

# rp = urllib.robotparser.RobotFileParser()
# rp.set_url('https://www.chotot.com/mua-ban-cho-tp-ho-chi-minh/robots.txt')
# rp.read()

url = 'https://www.chotot.com/mua-ban-cho-tp-ho-chi-minh'
# rp.can_fetch('*', url)

def crawl_one_dog(link):
    print('https://www.chotot.com' + link)
    driver = webdriver.Firefox()
    try:
        driver.get('https://www.chotot.com' + link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        price = np.nan
        description = np.nan
        breed = np.nan        
        age = np.nan        
        size = np.nan
        address = np.nan
        post_time = np.nan
        # phone_num = np.nan

        post = soup.find('span', attrs = {'class': 'AdImage_imageCaptionText__ScM56'})
        post_time = post.text if post else np.nan 

        price_tag = soup.find('span', attrs = {'itemprop': 'price'})
        price = price_tag.text if price_tag else np.nan

        description_tag = soup.find('p', attrs = {'class': 'AdDecription_adBody__qp2KG'})
        description = description_tag.text if description_tag else np.nan

        breed_tag = soup.find('span', attrs = {'itemprop': 'pet_breed'})
        breed = breed_tag.text if breed_tag else np.nan

        age_tag = soup.find('span', attrs = {'itemprop': 'pet_age'})
        age = age_tag.text if age_tag else np.nan

        size_tag = soup.find('span', attrs = {'itemprop': 'pet_size'})
        size = size_tag.text if size_tag else np.nan

        address_tag = soup.find('div', attrs={'class':'media-body media-middle AdParam_address__5wp1F'})
        address = address_tag.text if address_tag else np.nan

        # # Click the button to show the phone number
        # driver.execute_script("var element = document.querySelector('.aw__s1cdo2zu'); if (element) element.parentNode.removeChild(element);")
        # button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ShowPhoneButton_icon__wsnZ5')))
        # driver.execute_script("arguments[0].scrollIntoView();", button)
        # button.click()
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # # Wait for the phone number to load (adjust the timeout as needed)
        # phone_num_tag = soup.find('div', attrs = {'class': 'ShowPhoneButton_phoneButton__p5Cvt ShowPhoneButton_phoneClicked__IxuR6'})
        # phone_num = phone_num_tag.text if phone_num_tag else np.nan

        driver.quit()
        return post_time, price, description, breed, age, size, address
    except InvalidArgumentException:
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    finally:
        driver.quit()


df = pd.DataFrame()
param = '?page='
# index_page = 123
index_page = 1
while(True):
    driver = webdriver.Firefox()

    driver.get(url + param + str(index_page))
    print(url + param + str(index_page))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    not_found = soup.find('div', attrs={'class': 'NotFound_content__KtIbC'})
    if not_found is not None:
        print('No more dogs to crawl')
        break
    
    dogs_links = soup.find_all('a', attrs={'class': 'AdItem_adItem__gDDQT'})
    # item_footers = soup.find_all('span', attrs={'class': 'AdItemFooter_item__v9Cg0'})
    # post = [item.text if item else np.nan for item in item_footers]

    driver.quit()

    for i in dogs_links:
        post_time, price, description, breed, age, size, address = crawl_one_dog(i['href'])
        if pd.isna(breed):
            link = np.nan
        else: 
            link = 'https://www.chotot.com' + i['href']

        data = pd.DataFrame({
                'post_time' : [post_time],
                'price': [price],
                'description': [description],
                'breed': [breed],
                'age': [age],
                'size': [size],
                'address': [address],
                'link': [link],
                # 'phone_num': [phone_num]
            })
        df = pd.concat([df, data], axis = 0)    

    index_page += 1

df.to_csv('Dog.csv', index = False)
df.head(10)