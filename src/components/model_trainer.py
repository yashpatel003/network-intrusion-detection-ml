import sys
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
    GradientBoostingClassifier
)
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from src.models.network_model import NetworkModel
from src.utils.metrics_utils import save_classification_reports_yaml
from src.utils.utils import save_object, load_object, load_numpy_array_data, evaluate_models
from src.config.configuration import Configuration
from src.exception.exception import CustomException
from src.logging.logger import logger


# Model Trainer class
class ModelTrainer:
    def __init__(self, configuration: Configuration) -> None:
        try:
            self.config = configuration
        except Exception as e:
            raise CustomException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):
        """
        Trains multiple ML models with given hyperparameters and selects the best one.
        """

        # Define models to train
        models = {
            # "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            # "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1, max_iter=500),
            # "AdaBoost": AdaBoostClassifier(),
        }

        # Hyperparameter grid for each model
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
            },
            # "Random Forest": {
            #     'n_estimators': [8, 16, 32, 64, 128, 256],
            # },
            # "Gradient Boosting": {
            #     'learning_rate': [0.1, 0.01, 0.05, 0.001],
            #     'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
            #     'n_estimators': [8, 16, 32, 64, 128, 256],
            # },
            "Logistic Regression": {},
            # "AdaBoost": {
            #     'learning_rate': [0.1, 0.01, 0.001],
            #     'n_estimators': [8, 16, 32, 64, 128, 256],
            # }
        }

        # Evaluate all models and get their performance scores
        trained_models, model_report = evaluate_models(
            X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
            models=models, params=params
        )

        # Select the model with highest accuracy
        best_model_name = max(model_report, key=model_report.get)
        best_model_score = model_report[best_model_name]
        best_model = trained_models[best_model_name]

        # After predictions
        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        # Save YAML reports and ensure directory exists
        metrics_file_path = self.config.get_value("evaluation","evaluation_report")
        os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)
        print(metrics_file_path)
       
        save_classification_reports_yaml(y_train,y_train_pred,y_test,y_test_pred,metrics_file_path)
        
        logger.info(f"Best Model: {best_model_name} with Accuracy: {best_model_score:.4f}")

        # Load preprocessor and target encoder
        preprocessor = load_object(self.config.get_value("transformation","transformer_object"))
        target_encoder = load_object(self.config.get_value("transformation","target_object"))

        network_model=NetworkModel(preprocessor=preprocessor,model=best_model,target_encoder=target_encoder)
        
        # Ensure model output directory exists
        model_file_path = self.config.get_value("training","model_output")
        os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
     
        print(model_file_path)
        # Save the network model
        model_path = self.config.get_value("training","model_output")
        save_object(model_file_path,obj=network_model)

        # Log model saving information
        logger.info(f"Trained model saved at: {model_file_path}")
        logger.info(f"Model trainer completed. Best model saved at: {model_file_path}")

    def initiate_model_trainer(self):
        """
        Load transformed data, train models and push best model.
        """
        try:
            logger.info("Loading transformed train and test arrays.")

            train_file_path = self.config.get_value("transformation","transformed_train_data")
            test_file_path = self.config.get_value("transformation","transformed_test_data")

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            logger.info("Starting model training.")
            self.train_model(X_train, y_train, X_test, y_test)
            
        except Exception as e:
            raise CustomException(e, sys)
