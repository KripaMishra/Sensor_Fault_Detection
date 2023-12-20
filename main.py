from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os, sys

if __name__=='__main__':
    try:
        training_pipeline= TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

