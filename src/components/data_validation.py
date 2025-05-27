import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

from src.config.configuration import Configuration
from src.exception.exception import CustomException
from src.logging.logger import logger
from src.utils.utils import read_yaml_file, write_yaml_file  

class DataValidation:
    def __init__(self, configuration: Configuration):
        """
        Initialize DataValidation with configuration object.
        Loads the schema YAML file and data validation config.
        """
        try:
            self.config = configuration
    
            # Load schema config (column definitions) from YAML
            self._schema_config = read_yaml_file(self.config.get_value("validation","schema_file"))
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Read CSV data into a pandas DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validate if the number of columns in dataframe matches the schema.
        """
        try:
            required_columns = len(self._schema_config["columns"])
            actual_columns = len(dataframe.columns)

            logger.info(f"Required number of columns: {required_columns}")
            logger.info(f"Dataframe contains: {actual_columns} columns")

            return required_columns == actual_columns
        except Exception as e:
            raise CustomException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Check for dataset drift using KS-test between base_df and current_df.
        Writes a YAML report of drift results.
        """
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                test_result = ks_2samp(d1, d2)
                p_value = test_result.pvalue

                # Drift detected if p-value is below threshold
                drift_found = p_value < threshold

                if drift_found:
                    status = False  # If any column has drift, mark status False

                report[column] = {
                    "p_value": float(p_value),
                    "drift_status": drift_found
                }

            # Write drift report to file
            drift_report_file_path = self.config.get_value("validation","report_file")
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report , replace=True)

            logger.info(f"Drift report saved to: {drift_report_file_path}")
            return status

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self):
        """
        Main method to orchestrate data validation steps:
        - Read train and test data
        - Validate columns
        - Detect data drift
        - Save valid data files
        - Return DataValidationArtifact
        """
        try:
            # Get file paths from ingestion artifact config
            train_file_path = self.config.get_value("file_paths","train_data")
            test_file_path = self.config.get_value("file_paths","test_data")

            # Read train and test datasets
            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            # Validate number of columns for both datasets
            if not self.validate_number_of_columns(train_dataframe):
                error_message = "Train dataframe does not contain all required columns."
                logger.error(error_message)
                raise CustomException(error_message, sys)

            if not self.validate_number_of_columns(test_dataframe):
                error_message = "Test dataframe does not contain all required columns."
                logger.error(error_message)
                raise CustomException(error_message, sys)

            # Detect dataset drift between train and test datasets
            threshold = self.config.get_value("validation","drift_threshold")
            drift_status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe , threshold=threshold)

            # Save validated train and test data files
        
            train_valid_path = self.config.get_value("validation","valid_train_file_path")
            test_valid_path  = self.config.get_value("validation","valid_test_file_path")

            train_valid_dir = os.path.dirname(train_valid_path)
            test_valid_dir  = os.path.dirname(test_valid_path)

            os.makedirs(train_valid_dir, exist_ok=True)
            os.makedirs(test_valid_dir, exist_ok=True)

            train_dataframe.to_csv(train_valid_path, index=False, header=True)
            test_dataframe.to_csv(test_valid_path, index=False, header=True)


            logger.info("Validated train and test data saved successfully.")

            logger.info("Data Validation Artifact created.")

        except Exception as e:
            raise CustomException(e, sys)
