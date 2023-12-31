import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGO_DB_URL_KEY
import certifi
import os
ca= certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url ="mongodb+srv://kripa5661:%40_KH20064501043@cluster0.zinz8vx.mongodb.net/" #os.getenv(MONGODB_URL_KEY)

                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")

                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client

            self.database = self.client[database_name]

            self.database_name = database_name

        except Exception as e:
            raise SensorException(e, sys)