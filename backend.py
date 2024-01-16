import json
from flask import send_from_directory
from flask import Flask, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS
import folium
import pymongo

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://saurabh:Solarwind%401@companydata.g6xbxk5.mongodb.net/asm3"  
mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for all origins
# Check if the connection was successful
if mongo.db is None:
    print("Failed to connect to MongoDB")
    exit(1)
@app.route('/api/data')
def get_data():
    data = list(mongo.db.result.find())  # Convert the cursor to a list
    return jsonify(dumps(data))  # Convert the list to JSON and return it

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/map')
def map():
    def create_folium_map(geojson_path, data_collection):
        # Read the GeoJSON file
        with open(geojson_path, 'r') as file:
            geo_json_data = json.load(file)

        # Create a map centered around Ho Chi Minh City
        m = folium.Map(location=[10.762622, 106.660172], zoom_start=10)

        # Add the GeoJSON layer to the map
        folium.GeoJson(
            geo_json_data,
            name='geojson'
        ).add_to(m)

       
        # Define a dictionary that maps diseases to colors
        disease_colors = {
            '(vertigo) paroymsal positional vertigo': 'red',
            'acne': 'blue',
            'aids': 'green',
            'alcoholic hepatitis': 'purple',
            'allergy': 'orange',
            'arthritis': 'darkred',
            'bronchial asthma': 'lightred',
            'cervical spondylosis': 'beige',
            'chicken pox': 'darkblue',
            'chronic cholestasis': 'darkgreen',
            'common cold': 'cadetblue',
            'dengue': 'darkpurple',
            'diabetes': 'pink',
            'dimorphic hemmorhoids(piles)': 'gray',
            'drug reaction': 'black',
            'fungal infection': 'lightgreen',
            'gastroenteritis': 'darkgray',
            'gerd': 'lightgray',
            'heart attack': 'lightblue',
            'hepatitis a': 'lightgreen',
            'hepatitis b': 'darkgreen',
            'hepatitis c': 'blue',
            'hepatitis d': 'purple',
            'hepatitis e': 'orange',
            'hypertension': 'darkred',
            'hyperthyroidism': 'lightred',
            'hypoglycemia': 'beige',
            'hypothyroidism': 'darkblue',
            'impetigo': 'darkgreen',
            'jaundice': 'cadetblue',
            'malaria': 'darkpurple',
            'migraine': 'pink',
            'osteoarthristis': 'gray',
            'paralysis (brain hemorrhage)': 'black',
            'peptic ulcer diseae': 'lightgreen',
            'pneumonia': 'darkgray',
            'psoriasis': 'lightgray',
            'tuberculosis': 'lightblue',
            'typhoid': 'red',
            'urinary tract infection': 'blue',
            'varicose veins': 'green',
        }
        # Add markers for each data point in MongoDB
        for data_point in data_collection.find():
            lat, lon = data_point['latitude'], data_point['longitude']
            disease = data_point['predicted_disease']
            color = disease_colors.get(disease, 'black')  # Use black as the default color
            folium.Marker(
                [lat, lon], 
                popup=f"Disease: {disease}, Color: {color}", 
                icon=folium.Icon(color=color)
            ).add_to(m)
        # Return the map
        return m._repr_html_()

        
    # Modify the MongoDB connection details as needed
    client = pymongo.MongoClient("mongodb+srv://saurabh:Solarwind%401@companydata.g6xbxk5.mongodb.net/")
    db = client["asm3"]
    collection = db["result"]

    # Path to the GeoJSON file
    geojson_path = './district-boundary-hcm-city.geojson'

     # Call the create_folium_map function with the path to your GeoJSON file and data collection
    map_html = create_folium_map(geojson_path, collection)

    # Return the map as HTML
    return map_html

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)