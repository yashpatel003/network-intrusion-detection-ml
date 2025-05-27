import os, sys
import pandas as pd
import certifi
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split

from src.config.configuration import Configuration
from src.logging.logger import logger
from src.exception.exception import CustomException


class DataIngestion:
    def __init__(self, configuration: Configuration) -> None:
        """
        Initialize DataIngestion class with a configuration instance.
        """
        try:
            self.configuration: Configuration = configuration
            logger.info("Initialized DataIngestion class successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def read_data_db(self) -> pd.DataFrame:
        """
        Connect to MongoDB, read data from the specified collection, 
        convert it into a Pandas DataFrame, and clean it.
        """
        try:
            logger.info("Reading data from MongoDB collection.")

            # Get database details from config
            database_name = self.configuration.get_db_value('database')
            collection_name = self.configuration.get_db_value('collection')
            mongo_uri = self.configuration.get_db_value('uri_env_key')

            # Load SSL certificate authority file path for a secure TLS connection
            ca: str = certifi.where()

            # Connect to MongoDB
            client = MongoClient(
                mongo_uri,
                tlsCAFile=ca,
                connectTimeoutMS=100000,  
                socketTimeoutMS=100000   
            )
            collection = client[database_name][collection_name]

            # Fetch all records from collection
            data_cursor = collection.find({}).batch_size(10000)
            data_list = list(data_cursor)

            # Convert list of documents to DataFrame
            data_df = pd.DataFrame(data_list)

            # Drop MongoDB's default '_id' field if present
            if '_id' in data_df.columns:
                data_df.drop('_id', axis=1, inplace=True)
                logger.info("Dropped '_id' column from the DataFrame.")

            logger.info(f"Successfully read {len(data_df)} records from MongoDB.")

            # Close the MongoDB connection
            client.close()

            return data_df

        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Save the ingested data as a CSV file into a local feature store directory.
        """
        try:
            logger.info("Exporting data to feature store.")

            # Fetch feature store file path from config
            feature_store_path = self.configuration.get_value("file_paths", "feature_store")

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

            # Export data as CSV
            df.to_csv(feature_store_path, index=False, header=True)
            logger.info(f"Data exported successfully to feature store at: {feature_store_path}")

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def split_train_test(self, df: pd.DataFrame) -> None:
        """
        Split the data into train and test datasets, and save them as separate CSV files.
        """
        try:
            logger.info("Performing train-test split.")

            # Get split parameters from config
            test_size = self.configuration.get_value("training", "test_size")
            random_state = self.configuration.get_value("training","random_state")

            # Perform the split
            train_set, test_set = train_test_split(df, test_size=test_size, random_state=random_state)

            logger.info(f"Train set size: {len(train_set)}, Test set size: {len(test_set)}")

            # Get file paths for train and test data
            train_path = self.configuration.get_value("file_paths", "train_data")
            test_path = self.configuration.get_value("file_paths", "test_data")

            # Create directories if needed
            os.makedirs(os.path.dirname(train_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_path), exist_ok=True)

            # Export train and test sets as CSV files
            train_set.to_csv(train_path, index=False, header=True)
            test_set.to_csv(test_path, index=False, header=True)

            logger.info(f"Train data saved to: {train_path}")
            logger.info(f"Test data saved to: {test_path}")

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> None:
        """
        Execute the full data ingestion pipeline:
        1. Read data from MongoDB.
        2. Export raw data to feature store.
        3. Split data into train and test files.
        """
        try:
            logger.info("Starting data ingestion process.")

            # 1. Read data from database
            dataframe = self.read_data_db()

            # 2. Export raw data to feature store
            dataframe = self.export_data_into_feature_store(dataframe)

            # 3: Split the data into train and test sets
            self.split_train_test(dataframe)

            logger.info("Data ingestion process completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)

