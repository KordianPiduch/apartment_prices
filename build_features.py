import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


FEATURES = ['area_m2', 'rooms', 'build_yr', 'parking', 'terrace', 'district', 'market', 'building_type']
TARGET = 'price'


def build_features(df, features, target):
    X = df[features]
    y = df[target]

    X['district'] = X['district'].astype('category')
    X['market'] = X['market'].astype('category')
    X['building_type'] = X['building_type'].astype('category')

    return X, y


def split_sets(X, y, test_size=0.2):
    attr_num = X.select_dtypes(include='number').columns
    attr_cat = X.select_dtypes(exclude='number').columns

    pipeline_num = Pipeline(
        [
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]
    )

    pipeline_cat = Pipeline(
        [
            ('imputer', SimpleImputer(strategy="most_frequent")),
            ('ohe', OneHotEncoder(sparse=False)),
        ]
    )

    pipeline_full = ColumnTransformer(
        [
            ('numeric', pipeline_num, attr_num),
            ('category', pipeline_cat, attr_cat)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=test_size)

    X_train_tr = pd.DataFrame(
        data=pipeline_full.fit_transform(X_train),
        columns=pipeline_full.get_feature_names_out()
    )
    X_test_tr = pd.DataFrame(
        data=pipeline_full.transform(X_test),
        columns=pipeline_full.get_feature_names_out()
    )

    return X_train_tr, X_test_tr, y_train, y_test


def build_data_sets(df, features=FEATURES, target=TARGET):
    X, y = build_features(df, features, target)
    return split_sets(X, y)
