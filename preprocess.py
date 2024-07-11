import numpy as np
import pandas as pd
# import regex as re

data = pd.read_csv('Dog.csv')
data.info()

def preprocess_price(df):

    df = df.dropna(subset = ['breed'])

    df['price'] = df['price'].str.replace(r'[^0-9]+', '', regex = True)
    df['price'] = pd.to_numeric(df['price'])

    df['type_time'] = df['post_time'].str.split()
    df['type'] = df['type_time'].apply(lambda x: ' '.join(x[:3]))
    df['time'] = df['type_time'].apply(lambda x: ' '.join(x[-3:]))
    df.drop(columns=['type_time', 'post_time'], inplace = True)

    df['age'] = df['age'].str.split('(').str[0].str.strip()
    df['size'] = df['size'].str.split('(').str[0].str.strip()
    return df

# pd.set_option('display.max_colwidth', None)
data = preprocess_price(data)
data.to_csv('Preprocessed_Dog.csv', index = False)

print(data.info())

