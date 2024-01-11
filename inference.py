# import subprocess
# import sys

# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# try:
#     import joblib
# except ImportError:
#     install('joblib')  # specify the version you need
# import joblib
# import numpy as np

# def model_fn(model_dir):
#     model = joblib.load(f"{model_dir}/model.joblib")
#     return model


# def input_fn(request_body, request_content_type):
#     if request_content_type == "text/csv":
#         # Convert string to numpy array
#         print("here")
#         data = np.fromstring(request_body, sep=',')

#         # Print the original shape
#         print("Original shape:", data.shape)

#         # Reshape the data
#         data = data.reshape(1, -1)

#         # Print the new shape
#         print("New shape:", data.shape)

#         return data
#     else:
#         # Handle other content-types or raise an exception
#         pass

# def predict_fn(input_data, model):
#     prediction = model.predict(input_data)
#     return prediction
