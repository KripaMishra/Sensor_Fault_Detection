from sensor.utils.main_utils import load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging 
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
import os, sys
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object, load_object

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
    data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact
        

        except Exception as e:
            raise SensorException(e,sys)


    def perform_hyper_parameter_tuning(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def train_model(self,x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise e

    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            logging.info("Entered the initiate_model_trainer method of class ModelTrainer")

            train_file_path= self.data_transformation_artifact.transformed_train_file_path
            test_file_path= self.data_transformation_artifact.transformed_test_file_path

            logging.info("loading the training array and testing array in initiate_model_trainer of class ModelTrainer")

            train_arr= load_object(train_file_path)
            test_arr= load_object(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train[:,-1],
                test[:,:-1],
                test[:,-1],
            )

            model=  self.trained_model(x_train, x_test)
            y_train_pred= model.predict(x_train)
            classification_train_metric= get_classification_score(y_true= y_train, y_pred=y_train_pred)

            logging.info("compairing the model f1 score with expected accuracy")
            if classification_train_metric<=model_trainer_config.expected_accuracy:
                raise Exception("Trained Model failed to meet the expected accuracy")
            y_test_pred= model.predict(x_test)

            logging.info("checking for OverFitting and UnderFitting in initiate_model_trainer method of class ModelTrainer")
            
            diff= abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            if dff>model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model contains Overfitting or Underfitting, not good for experimentation")
            preprocessor= load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path= os.path.dirname(self.model_trainer_config.trained_model_file_path)

            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model =SensorModel(preprocessor=preprocessor, model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj= sensor_model)

            logging.info("creating the model trainer artifact")

            model_trainer_artifact= ModelTrainerArtifact(trained_model_file_path=self.model_config_file_path.trained_model_file_path,
            train_metric_artifact= classification_train_metric,
            test_metric_artifact= classification_test_metric,
            )

            loggin.info(f"Model Trainer Artifact: {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)

