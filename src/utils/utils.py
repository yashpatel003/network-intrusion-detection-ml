
import os
import numpy as np
import pickle
import yaml
from src.exception.exception import CustomException
import sys

def save_numpy_array_data(file_path, array):
    """
    Saves a numpy array to a file in .npy format.

    Args:
        file_path (str): Path where the numpy array should be saved.
        array (numpy.ndarray): The numpy array to save.

    Raises:
        CustomException: If any error occurs during the file writing process.
    """
    try:
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        # Save the numpy array to the specified file path
        np.save(file_path, array)

    except Exception as e:
        # Raise custom exception with original error and system info
        raise CustomException(e, sys)

def save_object(file_path, obj):
    """
    Serializes and saves a Python object using pickle.

    Args:
        file_path (str): Path where the serialized object should be saved.
        obj (any): The Python object to serialize and save.

    Raises:
        CustomException: If any error occurs during the serialization process.
    """
    try:
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        # Serialize and save the object to file using pickle
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    """
    Loads a serialized Python object from a file.

    Args:
        file_path (str): Path to the serialized object.

    Returns:
        any: The deserialized Python object.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    Args:
        file_path (str): Path to the numpy array data
    Returns:
      np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e
    

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a Python dictionary.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Contents of the YAML file.

    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file. Optionally replaces existing file.

    Args:
        file_path (str): Destination file path.
        content (object): Data to be written to YAML (usually dict or list).
        replace (bool, optional): If True, existing file is deleted before writing. Defaults to False.

    Raises:
        NetworkSecurityException: Custom exception if file write fails.
    """
    try:
        # Remove existing file if replace flag is True
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write content to YAML file
        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise CustomException(e, sys) from e

