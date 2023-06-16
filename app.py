import numpy as np
from PIL import Image
from io import BytesIO
from google.cloud import aiplatform
from google.oauth2 import service_account
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return ({'message': 'Sukses'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Menerima tautan gambar dari payload JSON
        image_file = request.files['image']
        image = Image.open(image_file)

        # Mengubah gambar menjadi array NumPy
        x_test = np.asarray(image)
        # Perform the resizing operation
        resized_image_data = image.resize((180, 180))

        # Add batch dimension
        resized_image_data = np.expand_dims(resized_image_data, axis=0)

        # Convert the data type to int8
        resized_image_data = resized_image_data.astype(np.int16)

        # Convert the data to a list
        resized_image_data = resized_image_data.tolist()

        # Load credentials from JSON file
        credentials = service_account.Credentials.from_service_account_file('D:/SEM 6/Capstone/Procecing data/credential.json')

        # Inisialisasi objek endpoint dengan kredensial
        endpoint = aiplatform.Endpoint(
            endpoint_name="projects/288463562539/locations/us-central1/endpoints/305220029824106496",
            credentials=credentials
        )

        # Make the prediction request
        prediction = endpoint.predict(instances=resized_image_data).predictions

        # Convert the predicted array to a NumPy array
        predicted_array = np.array(prediction)

        # Find the index of the highest value
        highest_class_index = np.argmax(predicted_array)

        url = "https://backend-dot-recipe-finder-388213.as.r.appspot.com/findfood"

        # Menyiapkan data permintaan
        data = {
            "predicted_class": str(highest_class_index)
        }

        headers = {
            "Authentication": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgsImlhdCI6MTY4NjUwNDI4OX0.L3QT-mSohJ1phz7cpF2b63_smqJbsfMeMxpnuezPud0",
            "Content-Type": "application/json"
        }

        # Mengirim permintaan POST ke URL API dengan payload JSON
        response = requests.post(url, json=data ,headers=headers)

        # Mendapatkan respons dari API
        api_response = response.json()

        # Mengembalikan respons dari API sebagai respons Flask
        return jsonify(api_response)

       

       
    
    except Exception as e:
        error_message = str(e)
        return jsonify({'error' : True,
            'message': error_message}), 500

if __name__ == '__main__':
    app.run()
