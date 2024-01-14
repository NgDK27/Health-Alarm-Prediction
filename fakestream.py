from flask_socketio import emit
import csv
from faker import Faker
from faker.providers import DynamicProvider
import random
import pymongo
import time
from datetime import datetime, timedelta
import json
import pandas as pd
import boto3

# MongoDB Connection Setup
client = pymongo.MongoClient("mongodb+srv://saurabh:Solarwind%401@companydata.g6xbxk5.mongodb.net/")  # Replace with your MongoDB URI
db = client["asm3"]  # Replace with your database name
collection = db["result"]  # Replace with your collection name

# Function to read CSV and return a list of rows along with column names
def read_csv_to_list(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        columns = next(csv_reader)  # Get column names from the first row
        data = [dict(zip(columns, row)) for row in csv_reader]  # Create a dict for each row
    return columns, data
# CSV File Path
csv_file_path = '/home/mr-awesomeness/Downloads/dataset_for_simulating_streaming.csv'  # Update with your CSV file path
columns, csv_data = read_csv_to_list(csv_file_path)
# District Coordinates
district_coordinates = {
    'd1': (10.7763897, 106.7011391), 'd2': (10.7763897, 106.7011391),
    'd3': (10.7763897, 106.7011391), 'd4': (10.8420693, 106.8277083),
    'd5': (10.7763897, 106.7011391), 'd6': (10.7763897, 106.7011391),
    'd7': (10.7763897, 106.7011391), 'd8': (10.7763897, 106.7011391),
    'd9': (10.7763897, 106.7011391), 'd10': (10.8155799, 106.6257578),
    'd11': (10.7008257, 106.7287453), 'd12': (10.815238, 106.6260036),
    'Binh Tan District': (10.7703708, 106.5996353),
    'Binh Thanh District': (10.8117887, 106.7039109),
    'Phu Nhuan District': (10.800981, 106.6794379),
    'Tan Binh District': (10.802583, 106.6521157),
    'Tan Phu District': (10.7914967, 106.6278431),
    'Thu Duc District': (10.82202275, 106.71830155362943)
}



# Create a Dynamic Provider with the CSV data
class CSVDataProvider(DynamicProvider):
    def __init__(self, elements):
        super().__init__(provider_name="csv_row", elements=elements)

    def generate_csv_data(self):
        return self.random_element(self.elements)

# Faker setup
fake = Faker()
csv_data_provider = CSVDataProvider(csv_data)
fake.add_provider(csv_data_provider)


# Function to assign latitude and longitude to a row
def assign_lat_long(district_coordinates):
    district = random.choice(list(district_coordinates.keys()))
    lat_long = district_coordinates[district]
    if isinstance(lat_long, tuple) and len(lat_long) == 2:
        return lat_long
    else:
        raise ValueError(f"Invalid latitude/longitude data for district {district}")

# Function to update latitude and longitude every two hours
def update_lat_long_assignment(csv_data, district_coordinates):
    for row in csv_data:
        latitude, longitude = assign_lat_long(district_coordinates)
        row['Latitude'], row['Longitude'] = latitude, longitude
        row['District'] = [district for district, coords in district_coordinates.items() if coords == (latitude, longitude)][0]

# Initial assignment
update_lat_long_assignment(csv_data, district_coordinates)

sagemaker_runtime = boto3.client('sagemaker-runtime')
endpoint_name = 'Entry43'  # Your actual endpoint name

# Function to prepare the data for prediction
def prepare_data_for_prediction(csv_row_dict):
    all_column_names = list(csv_row_dict.keys())
    columns_to_exclude = ['medicine_name', 'disease', 'District']
    remaining_columns = [col for col in all_column_names if col not in columns_to_exclude]
    data = pd.DataFrame(columns=remaining_columns)
    for column_name in remaining_columns:
        data.at[0, column_name] = csv_row_dict[column_name]
    csv_data = data.to_csv(index=False, header=False)
    csv_data_bytes = csv_data.encode()
    return csv_data_bytes

# Function to generate and insert data into MongoDB
def generate_and_insert_data():
    global start_time  # Declare global to update the start_time variable
    start_time = datetime.now()  # Store the start time

    while True:
        current_time = datetime.now()

        # Check if two hours have passed and update latitude and longitude
        if current_time >= start_time + timedelta(hours=2):
            update_lat_long_assignment(csv_data, district_coordinates)
            start_time = current_time  # Reset start time

        for csv_row_dict in csv_data:
            # csv_row_dict['Suffering_Population'] = generate_suffering_population()
            csv_row_dict['Timestamp'] = current_time

            # Remove the '_id' field if it exists in the dictionary
            csv_row_dict.pop('_id', None)

            # Prepare the data for prediction
            csv_data_bytes = prepare_data_for_prediction(csv_row_dict)

            # Make the prediction
            response = sagemaker_runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='text/csv',
                Body=csv_data_bytes
            )
            prediction = json.loads(response['Body'].read().decode())
            print(f"Predictions: {prediction}")


            # Add the prediction to the csv_row_dict and insert it into MongoDB
            csv_row_dict['prediction'] = prediction
            collection.insert_one(csv_row_dict)
            print(f"Inserted: {csv_row_dict}")

            # Emit a WebSocket event with the inserted data
            emit('data_inserted', csv_row_dict, broadcast=True)

            time.sleep(60)  # Wait for 60 seconds

generate_and_insert_data()