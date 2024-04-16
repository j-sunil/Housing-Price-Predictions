import logging
from src.data_etl import data_etl, preprocess_data
from src.model import custom_train_test_split, train, save_model


TRAIN_DATA = r'\housing_price_prediction\data\raw_housing.csv'
RANDOM_STATE = 100
SAVE_MODEL = r'\housing_price_prediction\models\model.joblib'
log_file_path = r'\housing_price_prediction\data\housing_prediction.log'


def main(TRAIN_DATA, RANDOM_STATE, SAVE_MODEL, log_file_path):
    try:
        logging.basicConfig(filename=log_file_path, level=logging.INFO)

        logging.info('Performing data ETL...')
        df_refined = data_etl(TRAIN_DATA)
        X, y = preprocess_data(df_refined)

        logging.info('Performing custom train-test split...')
        X_train, X_test, y_train, y_test = custom_train_test_split(X, y, RANDOM_STATE)

        logging.info('Training the model...')
        regr = train(X_train, y_train)

        logging.info('Saving the model...')
        save_model(regr, SAVE_MODEL)

        logging.info('Model training and saving completed successfully.')

    except Exception as e:
        # Log any exceptions
        logging.exception("An error occurred: {}".format(str(e)))

main(TRAIN_DATA, RANDOM_STATE, SAVE_MODEL, log_file_path)
