import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.config.configuration import Configuration
from src.exception.exception import CustomException
from src.logging.logger import logger


if __name__ == '__main__':
    try:
        # Load the configuration file
        config = Configuration("config/config.yaml")

         # ----------------------- Data Ingestion Phase -----------------------
        # data_ingestion=DataIngestion(config)
        # logger.info("Initiate the data ingestion")
        # data_ingestion.initiate_data_ingestion()
        # logger.info("✅ Data Initiation Completed")

        # ----------------------- Data Validation Phase -----------------------
        logger.info("🔍 Initiating Data Validation...")
        data_validation = DataValidation(config)
        data_validation.initiate_data_validation()
        logger.info("✅ Data Validation completed successfully.")

        # ----------------------- Data Transformation Phase -----------------------
        logger.info("🔧 Starting Data Transformation...")
        data_transformation = DataTransformation(config)
        data_transformation.initiate_data_transformation()
        logger.info("✅ Data Transformation completed successfully.")

        # ----------------------- Model Training Phase (Uncomment when needed) -----------------------
        # logger.info("🏋️‍♂️ Starting Model Training...")
        # model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        # model_trainer = ModelTrainer(
        #     model_trainer_config=model_trainer_config,
        #     data_transformation_artifact=data_transformation_artifact
        # )
        # model_trainer_artifact = model_trainer.initiate_model_trainer()
        # logger.info("✅ Model Training completed and artifact created.")

    except Exception as e:
        raise CustomException(e, sys)