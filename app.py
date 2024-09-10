from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/ring', methods=['POST'])
def ring_doorbell():
    # Get the message and image from the form submission
    message = request.form.get('message')
    image = request.files.get('image')
    
    # Response back with the data received
    response = {
        'status': 'success',
        'message': message,
        'image_uploaded': bool(image),
        'image_path': image.filename if image else None
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)