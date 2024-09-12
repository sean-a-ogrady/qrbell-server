from flask import Flask, request, jsonify, make_response
import os
from flask_cors import CORS
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://sean-a-ogrady.github.io"}})
# CORS(app)

load_dotenv()
PUSHOVER_USER_KEY = os.environ.get('PUSHOVER_USER_KEY')
PUSHOVER_APP_TOKEN = os.environ.get('PUSHOVER_APP_TOKEN')

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/ring', methods=['POST'])
def ring_doorbell():
    # Extract message and image from the form data
    message = request.form.get('message', 'Someone is at your door!')
    image = request.files.get('image')  # Image from form input

    # Prepare the payload for Pushover
    pushover_data = {
        'token': PUSHOVER_APP_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': message
    }

    # Prepare the file for Pushover (multipart form-data)
    files = None
    if image:
        MAX_FILE_SIZE = 2.5 * 1024 * 1024  # 2.5 MB
        image_bytes = image.read()

        if len(image_bytes) > MAX_FILE_SIZE:
            return make_response(jsonify({'status': 'error', 'message': 'File is too large (max 2.5 MB). Add a new image or refresh page to remove.'}), 400)
        
        # Reset file pointer to the beginning after reading
        image.seek(0)

        files = {'attachment': (image.filename, image.stream, image.mimetype)}

    try:
        # Send the message and attachment to Pushover
        pushover_response = requests.post(
            'https://api.pushover.net/1/messages.json',
            data=pushover_data,
            files=files,
            timeout=10
        )
        pushover_response.raise_for_status()  # Raises an error for 4xx/5xx responses

        pushover_result = pushover_response.json()
        response = {
            'status': 'success',
            'pushover_status': pushover_result.get('status'),
            'message': message,
            'image_uploaded': bool(image)
        }
        return make_response(jsonify(response), 200)

    except requests.exceptions.RequestException as e:
        return make_response(jsonify({'status': 'error', 'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)