import os
import sys
import json
import certifi
import time
import pandas as pd
from typing import List, Dict
from pymongo.mongo_client import MongoClient
from pymongo import errors
from dotenv import load_dotenv

from src.exception.exception import CustomException
from src.logging.logger import logger 

# Load environment variables from a .env file
load_dotenv()

# Retrieve MongoDB URI from environment variables
MONGO_DB_URI: str = os.getenv("MONGO_URI")

# Load SSL certificate authority file path for a secure TLS connection
ca: str = certifi.where()


class NetworkDataHandler:
    """
    Handles network intrusion data operations:
    - Converts CSV files to JSON-like records
    - Inserts data into a Database
    """

    def __init__(self) -> None:
        """
        Initialize the MongoDB client connection using the connection URI 
        and SSL certificate for a secure connection.
        """
        try:
            self.client = MongoClient(
                MONGO_DB_URI,
                tlsCAFile=ca,
                connectTimeoutMS=100000,  
                socketTimeoutMS=100000   
            )
            logger.info("MongoDB client initialized successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def csv_to_json_records(self, file_path: str) -> List[Dict]:
        """
        Converts a CSV file to a list of JSON-like dictionary records.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            List[Dict]: List of dictionary records.
        """
        try:
            data: pd.DataFrame = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records: List[Dict] = json.loads(data.to_json(orient='records'))
            logger.info(f"Converted {len(records)} records from CSV to JSON format.")
            return records
        except Exception as e:
            logger.error("Error while converting CSV to JSON.")
            raise CustomException(e, sys)

    def insert_records_to_db(
        self,
        records: List[Dict],
        database_name: str,
        collection_name: str,
        batch_size: int = 10000
    ) -> int:
        """
        Inserts records into a MongoDB collection in batches with retry logic.

        Args:
            records (List[Dict]): List of records to insert.
            database_name (str): Name of the target database.
            collection_name (str): Name of the target collection.
            batch_size (int): Number of records per batch. Default is 10,000.

        Returns:
            int: Total number of records successfully inserted.
        """
        try:
            client: MongoClient = self.client
            database = client[database_name]
            collection = database[collection_name]

            total_inserted = 0
            total_batches = (len(records) + batch_size - 1) // batch_size

            # Split records into batches and insert them one by one
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                attempt = 0
                success = False

                # Retry mechanism: attempt up to 3 times per batch
                while attempt < 3 and not success:
                    try:
                        # Insert current batch, unordered so it continues on errors like duplicates
                        result = collection.insert_many(batch, ordered=False)
                        inserted_count = len(result.inserted_ids)
                        total_inserted += inserted_count

                        logger.info(
                            f"Inserted batch {i // batch_size + 1}/{total_batches} — {inserted_count} records."
                        )
                        success = True

                    except errors.BulkWriteError as bwe:
                        # Handle bulk write errors like duplicate key issues
                        logger.error(f"Bulk write error in batch {i // batch_size + 1}: {bwe.details}")
                        success = True  # Continue even if partial insert occurs

                    except Exception as e:
                        # Log the failure and retry after a short delay
                        attempt += 1
                        logger.error(f"Attempt {attempt} failed for batch {i // batch_size + 1}: {e}")
                        time.sleep(2)

                if not success:
                    logger.error(f"Failed to insert batch {i // batch_size + 1} after 3 attempts.")

            logger.info(
                f"Total records successfully inserted into '{database_name}.{collection_name}': {total_inserted}"
            )
            return total_inserted

        except Exception as e:
            logger.error("An error occurred during data ingestion.")
            raise CustomException(e, sys)



if __name__ == "__main__":
    try:
        # CSV file path for processed network intrusion data
        FILE_PATH: str = "../../data/processed/clean_network_data.csv"
        
        # Target database and collection names
        DATABASE_NAME: str = "network_security"
        COLLECTION_NAME: str = "intrusion_records"

        # Create an instance of the data handler
        handler = NetworkDataHandler()

        # Convert the CSV file to a list of JSON-like records
        records = handler.csv_to_json_records(FILE_PATH)

        # Insert records into MongoDB in batches
        inserted_count = handler.insert_records_to_db(records, DATABASE_NAME, COLLECTION_NAME)

        # Log a final success message
        logger.info(f"Successfully inserted {inserted_count} records into MongoDB.")

    except Exception as e:
        logger.error(f"An error occurred during data ingestion: {e}")
