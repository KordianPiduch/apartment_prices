import numpy as np
import pandas as pd
import pickle
from build_features import build_data_sets
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor


MODEL_CONFIG = {
    'loss': 'absolute_error',
    'max_depth': 4,
    'min_samples_split': 7,
    'n_estimators': 150,
    'random_state': 42
}


def check_model(model, X_train, X_test, y_train, y_test, rounds=2):
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    mae_train = int(mean_absolute_error(y_train, y_pred_train))
    mae_test = int(mean_absolute_error(y_test, y_pred_test))
    r2_train = np.round(r2_score(y_train, y_pred_train),rounds)
    r2_test = np.round(r2_score(y_test, y_pred_test),rounds)

    rmse_train = int(mean_squared_error(y_train, y_pred_train, squared=False))
    rmse_test = int(mean_squared_error(y_test, y_pred_test, squared=False))

    # show results
    print('|', "".center(6), '|', 'train'.center(10), '|', 'test'.center(10), '|')
    print('*', ''.center(6, '-'),'*', ''.center(10,'-'), '*', ''.center(10,'-'), '*')
    print('|', 'MAE'.center(6),'|', str(mae_train).center(10), '|', str(mae_test).center(10), '|')
    print('|', 'R2'.center(6),'|', str(r2_train).center(10), '|', str(r2_test).center(10), '|')
    print('|', 'RMSE'.center(6),'|', str(rmse_train).center(10), '|', str(rmse_test).center(10), '|')
    

def train_model():
    df = pd.read_csv('data/processed/otodom_cleaned.csv', index_col=0)
    X_train, X_test, y_train, y_test = build_data_sets(df=df)

    model = GradientBoostingRegressor(**MODEL_CONFIG)
    model.fit(X_train, y_train)

    # save model
    with open("models/gradient_boosting.pkl", "wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    train_model()
