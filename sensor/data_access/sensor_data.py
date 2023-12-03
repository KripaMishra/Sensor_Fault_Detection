import sys
import numpy as np
import pandas as pd
import json
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
import logging

class SensorData:
    """
    This class helps to export entire MongoDB record as a pandas DataFrame.
    """

    def __init__(self):
        """
        Initialize the SensorData class and establish a connection to MongoDB.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            logging.error(f"Error initializing SensorData: {e}")
            raise SensorException(e, sys)

    def save_csv_file(self, file_path, collection_name: str, database_name:str = None):
        try:
            data_frame = pd.read_csv(file_path)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            collection = self.get_collection(collection_name, database_name)
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            logging.error(f"Error saving CSV file to MongoDB: {e}")
            raise SensorException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name:str = None) -> pd.DataFrame:
        try:
            """
            Export entire collection as a DataFrame.
            Returns a pd.DataFrame of the collection.
            """
            collection = self.get_collection(collection_name, database_name)
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df
        except Exception as e:
            logging.error(f"Error exporting collection as DataFrame: {e}")
            raise SensorException(e, sys)

    def get_collection(self, collection_name: str, database_name:str = None):
        """
        Get the MongoDB collection based on the provided collection and database names.
        """
        if database_name is None:
            return self.mongo_client.database[collection_name]
        else:
            return self.mongo_client[database_name][collection_name]
