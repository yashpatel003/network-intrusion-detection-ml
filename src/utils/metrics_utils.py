import yaml
import datetime
import os
from sklearn.metrics import classification_report, accuracy_score, f1_score
from src.logging.logger import logger
from src.utils.utils import write_yaml_file

def save_classification_reports_yaml(y_train, y_train_pred, y_test, y_test_pred, file_path):
    """
    Generate classification reports for train and test sets, save both in one YAML file.

    Args:
        y_train: True labels for training data.
        y_train_pred: Predicted labels for training data.
        y_test: True labels for test data.
        y_test_pred: Predicted labels for test data.
        file_path: Full path including filename where YAML will be saved.
    """
    # Create report dict for train
    train_report = classification_report(y_train, y_train_pred, output_dict=True)
    train_report['accuracy'] = accuracy_score(y_train, y_train_pred)
    train_report['f1_weighted'] = f1_score(y_train, y_train_pred, average='weighted')

    # Create report dict for test
    test_report = classification_report(y_test, y_test_pred, output_dict=True)
    test_report['accuracy'] = accuracy_score(y_test, y_test_pred)
    test_report['f1_weighted'] = f1_score(y_test, y_test_pred, average='weighted')

    # Get current timestamp in ISO format
    current_time = datetime.datetime.now().isoformat()

    # Combine into one dictionary with timestamp
    combined_report = {
        "timestamp": current_time,
        "train_report": train_report,
        "test_report": test_report
    }

    # Save combined report as YAML
    write_yaml_file(file_path=file_path, content=combined_report, replace=True)
    
    logger.info(f"Saved combined train/test classification report at: {file_path}")
