from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json

app = Flask(__name__)

# Define the folder containing CSV files
CSV_FOLDER = r'C:\Users\admin\Desktop\my_project\chat\data\citypulse_pollution_csv_data_aarhus_aug_oct_2014\pollution - 副本'

def extract_coordinates():
    coordinates = []
    for file in os.listdir(CSV_FOLDER):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(CSV_FOLDER, file))
            if 'latitude' in df.columns and 'longitude' in df.columns:
                lat = df['latitude'].iloc[0]
                lng = df['longitude'].iloc[0]
                coordinates.append({'lat': lat, 'lng': lng})
    return coordinates

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    coordinates = extract_coordinates()
    return jsonify(coordinates)

if __name__ == '__main__':
    app.run(debug=True)
