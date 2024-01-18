import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import joblib
except ImportError:
    install('joblib')  # specify the version you need
import joblib
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def model_fn(model_dir):
    """
    Load the joblib model from the specified directory.
    """
    try:
        model = joblib.load(f"{model_dir}/model.joblib")
        logging.info("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error("Error in loading model: %s", e)
        raise

def input_fn(request_body, request_content_type):
    """
    Parse input data payload
    """
    try:
        if request_content_type == "text/csv":
            data = np.genfromtxt(request_body.splitlines(), delimiter=',')
            logging.info("Input data processed successfully.")
            return data.reshape(1, -1)  # Reshape if necessary
        else:
            raise ValueError(f"Unsupported content type: {request_content_type}")
    except Exception as e:
        logging.error("Error in input_fn: %s", e)
        raise

def predict_fn(input_data, model):
    """
    Make a prediction using the input data and loaded model.
    """
    try:
        predictions = model.predict(input_data)
        logging.info("Prediction successful.")
        return predictions
    except Exception as e:
        logging.error("Error in predict_fn: %s", e)
        raise
