from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from gradio_client import Client
import cv2
import os
import time
import pyttsx3

app = Flask(__name__, static_url_path='/kalpana/static', static_folder='kalpana/static')  # Define the static folder
CORS(app)

IMAGE_DIR = './kalpana/static/images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def capture_image():
    # Initialize the camera (use 0 for the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    # Capture a single frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    if ret:
        # Save the image
        path = f"image_{int(time.time())}.jpg"
        filename = os.path.join(IMAGE_DIR, path)
        cv2.imwrite(filename, frame)
        print(f"Image saved to {filename}")
        return filename
    else:
        print("Failed to capture image")
        return None

def process_image(path):
    client = Client(
        "https://ybelkada-llava-1-5-dlai.hf.space/")
    result = client.predict(
        "Describe this image",
        path,
        api_name="/predict"
    )
    print(result)
    return result

def convert_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/capture', methods=['POST'])
def capture_and_save():
    path = capture_image()
    if path:
        desc = process_image(path)
        convert_to_speech(desc)  # Convert description to speech
        return jsonify({'image_url': './kalpana/static/images/' + os.path.basename(path), 'description': desc})
    else:
        return jsonify({'error': 'Failed to capture image'}), 500

@app.route('/')
def home():
    return render_template('index4.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
