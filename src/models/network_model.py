import sys
from src.exception.exception import CustomException

class NetworkModel:
    def __init__(self, preprocessor, model, target_encoder):
        """
        Custom model wrapper to handle prediction with preprocessing and decoding.
        """
        try:
            self.preprocessor = preprocessor          # Input features transformer
            self.model = model                        # Trained model 
            self.target_encoder = target_encoder      # LabelEncoder used on target variable or Output features transformer
        
        except Exception as e:
            raise CustomException(f"Error initializing NetworkModel: {e}", sys)

    def predict(self, x):
        """
        Predict using raw input features.
        Transforms input → predicts → decodes prediction labels to original form.
        """
        try:
            # Transform the raw input using the preprocessor
            x_transformed = self.preprocessor.transform(x)

            # Predict using the trained model (returns encoded integers like 0, 1, 4)
            y_pred = self.model.predict(x_transformed)

            # Decode the integer predictions to original category labels 
            y_pred_decoded = self.target_encoder.inverse_transform(y_pred)

            return y_pred_decoded , y_pred
        
        except Exception as e:
            raise CustomException(f"Error during prediction: {e}", sys)
