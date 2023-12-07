from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig,ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

from sensor.exception import SensorException
import sys,os
from sensor.logger import logging

class TrainPipeline:
    def __init__(self):
        training_pipeline_config= TrainingPipelineConfig()
        self.data_ingestion_config= DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        self.data_validation_config = DataValidationConfig(training_pipeline_config= training_pipeline_config)
        self.data_transformation_config= DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        self.training_pipeline_config= training_pipeline_config


    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from mongodb")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e


    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(
                data_validation_artifact, self.data_transformation_config
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Performed the data transformation operation")
            logging.info("Exited the start_data_transformation method of TrainPipeline class")

            return data_transformation_artifact
        except Exception as e:
            raise SensorException (e,sys)


    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        logging.info("Entering the start_model_trainer")
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config= self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Performed the start_model_trainer operation")
            logging.info("Exited the start_model_trainer method of TrainPipeline class") 
            return model_trainer_artifact
        except  Exception as e:
            raise  SensorException(e,sys)


    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                 model_trainer_artifact:ModelTrainerArtifact,
                                ):
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except  Exception as e:
            raise  SensorException(e,sys)


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
                data_ingestion_artifact = self.start_data_ingestion()
                data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
                data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
                model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
                model_eval_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
                if not model_eval_artifact.is_model_accepted:
                    raise Exception("Trained model is not better than the best model")
                model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
                TrainPipeline.is_pipeline_running=False
            except  Exception as e:
                TrainingPipeline.is_pipeline_running= False
                raise  SensorException(e,sys)


        