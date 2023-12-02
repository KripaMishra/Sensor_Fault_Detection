from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging

class TrainPipeline:
    def __init__(self):
        training_pipeline_config= TrainingPipelineConfig()
        self.data_ingestion_config= DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        self.training_pipeline_config= training_pipeline_config


    def start_data_ingestion(self)-> 
        try:
            logging.INFO("data ingestion started")
            logging.INFO("data ingestion completed")
        except Exception as e:
            raise SensorException (e,sys)


        
    def start_data_validation(self)-> 
        try:
            pass
        except Exception as e:
            raise SensorException (e,sys)



    def start_data_transformation(self)-> 
        try:
            pass
        except Exception as e:
            raise SensorException (e,sys)


    def start_model_trainer(self)-> 
        try:
            pass
        except Exception as e:
            raise SensorException (e,sys)


    def start_model_evaluation(self)-> 
        try:
            pass
        except Exception as e:
            raise SensorException (e,sys)

    def start_model_pusher(self)-> 
        try:
            pass
        except Exception as e:
            raise SensorException (e,sys)


    def sync_artifact_dir_to_s3(self):
                try:
                   pass
                except Exception as e:
                    raise SensorException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
            try:
                data_ingestion_artifact:DataIngestionArtifact= self.start_data_ingestion()
            except  Exception as e:
                raise  SensorException(e,sys)


        