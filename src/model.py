import logging
import  pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

log_file_path = r'\housing_price_prediction\data\housing_prediction.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def custom_train_test_split(df_features, y, random_state):
    try:
        X_train, X_test, y_train, y_test = train_test_split(df_features, y, test_size=0.2, random_state=random_state)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.exception("An error occurred in custom_train_test_split: {}".format(str(e)))
        return None, None, None, None

def train(X_train, y_train):
    try:
        regr = RandomForestRegressor(max_depth=12)
        regr.fit(X_train, y_train)
        return regr
    except Exception as e:
        logging.exception("An error occurred in train: {}".format(str(e)))
        return None

def save_model(model, filename):
    try:
        with open(filename, 'wb'):
            joblib.dump(model, filename, compress=3)
    except Exception as e:
        logging.exception("An error occurred in save_model: {}".format(str(e)))

def load_model(filename):
    try:
        model = joblib.load(filename)
        return model
    except Exception as e:
        logging.exception("An error occurred in load_model: {}".format(str(e)))
        return None

def predict(X, model):
    try:
        Y = model.predict(X)
        return Y
    except Exception as e:
        logging.exception("An error occurred in predict: {}".format(str(e)))
        return None

def add_predicted_prices(df_refined, y_pred_test):
    predicted_prices_df = pd.DataFrame({'predicted_price': y_pred_test})
    df_with_predictions = pd.concat([df_refined, predicted_prices_df], axis=1)
    return df_with_predictions