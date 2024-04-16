import logging
import pandas as pd
import numpy as np

log_file_path = r'\housing_price_prediction\data\housing_prediction.log'

logging.basicConfig(filename=log_file_path, level=logging.INFO)

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def data_etl(path):
    try:
        column_mapping = {
            'LONGITUDE': 'longitude',
            'LAT': 'latitude',
            'MEDIAN_AGE': 'housing_median_age',
            'ROOMS': 'total_rooms',
            'BEDROOMS': 'total_bedrooms',
            'POP': 'population',
            'HOUSEHOLDS': 'households',
            'MEDIAN_INCOME': 'median_income',
            'OCEAN_PROXIMITY': 'ocean_proximity',
            'MEDIAN_HOUSE_VALUE': 'median_house_value'
        }

        schema = {
            'longitude': 'float64',
            'latitude': 'float64',
            'housing_median_age': 'float64',
            'total_rooms': 'float64',
            'total_bedrooms': 'float64',
            'population': 'float64',
            'households': 'float64',
            'median_income': 'float64',
            'median_house_value': 'float64',
            'ocean_proximity': 'object'
        }

        df = pd.read_csv(path)

        selected_columns = [col for col in column_mapping.keys() if col in df.columns]
        df_selected = df.loc[:, selected_columns]

        df_selected = df_selected.rename(columns=column_mapping)

        schema = {col: dtype for col, dtype in schema.items() if col in df_selected.columns}

        df_selected.replace({'': np.nan, 'NA': np.nan, 'None': np.nan, 'Null': np.nan}, inplace=True)

        df_dropna = df_selected.dropna(axis=0)

        for col, dtype in schema.items():
            df_dropna[col] = df_dropna[col].astype(dtype)

        df_refined = df_dropna.copy()

        return df_refined
    except Exception as e:
        logging.exception("An error occurred in data_etl: {}".format(str(e)))
        return None

def preprocess_data(df_refined):
    try:
        df_dummies = pd.get_dummies(df_refined['ocean_proximity'])

        column_mapping = {
            '<1H OCEAN': 'ocean_proximity_<1H OCEAN',
            'INLAND': 'ocean_proximity_INLAND',
            'ISLAND': 'ocean_proximity_ISLAND',
            'NEAR BAY': 'ocean_proximity_NEAR BAY',
            'NEAR OCEAN': 'ocean_proximity_NEAR OCEAN'
        }

        for key in column_mapping.keys():
            if key not in df_dummies.columns:
                df_dummies[column_mapping[key]] = False

        df_dummies.rename(columns=column_mapping, inplace=True)

        columns_to_drop = set(df_dummies.columns) - set(column_mapping.values())
        df_dummies.drop(columns=columns_to_drop, inplace=True)

        df_refined_with_dummies = pd.concat([df_refined, df_dummies], axis='columns')

        df_refined_with_dummies.drop(columns=['ocean_proximity'], inplace=True)

        if 'median_house_value' in df_refined_with_dummies.columns:
            df_features = df_refined_with_dummies.drop(['median_house_value'], axis=1)
            y = df_refined_with_dummies['median_house_value'].values
            return df_features, y
        else:
            return df_refined_with_dummies.copy(), None
    except Exception as e:
        logging.exception("An error occurred in preprocess_data: {}".format(str(e)))
        return None, None

def save_dataframe_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"DataFrame saved to {file_path} successfully.")
    except Exception as e:
        logging.exception(f"An error occurred while saving the DataFrame to CSV: {str(e)}")
