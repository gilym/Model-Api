from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

@app.route('/resize-image', methods=['POST'])
def resize_image():
    # Menerima gambar dari permintaan
    image_file = request.files['image']
    image = Image.open(image_file)

    # Resize gambar
    resized_image = image.resize((180, 180))

    # Mengubah gambar menjadi array NumPy
    resized_image_data = np.asarray(resized_image)

    # Menambahkan dimensi batch
    resized_image_data = np.expand_dims(resized_image_data, axis=0)

    # Konversi tipe data menjadi int16
    resized_image_data = resized_image_data.astype(np.int16)

    # Mengonversi data menjadi list
    resized_image_data = resized_image_data.tolist()

    # Mengembalikan hasil resize dalam response
    return jsonify(resized_image_data)

if __name__ == '__main__':
    app.run()
