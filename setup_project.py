import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Project name
project_name = "stock_market_predictor"

# List of files and directories to create
file_list = [
    # Source code directory structure
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data/__init__.py",
    f"src/{project_name}/models/__init__.py",
    f"src/{project_name}/sentiment/__init__.py",
    f"src/{project_name}/visualization/__init__.py",
    f"src/{project_name}/api/__init__.py",

    f"src/{project_name}/data/data_ingestion.py",
    f"src/{project_name}/data/data_preprocessing.py",
    f"src/{project_name}/data/feature_engineering.py",

    f"src/{project_name}/models/ml_model.py",
    f"src/{project_name}/models/lstm_model.py",
    f"src/{project_name}/models/model_utils.py",

    f"src/{project_name}/sentiment/news_sentiment.py",
    f"src/{project_name}/sentiment/twitter_sentiment.py",
    f"src/{project_name}/sentiment/sentiment_utils.py",

    f"src/{project_name}/visualization/eda_plots.py",
    f"src/{project_name}/visualization/prediction_charts.py",

    f"src/{project_name}/api/app.py",

    # Data folders
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/external/.gitkeep",

    # Notebooks folder
    "notebooks/.gitkeep",

    # Models folder
    "models/ml/.gitkeep",
    "models/dl/.gitkeep",

    # Reports folder
    "reports/figures/.gitkeep",

    # Deployment
    "deployment/Dockerfile",
    "deployment/docker-compose.yml",
    "deployment/requirements.txt",
    "deployment/Procfile",
    "deployment/README.md",

    # Dashboard
    "dashboard/streamlit_app/app.py",
    "dashboard/assets/.gitkeep",

    # Root files
    ".gitignore",
    "README.md",
    "LICENSE",
    "requirements.txt",
    "environment.yml",
    "config.yaml",
    "setup.py",
]

# Loop through the file list and create directories/files
for filepath in file_list:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"📁 Created directory: {filedir}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"📝 Created file: {filepath}")
    else:
        logging.info(f"✅ File already exists: {filepath}")

logging.info("🎉 Project structure setup complete!")
