import logging
from sqlalchemy import create_engine

log_file_path = r'\housing_price_prediction\data\housing_prediction.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO)
def push_dataframe_to_db(df, table_name, log_file_path):
    try:
        hostname = "hostname"
        database = "database"
        username = "username"
        port = port
        password = "password"

        engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}")

        conn = engine.connect()

        df.to_sql(table_name, engine, if_exists='append', index=False)

        logging.info(f"Data pushed to {table_name} table successfully.")

    except Exception as e:
        logging.exception(f"An error occurred while pushing data to the database: {str(e)}")

    finally:
        if conn is not None:
            conn.close()




