from flask import Flask, request, jsonify, make_response
import os
from flask_cors import CORS
from dotenv import load_dotenv
import requests

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "https://sean-a-ogrady.github.io/qrbell-website/"}})
CORS(app)

load_dotenv()
PUSHOVER_USER_KEY = os.environ.get('PUSHOVER_USER_KEY')
PUSHOVER_APP_TOKEN = os.environ.get('PUSHOVER_APP_TOKEN')

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/ring', methods=['POST'])
def ring_doorbell():
    message = request.form.get('message')
    image = request.files.get('image')
    image_uploaded = False
    pushover_data = {
        'user': PUSHOVER_USER_KEY,
        'token': PUSHOVER_APP_TOKEN,
        'message': message,
    }
    if image:
        image_uploaded = True
        pushover_data['attachment'] = (image.filename, image.stream, image.mimetype)
    # Send request to Pushover API
    try:
        pushover_response = requests.post('https://api.pushover.net/1/messages.json', data=pushover_data, files=files)
        pushover_response.raise_for_status()  # Raise an exception for 4xx/5xx responses

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