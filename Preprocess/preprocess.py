import numpy as np
import pandas as pd
import regex as re

data = pd.read_csv('Dog.csv')
data.info()

def preprocess(df):

    df = df.dropna(subset = ['breed'])

    df['price'] = df['price'].str.replace(r'[^0-9]+', '', regex = True)
    df['price'] = pd.to_numeric(df['price'])

    df['type_time'] = df['post_time'].str.split()
    df['type'] = df['type_time'].apply(lambda x: ' '.join(x[:3]))
    df['time'] = df['type_time'].apply(lambda x: ' '.join(x[-3:]))
    df.drop(columns=['type_time', 'post_time'], inplace = True)

    df['age'] = df['age'].str.split('(').str[0].str.strip()
    df['size'] = df['size'].str.split('(').str[0].str.strip()
    
    df['district'] = df['address'].apply(lambda x: re.search(r'Quận\s[\w\s]+', x).group(0) if re.search(r'Quận\s[\w\s]+', x) else None)
    city_regex = r'( TP HCM| Thành Phố Hồ Chí Minh| TP Hồ Chí Minh)'
    df['district'] = df['district'].str.replace(city_regex, '', regex = True)
    return df

# pd.set_option('display.max_colwidth', None)
data = preprocess(data)
data.to_csv('Preprocessed_Dog.csv', index = False)

print(data.info())
# print(data['district'].value_counts())

