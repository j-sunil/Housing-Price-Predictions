import logging
from src.data_etl import data_etl, preprocess_data , save_dataframe_to_csv
from src.model import load_model, predict, add_predicted_prices
from src.db import push_dataframe_to_db


log_file_path = r'\housing_price_prediction\data\housing_prediction.log'
VALIDATE_DATA = r'\housing_price_prediction\data\raw_validate.csv'
Refined_Validate_Data = r'\housing_price_prediction\data\Refined_Validate_Data.csv'
Validate_with_Predictions = r'\housing_price_prediction\data\Validate_with_Predictions.csv'
MODEL_NAME = r'\housing_price_prediction\models\model.joblib'

def validate_data(VALIDATE_DATA, MODEL_NAME, log_file_path):
    try:
        logging.basicConfig(filename=log_file_path, level=logging.INFO)

        logging.info('ETL of data ...')
        df_refined = data_etl(VALIDATE_DATA)

        logging.info('saving df_refined as csv without predictions in local system ...')
        save_dataframe_to_csv(df_refined , Refined_Validate_Data)

        logging.info('Pushing housing data without predictions to db...')
        table_name = "refined_housing"
        push_dataframe_to_db(df_refined, table_name, log_file_path)

        logging.info('Preprocessing of data...')
        X, y = preprocess_data(df_refined)

        logging.info('Loading the model...')
        model = load_model(MODEL_NAME)

        logging.info('Calculating test dataset predictions...')
        y_pred_test = predict(X, model)

        logging.info('Creating final dataset with predictions...')
        df_housing_pred = add_predicted_prices(df_refined, y_pred_test)
        print(df_housing_pred)

        logging.info('saving df_housing_pred as csv with predictions in local system ...')
        save_dataframe_to_csv(df_housing_pred, Validate_with_Predictions)

        logging.info('Pushing housing data with predictions to db...')
        table_name = "housing_prediction"
        push_dataframe_to_db(df_housing_pred, table_name , log_file_path)
        return df_housing_pred

    except Exception as e:
        logging.exception("An error occurred: {}".format(str(e)))
        return None


validate_data(VALIDATE_DATA, MODEL_NAME, log_file_path)
