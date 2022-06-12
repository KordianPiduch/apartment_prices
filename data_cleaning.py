import pandas as pd
import numpy as np

# read file from scraper
df = pd.read_csv('../data/raw/otodom.csv', index_col=0, na_values='-1')

# drop unnecessary columns
df.drop('title', axis=1, inplace=True)

# make some NaN
df = df.replace('zapytaj', np.nan)
df = df.replace('brak', np.nan)

# area
df["area_m2"] = df["area_m2"].str.replace(',','.').astype(float) 

# rooms
df["rooms"] = df['rooms'].apply(lambda x: x if str(x).isdecimal() else np.nan).astype(float)  # string "wiecej" replaced with np.nan

# price per square meters to float 
df['price_m2'] = df['price_m2'].str[:-5].str.replace(' ', '').astype(float)


# total price
df['price'] = df['price'].replace('Zapytaj o cenę', np.nan).str.replace('zł', 'pln').str.replace(' ', '').str.replace(',', '.')

df['currency'] = df.price[~df.price.isna()].apply(lambda x: x[-3:].lower())  # helping column
df['price'] = df.price[~df.price.isna()].apply(lambda x: x[:-3]).astype(float)

df[df['currency'] == 'eur']  # only 3 apartments in dataset has price in eur. But we got price per square meter in pln and apartment area.


# change price from eur to pln
df.loc[df['currency'] == 'eur','price'] = df['price_m2'] * df['area_m2']
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
# create new columns: balkon, ogrodek, taras
df['balkon'] = df['outdoors'].apply(lambda x: 1 if 'balkon' in str(x) else 0)
df['ogrodek'] = df['outdoors'].apply(lambda x: 1 if 'ogródek' in str(x) else 0)
df['taras'] = df['outdoors'].apply(lambda x: 1 if 'taras' in str(x) else 0)
df.drop('outdoors', axis=1, inplace=True)

# parking
df['parking'] = df['parking'].apply(lambda x: 1 if str(x) == 'garaż/miejsce parkingowe' else 0)  # there is 'garaz/miejsce parkingowe' or NaN -> all NaN will be 0

# from address column create new column with neighbourhood name
df['dzielnica'] = df.loc[~df.address.isna(), 'address'].apply(lambda x: x.split(',')[1])


# save to csv - file with a lot of NaN values -> still need to be processed
df.to_csv('../data/interim/otodom_interim.csv')