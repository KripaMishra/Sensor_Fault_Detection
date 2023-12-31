import os 
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME


SAVED_MODEL_DIR = os.path.join("saved_models")

#training pipeline variables

# prerpocessing constants
TARGET_COLUMN= "class"
PIPELINE_NAME:str = "sensor"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "sensor.csv"

#train,test constants
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCESSING_OBJECT_FILE_NAME: str= "preprocessor.pkl"

#model training constants

MODEL_FILE_NAME:str = "model.pkl"
SCHEMA_FILE_PATH= os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS= "drop_columns"

"""
Data Ingestion Constants
"""
DATA_INGESTION_COLLECTION_NAME: str = "sensor_collection"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


"""
Data Validation Constants
"""
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str= "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str= "report.yaml"

"""
Data Transformation Constants
"""
DATA_TRANSFORMATION_DIR_NAME: str= "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str= "transformed_object"

"""
Model Trainer Constants
"""
MODEL_TRAINER_DIR_NAME:str= "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model" 
MODEL_TRAINER_TRAINED_MODEL_NAME:str= "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float= 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

"""
Model Evaluation Constants
"""
MODEL_EVALUATION_DIR_NAME:str="model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float= 0.2
MODEL_EVALUATION_REPORT_NAME= "report.yaml"

"""
Model Pusher Constants
"""
MODEL_PUSHR_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR= SAVED_MODEL_DIR



