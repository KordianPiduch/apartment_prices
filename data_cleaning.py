import pandas as pd
import numpy as np

RAW_PATH = './data/raw/otodom.csv'
OUTPUT_PATH = 'data/processed/otodom_cleaned.csv'


def read_data(path):
    df = pd.read_csv(path, index_col=0)
    return df


def save_data(df, path):
    df.reset_index(drop=True, inplace=True)
    df.to_csv(path)


def clean_floor_column(series):
    # delete unnecessary text and replace some symbols
    s = series.str.replace('Piętro\n', '')
    s = s.str.replace("parter", '0').str.replace('suterena', '-0.5').str.replace("> ", '')
    s = s.replace("zapytaj", np.nan)
    s = s.str.replace('poddasze', 'p')

    # for values without max floor in building add / at the end of the string
    s1 = s[~s.isna()]
    s1 = s1[~s1.str.contains('/')].apply(lambda x: x + '/')
    s[s1.index] = s1
    return s


def get_district_by_street(df):
    steet_district = {
        "górskiego": "Wzgórze Św. Maksymiliana",
        "przebendowskich": "Orłowo",
        "dembińskiego": "Grabówek",
        "morska": "Chylonia",
        "zygmuntowska": "Śródmieście",
        "zwycięstwa": "Orłowo"
    }

    df['street'] = df.loc[df.district == "Gdynia", 'street'].apply(lambda x: x.replace('ul. ', '').strip())

    for street, district in steet_district.items():
        df.loc[(~df.street.isna()) & (df.street.str.lower().str.contains(street)), 'district'] = district

    df.loc[df.district == "Gdynia", "district"] = np.nan

    return df


def clean_columns(df):
    # Drop unnecessary columns
    df.drop('title', axis=1, inplace=True)

    # Make some NaN
    df = df.replace('zapytaj', np.nan)
    df = df.replace('brak', np.nan)
    df = df.replace('-1', np.nan)

    # Area
    df["area_m2"] = df["area_m2"].str.replace(',', '.').astype(float)

    # Rooms
    df["rooms"] = df['rooms'].apply(lambda x: x if str(x).isdecimal() else np.nan).astype(float)

    # Price per square meters to float
    df['price_m2'] = df['price_m2'].str[:-5].str.replace(' ', '').astype(float)

    # Total price
    df['price'] = df['price']\
        .replace('Zapytaj o cenę', np.nan)\
        .str.replace('zł', 'pln')\
        .str.replace(' ', '').str.replace(',', '.')

    df['currency'] = df.price[~df.price.isna()].apply(lambda x: x[-3:].lower())
    df['price'] = df.price[~df.price.isna()].apply(lambda x: x[:-3]).astype(float)

    df.loc[df['currency'] == 'eur', 'price'] = df['price_m2'] * df['area_m2']  # change price from eur to pln
    df.drop('currency', axis=1, inplace=True)  # drop helping column

    # Floor
    df['floor'] = clean_floor_column(df.floor)

    # Separate data from floor column into two columns with floor and max floor data
    df['max_floor'] = df['floor'][~df.floor.isna()].apply(lambda x: x.split('/')[1])
    df['floor'] = df['floor'][~df.floor.isna()].apply(lambda x: x.split('/')[0])
    df = df.replace('', np.nan)

    # Replace text value with number (p - poddasze)
    df.loc[df['floor'] == 'p', 'floor'] = df['max_floor']
    df['floor'] = df['floor'].astype(float)
    df['max_floor'] = df['max_floor'].astype(float)

    # Outdoors
    df['balcony'] = df['outdoors'].apply(lambda x: 1 if 'balkon' in str(x) else 0)
    df['backyard'] = df['outdoors'].apply(lambda x: 1 if 'ogródek' in str(x) else 0)
    df['terrace'] = df['outdoors'].apply(lambda x: 1 if 'taras' in str(x) else 0)
    df.drop('outdoors', axis=1, inplace=True)

    # Parking
    df['parking'] = df['parking'].apply(lambda x: 1 if str(x) == 'garaż/miejsce parkingowe' else 0)

    # Build year
    df['build_yr'] = df['build_yr'].astype(float)
    df['build_yr'] = df['build_yr'].apply(lambda x: x if 1500 < x < 2050 else np.nan)

    # Building age
    df['building_age'] = 2022 - df['build_yr']
    df['building_age'] = df['building_age'].apply(lambda x: x if -10 < x < 1500 else np.nan)

    # Elevator
    df['elevator'] = df['elevator'].map({'nie': 0, 'tak': 1})

    # Get district data from address
    df['district'] = df.loc[~df.address.isna(), 'address'].apply(lambda x: x.split(',')[1].strip())

    # Lack of street or district information
    df['district'] = df['district'].replace('pomorskie', np.nan)

    # Records with street, without district information:
    _ = df.loc[df.district == 'Gdynia', ['address', 'district']]
    df['street'] = df.loc[_.index, 'address'].apply(lambda x: x.split(',')[0].strip())

    # Drop all apartment without price and price per square meters
    df_na = df.loc[df.price.isna() & df.price_m2.isna()]
    df.drop(df_na.index, axis=0, inplace=True)

    # Apartments without a price
    df.loc[df.price.isna(), 'price'] = df['price_m2'] * df['area_m2']

    # OPTIONAL
    df = get_district_by_street(df)

    return df


def clean_data():
    df = read_data(RAW_PATH)
    df = clean_columns(df)
    save_data(df, OUTPUT_PATH)


if __name__ == '__main__':
    clean_data()
