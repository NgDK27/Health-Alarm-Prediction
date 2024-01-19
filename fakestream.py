import csv
from faker import Faker
import random
import pymongo
import time
from datetime import datetime, timedelta
import pandas as pd

# MongoDB Connection Setup
client = pymongo.MongoClient("mongodb+srv://saurabh:Solarwind%401@companydata.g6xbxk5.mongodb.net/")  # Replace with your MongoDB URI
db = client["asm3"]  # Replace with your database name
collection = db["streaming_data"]  # Replace with your collection name
fake = Faker()

csv_file_path = '/home/mr-awesomeness/Health-Alarm-Prediction/disease_symptoms_train.csv'  # Update with your CSV file path
df = pd.read_csv(csv_file_path)
df.drop('prognosis', axis=1, inplace=True)
# Get the column names and remove the "prognosis" column
all_column_names = df.columns.tolist()

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

# Initialize start_time
start_time = datetime.now()

# Function to assign a random district and its latitude, longitude to a dataframe row
def assign_district_data(row, district_coordinates):
    district = fake.random_element(elements=list(district_coordinates.keys()))
    lat, long = district_coordinates[district]
    row['District'] = district
    row['Latitude'] = lat
    row['Longitude'] = long
    return row

# Assign initial district data to the dataframe
df = df.apply(assign_district_data, axis=1, args=(district_coordinates,))

# Function to generate and insert data into MongoDB
def generate_and_insert_data(df, start_time, district_coordinates):
    while True:
        current_time = datetime.now()

        # Update district data every two hours
        if current_time >= start_time + timedelta(hours=2):
            df = df.apply(assign_district_data, axis=1, args=(district_coordinates,))
            start_time = current_time  # Reset start time

        # Insert updated data into MongoDB
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            row_dict['Timestamp'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            collection.insert_one(row_dict)  # Inserting the data into MongoDB
            print(f"Inserted: {row_dict}")
            time.sleep(0.1)  # Wait for 0.1 seconds

# Initialize start_time and call the function
start_time = datetime.now()
generate_and_insert_data(df, start_time, district_coordinates)