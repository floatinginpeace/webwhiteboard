from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
from PIL import Image
import io
import base64 
import os
import numpy as np
from collections import deque

app = Flask(__name__)
CORS(app)

# Instead of storing individual lines, we'll store entire states of the canvas
undo_stack = deque(maxlen=20)
background_color = 'white' 

def rgb_to_hex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/change_color', methods=['POST'])
def change_color():
    data = request.json 
    r,g,b = data['r'], data['g'], data['b']
    hex_color = rgb_to_hex(r,g,b)
    return jsonify({'color': hex_color})

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json['image']
    image_data = base64.b64decode(data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    
    image.save('whiteboard.png')
    return jsonify({'message': 'Image saved successfully'})

@app.route('/save_state', methods=['POST'])
def save_state():
    data = request.json['state']
    undo_stack.append(data)
    return jsonify({'message': 'State saved successfully'})

@app.route('/undo', methods=['POST'])
def undo():
    if len(undo_stack) > 1:
        undo_stack.pop()  # Remove the current state
        previous_state = undo_stack[-1]  # Get the previous state
        return jsonify({'state': previous_state})
    elif len(undo_stack) == 1:
        return jsonify({'state': undo_stack[0]})  # Return the initial state
    else:
        return jsonify({'message': 'Nothing to undo'})

if __name__ == '__main__':
    app.run(debug=True)
