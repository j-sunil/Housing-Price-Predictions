
## Housing Price Prediction

### Overview

The Housing Price Prediction project aims to provide an end-to-end automated solution for cleaning and preparing housing data received from customers in non-standardized formats. The cleaned data is then made available to the data science team for building machine learning models to predict housing prices.


### Project Structure

**Data Pipeline**

![Data_Pipeline](https://github.com/spj1803/Housing_Price_Predictions/assets/112913113/083ac290-a68e-4d4c-8405-63bd0e4716bd)

The project directory structure is as follows:

**data/**

Contains datasets used for model training and prediction.

    housing_prediction.csv: Refined housing dataset for model training.
    raw_housing.csv: Original housing dataset for model training.
    raw_validate.csv: Unstandardized dataset for predicting housing prices.
    Refined_Validate_Data.csv: Refined-Dataset without predicted prices.
    Validate_with_Predictions.csv: Refined-Dataset with predicted prices.

**models/**

Stores trained machine learning models.

    `model.joblib`: Serialized machine learning model.

**src/**

Contains source code files for data processing and model training.

    `__init__.py`: Package initialization file.
    `data_etl.py`: Data extraction, cleaning, and transformation.
    `db.py`: Database interaction and data loading.
    `model.py`: Machine learning model training, saving, development, and evaluation.
    
**test_model_main.py**

Applies the trained model to predict house prices and stores the results in the database. It's the final step in the prediction pipeline, ensuring seamless integration of machine learning insights into the database.

**train_model_main.py**

Orchestrates model training and storage for future predictions. It encapsulates the crucial process of model generation, ensuring robustness and efficiency in predicting house prices.

### Setup , Requirements and Handling of Pipeline

1. **Prerequisites**:
   - Ensure Python 3.9.12 is installed on your system or in a virtual environment.
   - Install required Python libraries as listed in requirements.txt:
     ```bash
     pip install -r requirements.txt
     ```
   - Place your dataset in the `data/` directory and the trained model in the `models/` directory.
   - Update the file paths accordingly in test_model_main.py and train_model_main.py.
   - Ensure to update database related credentials before pushing data to the database. 

2. **Running the Pipeline**:
   - Run `test_model_main.py` to start the ETL process, loading clean dataset without prediction to db , predicting house values with `model.joblib` and saving the predicted values to db.
   - Run `train_model_main.py` to start the ETL process on raw dataset required for training and saving the model.
