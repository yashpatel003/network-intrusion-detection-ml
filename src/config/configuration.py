import yaml
import os
from dotenv import load_dotenv

class Configuration:
    """
    A class to load and access project configuration values from a YAML file and environment variables.
    """

    def __init__(self, config_file_path: str):
        """
        Initialize Configuration by loading .env and YAML config.

        Args:
            config_file_path (str): Path to the YAML config file.
        """
        load_dotenv()  # Load environment variables from .env file
        self.config = self._load_config(config_file_path)

    def _load_config(self, file_path: str) -> dict:
        """
        Load YAML configuration file.

        Args:
            file_path (str): Path to the config YAML file.

        Returns:
            dict: Loaded config dictionary.
        """
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def get_db_value(self, key: str) -> str:
        """
        Retrieve a value from the 'db' section of the config.

        If the key is 'uri_env_key', fetch the value from environment variables.

        Args:
            key (str): Key name within the 'db' section.

        Returns:
            str: Value associated with the key.
        """
        if key == "uri_env_key":
            env_key = self.config['db'].get(key)
            return os.getenv(env_key)
        else:
            return self.config['db'].get(key)

    def get_section(self, section_name: str) -> dict:
        """
        Retrieve an entire section from the config.

        Args:
            section_name (str): Name of the config section.

        Returns:
            dict: The section's content.
        """
        return self.config.get(section_name, {})

    def get_value(self, section_name: str, key: str):
        """
        Retrieve a specific value from a section in the config.

        Args:
            section_name (str): Section name.
            key (str): Key within the section.

        Returns:
            Any: Value associated with the key or None if not found.
        """
        section = self.get_section(section_name)
        return section.get(key) if section else None


# Example usage:
if __name__ == "__main__":
    config = Configuration("../../config/config.yaml")

    mongo_uri = config.get_db_value("uri_env_key")
    database_name = config.get_db_value("database")
    train_path = config.get_value("file_paths", "train_data")

    print("Mongo URI:", mongo_uri)
    print("Database:", database_name)
    print("Train file path:", train_path)
