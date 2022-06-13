import pandas as pd
import numpy as np

# read file from scraper
df = pd.read_csv('./data/raw/otodom.csv', index_col=0, na_values='-1')

# drop unnecessary columns
df.drop('title', axis=1, inplace=True)

# make some NaN
df = df.replace('zapytaj', np.nan)
df = df.replace('brak', np.nan)

# area
df["area_m2"] = df["area_m2"].str.replace(',', '.').astype(float)

# rooms
df["rooms"] = df['rooms'].apply(lambda x: x if str(x).isdecimal() else np.nan).astype(float)

# price per square meters to float 
df['price_m2'] = df['price_m2'].str[:-5].str.replace(' ', '').astype(float)

# total price
df['price'] = df['price']\
    .replace('Zapytaj o cenę', np.nan)\
    .str.replace('zł', 'pln')\
    .str.replace(' ', '').str.replace(',', '.')

df['currency'] = df.price[~df.price.isna()].apply(lambda x: x[-3:].lower())  # helping column
df['price'] = df.price[~df.price.isna()].apply(lambda x: x[:-3]).astype(float)

df_eur = df[df['currency'] == 'eur']  # only 3 apartments in dataset has price in eur.

df.loc[df['currency'] == 'eur', 'price'] = df['price_m2'] * df['area_m2']  # change price from eur to pln
df.drop('currency', axis=1, inplace=True)  # drop helping column


# floor
def make_floor(series):
    # delete unnecessary text and replace some symbols 
    s = series.str.replace('Piętro\n', '')
    s = s.str.replace("parter", '0').str.replace('suterena', '-0.5').str.replace("> ", '')
    s = s.replace("zapytaj", np.nan)
    s = s.str.replace('poddasze', 'p')

    # for values without max floor in building add / at the end of the string
    s1 = s[~s.isna()]
    s1 = s1[~s1.str.contains('/')].apply(lambda x: x+'/')
    s[s1.index] = s1
    return s


df['floor'] = make_floor(df.floor)

# divide floor column to floor and max floor column 
df['max_floor'] = df['floor'][~df.floor.isna()].apply(lambda x: x.split('/')[1])
df['floor'] = df['floor'][~df.floor.isna()].apply(lambda x: x.split('/')[0])
df = df.replace('', np.nan)

# replace text value with number (p - poddasze)
df.loc[df['floor'] == 'p', 'floor'] = df['max_floor']
df['floor'] = df['floor'].astype(float)
df['max_floor'] = df['max_floor'].astype(float)

# outdoors
df['balcony'] = df['outdoors'].apply(lambda x: 1 if 'balkon' in str(x) else 0)
df['backyard'] = df['outdoors'].apply(lambda x: 1 if 'ogródek' in str(x) else 0)
df['terrace'] = df['outdoors'].apply(lambda x: 1 if 'taras' in str(x) else 0)
df.drop('outdoors', axis=1, inplace=True)

# parking
df['parking'] = df['parking'].apply(lambda x: 1 if str(x) == 'garaż/miejsce parkingowe' else 0)

# build year
df['build_yr'] = df['build_yr'].astype(float)

# building age
df['building_age'] = 2022 - df['build_yr']

# elevator
df['elevator'] = df['elevator'].map({'nie': 0, 'tak': 1})

# get district data from address
df['district'] = df.loc[~df.address.isna(), 'address'].apply(lambda x: x.split(',')[1].strip())

# lack of street or district information
d1 = df.loc[df.district == 'pomorskie', ['address', 'district']]
df['district'] = df['district'].replace('pomorskie', np.nan)

# records with street, without district information:
d2 = df.loc[df.district == 'Gdynia', ['address', 'district']]
df['street'] = df.loc[d2.index, 'address'].apply(lambda x: x.split(',')[0].strip())
# OPTIONAL: manually / by hand we can get district based on street

# all apartment without price and price per square meters to drop
df_na = df.loc[df.price.isna() & df.price_m2.isna()]
df.drop(df_na.index, axis=0, inplace=True)

# apartments without a price
df.loc[df.price.isna(), 'price'] = df['price_m2'] * df['area_m2']

df.reset_index(drop=True, inplace=True)

df.to_csv('data/interim/otodom_interim.csv')