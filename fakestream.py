

import csv
from faker import Faker
from faker.providers import DynamicProvider
import random
import pymongo
import time
from datetime import datetime, timedelta

# MongoDB Connection Setup
client = pymongo.MongoClient("mongodb+srv://saurabh:Solarwind%401@companydata.g6xbxk5.mongodb.net/")  # Replace with your MongoDB URI
db = client["asm3"]  # Replace with your database name
collection = db["streaming_data"]  # Replace with your collection name

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

# Function to generate a random number for suffering population
def generate_suffering_population():
    return random.randint(100, 1000)  # Adjust the range as needed

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

            collection.insert_one(csv_row_dict)  # Inserting the data into MongoDB
            print(f"Inserted: {csv_row_dict}")
            time.sleep(5)  # Wait for 5 seconds

generate_and_insert_data()