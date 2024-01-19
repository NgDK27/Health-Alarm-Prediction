# Disease Prediction and Medicine Recommendation Simulation System

## Overview
This project involves setting up a machine learning model using AWS SageMaker. It includes steps for copying files into a folder, running a Python script, training a model in Jupyter Notebook, and deploying the model using AWS services.

## Prerequisites
- Python
- AWS Account
- Jupyter Notebooks

## Setup and Installation

### Step 1: Prepare Local Environment
- **Copy Files:** Copy all the necessary files into a designated folder on your local machine.

### Step 2: Run Python Scripts
- **Run FakeStream.py:** Navigate to the folder containing `fakestream.py` and execute the script.
- **Model Training:** Open `model_training.ipynb` in a local Jupyter Notebook environment and run all the cells to train the model.

### Step 3: AWS SageMaker Setup
- **Create AWS Account:** If you do not have an AWS account, create one.
- **Launch SageMaker Notebook Instance:**
  - Create an instance of SageMaker Notebook - `ml.t2.xlarge`.
- **Import Files to SageMaker:**
  - Import `endpoint_creation_and_deployment.ipynb` and other generated files (`disease_mapping`, `district_mapping`, `medicine_name_mapping`) to the SageMaker notebook directory. Exclude `model.tar.gz` at this stage.

### Step 4: Run SageMaker Notebook
- **Execute Notebook:** Open `endpoint_creation_and_deployment.ipynb` in SageMaker and run the seventh cell (Procuring the tarball containing the trained model).

### Step 5: AWS S3 Setup
- **Upload Model to S3:**
  - Navigate to AWS S3 and locate the new folder created by the previous step and find the “diseasePrediction” folder within.
  - Import the `model.tar.gz` file into this folder.

### Step 6: Deploy Model
- **Complete Notebook Execution:** Return to `endpoint_creation_and_deployment.ipynb` in SageMaker and run all remaining cells to deploy the model and to run faker against this entry point.

### Step 7: Run the dashboard
- **Open the project in a code editor:** Since we are running the dashboard in local network, we cannot run the full-stack app in SageMaker. Ideally, you would use VS Code.
- **Run the backend:** Navigate to `backend.py` and click the run button or left mouse click, choose Run to start the Flask application.
- **Run the frontend:** Navigate to `index.html` and left mouse click and choose 'Open with Live Server'. A new tab will be opened on your browser.