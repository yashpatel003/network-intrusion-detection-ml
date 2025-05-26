
import sys, os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from src.config.configuration import Configuration
from src.exception.exception import CustomException
from src.logging.logger import logger
from src.utils.utils import save_numpy_array_data, save_object

class DataTransformation:

    def __init__(self, configuration: Configuration):
        """
        Constructor for initializing the DataTransformation object.
        """
        try:
            self.configuration: Configuration = configuration
            logger.info("Initialized DataTransformation class successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def read_data(self, file_path: str) -> pd.DataFrame:
        """
        Reads a CSV file and returns a DataFrame.
        """
        try:
            logger.info(f"Reading data from: {file_path}")
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformer_object(self, input_df: pd.DataFrame):
        """
        Creates and returns a ColumnTransformer object containing 
        preprocessing pipelines for numerical columns.
        """
        try:
            logger.info("Creating data transformation pipeline.")

            # Identify numerical columns
            numerical_cols = input_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            logger.info(f"Numerical columns: {numerical_cols}")

            # Numerical pipeline: median imputation + standard scaling
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            # Combine pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(transformers=[
                ("num_pipeline", num_pipeline, numerical_cols)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        """
        Executes the complete data transformation workflow:
        - Reads train and test data
        - Splits into input features and target labels
        - Applies preprocessing pipelines
        - Encodes target labels
        - Saves transformed data and pipeline objects
        - Returns artifact paths as a DataTransformationArtifact
        """
        try:
            logger.info("Starting data transformation process.")

            # Fetch target column name from config
            TARGET_COLUMN = self.configuration.get_value("training", "target_columns")

            # Read train and test datasets
            train_df = self.read_data(self.configuration.get_value("file_paths", "train_data"))
            test_df = self.read_data(self.configuration.get_value("file_paths", "test_data"))

            # Separate input features and target labels
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Get data transformation pipeline
            preprocessor = self.get_data_transformer_object(input_feature_train_df)

            # Fit on training data, then transform both train and test input features
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            # Encode target labels using LabelEncoder
            target_encoder = LabelEncoder()
            target_feature_train_df = target_encoder.fit_transform(target_feature_train_df)
            target_feature_test_df = target_encoder.transform(target_feature_test_df)

            # Save transformed train and test data as numpy arrays
            save_numpy_array_data(
                self.configuration.get_value("transformation", "transformed_train_data"),
                np.c_[transformed_input_train_feature, target_feature_train_df]
            )

            save_numpy_array_data(
                self.configuration.get_value("transformation", "transformed_test_data"),
                np.c_[transformed_input_test_feature, target_feature_test_df]
            )

            # Save the preprocessor object and label encoder object for later use
            save_object(
                self.configuration.get_value("transformation", "transformer_object"),
                preprocessor
            )
            save_object(
                self.configuration.get_value("transformation", "target_object"),
                target_encoder
            )

            logger.info("Data transformation process completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)
        
# def main():
#     try:
#         # Initialize configuration
#         config = Configuration("../../config/config.yaml")

#         # Create DataTransformation instance
#         data_transformation = DataTransformation(configuration=config)

#         # Run data transformation process
#         data_transformation.initiate_data_transformation()

#         # # Log success and artifact paths
#         # logger.info(f"Data Transformation Artifact:\n"
#         #             f"Preprocessor object: {transformation_artifact.transformed_object_file_path}\n"
#         #             f"Transformed train file: {transformation_artifact.transformed_train_file_path}\n"
#         #             f"Transformed test file: {transformation_artifact.transformed_test_file_path}")

#     except Exception as e:
#         logger.error(f"Error in data transformation pipeline: {e}")
#         raise CustomException(e, sys)

# if __name__ == "__main__":
#     main()

